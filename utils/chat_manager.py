import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ChatManager:
    
    def __init__(self, storage_dir: str = "data/chats"):

        self.storage_dir = storage_dir
        self._ensure_storage_dir()
        
    def _ensure_storage_dir(self):
        if not os.path.exists(self.storage_dir):
            try:
                os.makedirs(self.storage_dir)
                logger.info(f"Created chat storage directory: {self.storage_dir}")
            except Exception as e:
                logger.error(f"Failed to create chat storage directory: {str(e)}")
    
    def create_session(self, title: str = "New Chat") -> str:
        session_id = str(uuid.uuid4())
        return session_id
    
    def save_session(self, session_id: str, data: Dict):
        filepath = os.path.join(self.storage_dir, f"{session_id}.json")
        try:
            data["updated_at"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to save session {session_id}: {str(e)}")
            
    def load_session(self, session_id: str) -> Optional[Dict]:
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
        sessions = []
        if not os.path.exists(self.storage_dir):
            return []
            
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]
                session = self.load_session(session_id)
                if session and session.get("messages"):
                    sessions.append({
                        "id": session["id"],
                        "title": session.get("title", "Untitled Chat"),
                        "updated_at": session.get("updated_at", "")
                    })
        
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
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
        session = self.load_session(session_id)
        if session:
            session["title"] = new_title
            self.save_session(session_id, session)
    
    def delete_old_sessions(self, days: int = 30) -> int:
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
        if not os.path.exists(self.storage_dir):
            return 0
        return len([f for f in os.listdir(self.storage_dir) if f.endswith('.json')])
    
    def get_storage_size(self) -> int:
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

