from flask import Flask, render_template, request, send_from_directory
from src.utils import *
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():

    open_waste_slot()

    return render_template('insert.html')


@app.route('/waste/pick-type')
def pick_type():
    close_waste_slot()
    image_path = take_trash_picture()
    with open(image_path, 'rb') as f:
        image = f.read()
    
    dechet = find_object_from_picture(image)

    return render_template(
        'type.html',
        dechet=dechet,
        image_path=image_path[1:]
        )

@app.route('/confirmation', methods=['POST'])
def confirmation():
    waste_type = request.form['type']

    process_waste(waste_type)
    return render_template('confirmation.html')

@app.route("/camera/<path:path>")
def static_dir(path):
    return send_from_directory("./camera/", path)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
