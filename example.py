from googleapiclient.discovery import build
from numpy import require

api_key='AIzaSyDL4YxztyWkETWxkNAHA1Uin66Y7ovpGQg'

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    etag = "Nq1rWJctnecAQKjAsxDHIaOhFz4"

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='contentDetails',
        id="39-OF2TkNrQ"
    )

    response = request.execute()

    print(response)
    
    

if __name__ == "__main__":
    main()