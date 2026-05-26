import json
import os
import shutil
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from mistralai import Mistral
from pydantic import ValidationError
from validation import InvoiceModel

# Load API keys from environment
load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Establish base path boundaries relative to this specific script file
# Replaces hardcoded absolute routes to protect anonymity
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Internal folder architectures for unstructured data processing pipelines
RAW_FOLDER = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_FOLDER = os.path.join(PROJECT_ROOT, "data", "processed")
ARCHIVE_FOLDER = os.path.join(PROCESSED_FOLDER, "invoices_archive")
LOG_FILE = os.path.join(PROCESSED_FOLDER, "processed_log.json")
EXCEL_PATH = os.path.join(PROCESSED_FOLDER, "all_invoices.xlsx")
SUPPORTED_FORMATS = (".pdf", ".jpg", ".jpeg", ".png", ".tiff")

# Safe directory creation loop
for folder in [RAW_FOLDER, ARCHIVE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


# ==============================================================================
# PIPELINE AUDITING LOGIC (Prevents processing the same invoice multiple times)
# ==============================================================================
def is_already_processed(file_name):
    """Checks the JSON audit ledger file to see if the invoice has already been handled."""
    if not os.path.exists(LOG_FILE):
        return False
    try:
        with open(LOG_FILE, "r") as f:
            processed_files = json.load(f)
            return file_name in processed_files
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return False


def update_log(file_name):
    """Appends newly processed files into the JSON persistent state log."""
    processed_files = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                processed_files = json.load(f)
        except Exception:
            pass  # Fall back to an empty tracking collection block if parsing fails

    processed_files.append(file_name)
    with open(LOG_FILE, "w") as f:
        json.dump(processed_files, f)


# ==============================================================================
# CORE EXTRACTION BLOCKS (OCR Parsing and Large Language Model Processing)
# ==============================================================================
def process_invoice_ocr(file_name):
    """Sends the raw document stream to Mistral's dedicated OCR endpoint

    to isolate markdown layout schemas.
    """
    file_path = os.path.join(RAW_FOLDER, file_name)
    print(f"Starting cloud-level OCR tracking on: {file_name}")
    try:
        with open(file_path, "rb") as f:
            uploaded_file = client.files.upload(
                file={"file_name": file_name, "content": f.read()}, purpose="ocr"
            )

        # Grab transient viewing authorization endpoint link
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id)

        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "document_url", "document_url": signed_url.url},
        )
        return "\n".join([page.markdown for page in ocr_response.pages])
    except Exception as e:
        print(f"OCR Operational Failure on target system file: {e}")
        return None


