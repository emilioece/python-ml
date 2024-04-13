from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from folders import BASE_FOLDER, DATABASE_FOLDER


app = Flask(__name__)


# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_FOLDER
db = SQLAlchemy(app)

# SQL Model to store id, confidence level, issue, and response from GPT
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confidence = db.Column(db.Float)
    issue = db.Column(db.String(255))
    data = db.Column(db.String(255))

    def __repr__(self):
        return f'{self.issue} with {self.confidence}'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)