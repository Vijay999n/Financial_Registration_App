from flask import Flask, render_template, request
import csv
import os
from werkzeug.utils import secure_filename
from github import Github

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CSV file to store registrations locally
CSV_FILE = 'registrations.csv'

# Ensure CSV header exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name','Mobile','Address','Father Name','Mother Name',
            'Reference Name','Reference Contact','Amount Needed',
            'Return Date','Purpose','Aadhaar File','PAN File','Self Image File'
        ])

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'Name': request.form['name'],
        'Mobile': request.form['mobile'],
        'Address': request.form['address'],
        'Father Name': request.form['father_name'],
        'Mother Name': request.form['mother_name'],
        'Reference Name': request.form['ref_name'],
        'Reference Contact': request.form['ref_contact'],
        'Amount Needed': request.form['amount_needed'],
        'Return Date': request.form.get('return_date', ''),
        'Purpose': request.form['purpose'],
    }

    # Save uploaded files
    aadhaar_file = request.files['aadhaar']
    aadhaar_filename = os.path.join(UPLOAD_FOLDER, secure_filename(aadhaar_file.filename))
    aadhaar_file.save(aadhaar_filename)
    data['Aadhaar File'] = aadhaar_filename

    pan_file = request.files['pan']
    pan_filename = os.path.join(UPLOAD_FOLDER, secure_filename(pan_file.filename))
    pan_file.save(pan_filename)
    data['PAN File'] = pan_filename

    self_image_file = request.files['self_image']
    self_image_filename = os.path.join(UPLOAD_FOLDER, secure_filename(self_image_file.filename))
    self_image_file.save(self_image_filename)
    data['Self Image File'] = self_image_filename

    # Append data to local CSV
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['Name'], data['Mobile'], data['Address'], data['Father Name'],
            data['Mother Name'], data['Reference Name'], data['Reference Contact'],
            data['Amount Needed'], data['Return Date'], data['Purpose'],
            data['Aadhaar File'], data['PAN File'], data['Self Image File']
        ])

    # --- Push CSV to GitHub using PyGithub ---
    try:
        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Set in Render
        GITHUB_REPO = "https://github.com/Vijay999n/Financial_Registration_App.git"  # Replace with your GitHub repo, e.g., vijayshankar/financial-registration
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        CSV_PATH = "registrations.csv"

        # Read local CSV content
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            file = repo.get_contents(CSV_PATH)
            repo.update_file(file.path, "Update registrations.csv", content, file.sha)
        except:
            repo.create_file(CSV_PATH, "Create registrations.csv", content)

        print("CSV updated on GitHub successfully.")
    except Exception as e:
        print("Failed to update CSV on GitHub:", e)
    # ---------------------------------------------

    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

