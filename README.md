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
* **Make (5 Steps):** `Gmail Watch -> Get Attachment -> Iterator -> AI Document Extractor -> Google Sheets Append`.
* **n8n (7 Steps):** `Google Drive Trigger -> Download File Binary -> Parse PDF content -> Edit Fields Mapping -> LLM Node Model Message -> JavaScript Formatting -> Append Sheet Row`.

### 2. Granular Baseline Field Accuracy Score Sheets (Scale: 1 to 5)

| Field Parameter Target | Power Automate (Pre-trained) | UiPath (Pre-trained) | Make.com (Pre-trained) | Local Python (Mistral) | n8n Workflow (LLM Node) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Vendor Identity** | 5 | 5 | 5 | 5 | 5 |
| **VAT Registration ID** | 5 | 2 | 5 | 5 | 5 |
| **Currency Formats** | 5 | 5 | 5 | 5 | 5 |
| **Invoice Identifier No.** | 3 | 3 | 5 | 4 | 5 |
| **Invoice Issuance Date** | 3 | 3 | 5 | 3 | 5 |
| **Total Liability Amount** | 5 | 5 | 5 | 5 | 5 |
| **Service Period Tracking** | 4 | 0 | 4 | 5 | 5 |
| **Subtotal Accounting** | 4 | 0 | 0 | 5 | 5 |
| **Calculated Mean Score** | **4.25** | **2.88** | **4.25** | **4.25** | **5.00** |

> **Exclusion Note on Cloud-Native Variant Pipelines:** Highly optimized cloud architectures—specifically the **Cloud Mistral (API) Python Ingestion Pipeline** and enterprise cloud LLM nodes—are omitted from this baseline error evaluation matrix. Because these variants leverage unconstrained remote infrastructure, decoupled high-fidelity OCR endpoints (`mistral-ocr-latest`), and advanced context models (`mistral-large-latest`), they achieved a perfect 100% data extraction accuracy rate (Score: 5.00) across all fields and document test shapes exhibiting zero operational failure variations.

---

## Section III: MCDA Scoring Matrix Revisions (Supports Table 4)

The Multi-Criteria Decision Analysis (MCDA) metrics are evaluated against clustered performance benchmarks to maintain strict analytical objectivity:

* **Processing Speed (Latency Clusters):**
  * **Score 5:** 0–5 seconds *(Near real-time execution; achieved by cloud API pipelines)*
  * **Score 4:** >5–20 seconds *(Fast operational response with minimal latency footprint)*
  * **Score 3:** >20–60 seconds *(Acceptable standard office automated latency)*
  * **Score 2:** >60–180 seconds *(Slow processing with visible execution blockages)*
  * **Score 1:** >180 seconds *(Severe processing delays; unfeasible for scalable real-time loops)*
* **Resource Availability Constraints:**
  * **Score 5 (Highly Favorable):** Effectively unlimited open-source or unmetered cloud framework allocation thresholds.
  * **Score 3 (Medium):** Moderate processing limits with manageable administrative overhead or subscription parameters.
  * **Score 1 (Unfavorable):** Restricted trial quotas or steep local hardware compute inferencing dependencies.
* **Monitoring & Observability Frameworks:**
  * **Score 5 (Native):** Automatic dashboard compilation, historical trace routing, and built-in alerts.
  * **Score 1 (Manual):** Telemetry tracking, execution retry loops, and error auditing logging must be programmatically injected from scratch.

---

## Section IV: Repositories and Source Code Artifacts

The repository includes the full modular scripts deployed during evaluation within the `/process_artifacts/` directory. Below is the deterministic system prompting paradigm utilized within the pipeline environments to execute zero-shot extraction:

```python
# Unified Tax Compliance Prompt Paradigm utilized across Local and Cloud Pipelines
prompt = f"""
ACT AS A GERMAN TAX AUDITOR. Your task is to extract data from an invoice into JSON format.

ENTITY DEFINITIONS:
- VENDOR: The company SELLING the service (found in the HEADER or gray FOOTER area).
- CUSTOMER: The company BUYING the service (found near 'Rechnungsempfänger' or 'Auftraggeber').

FIELD-SPECIFIC RULES:
1. vendor_name: Extract the full legal name of the seller. Use footer layout structures as priority references.
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
"""
