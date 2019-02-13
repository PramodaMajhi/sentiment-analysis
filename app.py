import errno
import json
import os

import requests
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

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
ALLOWED_EXTENSIONS = set(['pb', 'index'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_VARIABLES'] = UPLOAD_FOLDER_VARIABLES


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


success = {
    "status": "success",
    "message": "successfully uploaded"
}

def fileList(path):
    success["files"] = []
    for f in request.files.getlist('file'):
        filename = secure_filename(f.filename)
        if filename.startswith("variables."):
            variablepath = path + '\\' + 'variables'
            ensure_dir(variablepath)
            f.save(os.path.join(variablepath, filename))
            success["files"].append(filename)
        else:
            f.save(os.path.join(path, filename))
            success["files"].append(filename)


def ensure_dir(directory):
    # print(directory)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            # print("directory created")
        except OSError as e:
            if e.errno != errno.EEXITS:
                raise


class UploadModel(Resource):
    def post(self):
        print("entered upload model method")
        modelInfo = request.form['modelInfo']
        print('request.get_json()', request.get_json())
        emptyJson = {
            "status": "failed",
            "message": "Model information is was not supplied!"
        }
        if modelInfo == '':
            return emptyJson
        listFiles = []
        for f in request.files.getlist('file'):
            fname = secure_filename(f.filename)
            print(fname)
            listFiles.append(fname)

        if 'saved_model.pb' not in listFiles:
            fileNotPresent = {
                "status": "failed",
                "message": "Model file 'saved_model.pb' was not selected!"
            }
            return fileNotPresent

        json_string = json.loads(modelInfo)
        modelname = (json_string['modelname'])
        version = (json_string['version'])
        path = app.config['UPLOAD_FOLDER'] + '\\' + modelname + '\\' + version
        ensure_dir(path)
        fileList(path)
        return success

api.add_resource(UploadModel, '/uploadModel')

if __name__ == '__main__':
    app.run(port=7000,debug=True)
