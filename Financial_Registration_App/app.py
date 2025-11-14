from flask import Flask, render_template, request
import csv
import os

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
    aadhaar_filename = os.path.join(UPLOAD_FOLDER, aadhaar_file.filename)
    aadhaar_file.save(aadhaar_filename)
    data['Aadhaar File'] = aadhaar_filename

    pan_file = request.files['pan']
    pan_filename = os.path.join(UPLOAD_FOLDER, pan_file.filename)
    pan_file.save(pan_filename)
    data['PAN File'] = pan_filename

    self_image_file = request.files['self_image']
    self_image_filename = os.path.join(UPLOAD_FOLDER, self_image_file.filename)
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

    return render_template('success.html')
    
if __name__ == '__main__':
    app.run(debug=True)

