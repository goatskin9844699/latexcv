import json
import os
from jinja2 import Template

def load_json(file_path):
    """Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        dict: Loaded JSON data
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def load_template(file_path):
    """Load a template file.
    
    Args:
        file_path: Path to the template file
        
    Returns:
        str: Template content
    """
    with open(file_path, 'r') as f:
        return f.read()

def generate_latex(json_data, template):
    """Generate LaTeX content from JSON data and template.
    
    Args:
        json_data: Dictionary containing the data
        template: Template string
        
    Returns:
        str: Generated LaTeX content
    """
    jinja_template = Template(template)
    return jinja_template.render(**json_data)

def save_latex(content, output_file):
    """Save LaTeX content to a file.
    
    Args:
        content: LaTeX content to save
        output_file: Path to save the content to
    """
    with open(output_file, 'w') as f:
        f.write(content) 