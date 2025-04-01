import pytest
import json
import os
from pathlib import Path
from json_to_latex import load_json, load_template, generate_latex, save_latex, escape_latex

@pytest.fixture
def test_json_data():
    return {
        "name": "Test & User",  # Added special character
        "email": "test@example.com",
        "phone": "+1 (555) 123-4567",
        "summary": "Test summary with % and $ symbols",  # Added special characters
        "work_experience": [
            {
                "role": "Test Role & Manager",  # Added special character
                "company": "Test Company",
                "location": "Test Location",
                "from_date": "01/2020",
                "to_date": "12/2023",
                "description": ["Test achievement 1", "Test achievement 2"]
            }
        ]
    }

@pytest.fixture
def test_template():
    return """
    Name: \\VAR{name|escape_latex}
    Email: \\VAR{email|escape_latex}
    Phone: \\VAR{phone|escape_latex}
    Summary: \\VAR{summary|escape_latex}
    \\BLOCK{for exp in work_experience}
    Role: \\VAR{exp.role|escape_latex}
    Company: \\VAR{exp.company|escape_latex}
    \\BLOCK{endfor}
    """

def test_escape_latex():
    """Test LaTeX special character escaping."""
    test_cases = [
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\^{}"),
        ("\\", r"\textbackslash{}"),
        ("Test & User", r"Test \& User"),
        ("Cost: $50", r"Cost: \$50"),
    ]
    
    for input_str, expected in test_cases:
        assert escape_latex(input_str) == expected

def test_load_json(tmp_path):
    """Test loading JSON data."""
    json_data = {"test": "data"}
    json_file = tmp_path / "test.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f)
    
    loaded_data = load_json(json_file)
    assert loaded_data == json_data

def test_load_template(tmp_path):
    """Test loading template file."""
    template_content = "Test template"
    template_file = tmp_path / "test.tex"
    with open(template_file, 'w') as f:
        f.write(template_content)
    
    loaded_template = load_template(template_file)
    assert loaded_template == template_content

def test_generate_latex(test_json_data, test_template):
    """Test template rendering with LaTeX escaping."""
    latex_content = generate_latex(test_json_data, test_template)
    
    # Check if key information is present and properly escaped
    assert r"Test \& User" in latex_content
    assert "test@example.com" in latex_content
    assert r"Test summary with \% and \$ symbols" in latex_content
    assert r"Test Role \& Manager" in latex_content

def test_save_latex(tmp_path):
    """Test saving LaTeX content."""
    latex_content = "Test LaTeX content"
    output_file = tmp_path / "output.tex"
    
    save_latex(latex_content, output_file)
    
    assert output_file.exists()
    with open(output_file, 'r') as f:
        saved_content = f.read()
    assert saved_content == latex_content

def test_save_latex_creates_directory(tmp_path):
    """Test that save_latex creates output directory if needed."""
    latex_content = "Test LaTeX content"
    output_dir = tmp_path / "subdir"
    output_file = output_dir / "output.tex"
    
    save_latex(latex_content, output_file)
    
    assert output_dir.exists()
    assert output_file.exists()

def test_full_pipeline(tmp_path):
    """Test the entire pipeline with LaTeX escaping."""
    json_data = {
        "name": "Test & User",
        "email": "test@example.com"
    }
    template = "Name: \\VAR{name|escape_latex}\nEmail: \\VAR{email|escape_latex}"
    
    # Create temporary files
    json_file = tmp_path / "test.json"
    template_file = tmp_path / "test.tex"
    output_file = tmp_path / "output.tex"
    
    # Save test files
    with open(json_file, 'w') as f:
        json.dump(json_data, f)
    with open(template_file, 'w') as f:
        f.write(template)
    
    # Run pipeline
    loaded_json = load_json(json_file)
    loaded_template = load_template(template_file)
    latex_content = generate_latex(loaded_json, loaded_template)
    save_latex(latex_content, output_file)
    
    # Verify output
    assert output_file.exists()
    with open(output_file, 'r') as f:
        final_content = f.read()
    assert r"Test \& User" in final_content
    assert "test@example.com" in final_content 