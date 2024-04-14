from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os.path import join
from datetime import datetime
from folders import DATABASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER
from folders import latest_image
from detect_local import *
from werkzeug.utils import secure_filename

# Create Flask object
app = Flask(__name__)

# Input Folder
app.config['INPUT_FOLDER'] = INPUT_FOLDER

# Store database in app.db
DATABASE_PATH = join(DATABASE_FOLDER, 'app.db')

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
db = SQLAlchemy(app)

# Response Model to store id, confidence level, issue, and response from GPT
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confidence = db.Column(db.Float)
    issue = db.Column(db.String(255))
    data = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'{self.issue} with {self.confidence}'

# Route to handle file upload
#TODO : return render_template('index.html', uploaded_file=filename) 
@app.route('/', methods=['POST', 'GET'])
def index():
    latest_image_url = None 
    if request.method == 'POST':
        #  might be redundant?
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        # FILE PROCESSING
        if file:
            filename = secure_filename(file.filename)
            file_path = join(INPUT_FOLDER, filename)  # Save to static folder
            file.save(file_path)
            output = model()
            latest_image_url = latest_image(OUTPUT_FOLDER)


    

    return render_template('index.html', latest_image_url=latest_image_url)
        
        


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
