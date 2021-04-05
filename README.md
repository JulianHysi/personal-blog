# Personal Blog

## Personal blog website that I'm building using Python and Flask

I use this project for my own personal blog, however, it is not really tailored to the core for my own specific needs.  
It can still serve as a simple, general-purpose blog for almost anyone out there.  
It can also be of great use if you'd like to play around with Python, Flask or web development in general.  
I accept pull requests (See [CONTRIBUTING.MD](https://github.com/JulianHysi/personal_blog/blob/master/CONTRIBUTING.md) for more)  

### Example
Visit [julianhysi.com](https://julianhysi.com) to see the deployed application.  
Note: the production source code has a few deplyoment tweaks compared to this repo.

### Features include:
- create, edit and delete an account/profile
- auth system, reset password
- create, edit and delete posts (admin only)
- create, edit and delete books (admin only) 
- comment on a post (users only)
- full-text search posts 
- add tags to the post when you create it, update tags
- view posts (by user, by tag, sorted by date, paginated)

### Tech stack:
- Python 3.x
- Flask
- Jinja2
- SQLite
- SQLAlchemy
- ElasticSearch
- HTML5 and Boostrap 4

### Setting up the virtual environment and dependencies:
1. install Anaconda and verify it works (see Anaconda docs if you don't know how)
2. clone the repo locally and cd to its folder
3. hit `conda env create -f environment.yaml --name env_name` to create the virtual environment
4. hit `conda activate env_name` to activate the virtual environment
5. while the environment is activated, hit `conda list` to verify the dependencies have indeed been installed
6. set environment variables (see section below)
7. install, config and run Elastic server following this guide: https://tecadmin.net/setup-elasticsearch-on-ubuntu/
8. hit `export FLASK_APP=run.py`
9. hit `flask db upgrade` to create the db schema

### Setting environment variables:
1. `SECRET_KEY` (random hex that should be kept secret, see Flask docs for more)
2. `DATABASE_URI` (sqlite database uri, you may set it to `sqlite:///blog.db`)  
**the following 3 variables are necessary only if you want the full functionality**
3. `MAIL_USERNAME` (the email account used for sending emails to users, needed by the password reset feature)
4. `MAIL_PASSWORD` (the email password used for sending emails to users, needed by the password reset feature)
5. `ELASTICSEARCH_URL` (elastic database url, needed by search feature, usually it's `http://localhost:9200`)

### Running the application:
1. make sure you have the above mentioned dependencies installed, and the virtual env activated
2. in the project's top level directory, hit `python run.py`
3. the server should start, and you can access the localhost port 5000 on a browser to see the app
