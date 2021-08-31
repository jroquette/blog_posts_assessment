"""
Run application flask
"""
import os
from blog_post import app

if __name__ == '__main__':
    debug = eval(os.getenv('DEBUG')) or False
    app.run(debug=debug)
