"""
Logging Configuration Module with PII Sanitization
Sets up centralized logging for the application with security features
"""

import logging
import os
import re
from datetime import datetime
from typing import Optional


# PII Patterns to sanitize from logs
PII_PATTERNS = [
    (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]'),  # SSN
    (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CC-REDACTED]'),  # Credit card
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL-REDACTED]'),  # Email
    (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE-REDACTED]'),  # Phone numbers
    (r'\bAPIKEY[:\s]+[\w-]+', '[APIKEY-REDACTED]'),  # API keys
    (r'\b(sk|pk)[-_][a-zA-Z0-9]{20,}\b', '[TOKEN-REDACTED]'),  # API tokens
]


class PIISanitizingFilter(logging.Filter):
    """Filter to remove PII from log messages"""
    
    def filter(self, record):
        """Sanitize PII from log record"""
        if isinstance(record.msg, str):
            record.msg = sanitize_pii(record.msg)
        if record.args:
            record.args = tuple(
                sanitize_pii(str(arg)) if isinstance(arg, str) else arg 
                for arg in record.args
            )
        return True


def sanitize_pii(text: str) -> str:
    """
    Remove PII patterns from text
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return text
        
    sanitized = text
    for pattern, replacement in PII_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    
    return sanitized


def setup_logger(
    name: str = __name__,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True,
    sanitize_pii: bool = True
) -> logging.Logger:
    """
    Setup logger with file and console handlers with PII sanitization
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        console_output: Whether to output to console
        sanitize_pii: Whether to sanitize PII from logs
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Add PII sanitization filter
    if sanitize_pii:
        pii_filter = PIISanitizingFilter()
        logger.addFilter(pii_filter)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to create file handler: {str(e)}")
    
    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get or create a logger
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
