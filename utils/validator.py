from typing import List, Dict
import csv
import re
import logging

def validate_email(email: str) -> bool:
    """Validate email with comprehensive regex"""
    pattern = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_recipients(file_path: str = 'data/recipients.csv') -> List[Dict]:
    """Load and validate recipients from CSV"""
    valid_recipients = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            # Detect CSV dialect
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            
            reader = csv.DictReader(f, dialect=dialect)
            
            if 'email' not in reader.fieldnames:
                logging.error("CSV must contain 'email' column")
                return []
            
            for row in reader:
                email = row['email'].strip()
                if validate_email(email):
                    valid_recipients.append(row)
                else:
                    logging.warning(f"Invalid email skipped: {email}")
        
        logging.info(f"Loaded {len(valid_recipients)} valid recipients")
        return valid_recipients
    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []
    except Exception as e:
        logging.error(f"Error reading CSV: {str(e)}")
        return []