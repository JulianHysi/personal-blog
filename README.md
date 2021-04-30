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
**follow all these steps to set up a contribution workflow**  
**skip to the Docker workflow at the end, if you simply want to run the app**
1. clone the repo locally and cd to its folder
2. hit `python -m venv venv` to create a virtual environment
3. hit `source venv/bin/activate` to activate the virtual environment
4. while the environment is activated, hit `pip install -r requirements.txt` to install dependencies
5. hit `pip list` to verify the dependencies have been installed
6. set environment variables (see section below)
7. install, config and run Elastic server following this guide: (https://tecadmin.net/setup-elasticsearch-on-ubuntu/)
8. hit `export FLASK_APP=run.py`
9. hit `flask db upgrade` to create the db schema
10. see section below on how to run the application

### Setting environment variables:
1. `SECRET_KEY` (random hex that should be kept secret, see Flask docs for more)
2. `DATABASE_URI` (sqlite database uri, set it to `sqlite:///static/db/blog.db`)  
**the following 3 variables are necessary only if you want the full functionality**
3. `MAIL_USERNAME` (the email account used for sending emails to users, needed by the password reset feature)
4. `MAIL_PASSWORD` (the email password used for sending emails to users, needed by the password reset feature)
5. `ELASTICSEARCH_URL` (elastic database url, needed by search feature, you may use `http://localhost:9200`)

### Running the application:
1. make sure you have the above mentioned dependencies installed, and the virtual env activated
2. in the project's top level directory, hit `python run.py`
3. the server should start, and you can access the localhost port 5000 on a browser to see the app

### Docker workflow
**this workflow is a simpler alternative to the contribution workflow from above**
1. install Docker (https://linuxize.com/post/how-to-install-and-use-docker-on-ubuntu-20-04/)
2. hit `docker build -t personal_blog:latest` to build an image off of Dockerfile
3. set environment variables (see section above)
4. pull an elastic image: `docker pull docker.elastic.co/elasticsearch/elasticsearch:7.12.1`
5. run an elastic container: `docker run --name elasticsearch -p 9200:9200 -p 9300:9300 -d --rm -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.12.1` and wait a few seconds
6. hit `bash docker_run.sh` and access the app on the given port
