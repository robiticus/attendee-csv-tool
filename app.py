from flask import Flask, request, render_template, send_file
import csv
import io
import re

app = Flask(__name__)

# Improved function to extract emails and names from raw text
def extract_data(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    data = []
    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'

    i = 0
    while i < len(lines):
        line = lines[i]
        email_match = re.search(email_pattern, line)

        if email_match:
            email = email_match.group(1)

            # Check if the previous line contains a name
            if i > 0:
                name_parts = lines[i - 1].split()
                if len(name_parts) == 2:  # First and Last Name
                    first_name, last_name = name_parts
                else:
                    first_name, last_name = name_parts[0], ""
            else:
                first_name, last_name = "", ""

            data.append([email, first_name, last_name])

        i += 1

    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw_text = request.form['raw_text']
        extracted_data = extract_data(raw_text)

        # Create CSV in memory
        output = io.StringIO()
        csv_writer = csv.writer(output)
        for row in extracted_data:
            csv_writer.writerow(row)
        output.seek(0)

        return send_file(io.BytesIO(output.getvalue().encode()), 
                         mimetype='text/csv',
                         as_attachment=True,
                         download_name='attendees.csv')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
