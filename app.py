from flask import Flask
from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, request, session
from flask import send_file, send_from_directory, safe_join, abort
import time
from flaskthreads import AppContextThread
app = Flask(__name__)


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)
   app.run(host = '0.0.0.0',port=5000,threaded=True)
