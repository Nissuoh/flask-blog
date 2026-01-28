import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    try:
        with open('blog_posts.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_posts(posts):
    with open('blog_posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    return render_template('index.html', posts=load_posts())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_id = max([p['id'] for p in posts], default=0) + 1
        new_post = {
            "id": new_id,
            "author": request.form.get('author'),
            "title": request.form.get('title'),
            "content": request.form.get('content')
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Post nicht gefunden", 404
    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
