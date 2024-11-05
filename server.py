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
        # More advanced table extraction
        tables = extract_tables_from_pdf(temp_path)
        
        if not tables:
            return jsonify({'error': 'No tables found in PDF'}), 404
        
        # Convert all tables to result format
        result = {
            'tables': [
                {
                    'columns': df.columns.tolist(),
                    'rows': df.values.tolist()
                } for df in tables
            ]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

def extract_tables_from_pdf(pdf_path):
    # Create directory for CSV output if it doesn't exist
    #os.makedirs(output_dir, exist_ok=True)
    
    # Open PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Track the number of tables for unique naming
        table_count = 1
        
        # Process each page
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i + 1}...")

            # Use Camelot to extract tables from the page
            # Camelot works best when tables have clear borders (lattice mode)
            tables = camelot.read_pdf(pdf_path, pages=str(i + 1), flavor="stream")  # use "lattice" if tables have borders
            
            # Process each detected table
            for table in tables:
                df = table.df  # Convert the Camelot table to a DataFrame
                # Basic cleaning: Remove empty rows and columns
                df.dropna(how='all', inplace=True)
                df.dropna(axis=1, how='all', inplace=True)

                # Additional cleaning to remove rows and columns that are mostly empty
                df = df[~df.iloc[:, 1:].apply(lambda row: row.isna() | (row == ''), axis=1).all(axis=1)]
                df = df.dropna(thresh=2, axis=1).replace('', pd.NA).dropna(thresh=2, axis=1)
                
                # Check if the DataFrame has valid content before saving
                print((df.notna().sum(axis=1) == 1).sum() > (len(df) / 2))
                print(len(df))
                if not df.empty and (df.notna().sum(axis=1) == 1).sum() < (len(df) / 2):
                    print(df)
                    return df

if __name__ == '__main__':
    app.run(debug=True)