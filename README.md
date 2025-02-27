# Pharmacist-s-assistant
# Pharmacy Inventory Management with OCR

## Overview
This Flask-based application utilizes Azure's Computer Vision OCR API to scan and recognize medicine names from uploaded images. It then checks stock availability from a CSV dataset.

## Features
- **Upload Images**: Users can upload images of medicine labels.
- **OCR Processing**: Extracts text from images using Azure Computer Vision.
- **Medicine Name Extraction**: Matches extracted text against a CSV database.
- **Stock Checking**: Displays whether the medicine is in stock or out of stock.
- **User Notifications**: Provides feedback messages on medicine availability.

## Prerequisites
- Python 3.x
- Flask
- Pandas
- Azure Cognitive Services - computer vision (Subscription Key and Endpoint)
- regular expression

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project folder:
   ```sh
   cd pharmacy-ocr-app
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration
Update your Azure Cognitive Services credentials in `app.py`:
```python
subscription_key = "your_azure_subscription_key"
endpoint = "your_azure_endpoint"
```
Ensure that your `medicines.csv` file is available in the correct directory.

## Usage
1. Start the Flask application:
   ```sh
   python app.py
   ```
2. Open a web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
3. Upload an image to process and check medicine availability.

## Folder Structure
```
pharmacy-ocr-app/
│-- static/uploads/       # Stores uploaded images
│-- templates/index.html  # HTML template for UI
│-- app.py                # Flask application script
│-- medicines.csv         # Medicine stock data
│-- requirements.txt      # Python dependencies
```

## Notes
- Ensure your Azure API key is valid.
- Flask debug mode is enabled for development (`debug=True`). Disable it for production.
- The CSV file must include a `Medicine Name` column for name matching.

## License
This project is open-source under the MIT License.

