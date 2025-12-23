"""
Google Sheets service for storing patient symptoms
"""
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import jdatetime
import pytz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import get_settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GoogleSheetsService:
    """Service for interacting with Google Sheets"""
    
    def __init__(self):
        self.settings = get_settings()
        self._service = None
        self._locks: Dict[str, asyncio.Lock] = {}
    
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
        """Get or create Sheets service"""
        if self._service is None:
            try:
                credentials = self._get_credentials().with_scopes(
                    self.settings.SCOPES_SHEETS
                )
                self._service = build('sheets', 'v4', credentials=credentials)
                logger.info("Google Sheets service created successfully")
            except Exception as e:
                logger.error(f"Failed to create Sheets service: {e}")
                raise
        return self._service
    
    def _get_lock(self, sheet_name: str) -> asyncio.Lock:
        """Get or create a lock for a specific sheet"""
        if sheet_name not in self._locks:
            self._locks[sheet_name] = asyncio.Lock()
        return self._locks[sheet_name]
    
    def sheet_exists(self, sheet_name: str) -> bool:
        """Check if a sheet exists"""
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.settings.GOOGLE_SHEET_ID
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            return any(s['properties']['title'] == sheet_name for s in sheets)
        except HttpError as e:
            logger.error(f"Error checking sheet existence: {e}")
            return False
    
    def create_sheet(self, sheet_name: str) -> bool:
        """Create a new sheet with headers"""
        try:
            # Create sheet
            requests = [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }]
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.settings.GOOGLE_SHEET_ID,
                body={'requests': requests}
            ).execute()
            
            # Add headers
            header = [['تاریخ', 'ساعت', 'نوع علامت', 'مقدار']]
            self.service.spreadsheets().values().update(
                spreadsheetId=self.settings.GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A1:D1',
                valueInputOption='RAW',
                body={'values': header}
            ).execute()
            
            logger.info(f"Created new sheet: {sheet_name}")
            return True
        except HttpError as e:
            logger.error(f"Error creating sheet: {e}")
            return False
    
    async def save_symptom(self, user_id: str, symptom_type: str, value: str) -> Dict[str, Any]:
        """Save a symptom to the user's sheet"""
        sheet_name = f"User_{user_id}"
        
        # Use lock to prevent race conditions
        async with self._get_lock(sheet_name):
            # Ensure sheet exists
            if not self.sheet_exists(sheet_name):
                self.create_sheet(sheet_name)
            
            try:
                # Get current time in Iran timezone
                iran_tz = pytz.timezone('Asia/Tehran')
                now = datetime.now(iran_tz)
                jd = jdatetime.datetime.fromgregorian(datetime=now)
                current_date = jd.strftime('%Y-%m-%d')
                current_time = now.strftime('%H:%M:%S')
                
                # Append data
                new_row = [[current_date, current_time, symptom_type, value]]
                
                self.service.spreadsheets().values().append(
                    spreadsheetId=self.settings.GOOGLE_SHEET_ID,
                    range=f'{sheet_name}!A:D',
                    valueInputOption='RAW',
                    body={'values': new_row}
                ).execute()
                
                logger.info(f"Saved symptom for {user_id}: {symptom_type} = {value}")
                return {
                    "success": True,
                    "message": "Symptom saved successfully",
                    "timestamp": f"{current_date} {current_time}"
                }
            except HttpError as e:
                logger.error(f"Error saving symptom: {e}")
                raise
    
    def get_user_history(self, user_id: str, symptom_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get symptom history for a user"""
        sheet_name = f"User_{user_id}"
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.settings.GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A2:D'
            ).execute()
        except HttpError as e:
            if "not found" in str(e).lower() or "Unable to parse" in str(e):
                logger.info(f"No data found for user: {user_id}")
                return []
            logger.error(f"Error fetching history: {e}")
            raise
        
        rows = result.get('values', [])
        
        if not rows:
            return []
        
        symptoms = []
        for row in rows:
            if len(row) >= 4:
                symptom_type = row[2]
                
                # Apply filter if provided
                if symptom_filter and symptom_filter not in symptom_type:
                    continue
                
                symptoms.append({
                    'date': row[0],
                    'time': row[1],
                    'type': symptom_type,
                    'value': row[3]
                })
        
        logger.info(f"Retrieved {len(symptoms)} records for user: {user_id}")
        return symptoms

# Global service instance
sheets_service = GoogleSheetsService()
