import logging
import os
import re
from datetime import datetime
from typing import Optional


PII_PATTERNS = [
    (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]'),
    (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CC-REDACTED]'),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL-REDACTED]'),
    (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE-REDACTED]'),
    (r'\bAPIKEY[:\s]+[\w-]+', '[APIKEY-REDACTED]'),
    (r'\b(sk|pk)[-_][a-zA-Z0-9]{20,}\b', '[TOKEN-REDACTED]'),
]


class PIISanitizingFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = sanitize_pii(record.msg)
        if record.args:
            record.args = tuple(
                sanitize_pii(str(arg)) if isinstance(arg, str) else arg 
                for arg in record.args
            )
        return True


def sanitize_pii(text: str) -> str:
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

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    if sanitize_pii:
        pii_filter = PIISanitizingFilter()
        logger.addFilter(pii_filter)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
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
    return logging.getLogger(name)
