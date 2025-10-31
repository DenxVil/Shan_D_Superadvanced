"""
Mail Configuration System
Handles email configuration from environment variables/GitHub secrets
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class MailConfig:
    """Manages email configuration and sending"""
    
    def __init__(self):
        """Initialize mail configuration from environment variables"""
        self.smtp_host = os.environ.get('SMTP_HOST', '')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_user = os.environ.get('SMTP_USER', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_user)
        
        self._config_status = self._check_configuration()
    
    def _check_configuration(self) -> Dict[str, any]:
        """
        Check if mail configuration is properly set
        
        Returns:
            Dictionary with configuration status and details
        """
        missing_vars = []
        
        if not self.smtp_host:
            missing_vars.append('SMTP_HOST')
        if not self.smtp_user:
            missing_vars.append('SMTP_USER')
        if not self.smtp_password:
            missing_vars.append('SMTP_PASSWORD')
        
        is_configured = len(missing_vars) == 0
        
        status = {
            'enabled': is_configured,
            'smtp_host': self.smtp_host if self.smtp_host else 'Not configured',
            'smtp_port': self.smtp_port,
            'smtp_user': self.smtp_user if self.smtp_user else 'Not configured',
            'from_email': self.from_email if self.from_email else 'Not configured',
            'missing_variables': missing_vars,
            'reason': self._get_status_reason(is_configured, missing_vars)
        }
        
        return status
    
    def _get_status_reason(self, is_configured: bool, missing_vars: list) -> str:
        """
        Get human-readable reason for mail configuration status
        
        Args:
            is_configured: Whether mail is properly configured
            missing_vars: List of missing environment variables
        
        Returns:
            Human-readable status reason
        """
        if is_configured:
            return "Mail is properly configured and ready to use"
        else:
            missing_str = ', '.join(missing_vars)
            return f"Mail is disabled. Missing environment variables: {missing_str}. Please set these in GitHub Secrets or environment."
    
    def get_status(self) -> Dict[str, any]:
        """Get current mail configuration status"""
        return self._config_status.copy()
    
    def is_configured(self) -> bool:
        """Check if mail is properly configured"""
        return self._config_status['enabled']
    
    def send_certificate(self, to_email: str, certificate_path: Path, 
                        recipient_name: str, certificate_id: str) -> Dict[str, any]:
        """
        Send certificate via email
        
        Args:
            to_email: Recipient email address
            certificate_path: Path to certificate image
            recipient_name: Name of recipient
            certificate_id: Certificate ID
        
        Returns:
            Dictionary with send status
        """
        if not self.is_configured():
            logger.error("Cannot send email - mail not configured")
            return {
                'success': False,
                'error': 'Mail configuration is incomplete',
                'reason': self._config_status['reason']
            }
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = f'Your Certificate - {certificate_id}'
            
            # Email body
            body = f"""
Dear {recipient_name},

Congratulations on completing your course!

Please find your certificate attached to this email.

Certificate ID: {certificate_id}

Best regards,
Shan-D Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach certificate
            if certificate_path.exists():
                with open(certificate_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=certificate_path.name)
                    msg.attach(image)
            else:
                logger.error(f"Certificate file not found: {certificate_path}")
                return {
                    'success': False,
                    'error': 'Certificate file not found'
                }
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Certificate sent successfully to {to_email}")
            return {
                'success': True,
                'message': f'Certificate sent to {to_email}'
            }
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {e}")
            return {
                'success': False,
                'error': 'SMTP authentication failed. Please check SMTP_USER and SMTP_PASSWORD.'
            }
        except smtplib.SMTPConnectError as e:
            logger.error(f"SMTP Connection failed: {e}")
            return {
                'success': False,
                'error': f'Cannot connect to SMTP server {self.smtp_host}:{self.smtp_port}'
            }
        except Exception as e:
            logger.error(f"Failed to send certificate: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Initialize global mail config instance
mail_config = MailConfig()
