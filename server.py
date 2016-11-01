import os
from flask import Flask, flash, request, url_for, jsonify, redirect, send_from_directory, send_file, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from audio_deepdream_function import deepdream_func

app = Flask(__name__)
app.secret_key = 'dev'

#set up the uploads folder
UPLOAD_FOLDER = './audio'
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/")
def home():
    layers = ["mixed4d_3x3_bottleneck_pre_relu", "Nathan", "Jon"]
    return render_template('form.html', layers=layers)


@app.route("/post/", methods=['POST'])
@cross_origin()
def post():
    print(request.data)
    # name=request.form[request.data]
    # email=request.form['youremail']
    # myDict = {'a': 2, 'b': 3}
    # print(name)
    data = {"name": "name", "title": "album.title"}
    return jsonify(data)

@app.route("/test/", methods=['GET'])
@cross_origin()
def test():
    layer = 'mixed4d_3x3_bottleneck_pre_relu'
    channel = 139 # picking some feature channel to visualize
    path_to_audio = './audio/helix_drum_track.wav'
    iterations = 20
    octaves = 8

    print("Calling the function from test")
    # data = deepdream_func(layer,channel,path_to_audio,iterations,octaves)
    print("after the function call from test")
    # print(data['test'])
    # print(data['dream_spectrogram'])

    return send_file("out.png")
    # return data['test']
    # data = {"id": 7, "title": "OMG TEST COMPLETE"}
    # return jsonify(data)
    # return send_file("out.png")



@app.route('/image/<imageid>', methods=['POST', 'GET'])
@cross_origin()
def upload_file(imageid):
    print('You are looking at ' +imageid)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filelocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filelocation)
            return 'upload complete'
    elif request.method == 'GET':
        return send_file("out.png")
    return

# layer = 'mixed4d_3x3_bottleneck_pre_relu'
# channel = 139 # picking some feature channel to visualize
# path_to_audio = './audio/helix_drum_track.wav'
# iterations = 1
# octaves = 8
@app.route('/audio', methods=['POST', 'GET'])
@cross_origin()
def upload_audio():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filelocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filelocation)


            #get variables from the user's form
            layer = request.form['layer']
            channel = int(request.form['channel'])
            # path_to_audio = request.form['path_to_audio']
            iterations = int(request.form['iterations'])
            octaves = int(request.form['octaves'])
            path_to_audio = "./audio/"+str(filename)
            print("1")
            print(filename)
            print("2")
            print(path_to_audio)
            print("3")

            print("The forms data:")
            print(layer, channel, path_to_audio, iterations, octaves)
            #run the function
            deepdream_func(layer,channel,path_to_audio,iterations,octaves)

            #return the results
            return send_file("out.png")

            # return 'upload complete'
    elif request.method == 'GET':
        return send_from_directory("uploads", "the_books.mp3")
    return

    #TODO content streaming in flask is a thing that can work


if __name__ == "__main__":
    app.run()
