from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}  # Simple in-memory user store

def process_image(input_path, output_path):
    img = cv2.imread(input_path)
    background = cv2.imread('background.jpg')  # Pre-captured background
    background = cv2.resize(background, (img.shape[1], img.shape[0]))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_maroon = np.array([160, 100, 20])
    upper_maroon = np.array([180, 255, 150])
    mask = cv2.inRange(hsv, lower_maroon, upper_maroon)
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (15, 15), 0)
    mask_inv = cv2.bitwise_not(mask)
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(img, img, mask=mask_inv)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imwrite(output_path, final_output)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if username in users:
            return render_template('signup.html', error='Username already exists')
        users[username] = {'password': password}
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/invisible', methods=['GET', 'POST'])
def invisible():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['photo']
        input_path = os.path.join('uploads', file.filename)
        output_path = os.path.join('outputs', 'output.jpg')
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)
        file.save(input_path)
        process_image(input_path, output_path)
        return send_file(output_path, mimetype='image/jpeg')
    return render_template('invisible.html')


    # ...existing code...

import subprocess

@app.route('/cloak')
def cloak():
    # This will run your final.py script when the user clicks the button
    # Make sure final.py is in the same folder and has the correct code
    subprocess.Popen(['python', 'final.py'])
    return render_template('cloak.html')

# ...existing code...

if __name__ == '__main__':
    app.run(debug=True)