def extract_structured_data(markdown_text):
    """Parses raw document blocks via mistral-large to enforce

    compliance-level JSON models.
    """
    print("--- Executing Semantic Cloud Extraction (Mistral Large) ---")

    # Aligned perfectly with your local pipeline properties to match final schema keys
    prompt = f"""
ACT AS A GERMAN TAX AUDITOR. Your task is to extract data from an invoice into JSON format.

ENTITY DEFINITIONS:
- VENDOR: The company SELLING the service (found in the HEADER or gray FOOTER area).
- CUSTOMER: The company BUYING the service (found near 'Rechnungsempfänger' or 'Auftraggeber').

FIELD-SPECIFIC RULES:
1. vendor_name: Extract the full legal name of the seller. Use footer markdown structures as priority references.
2. invoice_number: The unique 'Rechnungsnummer' or 'Original VAT Invoice Number'.
3. vendor_vat_id: Look for 'USt-IdNr.' or 'VAT ID' associated with the VENDOR.
4. customer_name: Extract the legal entity name located under 'Rechnungsempfänger', 'Auftraggeber', or 'Bill to'. Skip prefixes like 'An' or 'Herr/Frau'.
5. due_date: Find 'Fälligkeitsdatum', 'Zahlbar bis', or 'Due date'.
6. net_amount, tax_amount, gross_amount: Extract strictly as FLOATS. 
   - If German format (1.200,50), convert to standard decimal form (1200.50).
   - If English format (1,200.50), convert to standard decimal form (1200.50).
   - Extract the explicit TOTAL AMOUNT value if a standalone gross amount isn't found.
7. is_reverse_charge: Boolean (true/false). Set to true if 'Steuerschuldumkehr' or 'Reverse Charge' exists on the document.
8. date_issued: 'Rechnungsdatum' or 'Original VAT Invoice Date'.
9. currency: Extract the currency as a 3-letter ISO code (e.g., EUR, USD, GBP). If ambiguous indicators exist, normalize explicitly (e.g., '€' -> 'EUR', '$' -> 'USD').

OUTPUT FORMAT:
Return ONLY valid JSON corresponding exactly to the field schema keys. If a target field is completely missing from the text, return null. Do not include markdown wrapping or extra commentary outside the JSON block.

RAW DOCUMENT TEXT ENTRIES:
--- START TEXT ---
{markdown_text}
--- END TEXT ---
"""

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a German or English tax compliance AI agent specialized in extraction auditing.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    try:
        raw_json = json.loads(chat_response.choices[0].message.content)
        # Structural Verification Guard Stage
        validated_invoice = InvoiceModel.model_validate_json(
            json.dumps(raw_json)
        )
        return validated_invoice.model_dump()
    except ValidationError as val_err:
        print(
            f" Pydantic Schema Validation Failure in Cloud Ingestion Block: {val_err}"
        )
        return None
    except Exception as e:
        print(f" Internal Processing Exception during field parsing: {e}")
        return None


# ==============================================================================
# DATA PERSISTENCE & FILE STORAGE LOGIC
# ==============================================================================
def save_to_system(json_data, original_filename):
    """Maps structured model dumps into corresponding localized spreadsheet columns."""
    row_data = {
        "Vendor": json_data.get("vendor_name"),
        "Invoice_Num": json_data.get("invoice_number"),
        "VAT_ID": json_data.get("vendor_vat_id"),
        "Customer": json_data.get("customer_name"),
        "Date": json_data.get("date_issued"),
        "Due_Date": json_data.get("due_date"),
        "Net": json_data.get("net_amount"),
        "Tax": json_data.get("tax_amount"),
        "Gross": json_data.get("gross_amount"),
        "Currency": json_data.get("currency"),
        "Reverse_Charge": json_data.get("is_reverse_charge"),
    }

    new_df = pd.DataFrame([row_data])

    if os.path.exists(EXCEL_PATH):
        existing_df = pd.read_excel(EXCEL_PATH)
        final_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        final_df = new_df

    final_df.to_excel(EXCEL_PATH, index=False)


def run_single_pipeline(file_name):
    """Manages the end-to-end execution path for a single document file transaction."""
    if is_already_processed(file_name):
        print(f"Bypassing {file_name}: Log index matches already processed entry.")
        return {"status": "error", "message": "File already processed."}

    markdown = process_invoice_ocr(file_name)
    if not markdown:
        return None

    data = extract_structured_data(markdown)
    if data:
        save_to_system(data, file_name)
        update_log(file_name)
        # Reliably move completed file to safety archive
        shutil.move(
            os.path.join(RAW_FOLDER, file_name),
            os.path.join(ARCHIVE_FOLDER, file_name),
        )
        print(f"Pipeline complete for: {file_name}\n")
        return data

    print(f" Pipeline failed for target file entry: {file_name}\n")
    return None


# ==============================================================================
# INDUSTRIAL SYSTEM RUN BATCH LOOPS
# ==============================================================================
if __name__ == "__main__":
    # Scrapes unstructured storage blocks to isolate files matching supported targets
    files_to_process = [
        f
        for f in os.listdir(RAW_FOLDER)
        if f.lower().endswith(SUPPORTED_FORMATS)
    ]
    print(f"Located {len(files_to_process)} invoices waiting for ingestion runs...")

    for file_name in files_to_process:
        run_single_pipeline(file_name)