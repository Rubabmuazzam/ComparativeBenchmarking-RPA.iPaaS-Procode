# Supplementary Research Material: Evaluation Rubrics and Empirical Artifacts

This repository serves as the anonymous supplementary research appendix for the paper titled *"Comparative Benchmarking of Automation Software for Knowledge-Intensive Processes: A Design Science Study"*. 
It provides full transparency, reproducible source code, and granular scoring criteria supporting the platform evaluations presented in the manuscript.

---

## Section I: Detailed Evaluation Rubrics (Supports Table 2)

To avoid space-constrained abstractions in the primary text, this section formalizes the precise boundaries and definitions utilized to grade development constraints.

### 1. Skill Level Categorization
* **Level 1 (GUI-only):** Basic visual configuration within deterministic layout designers. No variable initialization, raw data schema mapping, or standard syntax handling required.
* **Level 2 (Workflow Logic / Data Mapping):** Requires intermediate flow architecture design, iterative collection loops, conditional routing trees, and custom API parameter mapping.
* **Level 3 (Full SDLC / Code Management):** Requires traditional engineering methodologies, including environment variables management, runtime execution debugging, external package compilation, and dependency monitoring.

### 2. Architectural Transparency
* **Low (Black-box):** Inbound and outbound execution layers are obfuscated by proprietary cloud software. Payload inspection, internal intermediate states, and lower-level network logs are heavily restricted.
* **Medium (Partial Visibility):** Standard execution histories are accessible via graphical administrative dashboards, but lower-level data transformations and payload mutations are restricted during node processing.
* **High (Native Inspection):** Complete runtime inspection is available natively. Execution telemetry outputs full contextual data structures (e.g., native JSON/Schema payloads) at each sequential step.
* **Infinite (Full Internal Access):** Complete programmatic control over memory allocation, active environment execution blocks, internal program state values, and custom logging targets.

---

## Section II: Step Breakdowns & Granular Field Accuracy Logs (Supports Table 3)

The empirical evaluation traces explicit platform activities across common administrative extraction goals. 

### 1. Sequence Breakdowns by Platform
* **Power Automate (3 Steps):** `Trigger: File Creation (OneDrive) -> AI Builder (Pre-trained Extraction) -> Excel Row Insertion`.
* **UiPath (12 Steps):** `Assign Path -> Build DataTable -> For Each Loop -> Load Taxonomy -> Digitize Document (OmniPage OCR) -> Classify Document -> Keyword Classifier -> Data Extraction Scope -> ML Extractor -> Export Results -> Merge DataTable -> Write Workbook Range`.
* **Make (4 Steps):** `Gmail Watch -> Get Attachment -> Iterator -> AI Document Extractor -> Google Sheets Append`.
* **n8n (7 Steps):** `Google Drive Trigger -> Download File Binary -> Parse PDF content -> Edit Fields Mapping -> LLM Node Model Message -> JavaScript Formatting -> Append Sheet Row`.

### 2. Granular Field Accuracy Score Sheets (Scale: 1 to 5)

| Field Parameter | Power Automate (Pre-trained) | UiPath (Pre-trained) | Make (Pre-trained) | Custom Models (UiPath/PA) |
| :--- | :---: | :---: | :---: | :---: |
| **Vendor Name** | 5 | 5 | 5 | Correct / Mostly Correct |
| **Billed To / Customer** | — | 5 | — | Correct |
| **VAT ID** | 5 | 2 *(Missing in 2 cases)* | 5 | Correct |
| **Currency** | 5 | 5 | 5 | Correct *(1 Ambiguous case in PA)* |
| **Invoice Number** | 3 *(Double value collision)* | 3 *(Multiple value collision)* | 5 | Correct |
| **Invoice Date** | 3 *(Captured credit note)* | 3 *(Captured credit note)* | 5 | Correct |
| **Total Amount** | 5 | 5 | 5 | Correct |
| **Service Period** | 4 | 0 *(Unsupported in ML)* | 4 | Correct |
| **Subtotal** | 4 | 0 *(Unsupported in ML)* | 0 | Correct |
| **Average Score** | **4.25** | **2.88** | **4.25** | **4.75 - 4.88** |

---

## Section III: MCDA Scoring Matrix Revisions (Supports Table 4)

The Multi-Criteria Decision Analysis (MCDA) metrics are evaluated against clustered performance benchmarks to maintain strict analytical objectivity:

* **Processing Speed (Latency Clusters):**
  * **Score 5:** 0–5 seconds *(Near real-time execution)*
  * **Score 4:** >5–20 seconds *(Fast operational response)*
  * **Score 3:** >20–60 seconds *(Acceptable enterprise automated latency)*
  * **Score 2:** >60–180 seconds *(Slow processing with visible execution blockages)*
  * **Score 1:** >180 seconds *(Severe processing delays; unfeasible for real-time loops)*
* **Resource Availability Constraints:**
  * **Score 5 (Highly Favorable):** Effectively unlimited open-source or enterprise platform allocation.
  * **Score 3 (Medium):** Moderate processing limits with manageable administrative overhead.
  * **Score 1 (Unfavorable):** Restricted trial quotas or steep local hardware compute dependencies.
* **Monitoring & Observability Frameworks:**
  * **Score 5 (Native):** Automatic dashboard compilation, historical tracing, and built-in alerts.
  * **Score 1 (Manual):** Telemetry tracking, retry loops, and error logging must be programmatically injected.

---

## Section IV: Repositories and Source Code Artifacts

The repository includes full scripts deployed during evaluation. Below is the deterministic system prompting paradigm utilized within the `Python + Local LLM` and `Python + Mistral Cloud` environments to execute zero-shot extraction:

```python
# System prompt context for German tax law compliance pipeline
prompt = f"""
ACT AS A GERMAN TAX AUDITOR. Your task is to extract data from an invoice into JSON.
ENTITY DEFINITIONS:
- VENDOR: The company SELLING the service (found in the HEADER or gray FOOTER).
- CUSTOMER: The company BUYING the service (found near 'Rechnungsempfänger' or 'Auftraggeber').

FIELD-SPECIFIC RULES:
1. vendor_name: Extract the full legal name from the FOOTER at {footer_text}.
2. invoice_number: The unique 'Rechnungsnummer' or 'Original VAT Invoice Number'.
3. vendor_vat_id: Look for 'USt-IdNr.' or 'VAT ID' associated with the VENDOR (often in the footer).
4. customer_name: Extract the name located directly under 'Rechnungsempfänger' or 'Auftraggeber' or 'Bill to'. Skip 'An' or 'Herr/Frau'.
5. due_date: Find 'Fälligkeitsdatum' or 'Zahlbar bis' or 'Due date'.
6. net_amount, tax_amount/Mwst, gross_amount: Extract as FLOATS. 
   - If German format (1.200,50), convert to (1200.50).
   - If English format (1,200.50), convert to (1200.50). Extract TOTAL AMOUNT if gross amount not found.
7. is_reverse_charge: Boolean (true/false). Set to true if 'Steuerschuldumkehr' or 'Reverse Charge' exists.
8. date_issued: 'Rechnungsdatum' or 'Original VAT Invoice Date'.
9. currency: Extract the currency as a 3-letter ISO code (e.g., EUR, USD, GBP).
   - If you see '€', return 'EUR'.
   - If you see '$', return 'USD'.

OUTPUT FORMAT:
Return ONLY valid JSON. If a field is missing, use null.
"""
