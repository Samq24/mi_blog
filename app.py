from flask import Flask, render_template, abort
import json

app = Flask(__name__)

# Cargar posts desde JSON
def cargar_posts():
    with open('posts.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    posts = cargar_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def ver_post(post_id):
    posts = cargar_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
