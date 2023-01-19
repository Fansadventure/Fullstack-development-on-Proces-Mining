from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import FileField, SubmitField, IntegerField, DecimalField
from wtforms.validators import InputRequired, NumberRange
from werkzeug.utils import secure_filename

import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/')))
import alpha, heuristic_miner as hm, import_xes

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this_is_a_secret_key'

# app.config['UPLOAD_FOLDER'] =  'frontend/static/upload'   # for server
# app.config['OUTPUT_FOLDER'] =  'frontend/static/output'   # for server

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5M

class uploadFile_alpha(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['xes']), FileSize(app.config['MAX_CONTENT_LENGTH'])])  
    submit = SubmitField('Submit')

class uploadFile_heuristic(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['xes']), FileSize(app.config['MAX_CONTENT_LENGTH'])])  
    threshold_df = IntegerField('Threshold for direct follows', validators=[InputRequired(), NumberRange(min=0)], render_kw={"placeholder": "Allowed value i ≥ 0"})
    threshold_dm = DecimalField('Threshold for dependency measure', validators =[InputRequired(), NumberRange(0, 1, 0.01)], render_kw={"placeholder": "Allowed value 0 ≤ i ≤ 1"})
    submit = SubmitField('Submit')

@app.route("/")
@app.route("/introduction")
def home():
    return render_template('Introduction.html')                    

@app.route("/alpha_miner", methods = ['POST', 'GET'])
def alpha_miner():
    form = uploadFile_alpha()
    image = ''
    if request.method == 'GET':
        return render_template('AlphaMiner.html', form = form, image = image)

    result_msg = 'File upload failed. Only xes files is accepted.'
    if request.method == 'POST' and form.validate_on_submit():
        # remove the old uploaded files
        files = os.listdir('static/upload')
        for i in files:
            if i != '.gitkeep': 
                os.remove(os.path.join('static/upload', i))
        # save the new uploaded file
        f = form.file.data
        path = os.path.join('static/upload', secure_filename(f.filename))
        f.save(path)
        result_msg = 'The selected file [' + f.filename + '] is uploaded successfully.' 
        # import the xes file and use alpha to generate a petri net
        log = import_xes.importer().read_xes(path)
        alpha.footprint_matrix(log)
        alpha.draw_petri_net(log)
        petri_net = 'static/output/petri_net.gv.png'   
        footprint = 'static/output/footprint_matrix.png'
        return render_template('AlphaMiner.html', form = form, msg = result_msg, image_petri=petri_net, image_footprint=footprint)

    return render_template('AlphaMiner.html', form = form, msg = result_msg, image = image)

@app.route("/heuristic_miner", methods = ['POST', 'GET'])
def heuristic_miner():
    form = uploadFile_heuristic()
    image = ''
    if request.method == 'GET':
        return render_template('HeuristicMiner.html', form = form, image = image)
        
    result_msg = 'File upload failed. Only xes files is accepted.'
    if request.method == 'POST' and form.validate_on_submit():
        # clear the old uploaded files before saving the new one
        files = os.listdir('static/upload')
        for i in files:
            if i != '.gitkeep':
                os.remove(os.path.join('static/upload', i))
        # save the new uploaded file
        file = form.file.data
        path = os.path.join('static/upload', secure_filename(file.filename))
        file.save(path)
        result_msg = 'The selected file [' + file.filename + '] is uploaded successfully.' 
        # import the xes file and use hm to generate a petri net
        log = import_xes.importer().read_xes(path)
        hm.dm_matrix(log)
        hm.draw_denpendencyGraph(log, form.threshold_df.data, form.threshold_dm.data)
        hm.draw_cnet(log)
        in_bind = str(dict(sorted(hm.input_binding(log).items()))).replace('\'', '')
        out_bind = str(dict(sorted(hm.output_binding(log).items()))).replace('\'', '')
        bindings = (in_bind, out_bind)
        dg = 'static/output/dependency_graph.gv.png'
        matrix = 'static/output/dm_matrix.png'
        cnet = 'static/output/cnet.gv.png'
        images = (dg, matrix, cnet)
        images = (dg, matrix, cnet)
        return render_template('HeuristicMiner.html', form = form, msg = result_msg, images = images, bindings = bindings)
    return render_template('HeuristicMiner.html', form = form, msg = result_msg, image = image)
    
if __name__ == '__main__':
    app.run(host='::1', port=9009)
