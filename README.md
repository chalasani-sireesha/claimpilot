# ClaimPilot – Autonomous Insurance Claims Processing Agent

ClaimPilot is a lightweight insurance claims processing application that automatically reads FNOL (First Notice of Loss) documents, extracts important claim information, validates the data, classifies the claim, and routes it to the appropriate workflow.

The application uses a combination of **rule-based extraction, Groq AI fallback extraction, validation rules, and a routing engine** to provide an explainable claim-processing result.

---

## Features

* Upload FNOL documents in PDF or TXT format
* Extract important claim fields automatically
* Use Groq AI as a fallback when important fields are not extracted
* Detect missing mandatory fields
* Detect data inconsistencies
* Classify claims such as Vehicle, Injury, Property, Theft, and Fire
* Automatically route claims based on defined business rules
* Generate a short explanation for every routing decision
* Store processed claims in a database
* Display claim history in the dashboard
* Display claim processing statistics
* Django Admin support
* Automated tests for routing logic
* Browser-based dashboard for demonstration

---

## Processing Workflow

```text
FNOL PDF/TXT
     ↓
Document Upload
     ↓
Text Extraction
     ↓
Rule-Based Field Extraction
     ↓
AI Fallback Extraction
     ↓
Validation
     ↓
Claim Classification
     ↓
Routing Engine
     ↓
Reasoning / Explanation
     ↓
Database Storage
     ↓
Dashboard Result
```

---

## Fields Extracted

### Policy

* Policy Number
* Policyholder Name
* Effective Start Date
* Effective End Date

### Incident

* Incident Date
* Incident Time
* Location
* Description

### Parties

* Claimant
* Third Parties
* Contact Details

### Asset

* Asset Type
* Asset ID
* Estimated Damage

### Other

* Claim Type
* Attachments
* Initial Estimate

---

## Routing Rules

ClaimPilot applies the following business rules:

| Condition                                                 | Recommended Route  |
| --------------------------------------------------------- | ------------------ |
| Description contains `fraud`, `inconsistent`, or `staged` | Investigation Flag |
| Mandatory field is missing                                | Manual Review      |
| Claim type is Injury                                      | Specialist Queue   |
| Estimated damage is below ₹25,000                         | Fast-track         |
| Other cases                                               | Manual Review      |

### Routing Priority

When multiple conditions are present, the application evaluates them in this order:

```text
Investigation Flag
       ↓
Manual Review for Missing Fields
       ↓
Specialist Queue for Injury
       ↓
Fast-track for Damage < ₹25,000
       ↓
Manual Review
```

This priority prevents potentially suspicious claims from being automatically fast-tracked.

---

## AI Integration

ClaimPilot uses **Groq** for AI-assisted extraction.

The application first attempts normal field extraction using pattern-based processing.

If multiple important fields cannot be extracted, the system calls the Groq model as a fallback.

The AI is instructed to:

* Return structured JSON
* Avoid inventing information
* Return `null` for missing values
* Return dates in `YYYY-MM-DD` format
* Return monetary amounts as numbers

This hybrid approach combines predictable rule-based processing with AI-assisted extraction for less structured documents.

---

## Validation

The validation engine checks for:

### Missing Fields

Mandatory fields are checked after extraction.

Example:

```text
Missing Fields:
- Effective End Date
- Contact Details
```

### Inconsistencies

The application checks:

* Whether the incident date falls within the policy effective period
* Whether estimated damage and initial estimate are different

Example:

```text
Estimated damage and initial estimate differ by ₹500.00.
```

---

## Claim Classification

Claims are classified based on the claim type.

Supported classifications include:

```text
Vehicle
Injury
Property
Theft
Fire
Other
```

---

## Explainable Routing

For every processed claim, ClaimPilot returns a short explanation.

Example:

```text
Recommended Route: Fast-track

Reasoning:
All mandatory fields are available and estimated damage
is below ₹25,000.
```

For an investigation case:

```text
Recommended Route: Investigation Flag

Reasoning:
Investigation keywords were detected in the claim description.
```

---

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework

### AI

* Groq API
* `openai/gpt-oss-20b`

### Document Processing

* PyMuPDF

### Database

* SQLite

### Frontend

* HTML
* CSS
* JavaScript

### Development Tools

* VS Code
* Git
* GitHub

---

## Project Structure

```text
claimpilot/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── claimpilot/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── claims/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── extractor.py
│   ├── ai_extractor.py
│   ├── validator.py
│   ├── classifier.py
│   ├── routing.py
│   └── tests.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── sample_documents/
│
└── test_ai.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/chalasani-sireesha/claimpilot.git
```

Move into the project:

```bash
cd claimpilot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

The `.env` file is excluded from Git using `.gitignore`.

Never commit the actual API key to GitHub.

---

## Database Setup

Run:

```bash
python manage.py migrate
```

---

## Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open the application in the browser:

```text
http://127.0.0.1:8000/
```

---

## API Endpoints

### Process Claim

```text
POST /api/process-claim/
```

Accepts a PDF or TXT FNOL document.

### Claim History

```text
GET /api/claims/
```

Returns previously processed claims.

### Statistics

```text
GET /api/statistics/
```

Returns claim processing statistics.

---

## Example Result

```json
{
    "claimId": 1,
    "extractedFields": {
        "policyNumber": "POL-2026-00125",
        "policyholderName": "Ravi Kumar",
        "estimatedDamage": 18500,
        "claimType": "Vehicle"
    },
    "missingFields": [],
    "inconsistencies": [
        "Estimated damage and initial estimate differ by ₹500.00."
    ],
    "claimClassification": "Vehicle",
    "recommendedRoute": "Fast-track",
    "investigationFlag": false,
    "matchedKeywords": [],
    "reasoning": "All mandatory fields are available and estimated damage is below ₹25,000."
}
```

---

## Testing

Run the automated tests:

```bash
python manage.py test claims
```

The test suite covers:

* Fast-track claims
* Missing-field claims
* Injury claims
* Investigation claims
* High-damage claims

---

## Sample Documents

The `sample_documents` folder contains example FNOL documents that can be used to demonstrate different routing scenarios.

Examples include:

```text
sample_fnol.txt
missing_field.txt
injury_claim.txt
fraud_claim.txt
high_damage.txt
```

---

## Security

Sensitive configuration such as the Groq API key is stored in `.env` and excluded from version control.

The project does not store the API key in source code.

---

## Future Improvements

Possible future improvements include:

* Support for more document formats
* OCR for scanned FNOL documents
* More advanced document validation
* User authentication and role-based access
* Claim workflow status tracking
* Production database such as PostgreSQL
* Docker deployment
* More advanced AI-based inconsistency detection

---

## Author

**Chalasani Sireesha**

Python Full Stack Developer | Django | REST APIs | AI Applications
