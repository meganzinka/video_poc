# Video POC - YouTube Data API Fetcher

A Python script to fetch short videos (< 4 minutes) from a specific YouTube channel within the last year using the YouTube Data API.

## Features

- Fetches videos from a specific YouTube channel
- Filters for short videos (< 4 minutes duration)
- Searches within the last year date range
- Handles API pagination automatically
- Saves results to JSON file
- Comprehensive error handling

## Setup

### Prerequisites

- Python 3.8+
- Poetry (install from [python-poetry.org](https://python-poetry.org/docs/#installation))
- YouTube Data API key

### Installation

1. Clone or download this project
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

### Configuration

1. Get a YouTube Data API key:
   - Go to [Google Cloud Console](https://console.developers.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API key)

2. Set up your API key (choose one method):
   
   **Option A: Environment Variable**
   ```bash
   export YOUTUBE_API_KEY=your_api_key_here
   ```
   
   **Option B: .env File**
   ```bash
   cp services/01_url_pull/.env.example services/01_url_pull/.env
   # Edit .env and add your API key
   ```

## Usage

### Run with Poetry

```bash
# Run the script directly
poetry run python services/01_url_pull/main.py

# Or use the configured script shortcut
poetry run youtube-fetch
```

### Run in Poetry Shell

```bash
# Activate the virtual environment
poetry shell

# Then run normally
python services/01_url_pull/main.py
```

## Output

The script will:
1. Display progress as it fetches videos
2. Print a summary of all found videos
3. Save detailed video data to `youtube_videos.json`

### Example Output

```
✓ YouTube API client initialized successfully
Fetching videos from channel: UC-tE4p-L9f0-w1T1-v8a-qA
Date range: 2024-10-26T10:30:00Z to 2025-10-26T10:30:00Z
Looking for short videos (< 4 minutes)
------------------------------------------------------------
Fetching page 1...
  Found 50 videos on this page
  Total videos so far: 50
Fetching page 2...
  Found 25 videos on this page
  Total videos so far: 75
------------------------------------------------------------
✓ Completed! Total videos fetched: 75

[Video Summary Table]

✓ Successfully fetched 75 short videos from the channel
✓ Data saved to youtube_videos.json
```

## Development

### Add Dependencies

```bash
poetry add package_name
```

For development dependencies:
```bash
poetry add --group dev package_name
```

### Code Formatting & Linting

```bash
# Format code with black
poetry run black services/

# Lint with flake8
poetry run flake8 services/
```

### Testing

```bash
poetry run pytest
```

## Configuration

The script targets these API parameters:
- **Channel ID**: `UC-tE4p-L9f0-w1T1-v8a-qA`
- **Date Range**: Last 365 days from today
- **Video Duration**: Short (< 4 minutes)
- **Type**: Video only
- **Results per page**: 50 (with automatic pagination)

## Project Structure

```
video_poc/
├── pyproject.toml          # Poetry configuration
├── README.md               # This file
├── services/
│   ├── 01_url_pull/        # Stage 1: Fetch video URLs
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── .env.example
│   │
│   ├── 02_video_download/  # Stage 2: Download videos
│   │   └── __init__.py
│   │
│   ├── 03_transcription/   # Stage 3: Transcribe videos
│   │   └── __init__.py
│   │
│   └── common/             # Shared code
│       └── __init__.py
│
└── scripts/                # Utility scripts
    └── deploy_all.sh
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've run `poetry install`
2. **API key errors**: Verify your API key is set correctly and has YouTube Data API enabled
3. **Quota exceeded**: YouTube API has daily quotas; wait 24 hours or check your quota usage

### API Limits

- YouTube Data API has a daily quota limit
- Each search request costs quota units
- Monitor your usage in Google Cloud Console
