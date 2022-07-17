from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from skimage import io
from keras.models import load_model
import cv2
from PIL import Image  # use PIL
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print("File Received")
        filename = secure_filename(file.filename)

        print(filename)
        file.save("static/" + filename)
        # Heroku no need static
        # file = open("static/“+ filename,”r")
        model = load_model("Chest")
        img = Image.open("static/"+filename)  
        img = img.resize((100, 100))
        # need to transfer to np to reshape
        img = np.asarray(img, dtype="float32")
        # rgb to reshape to 1,100,100,3
        img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
        img.shape
        pred = model.predict(img)
        return(render_template("index.html", result=str(pred)))
    else:
        return(render_template("index.html", result="2"))


if __name__ == "__main__":
    app.run()
