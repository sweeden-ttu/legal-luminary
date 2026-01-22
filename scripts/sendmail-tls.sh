#!/bin/bash

# Postfix Sendmail Recursive Email Service
# Processes email queue recursively with opportunistic retry logic

set -euo pipefail

# Default configuration path
CONFIG_FILE="${CONFIG_FILE:-/etc/email-sender/config.conf}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Try project-local config if system config doesn't exist
if [[ ! -f "${CONFIG_FILE}" ]]; then
    CONFIG_FILE="${PROJECT_ROOT}/config/email-sender.conf"
fi

# Source configuration
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "ERROR: Configuration file not found: ${CONFIG_FILE}" >&2
    exit 1
fi

# Load configuration
source "${CONFIG_FILE}"

# Set defaults if not in config
QUEUE_DIR="${Queue_Directory:-${PROJECT_ROOT}/queue}"
PROCESSED_DIR="${Processed_Directory:-${QUEUE_DIR}/processed}"
FAILED_DIR="${Failed_Directory:-${QUEUE_DIR}/failed}"
LOG_DIR="${Log_Directory:-${PROJECT_ROOT}/logs}"
LOG_LEVEL="${Log_Level:-INFO}"
MAX_RETRIES="${Max_Retry_Attempts:-10}"
INITIAL_DELAY="${Initial_Retry_Delay:-60}"
MAX_DELAY="${Max_Retry_Delay:-3600}"
BACKOFF_MULT="${Retry_Backoff_Multiplier:-2}"
SENDER_EMAIL="${Sender_Email:-notary@legalluminary.com}"
EMAIL_SUBJECT="${Email_Subject:-fe79}"
USE_TLS="${Use_TLS:-true}"
VERIFY_TLS="${Verify_TLS:-true}"

# Create directories if they don't exist
mkdir -p "${QUEUE_DIR}" "${PROCESSED_DIR}" "${FAILED_DIR}" "${LOG_DIR}"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_file="${LOG_DIR}/email-sender-$(date '+%Y-%m-%d').log"
    
    # Check log level
    case "${LOG_LEVEL}" in
        DEBUG) ;;
        INFO)
            [[ "${level}" == "DEBUG" ]] && return
            ;;
        WARN)
            [[ "${level}" == "DEBUG" || "${level}" == "INFO" ]] && return
            ;;
        ERROR)
            [[ "${level}" != "ERROR" ]] && return
            ;;
    esac
    
    echo "[${timestamp}] [${level}] ${message}" | tee -a "${log_file}"
}

# Send email using postfix sendmail with TLS
send_email() {
    local email_file="$1"
    local recipient="${Low_Risk_Vendor}"
    local body
    
    # Read email body from file or use template
    if [[ -f "${email_file}" ]]; then
        body=$(cat "${email_file}")
    else
        # Use template if file doesn't exist
        local template_file="${PROJECT_ROOT}/templates/email-template.txt"
        if [[ -f "${template_file}" ]]; then
            body=$(cat "${template_file}")
        else
            body="Email content from queue item: ${email_file}"
        fi
    fi
    
    log "INFO" "Sending email to ${recipient} from file: ${email_file}"
    
    # Build sendmail command
    local sendmail_cmd="sendmail"
    local sendmail_args=("-t" "-f" "${SENDER_EMAIL}")
    
    # Add TLS flags if enabled
    if [[ "${USE_TLS}" == "true" ]]; then
        sendmail_args+=("-Am")  # Use submission port with TLS
    fi
    
    # Prepare email content
    local email_content=$(cat <<EOF
To: ${recipient}
Subject: ${EMAIL_SUBJECT}
Content-Type: text/plain; charset=UTF-8

${body}
EOF
)
    
    # Send email
    if echo "${email_content}" | "${sendmail_cmd}" "${sendmail_args[@]}" 2>&1; then
        log "INFO" "Email sent successfully to ${recipient}"
        return 0
    else
        local exit_code=$?
        log "ERROR" "Failed to send email to ${recipient} (exit code: ${exit_code})"
        return 1
    fi
}

# Process a single email file with retry logic
process_email_file() {
    local email_file="$1"
    local retry_count=0
    local delay="${INITIAL_DELAY}"
    
    while [[ ${retry_count} -lt ${MAX_RETRIES} ]]; do
        if send_email "${email_file}"; then
            # Success - move to processed directory
            local filename=$(basename "${email_file}")
            local processed_path="${PROCESSED_DIR}/${filename}.$(date +%s)"
            mv "${email_file}" "${processed_path}"
            log "INFO" "Moved processed email to: ${processed_path}"
            return 0
        else
            # Failure - implement exponential backoff
            retry_count=$((retry_count + 1))
            if [[ ${retry_count} -lt ${MAX_RETRIES} ]]; then
                log "WARN" "Retry attempt ${retry_count}/${MAX_RETRIES} after ${delay} seconds"
                sleep "${delay}"
                delay=$((delay * BACKOFF_MULT))
                if [[ ${delay} -gt ${MAX_DELAY} ]]; then
                    delay=${MAX_DELAY}
                fi
            fi
        fi
    done
    
    # All retries exhausted - move to failed directory
    local filename=$(basename "${email_file}")
    local failed_path="${FAILED_DIR}/${filename}.$(date +%s)"
    mv "${email_file}" "${failed_path}"
    log "ERROR" "All retry attempts exhausted. Moved to failed: ${failed_path}"
    return 1
}

# Recursively process queue directory
process_queue_recursive() {
    local queue_path="$1"
    local processed_count=0
    local failed_count=0
    
    log "INFO" "Starting recursive queue processing: ${queue_path}"
    
    # Find all files in queue directory (excluding processed and failed subdirectories)
    while IFS= read -r -d '' email_file; do
        # Skip processed and failed directories
        if [[ "${email_file}" == *"/processed/"* ]] || [[ "${email_file}" == *"/failed/"* ]]; then
            continue
        fi
        
        log "DEBUG" "Processing email file: ${email_file}"
        
        if process_email_file "${email_file}"; then
            processed_count=$((processed_count + 1))
        else
            failed_count=$((failed_count + 1))
        fi
        
    done < <(find "${queue_path}" -type f -not -path "*/processed/*" -not -path "*/failed/*" -print0 2>/dev/null || true)
    
    log "INFO" "Queue processing complete. Processed: ${processed_count}, Failed: ${failed_count}"
    
    return 0
}

# Main execution
main() {
    log "INFO" "Email sender service started"
    log "INFO" "Configuration file: ${CONFIG_FILE}"
    log "INFO" "Queue directory: ${QUEUE_DIR}"
    
    # Verify sendmail is available
    if ! command -v sendmail &> /dev/null; then
        log "ERROR" "sendmail command not found. Please install postfix."
        exit 1
    fi
    
    # Verify recipient email is configured
    if [[ -z "${Low_Risk_Vendor:-}" ]]; then
        log "ERROR" "Low_Risk_Vendor not configured in ${CONFIG_FILE}"
        exit 1
    fi
    
    # Process queue recursively
    process_queue_recursive "${QUEUE_DIR}"
    
    log "INFO" "Email sender service completed"
}

# Run main function
main "$@"
