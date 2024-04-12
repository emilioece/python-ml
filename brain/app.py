from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from folders import BASE_FOLDER


app = Flask(__name__)



db_path = os.path.join(BASE_FOLDER, 'database\\test.db')


if __name__ == '__main__':
    print(db_path)