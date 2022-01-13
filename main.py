import os, time, io
from app import app
from flask import flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError
#from image_rotation import rotate
from rotation import generalPipeline


s3 = boto3.client('s3')

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
        #saving a file to temp directory on local machine
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #uploading file to S3
        s3.upload_file(Bucket = SOURCE_BUCKET_NAME, Filename='static/uploads/'+filename, Key = filename)
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')

        try:
            #checking if the output file is ready on S3
            waiter = s3.get_waiter('object_exists')
            response_filename = filename+'-analyzeexpenseresponse.txt'
            waiter.wait(Bucket=DESTINATION_BUCKET_NAME, Key = response_filename, WaiterConfig={'Delay': 3, 'MaxAttempts': 10})
            print('Object exists: ' + DESTINATION_BUCKET_NAME +'/'+response_filename)
            #downloading the output file to temp folder on local machine
            s3.download_file(DESTINATION_BUCKET_NAME, response_filename, 'static/downloads/'+response_filename)
        except ClientError as e:
            raise Exception( "boto3 client error in use_waiters_check_object_exists: " + e.__str__())
        except Exception as e:
            #flash('Sorry, Failed to extract details, please try again.')
            #return redirect(request.url)
            return render_template("upload.html", filename=filename, data="Sorry, couldn't extact details from Image, please try again.")

        #reading output file from temp folder to display on webpage
        with io.open('static/downloads/'+response_filename, 'r', encoding="utf8") as myfile:
            data = myfile.read()
            print('data is:', data[:100])
        #rotating image into correct angle
        #rotate('static/uploads/'+filename)
        try:
            generalPipeline('static/uploads/'+filename)
        except Exception as f:
            print('exception occurred in rotation: ',f)
            flash('Sorry, Failed to rotate image, please try again.')
        return render_template('upload.html', filename=filename, data=data)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception:
        app.run(host='localhost', port=5000)
