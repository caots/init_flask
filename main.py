import json
import os
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, render_template, request, flash, send_from_directory, send_file

app = Flask(__name__)
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOADS_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

USER_LOGIN_JSON = '{"email": "user@gmail.com", "password": "123456"}'
ADMIN_LOGIN_JSON = '{"email": "admin@gmail.com", "password": "123456"}'
ROLE_JSON = '{"admin": "Admin", "user": "User"}'

USER_LOGIN = json.loads(USER_LOGIN_JSON)
ADMIN_LOGIN = json.loads(ADMIN_LOGIN_JSON)
ROLE_JSON = json.loads(ROLE_JSON)

@app.route('/')
def go_website():
  return redirect(url_for('login_page'))

# Login Func
@app.route('/login', methods=["POST", "GET"])
def login_page():
  try:
    if request.method == "POST":
      email = request.form["email"]
      password = request.form["password"]
      
      if email == USER_LOGIN["email"] and password ==  USER_LOGIN["password"]:
          return redirect(url_for('user_page'))
      if email == ADMIN_LOGIN["email"] and password ==  ADMIN_LOGIN["password"]:
          return redirect(url_for('admin_page'))
      flash('Wrong Email or Password, Please try again.')
      
    return render_template('login.html')
  except Exception as e:
    print('Exception Login: ', e)
        
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
  try:
    if request.method == 'POST':
      is_admin = request.args.get('is_admin')
      if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

      file = request.files['file']
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
      # pass upload file
      is_admin = is_admin == ROLE_JSON["admin"]
      if file and allowed_file(file.filename, is_admin):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'Upload file success: {file.filename}')  
        return redirect(url_for('admin_page'))
    
      flash('File is not allow')
    return redirect(url_for('admin_page'))
  except Exception as e:
        print('Exception Login: ', e)
        
@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def downloadFile(filename):
  try:
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    path = uploads + '/' + filename
    return send_file(path, as_attachment=True)
  except Exception as e:
        print('Exception Login: ', e)

def get_all_files_in_uploads_folder():
  files = []
  for file in os.listdir(UPLOADS_FOLDER):
    if os.path.isfile(os.path.join(UPLOADS_FOLDER, file)):
        files.append(file)
  return files 

def allowed_file(filename, is_admin = 0):
    if(is_admin == 0): 
      ALLOWED_EXTENSIONS = {'sam'}
    else:
      ALLOWED_EXTENSIONS = {'sam', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin Func
@app.route('/admin')
def admin_page():
  # get all file in folder uploads
  files = get_all_files_in_uploads_folder()
  return render_template('home.html', files = files, role = ROLE_JSON["admin"])

# User Func
@app.route('/user')
def user_page():
  # get all file in folder uploads
  files = get_all_files_in_uploads_folder()
  return render_template('home.html', files = files, role = ROLE_JSON["user"])

if __name__ == '__main__':
  app.run(debug=True)