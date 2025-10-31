"""
Certificate Database Management
Handles certificate generation tracking with proper error handling
"""
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CertificateDB:
    """Manages certificate database with proper table creation handling"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection"""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "data" / "certificates.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database schema
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema with IF NOT EXISTS to avoid errors"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create certificates table with IF NOT EXISTS
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    certificate_id TEXT UNIQUE NOT NULL,
                    user_name TEXT NOT NULL,
                    course_name TEXT NOT NULL,
                    issue_date TEXT NOT NULL,
                    email TEXT,
                    file_path TEXT,
                    attempts INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Create attempts log table with IF NOT EXISTS
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS certificate_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    certificate_id TEXT NOT NULL,
                    attempt_number INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (certificate_id) REFERENCES certificates(certificate_id)
                )
            """)
            
            # Create index if not exists
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_certificate_id 
                ON certificates(certificate_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_attempts_cert_id 
                ON certificate_attempts(certificate_id)
            """)
            
            conn.commit()
            conn.close()
            logger.info("Database schema initialized successfully")
            
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            # Log but don't crash - table might already exist
            if "already exists" not in str(e).lower():
                raise
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_certificate_record(self, certificate_data: Dict) -> str:
        """
        Create a new certificate record
        
        Args:
            certificate_data: Dictionary with certificate information
        
        Returns:
            Certificate ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.utcnow().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO certificates 
                (certificate_id, user_name, course_name, issue_date, email, 
                 file_path, attempts, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                certificate_data['certificate_id'],
                certificate_data['user_name'],
                certificate_data['course_name'],
                certificate_data['issue_date'],
                certificate_data.get('email', ''),
                certificate_data.get('file_path', ''),
                0,
                'pending',
                now,
                now
            ))
            
            conn.commit()
            logger.info(f"Certificate record created: {certificate_data['certificate_id']}")
            return certificate_data['certificate_id']
            
        except sqlite3.IntegrityError as e:
            logger.error(f"Certificate already exists: {e}")
            raise
        finally:
            conn.close()
    
    def log_attempt(self, certificate_id: str, status: str, error_message: Optional[str] = None):
        """
        Log a certificate generation attempt
        
        Args:
            certificate_id: Certificate ID
            status: Attempt status (success/failed)
            error_message: Optional error message
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get current attempt count
            cursor.execute(
                "SELECT attempts FROM certificates WHERE certificate_id = ?",
                (certificate_id,)
            )
            row = cursor.fetchone()
            
            if row:
                current_attempts = row['attempts']
                new_attempts = current_attempts + 1
                
                # Log the attempt
                cursor.execute("""
                    INSERT INTO certificate_attempts
                    (certificate_id, attempt_number, status, error_message, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    certificate_id,
                    new_attempts,
                    status,
                    error_message,
                    datetime.utcnow().isoformat()
                ))
                
                # Update certificate record
                cursor.execute("""
                    UPDATE certificates
                    SET attempts = ?, status = ?, updated_at = ?
                    WHERE certificate_id = ?
                """, (
                    new_attempts,
                    status,
                    datetime.utcnow().isoformat(),
                    certificate_id
                ))
                
                conn.commit()
                logger.info(f"Logged attempt {new_attempts} for {certificate_id}: {status}")
            else:
                logger.error(f"Certificate not found: {certificate_id}")
                
        except sqlite3.Error as e:
            logger.error(f"Error logging attempt: {e}")
        finally:
            conn.close()
    
    def get_certificate(self, certificate_id: str) -> Optional[Dict]:
        """Get certificate information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM certificates WHERE certificate_id = ?",
                (certificate_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        finally:
            conn.close()
    
    def get_attempts(self, certificate_id: str) -> List[Dict]:
        """Get all attempts for a certificate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM certificate_attempts 
                WHERE certificate_id = ?
                ORDER BY attempt_number DESC
            """, (certificate_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        finally:
            conn.close()
    
    def update_certificate_path(self, certificate_id: str, file_path: str):
        """Update certificate file path"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE certificates
                SET file_path = ?, updated_at = ?
                WHERE certificate_id = ?
            """, (
                file_path,
                datetime.utcnow().isoformat(),
                certificate_id
            ))
            
            conn.commit()
            
        finally:
            conn.close()


# Global database instance
certificate_db = CertificateDB()
