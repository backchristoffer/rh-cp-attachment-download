import requests
import os
import argparse
import re
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser(description='Download Red Hat support case attachments.')
parser.add_argument('--token', help='Red Hat API token')
parser.add_argument('--file', help='Path to file containing comma-separated case numbers')
parser.add_argument('--dir', help='Directory to save attachments')
args = parser.parse_args()

#This takes your OFFTOKEN and generates a ACCESSTOKEN that will be used with your API calls to the red hat api
def get_access_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": "rhsm-api",
        "refresh_token": os.getenv("OFFTOKEN")
    }
    try:
        r = requests.post(url="https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token", data=data)
        r.raise_for_status()
        access_token = r.json().get("access_token")
        if access_token:
            print("[INFO] Successfully retrieved access token from offline token.")
        return access_token
    except requests.exceptions.RequestException as request_error:
        print(f"Error refreshing access token: {request_error}")
        return None
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

# This access token will be used with api calls
access_token = args.token or os.getenv('API_TOKEN') or get_access_token()

if not access_token:
    raise ValueError("No valid API access token available. Provide --token or set OFFTOKEN in .env to fetch one.")

headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}
# using binary headers for .tgz or maybe .txt files instead of getting HTML. It will treat it like a file download
binary_headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/octet-stream'
}

CASE_FILE_PATH = args.file or os.getenv('CASE_FILE_PATH', '')
DOWNLOAD_DIR = Path(args.dir).resolve() if args.dir else Path(os.getenv('DOWNLOAD_DIR')).resolve() if os.getenv('DOWNLOAD_DIR') else Path.cwd() / 'attachments'
CASE_NUMBERS_ENV = os.getenv('CASE_NUMBERS', '')

# Gather case numbers from file or .env
def get_case_numbers():
    if CASE_FILE_PATH and Path(CASE_FILE_PATH).is_file():
        with open(CASE_FILE_PATH, 'r') as f:
            content = f.read()
            return [case.strip() for case in content.split(',') if case.strip()]
    return [case.strip() for case in CASE_NUMBERS_ENV.split(',') if case.strip()]

CASE_NUMBERS = get_case_numbers()

if not CASE_NUMBERS:
    raise ValueError("No case numbers provided. Use --file or set CASE_NUMBERS/CASE_FILE_PATH in .env.")

def get_filename_from_headers(headers, default_name):
    content_disp = headers.get('Content-Disposition', '')
    match = re.search(r'filename="?([^";]+)"?', content_disp)
    return match.group(1) if match else default_name

def download_attachments_for_case(case_number):
    case_dir = DOWNLOAD_DIR / f'case_{case_number}'
    case_dir.mkdir(parents=True, exist_ok=True)

    url = f'https://api.access.redhat.com/support/v1/cases/{case_number}/attachments'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f'[ERROR] Case {case_number}: Failed to fetch attachments ({response.status_code})')
        print(f'[DEBUG] Response: {response.text}')
        return

    try:
        data = response.json()
        attachments = data.get('attachments') if isinstance(data, dict) else data
    except Exception as e:
        print(f'[ERROR] Failed to parse JSON for case {case_number}: {e}')
        return

    if not attachments:
        print(f'[INFO] Case {case_number}: No attachments found.')
        return

    for attachment in attachments:
        fallback_name = attachment.get('fileName', 'unnamed')
        download_link = attachment.get('link')

        if not download_link:
            print(f'[WARNING] Case {case_number}: Skipping invalid attachment metadata')
            continue

        print(f'[INFO] Case {case_number}: Downloading {fallback_name}...')

        file_response = requests.get(download_link, headers=binary_headers, stream=True)
        if file_response.status_code == 200:
            final_name = get_filename_from_headers(file_response.headers, fallback_name)
            file_path = case_dir / final_name
            with open(file_path, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f'[SUCCESS] Case {case_number}: Downloaded {final_name}')
        else:
            print(f'[ERROR] Case {case_number}: Failed to download {fallback_name} ({file_response.status_code})')
            print(f'[DEBUG] Response: {file_response.text}')

def main():
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    for case_number in CASE_NUMBERS:
        download_attachments_for_case(case_number)

if __name__ == '__main__':
    main()