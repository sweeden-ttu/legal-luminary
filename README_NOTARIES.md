# Notary Public Directory

This directory contains tools and data for maintaining a directory of notary publics serving Bell County and Central Texas.

## Files

- `scripts/scrape-notaries.py` - Web crawler to collect notary information from Notary Rotary
- `_data/notaries.yml` - YAML data file containing notary information
- `_pages/notaries.md` - Jekyll page displaying the notary directory

## Setup

Install required Python packages:

```bash
uv pip install -r requirements_notaries.txt
```

Or using pip:

```bash
pip install -r requirements_notaries.txt
```

## Usage

Run the scraper to collect notary information:

```bash
python scripts/scrape-notaries.py
```

The script will:
1. Fetch the listing page from Notary Rotary
2. Extract all notary detail page URLs
3. Visit each detail page and extract:
   - Name and location
   - Phone number
   - Email address
   - Website
   - Experience and services
   - Addresses
   - Notary details (24hr service, fingerprinting, etc.)
4. Save all data to `_data/notaries.yml`

## Data Structure

The `notaries.yml` file contains an array of notary objects with the following structure:

```yaml
- name: "Notary Name"
  location: "City, State"
  phone: "phone number"
  email: "email@example.com"
  website: "http://website.com"
  experience: "Experience description"
  loan_signing_types: "Types of loan signings"
  general_notary_work: "Types of general notary work"
  compliance_skills: "Compliance and skills"
  equipment: "Equipment description"
  additional_services: "Additional services"
  availability: "Availability information"
  professional_standards: "Professional standards"
  credentials: "Credentials"
  service_area: "Service area"
  addresses:
    - type: "primary"
      address: "Full address"
  last_updated: "MM/DD/YYYY"
  hr_service: "Yes/No"
  does_fingerprinting: "Yes/No"
  has_laser_printer: "Yes/No"
  home_inspections: "Yes/No"
```

## Viewing the Directory

After running the scraper, the notary directory will be available at:

```
https://www.legalluminary.com/notaries/
```

The page displays all notaries with their contact information, services, and details in an easy-to-read format.

## Notes

- The scraper includes a 1-second delay between requests to be respectful to the Notary Rotary server
- Some notaries may not have email addresses listed (they may show "Please try back during normal business hours")
- The scraper handles various phone number formats and extracts them automatically
- Website URLs are automatically prefixed with `http://` if not already present

## Troubleshooting

If the scraper fails:
- Check your internet connection
- Verify the Notary Rotary website is accessible
- Some detail pages may have different HTML structure - the scraper includes fallback parsing methods
- Check the error messages in the console output
