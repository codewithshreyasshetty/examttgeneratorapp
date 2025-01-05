from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openpyxl import Workbook

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate-timetable', methods=['POST'])
def generate_timetable():
    try:
        files = request.files
        if not files:
            print("No files received!")
            return jsonify({'message': 'No files received'}), 400

        # Iterate through the uploaded files and save them
        for key in files:
            file = files[key]
            print(f"Received file: {file.filename}, type: {file.content_type}")
            
            # Check for allowed file extensions (you can modify this list)
            allowed_extensions = ['.csv', '.xlsx']
            filename = file.filename
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                print(f"Invalid file type: {filename}")
                return jsonify({'message': f"Invalid file type: {filename}"}), 400
            
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            print(f"File saved at {filepath}")

        # Simulate timetable generation logic (create a new Excel file)
        timetable_filename = 'timetable.xlsx'
        timetable_filepath = os.path.join(UPLOAD_FOLDER, timetable_filename)

        # Create a new workbook and add a sample sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Generated Timetable"
        
        # Add some sample data to the sheet (you can update this logic)
        ws.append(["Subject", "Start Time", "End Time", "Room"])
        ws.append(["Math", "09:00", "10:00", "Room 101"])
        ws.append(["Science", "10:00", "11:00", "Room 102"])
        ws.append(["English", "11:00", "12:00", "Room 103"])

        # Save the timetable to the uploads folder
        wb.save(timetable_filepath)
        print(f"Timetable saved at {timetable_filepath}")

        # Return the download URL of the generated timetable
        return jsonify({'message': 'Timetable generated successfully!', 'download_url': f'/uploads/{timetable_filename}'}), 200

    except Exception as e:
        print(f"Error in generate_timetable: {e}")
        return jsonify({'message': 'Failed to generate timetable.'}), 500

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return jsonify({'message': f'File {filename} will be served here.'})

if __name__ == '__main__':
    print("Flask server is starting...")
    app.run(debug=True)






