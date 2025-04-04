import requests
import os

API_TOKEN = os.getenv("API_TOKEN")
CASE_NUMBERS = os.getenv("CASE_NUMBERS")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")

if __name__ == "__main__":
    print(API_TOKEN)
    print(CASE_NUMBERS)
    print(DOWNLOAD_DIR)