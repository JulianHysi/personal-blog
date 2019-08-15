from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</>"

@app.route("/about")
def about():
    return "<h1>About Page</>"

if __name__ == '__main__':
    app.run(debug=True)