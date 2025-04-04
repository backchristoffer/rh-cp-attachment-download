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

### Option 2: Pass environment variables directly (no .env needed)

```bash
podman run --rm \
  -e OFFTOKEN="your_offline_token_here" \
  -e CASE_FILE_PATH="./cases.txt" \
  -e DOWNLOAD_DIR="./attachments" \
  -v $(pwd)/cases.txt:/app/cases.txt:ro \
  -v $(pwd)/attachments:/app/attachments \
  ghcr.io/backchristoffer/attachment-download:latest
```

## Running from GitHub Container Registry

You can run the container directly from the public registry:

```bash
podman run --rm \
  -e OFFTOKEN="your_offline_token_here" \
  -e CASE_FILE_PATH="./cases.txt" \
  -e DOWNLOAD_DIR="./attachments" \
  -v $(pwd)/cases.txt:/app/cases.txt:ro \
  -v $(pwd)/attachments:/app/attachments \
  ghcr.io/backchristoffer/attachment-download:latest
```

This requires no local build and pulls the latest image from GHCR.

## Run Options

### Using Python directly:
```bash
pip install pipenv
pipenv install
pipenv run python app.py
```

### Using Podman with local build:

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
- Or use `CASE_FILE_PATH` to point to a file (comma-separated, no quotes)

