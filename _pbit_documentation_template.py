import zipfile
import json
import os
from typing import Dict, List, Any

def extract_pbit_schema(pbit_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Extracts the schema from a .pbit file in Power BI, including advanced metadata.

    Args:
        pbit_path (str): Path to the .pbit file.

    Returns:
        Dict: Structure containing tables, columns, relationships, and metadata.

    Raises:
        FileNotFoundError: If the .pbit file or DataModelSchema is missing.
        ValueError: If the schema cannot be decoded.
    """
    temp_dir = "temp_pbit_extract"
    extracted_data = {"tables": {}, "relationships": []}

    try:
        # Extract the .pbit file
        with zipfile.ZipFile(pbit_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Try reading the schema with multiple encodings
        schema_path = os.path.join(temp_dir, 'DataModelSchema')
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"DataModelSchema file not found in {temp_dir}")

        schema = None
        encodings = ['utf-8-sig', 'utf-16-le', 'latin-1']  # Priority order

        for encoding in encodings:
            try:
                with open(schema_path, 'r', encoding=encoding) as f:
                    schema = json.load(f)
                break
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue

        if not schema:
            raise ValueError("Failed to decode DataModelSchema. Check encoding format.")

        # Process tables
        for table in schema.get("model", {}).get("tables", []):
            table_name = table.get("name", "N/A")
            extracted_data["tables"][table_name] = {
                "description": table.get("description", ""),
                "columns": [
                    {
                        "name": col.get("name", "N/A"),
                        "dataType": col.get("dataType", "unknown"),
                        "description": col.get("description", ""),
                        "is_hidden": col.get("isHidden", False),
                        "is_unique": col.get("isUnique", False)
                    } for col in table.get("columns", [])
                ],
                "measures": [
                    {
                        "name": measure.get("name", "N/A"),
                        "expression": measure.get("expression", "")
                    } for measure in table.get("measures", [])
                ]
            }

        # Process relationships
        for rel in schema.get("model", {}).get("relationships", []):
            extracted_data["relationships"].append({
                "from_table": rel.get("fromTable", "N/A"),
                "from_column": rel.get("fromColumn", "N/A"),
                "to_table": rel.get("toTable", "N/A"),
                "to_column": rel.get("toColumn", "N/A"),
                "cardinality": rel.get("cardinality", "N/A")
            })

    finally:
        # Ensure cleanup of the temporary directory
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(temp_dir)

    return extracted_data

def generate_markdown_documentation(schema: Dict) -> str:
    """
    Generates technical documentation in Markdown based on the extracted schema.

    Args:
        schema (Dict): Dictionary returned by extract_pbit_schema

    Returns:
        str: Markdown-formatted documentation
    """
    md = "# Power BI Model Documentation\n\n"

    # Tables
    md += "## Tables\n"
    for table_name, table_data in schema["tables"].items():
        md += f"### {table_name}\n"
        md += f"*Description*: {table_data['description']}\n\n"

        md += "#### Columns\n"
        md += "| Name | Type | Description | Hidden | Unique |\n"
        md += "|------|------|-------------|--------|--------|\n"
        for col in table_data["columns"]:
            md += f"| {col['name']} | {col['dataType']} | {col['description']} | {col['is_hidden']} | {col['is_unique']} |\n"

        md += "\n#### Measures\n"
        for measure in table_data["measures"]:
            md += f"- **{measure['name']}**: `{measure['expression']}`\n"

        md += "\n---\n"

    # Relationships
    md += "\n## Relationships\n"
    md += "| From Table | From Column | To Table | To Column | Cardinality |\n"
    md += "|------------|-------------|----------|-----------|-------------|\n"
    for rel in schema["relationships"]:
        md += f"| {rel['from_table']} | {rel['from_column']} | {rel['to_table']} | {rel['to_column']} | {rel['cardinality']} |\n"

    return md

# Execution
if __name__ == "__main__":
    try:
        pbit_path = "/content/your_archive_pbit.pbit"  # Update with your file path
        schema = extract_pbit_schema(pbit_path)

        # Generate documentation
        markdown_docs = generate_markdown_documentation(schema)
        with open("pbi_documentation.md", "w", encoding="utf-8") as f:
            f.write(markdown_docs)

        print("Documentation successfully generated: pbi_documentation.md")

    except Exception as e:
        print(f"Critical error: {str(e)}")