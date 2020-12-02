#Based upon https://github.com/jumbry/Flask-fileserver
# Flask-fileserver - see VERSION_ID below
# for gunicorn / Flask
# uses html templates in /templates
# requires read/write privileges to UPLOAD_FOLDER defined in app.config

import datetime
import os
from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

from DataBaseProcessor import *

VERSION_ID = "version 4.9"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEBUGGING = False #change this to True to allow access to debuging tools

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/var/www/uploads'

def _check_extension(filename):
  file, ext = os.path.splitext(filename)
  if (ext.replace('.', '') not in ALLOWED_EXTENSIONS):
    raise BadRequest('{0} has an invalid name or extension'.format(filename))

def _safe_filename(filename):
# ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS-UUUUUU.ext``
  filename = secure_filename(filename)
  date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S-%f")
  basename, extension = filename.rsplit('.', 1)
  return "{0}-{1}.{2}".format(basename, date, extension)

#debugging purposes only
@app.route('/')
def index():
    return 'Flask-fileserver %s' % VERSION_ID

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('list.html', files=files)

#app body
@app.route('/register', methods=['GET','POST'])
def register_public_key (KHash=None):
   if request.method == 'POST':
      KHash = request.form['password']
      PublicKeyID = RegisterPublicKey(KHash)
      if True: #Finagle's line
         return str(PublicKeyID)
   return render_template('register.html')

@app.route('/upload/<filename>', methods=['GET', 'POST'])
def upload_file(filename=None):
    if request.method == 'POST':
      file = request.files['image']
      address = request.form['address']
      _check_extension(filename)
      filename = _safe_filename(filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      IndexMessage(filename,address)
    return render_template('upload.html')

@app.route('/DownloadList')
def create_list():
   KHash = request.authorization.password
   PublicKeyID = request.authorization.username
   authorized = CorrectCredentials(PublicKeyID,KHash,"None")
   if authorized:
      filenames = GetMessages(PublicKeyID)
      return filenames
   else:
      return "failed"

@app.route('/OpenImage', methods=['POST'])
def open_file():
   KHash = request.authorization.password
   PublicKeyID = request.authorization.username
   filename = request.form['filename']
   authorized,trace = CorrectCredentials(PublicKeyID,KHash,filename)
   if not authorized:
      return "failed to access "+filename+" with PublicKeyID "+PublicKeyID+" and KHash "+KHash +" authorized= "+str(trace)
   if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
   raise BadRequest('{0} does not exist'.format(filename))

@app.route('/download/<filename>')
def download_file(filename):
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
      return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    raise BadRequest('{0} does not exist'.format(filename))

@app.route('/delete', methods=['POST'])
def delete_file(): #needs to add interact with database
   KHash = request.authorization.password
   PublicKeyID = request.authorization.username
   filename = request.form['filename']
   authorized = CorrectCredentials(PublicKeyID,KHash,filename)
   if not authorized:
      return "failed"
   if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
     os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
     return "suceeded"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
