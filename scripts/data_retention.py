import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.chat_manager import ChatManager
from utils.logger import setup_logger
from config.config import config

logger = setup_logger(__name__)

def cleanup_old_sessions(retention_days: int = None):
    if retention_days is None:
        retention_days = config.DEFAULT_RETENTION_DAYS
    
    logger.info(f"Starting data retention cleanup (retention period: {retention_days} days)")
    
    manager = ChatManager()
    
    initial_count = manager.get_session_count()
    initial_size = manager.get_storage_size()
    logger.info(f"Initial state: {initial_count} sessions, {initial_size / 1024:.2f} KB")
    
    deleted_count = manager.delete_old_sessions(days=retention_days)
    
    final_count = manager.get_session_count()
    final_size = manager.get_storage_size()
    logger.info(f"Final state: {final_count} sessions, {final_size / 1024:.2f} KB")
    logger.info(f"Cleanup completed: {deleted_count} sessions deleted")
    
    return deleted_count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Data retention cleanup utility")
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Delete sessions older than this many days (default: 90)"
    )
    
    args = parser.parse_args()
    
    cleanup_old_sessions(retention_days=args.days)
