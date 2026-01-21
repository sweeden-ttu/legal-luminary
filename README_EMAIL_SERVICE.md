# Postfix Sendmail Recursive Email Service

## Overview

A systemd service that runs a recursively opportunistic email algorithm using postfix sendmail with TLS encryption. The service processes email queue items and automatically retries failed sends until successful.

## Architecture

```
┌─────────────────┐
│  Systemd Service│
│  (email-sender) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Main Script    │
│  (sendmail-tls) │
└────────┬────────┘
         │
         ├──► Process Queue (recursive)
         │    └──► For each email in queue
         │
         └──► Retry Logic (opportunistic)
              └──► Retry failed sends until success
```

## Components

### 1. Configuration File

**Location:** `/etc/email-sender/config.conf` (or project-local `config/email-sender.conf`)

- Hidden variable `Low_Risk_Vendor` storing the recipient email address
- Email subject: `fe79`
- TLS settings for postfix
- Retry configuration (max attempts, delay intervals)
- Queue directory path

### 2. Main Script

**Location:** `scripts/sendmail-tls.sh`

**Features:**

- Reads "Low Risk Vendor" email from config
- Uses postfix sendmail with TLS flags
- Processes email queue recursively
- Implements opportunistic retry logic for failed sends
- Logs all operations

**Sendmail Command Structure:**

```bash
# Basic TLS sendmail example
sendmail -t -f "sender@domain.com" <<EOF
To: ${Low_Risk_Vendor}
Subject: fe79
Content-Type: text/plain; charset=UTF-8

${EMAIL_BODY}
EOF
```

**With explicit TLS/SSL:**

```bash
sendmail -Am -t -f "sender@domain.com" <<EOF
...
EOF
```

### 3. Email Queue System

**Location:** `queue/` directory

- Queue files containing email data to process
- Processing script recursively reads queue directory
- Moves processed items to `queue/processed/`
- Moves failed items to `queue/failed/` for retry

### 4. Systemd Service File

**Location:** `systemd/email-sender.service`

- Service definition for manual execution
- Environment variables
- Logging configuration
- Dependency on postfix service

### 5. Template System

**Location:** `templates/email-template.txt`

- Email body template
- Variable substitution support
- Support for dynamic content

## Installation

### 1. Install Dependencies

Ensure postfix is installed and configured:

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install postfix

# RHEL/CentOS
sudo yum install postfix
```

### 2. Copy Files to System Locations

```bash
# Create system directories
sudo mkdir -p /etc/email-sender
sudo mkdir -p /usr/local/bin
sudo mkdir -p /var/lib/email-sender/queue/{processed,failed}
sudo mkdir -p /var/log/email-sender

# Copy configuration (edit with your settings)
sudo cp config/email-sender.conf /etc/email-sender/config.conf
sudo chmod 600 /etc/email-sender/config.conf

# Copy script
sudo cp scripts/sendmail-tls.sh /usr/local/bin/sendmail-tls.sh
sudo chmod +x /usr/local/bin/sendmail-tls.sh

# Copy systemd service
sudo cp systemd/email-sender.service /etc/systemd/system/email-sender.service

# Copy template
sudo mkdir -p /etc/email-sender/templates
sudo cp templates/email-template.txt /etc/email-sender/templates/
```

### 3. Configure Email Settings

Edit `/etc/email-sender/config.conf`:

```bash
sudo nano /etc/email-sender/config.conf
```

Set the `Low_Risk_Vendor` email address and other settings as needed.

### 4. Reload Systemd and Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable email-sender.service
```

## Usage

### Manual Execution

Run the service manually:

```bash
sudo systemctl start email-sender.service
```

### Check Status

```bash
sudo systemctl status email-sender.service
```

### View Logs

```bash
# Systemd logs
sudo journalctl -u email-sender.service -f

# Application logs
tail -f /var/log/email-sender/email-sender-$(date +%Y-%m-%d).log
```

### Adding Emails to Queue

Place email content files in the queue directory:

```bash
echo "Email body content here" | sudo tee /var/lib/email-sender/queue/email-$(date +%s).txt
```

Or use the project-local queue:

```bash
echo "Email body content here" > queue/email-$(date +%s).txt
```

## Configuration Options

### Configuration File Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `Low_Risk_Vendor` | Recipient email address | Required |
| `Email_Subject` | Email subject line | `fe79` |
| `Sender_Email` | Sender email address | `sender@domain.com` |
| `Use_TLS` | Enable TLS encryption | `true` |
| `Verify_TLS` | Verify TLS certificates | `true` |
| `Max_Retry_Attempts` | Maximum retry attempts | `10` |
| `Initial_Retry_Delay` | Initial delay in seconds | `60` |
| `Max_Retry_Delay` | Maximum delay in seconds | `3600` |
| `Retry_Backoff_Multiplier` | Exponential backoff multiplier | `2` |
| `Queue_Directory` | Queue directory path | `/var/lib/email-sender/queue` |
| `Log_Directory` | Log directory path | `/var/log/email-sender` |
| `Log_Level` | Logging level (DEBUG/INFO/WARN/ERROR) | `INFO` |

