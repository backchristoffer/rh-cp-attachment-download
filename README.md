# Red Hat Support Case Attachment Downloader

This tool downloads attachments from Red Hat support cases using the Red Hat Customer Portal API.

## Setup

Get your offline token from: https://access.redhat.com/management/api

You can either use a `.env` file or pass parameters directly when running the script.

### Option 1: Using a `.env` file

Create a `.env` file like this:

```env
OFFTOKEN="your_offline_token_here"
CASE_NUMBERS="123456,234567,345678"
# Or use a file:
# CASE_FILE_PATH="./cases.txt"
DOWNLOAD_DIR="./attachments"
```

### Option 2: Using command-line arguments

You can provide the same information as flags:
```bash
pipenv run python app.py \
  --token your_access_token \
  --file cases.txt \
  --dir ./attachments
```

## Run Options

### Using Python directly:
```bash
pip install pipenv
pipenv install
pipenv run python app.py
```

### Using Podman:

Build the image:
```bash
podman build -t rh-attachments -f Containerfile .
```

Run the container:
```bash
podman run --rm \
  --env-file .env \
  -v $(pwd)/attachments:/app/attachments \
  rh-attachments
```

## Input Options
- Use `CASE_NUMBERS` in `.env` (comma-separated)
- Or use `CASE_FILE_PATH` to point to a file
- Or provide `--token`, `--file`, and `--dir` as parameters