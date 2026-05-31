from flask import Flask, request, jsonify, send_file, render_template_string
import os
import tempfile
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import re

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf', 'doc', 'rtf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def simple_align_documents(english_text, chinese_text):
    """
    A simple algorithm to align English and Chinese documents.
    This is a basic implementation - in a real application, you'd use
    more sophisticated NLP techniques for alignment.
    """
    # Split documents into paragraphs/sentences
    eng_paragraphs = [p.strip() for p in english_text.split('\n') if p.strip()]
    chn_paragraphs = [p.strip() for p in chinese_text.split('\n') if p.strip()]
    
    # Simple alignment - pair paragraphs sequentially
    # In a real app, you'd implement more sophisticated alignment logic
    aligned_pairs = []
    min_len = min(len(eng_paragraphs), len(chn_paragraphs))
    
    for i in range(min_len):
        aligned_pairs.append({
            'english': eng_paragraphs[i],
            'chinese': chn_paragraphs[i]
        })
    
    # Handle remaining paragraphs if one document is longer
    if len(eng_paragraphs) > len(chn_paragraphs):
        for i in range(min_len, len(eng_paragraphs)):
            aligned_pairs.append({
                'english': eng_paragraphs[i],
                'chinese': ''
            })
    elif len(chn_paragraphs) > len(eng_paragraphs):
        for i in range(min_len, len(chn_paragraphs)):
            aligned_pairs.append({
                'english': '',
                'chinese': chn_paragraphs[i]
            })
    
    return aligned_pairs

def create_aligned_file(aligned_data, output_format='txt'):
    """
    Create an aligned document in the specified format.
    """
    if output_format == 'txt':
        content = "ENGLISH\tCHINESE\n"
        content += "="*50 + "\n"
        
        for pair in aligned_data:
            eng_line = pair['english'].replace('\t', ' ').replace('\n', ' ')[:200]
            chn_line = pair['chinese'].replace('\t', ' ').replace('\n', ' ')[:200]
            content += f"{eng_line}\t{chn_line}\n"
    
    elif output_format == 'csv':
        content = "English Text,Chinese Text\n"
        for pair in aligned_data:
            eng_escaped = pair['english'].replace('"', '""')
            chn_escaped = pair['chinese'].replace('"', '""')
            content += f'"{eng_escaped}","{chn_escaped}"\n'
    
    else:  # Default to txt
        content = "ENGLISH\tCHINESE\n"
        content += "="*50 + "\n"
        for pair in aligned_data:
            content += f"{pair['english']}\n{pair['chinese']}\n\n"
    
    return content


@app.route('/')
def index():
    # Return the HTML content from the corpus_align.html file
    with open('corpus_align.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content


@app.route('/align_documents', methods=['POST'])
def align_documents():
    """
    Endpoint to handle document alignment.
    """
    try:
        # Check if the post request has the file parts
        if 'english_file' not in request.files or 'chinese_file' not in request.files:
            return jsonify({'error': 'Both English and Chinese files are required'}), 400
        
        english_file = request.files['english_file']
        chinese_file = request.files['chinese_file']
        
        if english_file.filename == '' or chinese_file.filename == '':
            return jsonify({'error': 'Both files must be selected'}), 400
        
        if not (allowed_file(english_file.filename) and allowed_file(chinese_file.filename)):
            return jsonify({'error': 'Invalid file types. Allowed: txt, docx, pdf, doc, rtf'}), 400
        
        # Save uploaded files temporarily
        english_filename = secure_filename(english_file.filename)
        chinese_filename = secure_filename(chinese_file.filename)
        
        english_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"eng_{uuid.uuid4()}_{english_filename}")
        chinese_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"chn_{uuid.uuid4()}_{chinese_filename}")
        
        english_file.save(english_filepath)
        chinese_file.save(chinese_filepath)
        
        # Read the content of the files
        def read_file_content(filepath):
            ext = filepath.rsplit('.', 1)[1].lower()
            if ext == 'txt':
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            elif ext in ['docx']:
                try:
                    from docx import Document
                    doc = Document(filepath)
                    full_text = []
                    for para in doc.paragraphs:
                        full_text.append(para.text)
                    return '\n'.join(full_text)
                except ImportError:
                    return "Document file detected but docx module not installed"
            elif ext in ['pdf']:
                try:
                    import PyPDF2
                    with open(filepath, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        return text
                except ImportError:
                    return "PDF file detected but PyPDF2 module not installed"
            elif ext in ['doc', 'rtf']:
                # For simplicity, treat as text files
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
        
        english_content = read_file_content(english_filepath)
        chinese_content = read_file_content(chinese_filepath)
        
        # Perform alignment
        aligned_data = simple_align_documents(english_content, chinese_content)
        
        # Generate aligned files in different formats
        output_files = []
        
        # Create TXT format
        txt_content = create_aligned_file(aligned_data, 'txt')
        txt_filename = f"aligned_{os.path.splitext(english_filename)[0]}_{os.path.splitext(chinese_filename)[0]}.txt"
        txt_filepath = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
        
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        output_files.append({
            'name': txt_filename,
            'size': os.path.getsize(txt_filepath),
            'download_url': f'/download/{txt_filename}',
            'format': 'txt'
        })
        
        # Create CSV format
        csv_content = create_aligned_file(aligned_data, 'csv')
        csv_filename = f"aligned_{os.path.splitext(english_filename)[0]}_{os.path.splitext(chinese_filename)[0]}.csv"
        csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        
        with open(csv_filepath, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        output_files.append({
            'name': csv_filename,
            'size': os.path.getsize(csv_filepath),
            'download_url': f'/download/{csv_filename}',
            'format': 'csv'
        })
        
        # Clean up temporary uploaded files
        os.remove(english_filepath)
        os.remove(chinese_filepath)
        
        return jsonify({
            'success': True,
            'message': 'Documents aligned successfully',
            'files': output_files
        })
        
    except Exception as e:
        print(f"Error in align_documents: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """
    Endpoint to download aligned files.
    """
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
