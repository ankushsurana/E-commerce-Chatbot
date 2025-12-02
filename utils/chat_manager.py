"""
Chat Session Manager
Handles saving, loading, and managing chat sessions for the application.
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configure logger
logger = logging.getLogger(__name__)

class ChatManager:
    """Manages chat sessions persistence"""
    
    def __init__(self, storage_dir: str = "data/chats"):
        """
        Initialize ChatManager
        
        Args:
            storage_dir: Directory to store chat files
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
        
    def _ensure_storage_dir(self):
        """Ensure storage directory exists"""
        if not os.path.exists(self.storage_dir):
            try:
                os.makedirs(self.storage_dir)
                logger.info(f"Created chat storage directory: {self.storage_dir}")
            except Exception as e:
                logger.error(f"Failed to create chat storage directory: {str(e)}")
    
    def create_session(self, title: str = "New Chat") -> str:
        """
        Create a new chat session (in-memory only until saved)
        
        Args:
            title: Initial title for the chat
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        # Note: We do NOT save to file here. 
        # Session is only saved when messages are added.
        return session_id
    
    def save_session(self, session_id: str, data: Dict):
        """
        Save chat session to file
        
        Args:
            session_id: Session ID
            data: Session data dictionary
        """
        filepath = os.path.join(self.storage_dir, f"{session_id}.json")
        try:
            # Update timestamp
            data["updated_at"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to save session {session_id}: {str(e)}")
            
    def load_session(self, session_id: str) -> Optional[Dict]:
        """
        Load chat session from file
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data dictionary or None if not found
        """
        filepath = os.path.join(self.storage_dir, f"{session_id}.json")
        if not os.path.exists(filepath):
            return None
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {str(e)}")
            return None
            
    def list_sessions(self) -> List[Dict]:
        """
        List all available chat sessions (excluding empty ones)
        
        Returns:
            List of session summaries (id, title, updated_at) sorted by date desc
        """
        sessions = []
        if not os.path.exists(self.storage_dir):
            return []
            
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]
                session = self.load_session(session_id)
                # Only include sessions that have messages
                if session and session.get("messages"):
                    sessions.append({
                        "id": session["id"],
                        "title": session.get("title", "Untitled Chat"),
                        "updated_at": session.get("updated_at", "")
                    })
        
        # Sort by updated_at descending (newest first)
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session
        
        Args:
            session_id: Session ID
            
        Returns:
            True if deleted, False otherwise
        """
        filepath = os.path.join(self.storage_dir, f"{session_id}.json")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Deleted session: {session_id}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete session {session_id}: {str(e)}")
                return False
        return False
    
    def update_session_title(self, session_id: str, new_title: str):
        """
        Update the title of a session
        
        Args:
            session_id: Session ID
            new_title: New title
        """
        session = self.load_session(session_id)
        if session:
            session["title"] = new_title
            self.save_session(session_id, session)
    
    def delete_old_sessions(self, days: int = 90) -> int:
        """
        Delete sessions older than specified days (for data retention compliance)
        
        Args:
            days: Delete sessions older than this many days
            
        Returns:
            Number of sessions deleted
        """
        from datetime import timedelta
        
        deleted_count = 0
        cutoff_date = datetime.now() - timedelta(days=days)
        
        if not os.path.exists(self.storage_dir):
            return 0
            
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_dir, filename)
                session_id = filename[:-5]
                
                try:
                    session = self.load_session(session_id)
                    if session:
                        updated_at = session.get("updated_at", "")
                        if updated_at:
                            session_date = datetime.fromisoformat(updated_at)
                            if session_date < cutoff_date:
                                if self.delete_session(session_id):
                                    deleted_count += 1
                                    logger.info(f"Deleted old session: {session_id}")
                except Exception as e:
                    logger.error(f"Error processing session {session_id}: {str(e)}")
        
        logger.info(f"Data retention: Deleted {deleted_count} sessions older than {days} days")
        return deleted_count
    
    def export_session(self, session_id: str, export_path: str = None) -> bool:
        """
        Export a session to JSON file (for data portability compliance)
        
        Args:
            session_id: Session ID
            export_path: Optional path to export file (default: session_id_export.json)
            
        Returns:
            True if exported successfully
        """
        session = self.load_session(session_id)
        if not session:
            return False
            
        if not export_path:
            export_path = f"{session_id}_export.json"
            
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(session, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported session {session_id} to {export_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export session {session_id}: {str(e)}")
            return False
    
    def delete_all_sessions(self) -> int:
        """
        Delete all chat sessions (for right to erasure compliance)
        
        Returns:
            Number of sessions deleted
        """
        deleted_count = 0
        
        if not os.path.exists(self.storage_dir):
            return 0
            
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"Failed to delete {filepath}: {str(e)}")
        
        logger.info(f"Deleted all sessions: {deleted_count} files")
        return deleted_count
    
    def get_session_count(self) -> int:
        """
        Get total number of stored sessions
        
        Returns:
            Count of sessions
        """
        if not os.path.exists(self.storage_dir):
            return 0
        return len([f for f in os.listdir(self.storage_dir) if f.endswith('.json')])
    
    def get_storage_size(self) -> int:
        """
        Get total storage size of all sessions in bytes
        
        Returns:
            Total size in bytes
        """
        total_size = 0
        if not os.path.exists(self.storage_dir):
            return 0
            
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except Exception:
                    pass
        
        return total_size

