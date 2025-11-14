from flask import Flask, render_template, request
import csv
import os
from werkzeug.utils import secure_filename
import git

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CSV file to store registrations
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

    # Append data to CSV
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['Name'], data['Mobile'], data['Address'], data['Father Name'],
            data['Mother Name'], data['Reference Name'], data['Reference Contact'],
            data['Amount Needed'], data['Return Date'], data['Purpose'],
            data['Aadhaar File'], data['PAN File'], data['Self Image File']
        ])

    # --- Push CSV to GitHub ---
    try:
        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Set in Render environment
        GITHUB_REPO = f"https://github.com/Vijay999n/Financial_Registration_App.git"  # Replace <username>/<repo>
        
        repo_dir = os.getcwd()
        repo = git.Repo(repo_dir)
        repo.git.add(CSV_FILE)
        repo.index.commit("Update registrations.csv")
        repo.git.push(GITHUB_REPO, repo.active_branch.name)
        print("CSV pushed to GitHub successfully.")
    except Exception as e:
        print("Git push failed:", e)
    # -----------------------------

    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


