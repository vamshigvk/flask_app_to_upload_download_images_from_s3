import os, time, json
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import boto3

s3 = boto3.client('s3',
                    aws_access_key_id=':)' ,
                    aws_secret_access_key= ':P' #,aws_session_token=
                     )

BUCKET_NAME='data.science.python.projects'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tiff'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        s3.upload_file(Bucket = BUCKET_NAME, Filename='static/uploads/'+filename, Key = 'textract/'+filename)
        #s3.upload_file(Bucket = BUCKET_NAME, Filename='static/uploads/'+filename, Key = 'textract_expenses/'+filename)
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        time.sleep(7)
        filename_json = filename.split('.')[0] +'.json'
        print('jsonfile name is',filename_json)
        try:
            s3.download_file(BUCKET_NAME, 'object_json/'+filename_json, 'static/downloads/'+filename_json)
        except:
            flash('Failed to load json file, try again')
            return redirect(request.url)
        filename_json = filename.split('.')[0] +'.json'
        with open('static/downloads/'+filename_json, 'r') as myfile:
            data = myfile.read()
        return render_template('upload.html', filename=filename, data=data)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
