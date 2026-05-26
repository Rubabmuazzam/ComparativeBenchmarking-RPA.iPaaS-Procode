# Supplementary Empirical Appendix: Granular Evaluation Logs and Platform Metrics

This document contains the complete, unabridged reference data, metrics, step-by-step sequences, and scoring rubrics supporting the platform evaluations presented in the primary manuscript.

---

## Appendix Table 1: Detailed Software Pipeline Implementations (Step-by-Step Sequences)
*This ledger validates the exact sequence counts (3 steps for Power Automate, 12 steps for UiPath, 5 steps for Make, and 7 nodes for n8n) utilized to score development complexity metrics.*

| Platform / Variant | Step No. | Component / Activity Name | Empirical Function in Knowledge-Intensive Process (KiP) |
| :--- | :---: | :--- | :--- |
| **Power Automate** | 1 | `Trigger: On File Creation` | Polls and monitors a target OneDrive folder for incoming unstructured multilingual invoice payloads. |
| *(Pre-trained & Custom)*| 2 | `AI Builder Node` | Invokes cognitive extraction layers (either out-of-the-box or fine-tuned) to parse document text blocks. |
| | 3 | `Add a Row into Table` | Automatically maps extracted bounding-box key-values directly into target Excel database rows. |
| **UiPath** | 1 | `Assign Activity` | Programmatically defines and instantiates localized project folder directory file system paths. |
| *(Document Understanding)*| 2 | `Build Data Table` | Allocates systemic runtime memory and provisions an empty schema data structure collection. |
| | 3 | `For Each File in Folder` | Instantiates a looping array iterator across the localized target invoice document directory. |
| | 4 | `Load Taxonomy` | Ingests the formal logical blueprint metadata model defining fields (e.g., Vendor, VAT ID, Amounts). |
| | 5 | `Digitize Document` | Deploys the OmniPage OCR engine to parse raw visual pixels into machine-readable text arrays. |
| | 6 | `Classify Document Scope` | Establishes the conditional classification boundary layers for incoming business documents. |
| | 7 | `Keyword Based Classifier` | Executes logical string matching rules to confirm the document matches an invoice layout taxonomy. |
| | 8 | `Data Extraction Scope` | Runs the execution engine layer responsible for field-by-field value and bounding-box parsing. |
| | 9 | `Machine Learning Extractor` | Queries the target model endpoint (Pre-trained baseline or fine-tuned Custom Model) to extract fields. |
| | 10 | `Export Extraction Results` | Serializes the deep extraction object array into a flat, loop-accessible system dataset object. |
| | 11 | `Merge Data Table` | Appends current loop transaction fields to the global master data table initialized in Step 2. |
| | 12 | `Write Range (Workbook)` | Commit-writes the consolidated in-memory ledger arrays into a persistent physical Excel document. |
| **Make.com** | 1 | `Gmail: Watch Emails` | Establishes a scheduled webhook/polling listener targeting inbound attachments in a mailbox. |
| | 2 | `Gmail: Get Attachment` | Pulls the raw binary file stream payload from secure mail servers into the workflow memory engine. |
| | 3 | `System Flow Iterator` | Deconstructs multi-file attachment arrays into individual linear downstream transaction queues. |
| | 4 | `AI Document Extractor` | Passes individual document objects into a pre-trained visual parsing core node. |
| | 5 | `Google Sheets: Add Row` | Appends extracted layout strings directly into individual spreadsheet lines on a cloud ledger. |
| **n8n** | 1 | `Google Drive Trigger` | Automated webhook node monitoring target cloud drive directories for new invoice creation. |
| | 2 | `Download File Binary` | Downloads localized binary streams of files directly from secure cloud infrastructure. |
| | 3 | `Extract from File (PDF)` | Deploys localized programmatic layout parsing engines to break binary data into a string chunk. |
| | 4 | `Edit Fields Mapping` | Formats data properties and prepares internal variables to be processed by downstream nodes. |
| | 5 | `Basic LLM Chat Node` | Routes the extracted document chunk to an integrated language model endpoint via custom prompts. |
| | 6 | `Code / JavaScript formatting` | Normalizes text, sanitizes outputs, and converts the LLM string block into clean JSON schema keys. |
| | 7 | `Google Sheets: Append Row` | Commits validated data keys as clean tabular tracking rows into a target spreadsheet. |

---

## Appendix Table 2: Granular Baseline Field-Level Extraction Accuracy Scores
*This matrix logs every attribute evaluation and maps out the arithmetic averages to ensure perfect analytical alignment with the paper's text. It contrasts commercial out-of-the-box extraction models against developer-orchestrated local pipelines.*

