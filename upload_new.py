# coding=utf-8
import os
from scripts.tf_mushrooms.predict_mushroom import tensorflow
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

from grib_processing import get_grib_info_by_eng_name


UPLOAD_FOLDER = 'scripts/tf_mushrooms/tf_files/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    res = tensorflow('/tf_files/uploads/' + filename)
    max = parse_tensorflow_res(res)
    #print(max)
    grib_info = get_grib_info_by_eng_name(max[0])
    return grib_info

    #return u'это {} с вероятностью {}'.format(max[0], max[1])
     # send_from_directory(app.config['UPLOAD_FOLDER'],
     #                           filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse_tensorflow_res(res):
    d = {}
    max_value=float(0)
    res1 = res.replace('\n', ' ').split(' ')
    for i in range(len(res1)//4):
        #print(i*4, (i+1)*4-1)
        name = res1[i*4]
        value_string = res1[(i+1)*4-1]
        value_string = value_string.strip()[0:-1]
        value = float(value_string)
        name = res1[i*4]
        d[name] = value
        value = max_value
        if d[name]>max_value:
            max_value = d[name]
            print (name, max_value)
            list_of_max = [name, max_value]
    return list_of_max
        

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
            return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
