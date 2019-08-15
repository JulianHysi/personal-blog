from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Julian Hysi',
        'title': 'First blog post',
        'content': 'First blog post contents',
        'date_posted': 'August 2019, 15 (?)'
    },
    {
        'author': 'Albor Hysi',
        'title': 'Second blog post',
        'content': 'Second blog post contents',
        'date_posted': 'August 2019, 15 (defo)'
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)