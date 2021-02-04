# Personal Blog

## Personal blog website that I'm building using Python and Flask

I use this project for my own personal blog, however, it is not really tailored to the core for my own specific needs.
It can still serve as a simple, general-purpose blog for almost anyone out there.
It can also be of great use if you'd like to play around with Python, Flask or web development in general.

<!-- add here a link to the blog, and a screenshot of it -->

Features include:
- create, edit and delete an account/profile
- auth system
- create, edit, and delete posts (admin only)
- comment on a post 
- add tags to the post when you create it
- view posts, by user, by tag or by date (no need to be logged in)

Tech stack:
- Python 3.x
- Flask
- Jinja2
- SQLite
- SQLAlchemy
- HTML5 and Boostrap 4

Version Control System used: Git<br>
License used: MIT (see LICENSE.md for more)<br>
Contributing: I accept pull requests (see CONTRIBUTE.md for more)<br>
<!-- add links for the referenced files above -->

Setting up the virtual environment and dependencies:
1. install Anaconda and verify it works (see Anaconda docs if you don't know how)
2. clone the repo locally and cd to it's folder
3. hit 'conda env create -f environment.yaml --name env\_name' to create the virtual environment
4. hit 'conda activate your\_env\_name' to activate the virtual environment
5. while the environment is activated, hit 'conda list' to verify the dependencies have been indeed installed
6. set SECRET\_KEY and DATABASE\_URI environment variables

Running the application:
1. make sure you have the above mentioned dependencies installed, and the virtual env activated
2. in the project's top level directory, hit 'python run.py'
3. the server should start, and you can access the localhost port 5000 on a browser to see the app
