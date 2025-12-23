"""
Google Drive service for fetching educational videos
"""
import json
from typing import List, Dict, Any
from functools import lru_cache
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..config import get_settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class GoogleDriveService:
    """Service for interacting with Google Drive"""
    
    def __init__(self):
        self.settings = get_settings()
        self._service = None
    
    def _get_credentials(self) -> Credentials:
        """Get Google credentials from environment"""
        try:
            creds_json = self.settings.GOOGLE_CREDENTIALS_JSON
            if not creds_json:
                raise Exception("GOOGLE_CREDENTIALS_JSON not found")
            
            creds_dict = json.loads(creds_json)
            return Credentials.from_service_account_info(creds_dict)
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            raise
    
    @property
    def service(self):
        """Get or create Drive service"""
        if self._service is None:
            try:
                credentials = self._get_credentials().with_scopes(
                    self.settings.SCOPES_DRIVE
                )
                self._service = build('drive', 'v3', credentials=credentials)
                logger.info("Google Drive service created successfully")
            except Exception as e:
                logger.error(f"Failed to create Drive service: {e}")
                raise
        return self._service
    
    def get_folder_id(self, folder_name: str) -> str:
        """Get folder ID by name"""
        try:
            query = (
                f"name='{folder_name}' and "
                f"mimeType='application/vnd.google-apps.folder' and "
                f"'{self.settings.MAIN_FOLDER_ID}' in parents and "
                f"trashed=false"
            )
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            items = results.get('files', [])
            if not items:
                logger.warning(f"Folder not found: {folder_name}")
                return None
            
            return items[0]['id']
        except HttpError as e:
            logger.error(f"Error finding folder: {e}")
            raise
    
    def get_files_in_folder(self, folder_id: str) -> List[Dict[str, Any]]:
        """Get all video and PDF files in a folder"""
        try:
            query = (
                f"'{folder_id}' in parents and "
                f"(mimeType contains 'video/' or name contains '.mp4' or name contains '.pdf') and "
                f"trashed=false"
            )
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType, size, webViewLink)',
                orderBy='name'
            ).execute()
            
            files = results.get('files', [])
            
            videos = []
            for file in files:
                file_type = "video" if "video" in file.get('mimeType', '') else "pdf"
                
                videos.append({
                    'id': file['id'],
                    'name': file['name'],
                    'type': file_type,
                    'url': f"https://drive.google.com/file/d/{file['id']}/preview",
                    'size': int(file.get('size', 0))
                })
            
            logger.info(f"Retrieved {len(videos)} files from folder {folder_id}")
            return videos
        except HttpError as e:
            logger.error(f"Error fetching files: {e}")
            raise
    
    def get_videos_for_disease(self, disease: str) -> List[Dict[str, Any]]:
        """Get all videos for a specific disease"""
        folder_name = self.settings.DISEASE_FOLDERS.get(disease)
        if not folder_name:
            logger.warning(f"Invalid disease: {disease}")
            return []
        
        folder_id = self.get_folder_id(folder_name)
        if not folder_id:
            return []
        
        return self.get_files_in_folder(folder_id)

# Global service instance
drive_service = GoogleDriveService()
