import os
import fitz  # PyMuPDF
import ollama
from pydantic import ValidationError
from validation import InvoiceModel


def extract_footer_text(file_path, footer_ratio=0.25):
    """Extracts bounding-box text blocks located inside the bottom section

    of the document to preserve vendor metadata.
    """
    doc = fitz.open(file_path)
    footer_text = []

    for page in doc:
        page_height = page.rect.height
        blocks = page.get_text("blocks")

        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            if y0 >= page_height * (1 - footer_ratio):
                footer_text.append(text.strip())

    doc.close()
    return "\n".join(footer_text)


def get_pdf_text(file_path):
    """Extracts all selectable text segments across document pages."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def process_invoice(file_name):
    """Processes unstructured PDF text using Mistral and enforces validation schemas."""
    file_path = os.path.join("data", "raw", file_name)

    # Core existence check
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    print(f"Processing {file_name} with Mistral...")
    raw_text = get_pdf_text(file_path)
    footer_text = extract_footer_text(file_path)

    if not raw_text:
        print("No selectable text found within the target PDF document.")
        return None

    # Optimized and isolated prompt targeting compliance validation
    prompt = f"""
ACT AS A GERMAN TAX AUDITOR. Your task is to extract data from an invoice into JSON format.

ENTITY DEFINITIONS:
- VENDOR: The company SELLING the service (found in the HEADER or gray FOOTER area).
- CUSTOMER: The company BUYING the service (found near 'Rechnungsempfänger' or 'Auftraggeber').

FIELD-SPECIFIC RULES:
1. vendor_name: Extract the full legal name of the seller. Use this isolated footer context as high-priority reference: {footer_text}
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
{raw_text}
--- END TEXT ---
"""

    try:
        response = ollama.generate(
            model="mistral",
            prompt=prompt,
            format="json",
            options={
                "temperature": 0,  # Forces deterministic zero-shot consistency
                "top_p": 0.1,  # Anchor to high-probability tokens
                "seed": 42,  # Stabilizes tracking execution runs
                "num_predict": 1024,  # Halts programmatic looping boundaries
            },
        )

        # Safety Net Validation Stage
        json_output = response["response"]
        invoice_obj = InvoiceModel.model_validate_json(json_output)

        print("\n SUCCESS! Pydantic Safety Net Passed.")
        print(f"   Vendor Name:    {invoice_obj.vendor_name}")
        print(f"   Invoice Number: {invoice_obj.invoice_number}")
        print(f"   Vendor VAT ID:  {invoice_obj.vendor_vat_id}")
        print(f"   Due Date:       {invoice_obj.due_date}")
        print(f"   Customer Name:  {invoice_obj.customer_name}")
        print(f"   Net Amount:     {invoice_obj.net_amount}")
        print(f"   Gross Amount:   {invoice_obj.gross_amount}")
        print(f"   Tax Amount:     {invoice_obj.tax_amount}")
        print(f"   Reverse Charge: {invoice_obj.is_reverse_charge}")
        print(f"   Date Issued:    {invoice_obj.date_issued}")
        print(f"   Currency Type:  {invoice_obj.currency}\n")

        return invoice_obj.model_dump_json()

    except ValidationError as val_error:
        print(
            f" Pydantic Schema Validation Failed. Model returned invalid format layout: {val_error}"
        )
        return None
    except Exception as e:
        print(f" Error encountered during automation pipeline processing: {e}")
        return None


if __name__ == "__main__":
   
    process_invoice("-------.pdf")