import csv
import time
from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
API_KEY = 'AIzaSyD6sy1zRQptyWFEcHSRfTjL_uGy6khW3yg'

def get_most_searched_videos(api_key, query, max_results=10):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results
    )
    response = request.execute()
    
    videos_data = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        
        video_request = youtube.videos().list(
            part='statistics',
            id=video_id
        )
        video_response = video_request.execute()
        statistics = video_response['items'][0]['statistics']
        
        views = statistics.get('viewCount', 0)
        likes = statistics.get('likeCount', 0)
        
        videos_data.append({
            'title': video_title,
            'views': views,
            'likes': likes
        })
    
    return videos_data

if __name__ == "__main__":
    query = input("Enter the search query: ")
    max_results = int(input("Enter the number of results to fetch: "))
    interval = int(input("Enter the time interval between scrapes (in seconds): "))
    
    while True:
        videos_data = get_most_searched_videos(API_KEY, query, max_results)
        
        # Write data to CSV file
        csv_file = 'youtube_data.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'views', 'likes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for video_data in videos_data:
                writer.writerow(video_data)
        
        print(f"Data has been successfully written to {csv_file}.")
        print(f"Waiting for {interval} seconds before the next scrape...")
        time.sleep(interval)
