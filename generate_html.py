import pandas as pd
import json
import os
import glob
from datetime import datetime

def find_selector_csv_files():
    """Find all CSV files matching the selector pattern."""
    pattern = "CSV/*_last_copies_*.csv"
    csv_files = glob.glob(pattern)
    return csv_files

def parse_csv_to_json(csv_file):
    """Parse CSV file and convert to JSON format."""
    try:
        # Read Barcode as string to preserve leading zeros
        df = pd.read_csv(csv_file, dtype={'Barcode': str})

        # Convert DataFrame to list of dictionaries
        books = []
        for _, row in df.iterrows():
            book = {
                'barcode': str(row.get('Barcode', '')),
                'title': str(row.get('Title', '')),
                'author': str(row.get('Author', '')),
                'callNumber': str(row.get('Call Number', '')),
                'poReleaseDate': str(row.get('PO Release Date', '')),
                'ytdCirculation': str(row.get('YTD Circulation', '0')),
                'prevYtdCirculation': str(row.get('Prev YTD Circulation', '0')),
                'selector': str(row.get('Selector', ''))
            }
            books.append(book)

        return books
    except Exception as e:
        print(f"Error parsing {csv_file}: {e}")
        return []

def extract_selector_name(filename):
    """Extract selector name from filename.

    Expected format: {Selector}_last_copies_{timestamp}.csv
    Example: Zak_last_copies_20260117.csv -> Zak
    """
    base_name = os.path.basename(filename)
    parts = base_name.split('_last_copies_')
    if len(parts) >= 1:
        return parts[0]
    return "Unknown"

def generate_html(csv_file, template_path='creator.html'):
    """Generate HTML file with embedded data from CSV."""

    # Extract selector name
    selector_name = extract_selector_name(csv_file)

    # Parse CSV data
    books_data = parse_csv_to_json(csv_file)

    if not books_data:
        print(f"No valid data found in {csv_file}, skipping...")
        return None

    # Read HTML template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
        return None

    # Generate session date
    session_date = datetime.now().strftime('%B %d, %Y')

    # Convert books to JSON
    books_json = json.dumps(books_data, indent=2)

    # Replace all placeholders in template
    html_with_data = html_template
    html_with_data = html_with_data.replace('{{OWNER_NAME}}', selector_name)
    html_with_data = html_with_data.replace('{{SESSION_DATE}}', session_date)
    html_with_data = html_with_data.replace('{{TOTAL_BOOKS}}', str(len(books_data)))
    html_with_data = html_with_data.replace('{{BOOKS_JSON}}', books_json)

    # Generate output filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"HTML/{selector_name}_repurchase_tool_{timestamp}.html"

    # Write output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_with_data)
        print(f"[OK] Generated: {output_filename} ({len(books_data)} books)")
        return output_filename
    except Exception as e:
        print(f"Error writing output file: {e}")
        return None

def main():
    """Main function to process all selector CSV files."""
    print("=" * 60)
    print("Book Repurchase Decision Tool - HTML Generator")
    print("=" * 60)
    print()

    # Check if template exists
    if not os.path.exists('creator.html'):
        print("ERROR: creator.html template not found!")
        print("Please make sure creator.html is in the same directory.")
        return

    # Find CSV files
    csv_files = find_selector_csv_files()

    if not csv_files:
        print("No CSV files found matching pattern: *_last_copies_*.csv")
        print("Please make sure your CSV files are in the current directory.")
        return

    print(f"Found {len(csv_files)} CSV file(s):")
    for csv_file in csv_files:
        print(f"  - {csv_file}")
    print()

    # Generate HTML for each CSV
    generated_files = []
    for csv_file in csv_files:
        print(f"Processing {csv_file}...")
        output_file = generate_html(csv_file)
        if output_file:
            generated_files.append(output_file)
        print()

    # Summary
    print("=" * 60)
    print(f"Generation complete! Created {len(generated_files)} HTML file(s):")
    for output_file in generated_files:
        print(f"  [OK] {output_file}")
    print()
    print("Next steps:")
    print("1. Open the HTML files in a web browser")
    print("2. Distribute to the appropriate selectors")
    print("3. Selectors can swipe through books and export decisions")
    print("=" * 60)

if __name__ == "__main__":
    main()
