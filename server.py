from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import tabula
import os
import pdfplumber
import camelot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze-pdf', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save the uploaded file temporarily
    temp_path = 'temp.pdf'
    file.save(temp_path)
    
    try:
        # Extract tables from PDF
        tables = extract_tables_from_pdf(temp_path)
        
        if tables is None or len(tables) == 0:
            return jsonify({'error': 'No tables found in PDF'}), 404
        
        # Convert DataFrame to list format
        result = {
            'tables': [{
                'columns': tables.columns.tolist(),
                'rows': tables.values.tolist()
            }]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i + 1}...")
            
            # Use Camelot to extract tables from the page
            tables = camelot.read_pdf(pdf_path, pages=str(i + 1), flavor="stream")
            
            for table in tables:
                df = table.df
                
                # Basic cleaning
                df = df.dropna(how='all')  # Drop rows where all values are NaN
                df = df.dropna(axis=1, how='all')  # Drop columns where all values are NaN
                
                # Remove rows that are mostly empty (more than 50% empty cells)
                empty_threshold = len(df.columns) * 0.5
                df = df[df.notna().sum(axis=1) > empty_threshold]
                
                # Only return if we have a valid table
                if not df.empty and len(df.columns) > 1 and len(df) > 1:
                    return df
    
    return None

if __name__ == '__main__':
    app.run(debug=True)