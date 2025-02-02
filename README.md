# auto-doc-pbi

This script automates the extraction of structured information from a Power BI report template (.pbit) file. It processes the model schema, identifies tables, columns, and relationships between data, and generates technical documentation in Markdown format for future reference.

The main goal is to make it easier to analyze the Power BI data model, allowing technical and business teams to understand the structure of reports without having to manually open Power BI.

## Key Features
- The script unpacks the .pbit file to access its internal schema
- Reads and interprets the structure of tables, columns, and relationships
- Identifies data types, measures (DAX formulas), and metadata
- Automatic Documentation Generation model

- Converts the extracted data into a well-structured document.
- Lists all tables, columns, and relationships in the model.
- Organizes the information in a user-friendly format suitable for review and auditing.
- Error Handling and compatibility
- Supports multiple encoding formats to avoid reading errors, ensuring the removal of temporary files to avoid wasted space. Includes clear error messages to facilitate problem diagnosis.

## How it works?

1. The user provides the path to the Power BI .pbit file.
2. The script extracts the information from the model and converts it to a readable format.
3. A documentation file (pbi_documentation.md) is automatically generated, containing all the details of the model.
4. The documentation can be shared with technical and business teams without having to open Power BI.

## User Case

Imagine that a data analyst needs to review the structure of a Power BI model to ensure that all tables and calculations are correct. 
Instead of opening Power BI and examining each detail manually, he or she can run this script and receive a well-organized document with all the necessary information.

This facilitates audits, internal documentation, and collaboration between technical and non-technical teams.

## Main Benefits
✅ Automates the extraction of metadata from Power BI.

✅ Improves transparency and data governance.

✅ Facilitates audits and reviews without having to open Power BI.

✅ Generates accessible documentation for technical and business teams.

✅ Avoids manual errors in identifying tables and relationships.

## Author

Vinícius Borges.
