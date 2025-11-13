from flask import Flask, render_template, request, redirect
import csv, os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CSV_FILE = "registrations.csv"

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    name = request.form["name"]
    mobile = request.form["mobile"]
    address = request.form["address"]
    father = request.form["father_name"]
    mother = request.form["mother_name"]
    reference = request.form["reference_contact"]

    # Get uploaded files
    aadhaar = request.files["aadhaar"]
    pan = request.files["pan"]
    cheque = request.files["cheque"]

    # Save files
    aadhaar_path = os.path.join(UPLOAD_FOLDER, aadhaar.filename)
    pan_path = os.path.join(UPLOAD_FOLDER, pan.filename)
    cheque_path = os.path.join(UPLOAD_FOLDER, cheque.filename)

    aadhaar.save(aadhaar_path)
    pan.save(pan_path)
    cheque.save(cheque_path)

    # Save form data to CSV
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Mobile", "Address", "FatherName", "MotherName", "ReferenceContact",
                             "AadhaarFile", "PANFile", "ChequeFile", "Timestamp"])
        writer.writerow([name, mobile, address, father, mother, reference,
                         aadhaar.filename, pan.filename, cheque.filename,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    return redirect("/payment")

@app.route("/payment")
def payment():
    upi_id = "7022118670@ybl"
    return f"""
    <html>
    <head>
      <title>Complete Payment</title>
      <meta name='viewport' content='width=device-width, initial-scale=1'>
    </head>
    <body style='font-family: sans-serif; text-align: center; padding: 20px;'>
      <h2>Complete ₹99 Payment</h2>
      <p>Scan the QR below or use your UPI app to pay ₹99 to:</p>
      <p><b>{upi_id}</b></p>
      <img src='https://api.qrserver.com/v1/create-qr-code/?data=upi://pay?pa={upi_id}&pn=CustomerRegistration&am=99&cu=INR' width='220'>
      <p style='margin-top:15px;'>After payment, you may close this page.</p>
      <a href='/' style='display:inline-block;margin-top:20px;padding:10px 20px;background:#007bff;color:white;text-decoration:none;border-radius:6px;'>Back to Home</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    # Use host='0.0.0.0' for Render deployment
    app.run(host="0.0.0.0", port=5000, debug=True)
