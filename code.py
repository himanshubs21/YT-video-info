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
