# Certificate Generation System

This module provides certificate generation with pixel-perfect accuracy, mail configuration, and comprehensive status monitoring.

## Features Implemented

### 1. Certificate Generation with Image Comparison
- **Template-based generation**: Uses `templates/Sample_certificate.png` as the reference
- **Pixel-perfect comparison**: Compares generated certificates against the template
- **Field positioning**: Ensures all fields (name, course, date, certificate ID) are at exact vertical positions
- **Similarity scoring**: Validates generated certificates match template with >95% similarity

### 2. Mail Configuration
- **GitHub Secrets support**: Reads SMTP configuration from environment variables
- **Status detection**: Automatically detects if mail is properly configured
- **Detailed error reporting**: Shows which environment variables are missing
- **Safe fallback**: System works without mail if not configured

Required environment variables:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

### 3. Database with Proper Error Handling
- **IF NOT EXISTS**: All table creations use `IF NOT EXISTS` to prevent SQLite errors
- **Attempt tracking**: Logs all certificate generation attempts
- **Status monitoring**: Tracks success/failure of each generation

### 4. Waiting Page with Attempts Counter
- **Real-time updates**: Polls server every 2 seconds for status
- **Attempt display**: Shows number of generation attempts
- **Auto-redirect**: Redirects to download when complete
- **Location**: `/certificate/waiting?id=CERT_ID`

### 5. Enhanced System Status Page
- **Mail configuration status**: Shows detailed mail setup with reasons
- **Missing variables**: Lists which environment variables need to be set
- **Certificate system**: Shows template status and success rate
- **Database status**: Monitors database connection and tables
- **Bot status**: Shows AI bot and model manager status
- **Location**: `/system/status`

## API Endpoints

### Certificate Management
- `POST /api/certificate/generate` - Generate a new certificate
- `GET /api/certificate/status/{cert_id}` - Get certificate status with attempts

### System Status
- `GET /api/system/status` - Get comprehensive system status (JSON)
- `GET /system/status` - View system status dashboard (HTML)

### UI Pages
- `GET /certificate/waiting?id={cert_id}` - Waiting page with attempts counter
- `GET /system/status` - System status dashboard

## Usage Examples

### Generate Certificate
```python
from src.utils.certificate_generator import certificate_generator

cert_data = {
    'name': 'John Doe',
    'course': 'Python Programming',
    'date': '2025-10-31',
    'certificate_id': 'CERT-001'
}

cert_path = certificate_generator.generate_certificate(cert_data)
comparison = certificate_generator.compare_with_template(cert_path)
print(f"Match: {comparison['match']}, Similarity: {comparison['similarity']}")
```

### Check Mail Configuration
```python
from src.utils.mail_config import mail_config

status = mail_config.get_status()
if status['enabled']:
    print("Mail is configured")
else:
    print(f"Reason: {status['reason']}")
    print(f"Missing: {status['missing_variables']}")
```

### Database Operations
```python
from src.storage.certificate_db import certificate_db

# Create record
cert_data = {
    'certificate_id': 'CERT-001',
    'user_name': 'John Doe',
    'course_name': 'Python Programming',
    'issue_date': '2025-10-31',
    'email': 'john@example.com'
}

certificate_db.create_certificate_record(cert_data)

# Log attempt
certificate_db.log_attempt('CERT-001', 'success')

# Get info
info = certificate_db.get_certificate('CERT-001')
print(f"Attempts: {info['attempts']}")
```

## Testing

Run the integration tests:
```bash
python tests/test_integration.py
```

## Files Added/Modified

### New Files
- `src/utils/certificate_generator.py` - Certificate generation system
- `src/utils/mail_config.py` - Mail configuration and sending
- `src/storage/certificate_db.py` - Certificate database with proper error handling
- `static/waiting.html` - Waiting page with attempts counter
- `static/status.html` - System status dashboard
- `templates/Sample_certificate.png` - Certificate template
- `tests/test_integration.py` - Integration tests

### Modified Files
- `web/web_app.py` - Added certificate and status API endpoints
- `.env.example` - Added mail configuration variables
- `.gitignore` - Excluded generated certificates but keep template

## Issue Fixes

✅ **Issue 1**: Certificate comparison - Now compares generated PNG to template with pixel-perfect accuracy
✅ **Issue 2**: Mail configuration - Properly reads from GitHub secrets/env vars with detailed error reporting
✅ **Issue 3**: SQLite table errors - All tables use `IF NOT EXISTS` to prevent errors
✅ **Issue 4**: Waiting page attempts - Shows real-time attempt counter
✅ **Issue 5**: System status - Shows mail configuration status with detailed reasons
