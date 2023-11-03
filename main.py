from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

messages = []
filtered_messages = []
max_messages = 10
previous_search = None

class Post:
    def __init__(self, id, name, post, timestamp, categories):
        self.id = id
        self.name = name
        self.post = post
        self.timestamp = timestamp
        self.categories = categories
        self.comments = []

class Comment:
    def __init__(self, parent_id, comment, timestamp,):
        self.parent_id = parent_id
        self.comment = comment
        self.timestamp = timestamp
        
def create_app():
    app = Flask(__name__)

    def get_next_id():
        return len(messages)

    @app.route('/policies')
    def politics():
        return render_template('policies.html')

    @app.route('/', methods=['GET'])
    def index_get():
        global previous_search
        error_message = ""
        filter_tag = request.args.get('filter', 'all')
        filtered_messages = filter_messages(filter_tag, previous_search)
        search_query = request.args.get('search')
        if search_query is not None and search_query.strip():
            filtered_messages = [message for message in filtered_messages if search_query.lower() in message.post.lower()]
            previous_search = search_query
            if not filtered_messages:
                error_message = "No results found"
        elif search_query is not None and len(search_query) == 0:
            filtered_messages = []
            error_message = "No results found"
        elif search_query is None or len(search_query) == 0:
            previous_search = None
        return render_template('index.html', messages=filtered_messages[-max_messages:], error=error_message, categories=["Secrets", "Family", "Health", "Confession", "Other"], filter=filter_tag, search=search_query)

    @app.route('/', methods=['POST'])
    def index_post():
        global previous_search
        error_message = ""
        filter_tag = request.form.get('filter', 'all')
        name = request.form.get('name', "")
        post = request.form.get('post', "")
        categories = request.form.getlist('categories')
        comment = request.form.get('comment', "")
        parent_id = request.form.get('parent_id', "")

        if not post.strip() and (comment is None or not comment.strip()):
            return render_template('index.html', messages=messages[-max_messages:], error="Message or comment cannot be blank.", categories=["Secrets", "Family", "Health", "Confession", "Other"], filter=filter_tag)

        if len(categories) > 2:
            return render_template('index.html', messages=messages[-max_messages:], categories=["Secrets", "Family", "Health", "Confession", "Other"], error="You can select up to 2 categories.", filter=filter_tag)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if comment:
            add_comment(parent_id, comment)
        else:
            add_post(name, post, timestamp, categories)

        if previous_search is None:
            return redirect(url_for('index_get', filter=filter_tag))
        else:
            return redirect(url_for('index_get', filter=filter_tag, search = previous_search))

    def add_post(name, post, timestamp, categories):
        message = Post(get_next_id(), name, post, timestamp, categories)
        messages.append(message)

    def add_comment(parent_id, comment):
        comment_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_data = Comment(parent_id, comment, comment_timestamp)

        if parent_id:
            parent_id = int(parent_id)
            if parent_id >= 0 and parent_id < len(messages):
                messages[parent_id].comments.append(comment_data)

    def filter_messages(filter_tag, search_query):
        filtered_messages = [message for message in messages if filter_tag is None or filter_tag == 'all' or filter_tag in message.categories]
        if search_query is not None and search_query.strip():
            filtered_messages = [message for message in filtered_messages if search_query.lower() in message.post.lower()]
        return filtered_messages

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
