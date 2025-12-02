"""
Data Retention Automation Script
Run this script periodically (e.g., via cron/Task Scheduler) to maintain compliance
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.chat_manager import ChatManager
from utils.logger import setup_logger

# Configure logger
logger = setup_logger(__name__)

def cleanup_old_sessions(retention_days: int = 90):
    """
    Clean up old chat sessions based on retention policy
    
    Args:
        retention_days: Delete sessions older than this (default: 90 days)
    """
    logger.info(f"Starting data retention cleanup (retention period: {retention_days} days)")
    
    manager = ChatManager()
    
    # Log current state
    initial_count = manager.get_session_count()
    initial_size = manager.get_storage_size()
    logger.info(f"Initial state: {initial_count} sessions, {initial_size / 1024:.2f} KB")
    
    # Delete old sessions
    deleted_count = manager.delete_old_sessions(days=retention_days)
    
    # Log final state
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
