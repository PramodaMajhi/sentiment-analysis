from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests
from werkzeug.utils import secure_filename
import os, errno
import json

app = Flask(__name__)
api = Api(app)

sentiments = [
    {
        'customer': 'member',
        'devicetype': 'MobileApp',
        'text': 'I ALWAYS HAVE TROUBLE PAYING MY BILL',
        'date_posted': 'April 20, 2018',
        'rating': 0
    },
    {
        'customer': 'member',
        'devicetype': 'website',
        'text': 'CANNOT MAKE PAYMENT. APP IS ALWAYS DOWN.',
        'date_posted': 'April 20, 2018',
        'rating': 3
    }
]

breastCanJson = {
    "examples":
        [
            {
                "clump_thickness": [10.0],
                "unif_cell_size": [3.0],
                "unif_cell_shape": [2.0],
                "marg_adhesion": [10.0],
                "single_epith_cell_size": [5.0],
                "bare_nuclei": [10.0],
                "bland_chrom": [5.0],
                "norm_nucleoli": [4.0],
                "mitoses": [4.0]
            }
        ]

}


class Sentiment(Resource):
    def get(self):
        return {'sentiments': sentiments}

    def post(self):
        json = request.get_json()
        return {'you sent': json}, 201


api.add_resource(Sentiment, '/sentiment')

headers = {
    "content-type": "application/json"
}


class BreastCancer(Resource):
    def get(self):
        return {'breastcancer': breastCanJson}

    def post(self):
        json = request.get_json()
        url = "http://localhost:8501/v1/models/breastcancer:classify"
        res = requests.post(url, headers=headers, json=request.get_json())
        print(res)
        if res.ok:
            return res.json()


api.add_resource(BreastCancer, '/breastcancer')

UPLOAD_FOLDER = 'C:\\Users\\pmajhi01\\Documents\\Dev_BackUp'
UPLOAD_FOLDER_VARIABLES = 'C:\\Users\\pmajhi01\\Documents\\Dev_BackUp\\variables'
# '/tmp/tfServing/allmodels/'
ALLOWED_EXTENSIONS = set(['txt', 'pb', 'doc', 'index', 'jpeg', 'gif', 'pptx', 'ppt', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_VARIABLES'] = UPLOAD_FOLDER_VARIABLES

uploadModelSuccessJson = {
    "success": 'true',
    "message": "successfully uploaded"
}
uploadModelFailedJson = {
    "status": 'failed',
    "message": "No file part or No selected file",
    "error": {
        "code": 123,
        "message": "An error occurred! due to model file was not selected"
    }
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fileList():
    for f in request.files.getlist('file'):
        print(f.filename)


def ensure_dir(directory):
    print(directory)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print("directory created")
        except OSError as e:
            if e.errno != errno.EEXITS:
                raise


class UploadModel(Resource):
    def post(self):

        modelInfo = request.form['modelInfo']
        fileList()
        if modelInfo == '':
            infojson = {
                "message": "Model information is mandatory!"
            }
            return infojson
        json_string = json.loads(modelInfo)
        # loop through the json to collect information
        # print(json_string['sub-directory']['variables']['filename'])
        # check if the post request has the file part
        if 'file' not in request.files:
            return uploadModelFailedJson

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return uploadModelFailedJson
        if file and allowed_file(file.filename) or file.filename.startswith("variables."):
            filename = secure_filename(file.filename)
            # print(filename)
            modelsucccess = {
                "status": 'success',
                "message": "successfully uploaded",
                "file": filename
            }
            newmodel = (json_string['newmodel'])
            modelname = (json_string['modelname'])

            if filename.startswith("variables."):
                if newmodel == 'True':
                    newpath = app.config['UPLOAD_FOLDER'] + '\\' + modelname + '\\' + 'variables'
                    ensure_dir(newpath)
                    file.save(os.path.join(newpath, filename))
            else:
                if newmodel == 'True':
                    newpath = app.config['UPLOAD_FOLDER'] + '\\' + modelname
                    ensure_dir(newpath)
                    file.save(os.path.join(newpath, filename))

            return modelsucccess
        else:
            uploaded = {
                "success": 'false',
                "message": "Please upload correct model file, the extension does not support."
            }
            return uploaded


api.add_resource(UploadModel, '/uploadModel')

if __name__ == '__main__':
    app.run(debug=True)
