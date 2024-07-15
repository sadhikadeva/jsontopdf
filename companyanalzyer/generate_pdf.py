import json
import pdfkit
from pybars import Compiler

def create_html(data):
    # Read Handlebars template from file
    with open('company_template.hbs', 'r') as f:
        template_source = f.read()

    # Compile the Handlebars template
    compiler = Compiler()
    template = compiler.compile(template_source)

    # Generate HTML from template and data
    html = template(data)
    return html

def main():
    # Read JSON data from file
    with open('company_data.json', 'r') as f:
        data = json.load(f)

    # Create HTML content
    html_content = create_html(data)

    # Define the output PDF file
    pdf_file = 'company_report.pdf'

    # Convert HTML to PDF using pdfkit
    pdfkit.from_string(html_content, pdf_file)

    print(f"PDF generated: {pdf_file}")

if __name__ == "__main__":
    main()