| Extraction Target Field | Power Automate (Pre-trained) | UiPath (Pre-trained) | Make.com (Pre-trained) | Local Python (Mistral/Ollama) | n8n Workflow (LLM Chat Node) | Target Performance Variances & Failure Mode Annotations |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Vendor Identity** | 5 | 5 | 5 | 5 | 5 | **High Stability:** Consistently isolated legal seller entities across varying header shapes. |
| **VAT Registration ID** | 5 | 2 | 5 | 5 | 5 | **UiPath Drop:** Failed to locate, map, or extract regional tax registration strings in 2 test files. |
| **Currency Formats** | 5 | 5 | 5 | 5 | 5 | **High Stability:** Isolated 3-letter ISO and local character symbols (€, $, £) seamlessly. |
| **Invoice Identifier No.** | 3 | 3 | 5 | 4 | 5 | **Collision Error (PA/UiPath):** Grabbed incorrect purchase order or tracking codes when multiple numbers appeared. |
| **Invoice Issuance Date** | 3 | 3 | 5 | 3 | 5 | **Collision Error (PA/UiPath):** Grabbed alternative transaction/credit-note timestamps instead of invoice issuance dates. |
| **Total Liability Amount** | 5 | 5 | 5 | 5 | 5 | **High Stability:** Successfully captured final transaction liabilities across layouts. |
| **Service Period Tracking** | 4 | 0 | 4 | 5 | 5 | **Native Constraints:** Extracted cleanly via start/end fields in PA/Make; **completely omitted** in UiPath ML layer. |
| **Subtotal Accounting** | 4 | 0 | 0 | 5 | 5 | **Model Boundaries:** Mapped with slight formatting shifts in PA; **wholly unextractable** in UiPath/Make baselines. |
| **Calculated Mean Score** | **4.25** | **2.88** | **4.25** | **4.25** | **5.00** | *Evaluation Scale Criteria: 1 (Wholly Incorrect/Missing Data) to 5 (Perfect Extraction across all instances).* |

### Methodological Note on Cloud-Native Pro-Code and Low-Code Pipelines
> **Exclusion Note on Cloud-Native Variant Pipelines:** Highly optimized cloud architectures—specifically the **Cloud Mistral (API) Python Ingestion Pipeline** and enterprise cloud LLM nodes—are intentionally omitted from this baseline error evaluation matrix. Because these variants leverage unconstrained remote infrastructure, decoupled high-fidelity OCR endpoints (`mistral-ocr-latest`), and advanced context models (`mistral-large-latest`), they achieved a perfect 100% data extraction accuracy rate (Score: 5.00) across all fields and document test shapes. Because they exhibited zero variations, discrepancies, or layout-driven failure modes, their inclusion in an error analysis table would provide no statistical divergence. They are instead benchmarked in the multi-criteria infrastructure analysis (MCDA) metrics.

---

## Appendix Table 3: Custom-Trained Layout Optimization Behavior Matrix
*This framework provides a detailed description of the dynamic fine-tuning behavior for custom models without forcing rigid, static numbers on layouts that vary by training set data.*

| Document Field Variable | Pre-Trained Baseline Behavior (All Platforms) | Custom Model Optimization Behavioral Profile |
| :--- | :--- | :--- |
| **Invoice Number & Date** | High risk of text collision when secondary tracking indicators or credit note strings appear near headers. | Custom-trained coordinate mapping completely neutralizes data noise by anchoring data extraction to specific, static document coordinates. |
| **VAT Identification Number** | Dropped or missed entirely depending on the regional layout structure of the international vendor. | Training parameters enforce explicit regex pattern tracking (e.g., DE, FR prefixes) independent of layout placement. |
| **Currency Context** | Generally stable on standard signs (€, $, £), but susceptible to ambiguous data formatting errors. | Grouping parameters anchor the currency format block explicitly to adjacent net/gross line item structures. |
| **Service Periods & Subtotals** | Frequently locked out or completely unsupported due to standard out-of-the-box product schema restrictions. | Custom template building allows developers to explicitly highlight line item tables, training the extractor to follow multi-page bounding grids. |

---

## Appendix Table 4: Analytical Calibration Values for Multi-Criteria Decisions (MCDA)
*Explains the objective boundaries and scoring scales used to derive the data clusters in Table 4 of the primary manuscript.*

### 1. Processing Speed Latency Clusters
* **Score 5 (Near Real-Time System Yield):** 0 to 5 seconds. Reached by unconstrained Cloud API runs.
* **Score 4 (Fast Operational System Yield):** >5 to 20 seconds. Low latency performance across cloud integration tiers.
* **Score 3 (Acceptable Office Ingestion Yield):** >20 to 60 seconds. Standard asynchronous low-code platform queuing bounds.
* **Score 2 (Obstructed Operational System Yield):** >60 to 180 seconds. Inefficiencies block active, human-in-the-loop processing paths.
* **Score 1 (Severe System Processing Bottleneck):** >180 seconds. Heavy hardware constraints or extensive local computing wait states (e.g., localized 540s inferencing latency bounds).

### 2. Computing Resource Availability Metrics
* **Score 5 (Highly Favorable Infrastructure):** Unlimited open-source scalability or zero computational licensing boundaries.
* **Score 3 (Balanced System Overhead):** Moderate data limits, subscription tiers, or low-maintenance administrative parameters.
* **Score 1 (Restricted Execution / Compute):** Highly limited trial loops, runtime quotas, or massive local hardware dependencies.

### 3. Monitoring & System Observability Categories
* **Score 5 (Native System Monitoring):** Automated background instrumentation logging, admin dashboards, and active telemetry alerting.
* **Score 1 (Manual System Monitoring):** System logging, try-catch telemetry loops, and auditing layers must be programmatically coded and maintained from scratch.