## Implementation Details

### Recursive Queue Processing

- Script recursively scans queue directory
- Processes each email item
- Handles nested directories if needed
- Maintains processing state
- Skips `processed/` and `failed/` subdirectories

### Opportunistic Retry Logic

- On send failure, retries with exponential backoff
- Maximum retry attempts configurable
- Delay increases: initial_delay * (backoff_multiplier ^ retry_count)
- Maximum delay cap prevents excessive waits
- Logs all retry attempts
- Moves to `failed/` directory after all retries exhausted

### TLS Configuration

- Uses postfix sendmail with TLS/STARTTLS via `-Am` flag
- Verifies TLS connection when enabled
- Handles certificate validation
- Logs TLS handshake status

## Security Considerations

### File Permissions

```bash
# Configuration file should be readable only by root
sudo chmod 600 /etc/email-sender/config.conf

# Script should be executable by root
sudo chmod 755 /usr/local/bin/sendmail-tls.sh

# Queue directories should be writable by service user
sudo chmod 755 /var/lib/email-sender/queue
```

### Secure Handling

- Config file permissions (600) to protect "Low Risk Vendor" email
- Secure handling of email addresses
- TLS encryption for all sends
- Input validation for queue items
- Rate limiting for retry attempts (configurable)

### Systemd Security Features

The service file includes:

- `NoNewPrivileges=true` - Prevents privilege escalation
- `PrivateTmp=true` - Private temporary directory
- `ProtectSystem=strict` - Read-only filesystem protection
- `ProtectHome=true` - Protects home directories
- `ReadWritePaths` - Explicit writable paths

## Testing

### Test Configuration

```bash
# Test script with project-local config
CONFIG_FILE=./config/email-sender.conf ./scripts/sendmail-tls.sh
```

### Test Email Sending

1. Create a test email file:

```bash
echo "Test email body" > queue/test-email.txt
```

2. Run the service:

```bash
sudo systemctl start email-sender.service
```

3. Check logs:

```bash
sudo journalctl -u email-sender.service
tail -f logs/email-sender-$(date +%Y-%m-%d).log
```

4. Verify email was sent and moved:

```bash
ls -la queue/processed/
```

### Integration Testing

- Unit tests for queue processing
- Integration tests with mock postfix
- Test TLS connection handling
- Test retry logic with simulated failures
- Manual execution verification

## Troubleshooting

### Common Issues

**1. sendmail command not found**

```bash
# Install postfix
sudo apt-get install postfix  # Debian/Ubuntu
sudo yum install postfix      # RHEL/CentOS
```

**2. Permission denied errors**

```bash
# Check file permissions
ls -la /etc/email-sender/config.conf
ls -la /usr/local/bin/sendmail-tls.sh

# Fix permissions
sudo chmod 600 /etc/email-sender/config.conf
sudo chmod 755 /usr/local/bin/sendmail-tls.sh
```

**3. Configuration file not found**

The script will try:
1. `/etc/email-sender/config.conf` (system-wide)
2. `./config/email-sender.conf` (project-local)

Set `CONFIG_FILE` environment variable to override.

**4. Emails not sending**

- Check postfix status: `sudo systemctl status postfix`
- Check postfix logs: `sudo tail -f /var/log/mail.log`
- Verify TLS configuration in postfix
- Test sendmail manually: `echo "test" | sendmail -t recipient@example.com`

**5. Queue files not processing**

- Verify queue directory exists and is writable
- Check script logs for errors
- Ensure files are in the queue directory (not subdirectories)

## Dependencies

- Postfix mail server installed and configured
- sendmail command available
- TLS certificates configured for postfix
- Systemd (for service management)
- Bash 4.0+ (for associative arrays and advanced features)

## Development

### Project Structure

```
legal-luminary/
├── config/
│   └── email-sender.conf          # Configuration file
├── scripts/
│   └── sendmail-tls.sh            # Main script
├── systemd/
│   └── email-sender.service       # Systemd service
├── templates/
│   └── email-template.txt         # Email template
├── queue/
│   ├── processed/                 # Successfully sent emails
│   └── failed/                    # Failed emails
└── logs/                          # Application logs
```

### Local Development

For local development without system installation:

```bash
# Use project-local config
export CONFIG_FILE=./config/email-sender.conf

# Run script directly
./scripts/sendmail-tls.sh
```

## License

This service is part of the Legal Luminary project.

## Support

For issues or questions, refer to the main project README or create an issue in the repository.
