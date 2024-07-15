import os
import json
import pdfkit
from flask import Flask, request, send_file, render_template_string
from pybars import Compiler

app = Flask(__name__)

# Define the Handlebars template
template_source = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{company_name}} Report</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .section { margin-bottom: 40px; }
        .section h2 { border-bottom: 2px solid #000; padding-bottom: 5px; }
    </style>
</head>
<body>
    <h1>{{company_name}} Report</h1>
    <div class="section">
        <h2>Basic Information</h2>
        <p><strong>Website URL:</strong> <a href="{{basic_info.website_url}}">{{basic_info.website_url}}</a></p>
        <p><strong>LinkedIn URL:</strong> <a href="{{basic_info.linkedin_url}}">{{basic_info.linkedin_url}}</a></p>
        <p><strong>Logo:</strong> <img src="{{basic_info.logo}}" alt="Company Logo"></p>
    </div>
    <div class="section">
        <h2>Company Overview</h2>
        <p><strong>Description:</strong> {{overview.description}}</p>
        <p><strong>Mission Statement:</strong> {{overview.mission_statement}}</p>
        <p><strong>Founding Date:</strong> {{overview.founding_date}}</p>
        <p><strong>Founders:</strong> {{#each overview.founders}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</p>
        <p><strong>Headquarters:</strong> {{overview.headquarters}}</p>
        <p><strong>Industry:</strong> {{#each overview.industry}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</p>
    </div>
    <div class="section">
        <h2>Products and Services</h2>
        <h3>Products</h3>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Features</th>
                </tr>
            </thead>
            <tbody>
                {{#each products}}
                <tr>
                    <td>{{product_name}}</td>
                    <td>{{description}}</td>
                    <td>{{category}}</td>
                    <td>{{#each features}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</td>
                </tr>
                {{/each}}
            </tbody>
        </table>
        <h3>Services</h3>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Features</th>
                </tr>
            </thead>
            <tbody>
                {{#each services}}
                <tr>
                    <td>{{service_name}}</td>
                    <td>{{description}}</td>
                    <td>{{category}}</td>
                    <td>{{#each features}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</td>
                </tr>
                {{/each}}
            </tbody>
        </table>
    </div>
    <div class="section">
        <h2>Technologies</h2>
        {{#each technologies}}
        <p><strong>{{technology_name}}:</strong> {{application}}</p>
        <p><strong>Partnerships:</strong> {{#each partnerships}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</p>
        {{/each}}
    </div>
    <div class="section">
        <h2>Leadership and Team</h2>
        <p><strong>CEO:</strong> {{leadership.ceo}}</p>
        <p><strong>Leadership Team:</strong> {{#each leadership.leadership_team}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</p>
        <p><strong>Employee Count:</strong> {{leadership.employee_count}}</p>
        <p><strong>Company Culture:</strong> {{leadership.company_culture}}</p>
    </div>
    <div class="section">
        <h2>Social Media Presence</h2>
        <p><strong>LinkedIn:</strong> <a href="{{social_media.linkedin}}">{{social_media.linkedin}}</a></p>
        <p><strong>Twitter:</strong> <a href="{{social_media.twitter}}">{{social_media.twitter}}</a></p>
        <p><strong>Facebook:</strong> <a href="{{social_media.facebook}}">{{social_media.facebook}}</a></p>
        <p><strong>Instagram:</strong> <a href="{{social_media.instagram}}">{{social_media.instagram}}</a></p>
    </div>
</body>
</html>
'''

# Compile the Handlebars template
compiler = Compiler()
template = compiler.compile(template_source)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get JSON data from request
    data = request.get_json()

    # Generate HTML content from template and data
    html_content = template(data)

    # Define the output PDF file
    pdf_file = 'company_report.pdf'

    # Convert HTML to PDF using pdfkit
    pdfkit.from_string(html_content, pdf_file)

    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    # Ensure wkhtmltopdf is in PATH
    os.environ['PATH'] += os.pathsep + '/usr/local/bin'

    app.run(debug=True)