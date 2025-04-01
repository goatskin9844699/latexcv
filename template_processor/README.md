# LaTeX CV Template Processor

A tool to generate LaTeX CV documents from JSON data using Jinja2 templating. This processor allows you to maintain your CV data in a structured JSON format and generate LaTeX documents using customizable templates.

## Directory Structure

```
.
├── tests/          # Test files containing pytest test suites
│   └── test_json_to_latex.py  # Tests for the main functionality
├── json_to_latex.py  # Main script for JSON to LaTeX conversion
└── README.md
```

## Features

- Convert JSON data to LaTeX documents
- Jinja2 templating for flexible LaTeX generation

## Installation

1. Make sure you're in the template_processor directory
2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The template processor provides several functions to handle JSON to LaTeX conversion:

```python
from json_to_latex import load_json, load_template, generate_latex, save_latex

# Load your JSON data
data = load_json("cv.json")

# Load your LaTeX template
template = load_template("cv_template.tex")

# Generate LaTeX content
latex_content = generate_latex(data, template)

# Save to file
save_latex(latex_content, "output/cv.tex")
```

## Testing

Run the tests using pytest:

```bash
python -m pytest tests/
```

## Template Syntax

The template uses Jinja2 syntax for variable substitution and control structures:

```latex
Name: {{ name }}
Email: {{ email }}

Experience:
{% for exp in work_experience %}
\item {{ exp.role }} at {{ exp.company }}
    {{ exp.description }}
{% endfor %}
```

## Example Data Structure

Your JSON data should follow this structure:

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1 (555) 123-4567",
    "summary": "Experienced professional...",
    "work_experience": [
        {
            "role": "Senior Developer",
            "company": "Tech Corp",
            "location": "San Francisco",
            "from_date": "01/2020",
            "to_date": "Present",
            "description": [
                "Led development of key features",
                "Managed team of 5 developers"
            ]
        }
    ]
}
``` 