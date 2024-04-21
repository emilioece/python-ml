from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os.path import join
from datetime import datetime
from folders import DATABASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER, INPUT_RELATIVE
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    confidence = db.Column(db.String(255), nullable = True)
    issue = db.Column(db.String(255), nullable = True)
    latest_image_url = db.Column(db.String(255), nullable = True)
    original_image_url = db.Column(db.String(255), nullable = True)

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
            # Save to static/images folder
            file_path = join(app.config['INPUT_FOLDER'], filename)  
            print(f'file path of uploaded photo: {file_path}')
            file.save(file_path)

            # relative path for input image 
            original_url = latest_image(INPUT_FOLDER)

            # create Response object
            response = Response(original_image_url = original_url)

            # input Response object id into model function to save in that folder.
            model_output = model(id = response.id)
            # latest image_url
            latest_image_url = model_output['processed_image_url']

            # store confidence, issue, and latest_image url in Response object
            response.confidence = model_output['confidence']
            response.issue = model_output['issue']
            response.latest_image_url = latest_image_url
            # commit to database
            try:
                db.session.add(response)
                db.session.commit()
                return redirect('/')

            except Exception as e:
                print(f"error uploading data: {str(e)}")
                return 'issue uploading data.'

    
    responses = Response.query.order_by(Response.date_created).all()
    return render_template('index.html', responses = responses)

@app.route('/view/<int:id>', methods=['POST', 'GET']) 
def view(id):
    response = Response.query.get_or_404(id)
    print(response.latest_image_url)
    if request.method == 'POST':
        return render_template('view.html', response=response)
    else:
        return render_template('view.html', response=response)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
