import os
import io
import time
import re
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
df = pd.read_csv(r"D:\MedicalDiagnosticAssistant\med\med\medicines.csv")
# 🔹 Flask Setup
app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔹 Azure OCR API credentials
subscription_key = "crjJybegYkZiDjNOh2XopRGS18S90s6angZMMO2VHTSt15APu5NoJQQJ99BBACHYHv6XJ3w3AAAFACOGAULG"

endpoint = "https://pharmacist.cognitiveservices.azure.com/"

# 🔹 Create Azure Computer Vision Client
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# 🔹 Load CSV dataset
csv_path = os.path.join(app.root_path, r"D:\MedicalDiagnosticAssistant\med\med\medicines.csv")
df = pd.read_csv(csv_path)

# 🔹 OCR Function using Azure
def process_image_with_ocr(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Convert bytes to a file-like object
    image_data_io = io.BytesIO(image_data)

    # Send image data to Azure OCR API
    response = client.read_in_stream(image_data_io, raw=True)

    # Extract operation ID from response headers
    operation_location = response.headers.get("Operation-Location")
    if operation_location:
        operation_id = operation_location.split("/")[-1]
    else:
        return None, "❌ Failed to retrieve operation ID from response."

    # Wait for processing to complete
    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Extract text from OCR response
    if result.status == 'succeeded':
        extracted_text = "\n".join(
            [line.text for read_result in result.analyze_result.read_results for line in read_result.lines]
        )
        return extracted_text, None
    else:
        return None, "❌ OCR processing failed."

# 🔹 Extract medicine name dynamically from OCR text
def extract_medicine_name(ocr_text, df):
    """ Extract medicine name from OCR text by matching with CSV data """
    for medicine_name in df["Medicine Name"].values:
        if medicine_name.lower() in ocr_text.lower():
            return medicine_name
    return None

# 🔹 Flask Route - Home (File Upload Interface)
# 🔹 Flask Route - Home (File Upload Interface)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Save the uploaded file to a folder
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)

            # Process the image with OCR
            ocr_text, ocr_error = process_image_with_ocr(image_path)
            if ocr_error:
                flash(ocr_error)
                return redirect(request.url)

            # Extract the medicine name from OCR text
            medicine_name = extract_medicine_name(ocr_text, df)  # Pass the dataframe
            if medicine_name:
                # Check if the medicine exists in the CSV
                if medicine_name in df["Medicine Name"].values:
                    stock_count = df.loc[df["Medicine Name"] == medicine_name, "Stock"].values[0]
                    if stock_count > 0:
                        flash(f"✅ {medicine_name} is in stock: {stock_count} available.")
                    else:
                        flash(f"⚠ {medicine_name} is out of stock. Reorder needed!")
                else:
                    flash(f"❌ {medicine_name} not found in the database.")
            else:
                flash("❌ No medicine name detected in the OCR output.")
            
            return redirect(url_for('index'))

    return render_template('index.html')


# Run the Flask app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
