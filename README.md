# Personal Blog

## Personal blog website that I'm building using Python and Flask

I use this project for my own personal blog, however, it is not really tailored to the core for my own specific needs.
It can still serve as a simple, general-purpose blog for almost anyone out there.
It can also be of great use if you'd like to play around with Python, Flask or web development in general.

<!-- add here a link to the blog, and a screenshot of it -->

Features include:
*create, edit and delete an account/profile
*auth system
*create, edit, and delete posts (admin only)
*comment on a post 
*add tags to the post when you create it
*view posts, by user, by tag or by date (no need to be logged in)


Version Control System used: Git
License used: MIT (see LICENSE.md for more)
Contributing: I accept pull requests (see CONTRIBUTE.md for more)

Environment variables you need to set:
*SECRET_KEY (needed by Flask)
*DATABASE\_URI

Setting up the virtual environment and dependencies:
*clone the repo locally and cd to it's folder
*hit 'conda create --f environment.yaml --name env\_name' to create the virtual environment
*hit 'conda activate your\_env\_name' to activate the virtual environment
*while the environment is activated, hit 'conda list' to verify the dependencies have been indeed installed

Running the application:
*make sure you have the virtual env activated
*in the project's top level directory, hit 'python run.py'
*the server should start, and you can access the localhost port 5000 on a browser to see the app

