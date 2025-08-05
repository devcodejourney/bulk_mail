import argparse
from utils.email_builder import build_email
from utils.sender import EmailSender
from utils.validator import load_recipients
import logging
import os
from time import sleep

def setup_logging():
    """Configure logging for the application"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/errors.log'),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Bulk Email Sender Tool')
    parser.add_argument('--recipients', default='data/recipients.csv', 
                       help='Path to recipients CSV file')
    parser.add_argument('--template', help='Email template to use (without extension)')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Test without actually sending')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between emails in seconds')
    
    args = parser.parse_args()
    
    try:
        # Load and validate recipients
        recipients = load_recipients(args.recipients)
        if not recipients:
            logging.error("No valid recipients found")
            return
        
        logging.info(f"Loaded {len(recipients)} valid recipients")
        
        # Initialize email sender
        sender = EmailSender()
        success_count = 0
        fail_count = 0
        
        # Send emails
        for recipient in recipients:
            email_content = build_email(
                recipient['email'],
                args.subject,
                args.template
            )
            
            if args.dry_run:
                logging.info(f"DRY RUN: Would send to {recipient['email']}")
                success_count += 1
            else:
                if sender.send(email_content):
                    success_count += 1
                else:
                    fail_count += 1
                
                sleep(args.delay)  # Throttle sending
        
        logging.info(f"Campaign complete: {success_count} sent, {fail_count} failed")
        
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()