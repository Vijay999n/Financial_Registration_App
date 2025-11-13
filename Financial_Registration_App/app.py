from flask import Flask, render_template, request
import os
import csv

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    mobile = request.form["mobile"]
    address = request.form["address"]
    father_name = request.form["father_name"]
    mother_name = request.form["mother_name"]
    ref_name = request.form["ref_name"]
    ref_contact = request.form["ref_contact"]

    aadhaar = request.files["aadhaar"]
    pan = request.files["pan"]

    aadhaar_path = os.path.join(UPLOAD_FOLDER, f"{name}_aadhaar.jpg")
    pan_path = os.path.join(UPLOAD_FOLDER, f"{name}_pan.jpg")

    aadhaar.save(aadhaar_path)
    pan.save(pan_path)

    csv_file = "registrations.csv"
    headers = ["Name", "Mobile", "Address", "Father Name", "Mother Name", "Ref Name", "Ref Contact"]

    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow([name, mobile, address, father_name, mother_name, ref_name, ref_contact])

    return "✅ Registration submitted successfully! Thank you."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
