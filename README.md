# YT-video-info
This repository extracts required details from a YT video in excel sheet. The O/P format is for my use. Modify it for you own convenience!

# YouTube Video Details Extraction and Export to Excel

This Python script extracts metadata from YouTube videos and saves the details into an Excel file. It uses the `yt-dlp` library for video extraction and `pandas` to manage and export the data.

## Features
- Extracts key metadata such as **Title**, **Uploader**, **Duration (in HH:MM:SS format)**, **Publish Year**, **View Count**, **Like Count**, **Dislike Count**, and **Description**.
- Converts all output (except numeric values) into **uppercase**.
- Saves the extracted data into an **Excel** file (`video_details.xlsx`).
- Handles multiple YouTube URLs inputted by the user.

## Prerequisites

Before running the script, ensure you have the following dependencies installed:

1. **Python 3.x** (Tested on Python 3.9+)
2. **yt-dlp** (a more feature-complete fork of `youtube-dl`)
3. **pandas** (for managing and exporting data to Excel)

You can install these dependencies by running the following commands:

```bash
pip install yt-dlp pandas openpyxl
```

Note: `openpyxl` is required to work with Excel files.

## Script Overview

The script performs the following steps:

1. Prompts the user to enter YouTube video URLs.
2. Extracts metadata from each URL using `yt-dlp`.
3. Converts relevant text data to uppercase.
4. Formats video duration to **HH:MM:SS** format.
5. Extracts the **Publish Year** from the upload date.
6. Saves the details to an Excel file `video_details.xlsx`.

## Script Details

```python
import yt_dlp
import pandas as pd

def get_video_details(video_urls):
    # List to hold the video details
    video_details = []
    
    # Iterate over the list of URLs
    for url in video_urls:
        try:
            # Setup options for yt-dlp
            ydl_opts = {
                'quiet': True,  # Suppress standard output
                'format': 'best',  # Get the best quality video
            }
            
            # Extract video details
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_info = {
                    'Title': info_dict.get('title', '').upper(),
                    'URL': url,
                    'Uploader': info_dict.get('uploader', '').upper(),
                    'Duration (HH:MM:SS)': format_duration(info_dict.get('duration', 0)),
                    'Publish Year': extract_publish_year(info_dict.get('upload_date')).upper(),
                    'View Count': str(info_dict.get('view_count', '')).upper(),
                    'Uploader ID': info_dict.get('uploader_id', '').upper(),
                    'Description': info_dict.get('description', '').upper(),
                    'Like Count': str(info_dict.get('like_count', '')).upper(),
                    'Dislike Count': str(info_dict.get('dislike_count', '')).upper(),
                    'Published Date': info_dict.get('upload_date', '').upper()
                }
                video_details.append(video_info)
        
        except Exception as e:
            print(f"Error extracting {url}: {e}")
    
    return video_details

def format_duration(duration_seconds):
    """
    Convert the duration from seconds to HH:MM:SS format.
    """
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def extract_publish_year(upload_date):
    """
    Extract the year from the upload date (YYYYMMDD format).
    """
    if upload_date:
        return upload_date[:4]  # Return the first 4 characters as the year
    return None

def save_to_excel(video_details, file_name="video_details.xlsx"):
    """
    Save the extracted video details to an Excel file.
    """
    df = pd.DataFrame(video_details)
    df.to_excel(file_name, index=False)
    print(f"Data successfully saved to {file_name}")

def main():
    """
    Main function to run the script.
    """
    # User input for video URLs
    urls = input("Enter YouTube video links, separated by commas: ").split(',')
    urls = [url.strip() for url in urls]  # Remove any extra spaces
    
    # Get the video details
    video_details = get_video_details(urls)
    
    # Save the details to Excel
    save_to_excel(video_details)

if __name__ == "__main__":
    main()
```

### Key Functions:
1. **`get_video_details(video_urls)`**: 
   - Extracts the video metadata for the provided URLs using `yt-dlp`.
   - Converts textual information to uppercase using `.upper()`.
   - Formats duration in `HH:MM:SS` format and extracts the publish year from the `upload_date`.

2. **`format_duration(duration_seconds)`**:
   - Converts video duration (in seconds) into `HH:MM:SS` format.

3. **`extract_publish_year(upload_date)`**:
   - Extracts the year from the `upload_date` (YYYYMMDD format).

4. **`save_to_excel(video_details, file_name)`**:
   - Saves the collected video details to an Excel file (`video_details.xlsx`).

5. **`main()`**:
   - Prompts the user to input YouTube URLs.
   - Calls the above functions to fetch, process, and save video metadata.

### Example Input:
```
https://www.youtube.com/watch?v=IwrN3eaZO9E, https://www.youtube.com/watch?v=Oo3qsxihXqY, https://www.youtube.com/watch?v=5wRosZbYlfY
```

### Example Output in Excel (`video_details.xlsx`):
| TITLE              | URL                                    | UPLOADER | DURATION (HH:MM:SS) | PUBLISH YEAR | VIEW COUNT | UPLOADER ID | DESCRIPTION | LIKE COUNT | DISLIKE COUNT | PUBLISHED DATE |
|--------------------|----------------------------------------|----------|---------------------|--------------|------------|-------------|-------------|------------|---------------|----------------|
| EXAMPLE VIDEO 1    | https://www.youtube.com/watch?v=IwrN3eaZO9E | USER1    | 00:05:12            | 2023         | 15000      | USER_ID1    | DESCRIPTION TEXT | 500        | 5             | 20231101       |
| EXAMPLE VIDEO 2    | https://www.youtube.com/watch?v=Oo3qsxihXqY | USER2    | 00:10:45            | 2022         | 12000      | USER_ID2    | DESCRIPTION TEXT | 300        | 3             | 20221112       |

### Running the Script

1. Install dependencies:
   ```bash
   pip install yt-dlp pandas openpyxl
   ```

2. Run the script:
   ```bash
   python3 p2.py
   ```

3. Enter YouTube video URLs when prompted:
   ```bash
   https://www.youtube.com/watch?v=IwrN3eaZO9E, https://www.youtube.com/watch?v=Oo3qsxihXqY, https://www.youtube.com/watch?v=5wRosZbYlfY
   ```

4. The metadata will be saved in an Excel file named `video_details.xlsx`.

## Troubleshooting

- **ffmpeg warning**: If you receive a warning that `ffmpeg` is not found, install `ffmpeg` on your system for better video quality download:
  
  - On **Ubuntu/Debian**:
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

  - On **macOS** (using Homebrew):
    ```bash
    brew install ffmpeg
    ```

- **Invalid URL**: Make sure you input valid YouTube URLs.
