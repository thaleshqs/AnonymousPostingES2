from flask import Flask, render_template, request

app = Flask(__name__)

posts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post = request.form['post']
        posts.append(post)
    return render_template('index.html', posts=reversed(posts[-5:]))

if __name__ == '__main__':
    app.run()
