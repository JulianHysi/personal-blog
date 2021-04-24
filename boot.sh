#!/bin/sh
conda activate personal_blog_env
flask db upgrade
exec python run.py
