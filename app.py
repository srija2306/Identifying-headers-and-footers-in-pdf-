from io import BytesIO
from flask import Flask, Response, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pandas as pd  # for handling Excel files
from your_document_processing_module import extract_text_above_below_margins
file = None
app = Flask(__name__)
CORS(app, origins=["*"])

# Define the upload directory
UPLOAD_FOLDER = 'New folder'
UPLOAD_PATH = "C:\\Users\\srija\\OneDrive\\Documents\\MyProject\\uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

# Set allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'pdf'}
df = pd.DataFrame()
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-endpoint', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    global file
    file = request.files['file']

    if file.filename == '':
        return jsonify({'noFile': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = "docparser.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file.close()
        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'Invalid file type'})

@app.route('/process-endpoint', methods=['POST'])
def proceed_file():
    global df,file
    if file:
        bottom_margin = 780  
        top_margin = 50 
        df = extract_text_above_below_margins("C:\\Users\\srija\\OneDrive\\Documents\\MyProject\\uploads\\docparser.pdf", top_margin, bottom_margin)
        os.remove("C:\\Users\\srija\\OneDrive\\Documents\\MyProject\\uploads\\docparser.pdf")
        return jsonify({'message': 'Process completed successfully'})
    return jsonify({'error': 'No file'})


@app.route('/download_excel', methods=['GET'])
def download_excel():
    global df
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='H&F', index=False)
        workbook = writer.book
        worksheet = writer.sheets['H&F']
        # Set column widths
        worksheet.set_column('A:C', 50)  # Adjust width as needed

    excel_data.seek(0)
    response = Response(excel_data.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = "attachment; filename=Headers&Footers.xlsx"
    return response

if __name__ == '__main__':
    app.run(debug=True)
