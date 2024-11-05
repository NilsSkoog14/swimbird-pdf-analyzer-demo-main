import pdfplumber
import pandas as pd
import camelot
import os

def extract_tables_from_pdf(pdf_path, output_dir="output_csv"):
    # Create directory for CSV output if it doesn’t exist
    os.makedirs(output_dir, exist_ok=True)
    
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


                df = df[~df.iloc[:, 1:].apply(lambda row: row.isna() | (row == ''), axis=1).all(axis=1)]
                df = df.dropna(thresh=2, axis=1).replace('', pd.NA).dropna(thresh=2, axis=1)
                

                # Check if the DataFrame has valid content before saving
                print((df.notna().sum(axis=1) == 1).sum() > (len(df) / 2))
                print(len(df))
                if not df.empty and (df.notna().sum(axis=1) == 1).sum() < (len(df) / 2):
                    print(df)
                    # Save each table as a separate CSV file
                    csv_filename = os.path.join(output_dir, f"table_{table_count}.csv")
                    df.to_csv(csv_filename, index=False)
                    print(f"Table {table_count} saved to {csv_filename}")
                    table_count += 1

    print("PDF processing complete. All tables saved as CSVs.")

# Run the program
pdf_path = "inputFile.pdf"
extract_tables_from_pdf(pdf_path)
