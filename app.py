from flask import Flask, render_template, request, redirect, url_for, abort
import json
import os

app = Flask(__name__)

POSTS_FILE = 'post.json'

# Cargar posts desde JSON
def cargar_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def guardar_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

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

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_post():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        posts = cargar_posts()  # ← corregido aquí
        nuevo_id = max([p['id'] for p in posts], default=0) + 1
        posts.append({'id': nuevo_id, 'titulo': titulo, 'contenido': contenido})
        guardar_posts(posts)
        return redirect(url_for('index'))
    return render_template('nuevo.html')

if __name__ == '__main__':
    app.run(debug=True)
