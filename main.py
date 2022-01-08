import os, time
from app import app
from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import boto3

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAWXYSJZ5ZEVBZSC46' ,
                    aws_secret_access_key= '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' #,aws_session_token=
                     )

#BUCKET_NAME='data.science.python.projects'
SOURCE_BUCKET_NAME='textract-analyzexpense-sourcebucket-1x7nf48xmbtqp'
DESTINATION_BUCKET_NAME = 'textract-analyzexpense-outputbucket-xfld43ubt72q'

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
        #s3.upload_file(Bucket = SOURCE_BUCKET_NAME, Filename='static/uploads/'+filename, Key = 'textract/'+filename)
        s3.upload_file(Bucket = SOURCE_BUCKET_NAME, Filename='static/uploads/'+filename, Key = filename)
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        time.sleep(8)
        filename_json = filename.split('.')[0] +'.json'

        try:
            
            #print('jsonfile name is',filename_json)
            response_filename = filename+'-analyzeexpenseresponse.txt'
            print('expense text filename is',response_filename)

            #s3.download_file(SOURCE_BUCKET_NAME, 'object_json/'+filename_json, 'static/downloads/'+filename_json)            
            s3.download_file(DESTINATION_BUCKET_NAME, response_filename, 'static/downloads/'+response_filename)
        except:
            flash('Failed to load extracted file, try again')
            return redirect(request.url)
        filename_json = filename.split('.')[0] +'.json'
        #with open('static/downloads/'+filename_json, 'r') as myfile:
        with open('static/downloads/'+response_filename, 'r', encoding="utf8") as myfile:
            data = myfile.read()
        return render_template('upload.html', filename=filename, data=data)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
