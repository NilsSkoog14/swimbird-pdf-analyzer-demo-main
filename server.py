from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import tabula
import os
import pdfplumber
import camelot
import numpy as np

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
        
        # Clean and prepare data for JSON serialization
        cleaned_tables = clean_dataframe_for_json(tables)
        
        return jsonify(cleaned_tables)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

def clean_dataframe_for_json(df):
    """Clean DataFrame to ensure JSON serialization."""
    if df is None:
        return {'tables': []}
    
    # Convert DataFrame to string type first
    df = df.astype(str)
    
    # Replace 'nan' and 'NA' strings with None
    df = df.replace({'nan': None, 'NA': None, 'NaN': None})
    
    # Convert DataFrame to the expected format
    result = {
        'tables': [{
            'columns': df.columns.tolist(),
            'rows': df.values.tolist()
        }]
    }
    
    return result

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
                df = df[~df.iloc[:, 1:].apply(lambda row: row.isna() | (row == ''), axis=1).all(axis=1)]
                df = df.dropna(thresh=2, axis=1).replace('', pd.NA).dropna(thresh=2, axis=1)
                

                # Check if the DataFrame has valid content before saving
                if not df.empty and (df.notna().sum(axis=1) == 1).sum() < (len(df) / 2):
                    return df
    
    return None

if __name__ == '__main__':
    app.run(debug=True)