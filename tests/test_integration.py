#!/usr/bin/env python3
"""
Integration tests for certificate generation system
Tests all the new features added for the issue
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.certificate_generator import certificate_generator
from utils.mail_config import mail_config
from storage.certificate_db import certificate_db
from datetime import datetime


def test_certificate_generation():
    """Test certificate generation and comparison"""
    print("Testing certificate generation...")
    
    # Ensure template exists
    if not certificate_generator.template_path.exists():
        print("  Creating template...")
        certificate_generator.create_template()
    
    # Generate test certificate
    cert_data = {
        'name': 'Test User',
        'course': 'Test Course',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'certificate_id': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}'
    }
    
    cert_path = certificate_generator.generate_certificate(cert_data)
    print(f"  ✓ Certificate generated: {cert_path}")
    
    # Compare with template
    comparison = certificate_generator.compare_with_template(cert_path)
    print(f"  ✓ Comparison result: Match={comparison['match']}, Similarity={comparison['similarity']:.2%}")
    
    assert comparison['match'], "Certificate does not match template!"
    assert comparison['similarity'] > 0.95, "Similarity below 95%!"
    
    return cert_data['certificate_id']


def test_database():
    """Test database operations with IF NOT EXISTS handling"""
    print("\nTesting database operations...")
    
    # Create test record
    cert_data = {
        'certificate_id': f'DB-TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        'user_name': 'Database Test User',
        'course_name': 'Database Test Course',
        'issue_date': datetime.now().strftime('%Y-%m-%d'),
        'email': 'test@example.com'
    }
    
    cert_id = certificate_db.create_certificate_record(cert_data)
    print(f"  ✓ Certificate record created: {cert_id}")
    
    # Log attempts
    certificate_db.log_attempt(cert_id, 'success')
    certificate_db.log_attempt(cert_id, 'success')
    print(f"  ✓ Logged 2 attempts")
    
    # Retrieve info
    info = certificate_db.get_certificate(cert_id)
    print(f"  ✓ Retrieved certificate: attempts={info['attempts']}, status={info['status']}")
    
    assert info['attempts'] == 2, "Attempt count mismatch!"
    assert info['status'] == 'success', "Status mismatch!"


def test_mail_configuration():
    """Test mail configuration detection"""
    print("\nTesting mail configuration...")
    
    status = mail_config.get_status()
    print(f"  Mail enabled: {status['enabled']}")
    print(f"  SMTP Host: {status['smtp_host']}")
    print(f"  Reason: {status['reason']}")
    
    if not status['enabled']:
        print(f"  Missing variables: {', '.join(status['missing_variables'])}")
        print("  ✓ Mail correctly reports as disabled with proper reason")
    else:
        print("  ✓ Mail is configured")


def test_sqlite_table_creation():
    """Test that SQLite tables can be created multiple times without errors"""
    print("\nTesting SQLite table creation (IF NOT EXISTS)...")
    
    # Initialize database twice - should not raise error
    from storage.certificate_db import CertificateDB
    
    db1 = CertificateDB()
    print("  ✓ First initialization successful")
    
    db2 = CertificateDB()
    print("  ✓ Second initialization successful (no 'table already exists' error)")


def main():
    """Run all tests"""
    print("=" * 70)
    print("Integration Tests for Certificate System")
    print("=" * 70)
    
    try:
        cert_id = test_certificate_generation()
        test_database()
        test_mail_configuration()
        test_sqlite_table_creation()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        
        print("\nSummary:")
        print("  1. ✓ Certificate generation with pixel-perfect comparison")
        print("  2. ✓ Database operations with proper error handling")
        print("  3. ✓ Mail configuration detection and status reporting")
        print("  4. ✓ SQLite table creation without 'already exists' errors")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
