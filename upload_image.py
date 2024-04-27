from flask import Flask, render_template, request, redirect, url_for
import Main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print("in")
    if 'image' not in request.files:
        return redirect(request.url)
    
    image = request.files['image']
    
    if image.filename == '':
        return redirect(request.url)
    
    image_path = image.filename
    print(image_path)
    image.save(image_path)
    
    result = Main.main(image_path)
    
    return redirect(url_for('result', text=result))

@app.route('/result/<text>')
def result(text):
    return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)

