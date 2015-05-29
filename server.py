from flask import Flask
from flask import jsonify,render_template,redirect,url_for,request,abort
from flask.ext.cors import CORS, cross_origin
import json
import subprocess

app = Flask(__name__)

modelsDirectory = 'cv'

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/api/v1.0', methods=['POST'])
def api_v1():
    if not request.json or not 'primetext' in request.json:
        abort(400)
        
    primetext = request.json['primetext']
    temperature = request.json['temperature']
    length = request.json['length']
    model = request.json['model']
    seed = request.json['seed']
    sample = request.json['sample']
    gpuid = request.json['gpuid']
    # override for public APIs
    gpuid = '-1' 

    searchstring = 'th ../char-rnn/sample.lua ../char-rnn/'+modelsDirectory+'/' + str(model) 
    searchstring += ' -gpuid ' + str(gpuid)
    searchstring += ' -primetext "' + str(primetext) + '"'
    searchstring += ' -temperature ' + str(temperature)
    searchstring += ' -length ' + str(length)
    searchstring += ' -seed ' + str(seed)
    searchstring += ' -sample ' + str(sample)
    
    responds = subprocess.Popen(searchstring, shell=True, stdout=subprocess.PIPE).stdout.read()
    
    # remove console stats output
    responds = responds.split('\n', 1)[1].split('\n', 1)[1].split('\n', 1)[1]
   
    return jsonify({'responds': responds}), 201

@app.route('/api/v1.0/model', methods=['POST'])
def api_v1_model():
    searchstring = '(cd ../char-rnn/cv/ && ls -t)'
    responds = subprocess.Popen(searchstring, shell=True, stdout=subprocess.PIPE).stdout.read()
    responds = responds.splitlines();
    return jsonify({'models': responds}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    
    