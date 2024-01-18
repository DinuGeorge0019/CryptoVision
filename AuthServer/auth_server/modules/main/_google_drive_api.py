import base64
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from config._credentials import DRIVE_API_CREDENTIALS
from requests import HTTPError


def drive_upload_file(image_path):
    """ 
    Insert new file.
    Returns : Id's of the file uploaded
    """
    try:

        service = build("drive", "v3", credentials=DRIVE_API_CREDENTIALS)

        file_metadata = {
            "name": image_path.split("/")[-1],
            'parents': ['1iIinaxjHkZS3AN5iOp543lrVc3qEVWhv']
        }

        media = MediaFileUpload(image_path, mimetype="image/png")

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        
    except HTTPError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")


def drive_download_file(image_file_id, download_image_path):
    """
    Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns :
        none
    """
    try:

        service = build("drive", "v3", credentials=DRIVE_API_CREDENTIALS)

        request = service.files().get_media(fileId=image_file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
    
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
        
        # Write the downloaded bytes to a file at the specified path
        with open(download_image_path, 'wb') as f:
            f.write(file.getvalue())
        
    except HTTPError as error:
        print(f"An error occurred: {error}")

    

