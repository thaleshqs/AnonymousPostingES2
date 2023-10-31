from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='./templates')

messages = []
max_messages = 10

def get_next_id():
    return len(messages)

@app.route('/policies')
def politics():
    return render_template('policies.html')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    filter_tag = request.args.get('filter')
    filtered_messages = []
    error_message = ""
    
    if filter_tag is None:
        filter_tag = 'all'

    if request.method == 'POST':
        name = request.form['name']
        post = request.form['post']
        
        categories = request.form.getlist('categories')
        comment = request.form.get('comment')
        parent_id = request.form.get('parent_id')
        selected_categories = request.form.getlist('categories')

        if not post.strip() and (comment is None or not comment.strip()):
            return render_template('index.html', messages=messages[-max_messages:], error="Message or comment cannot be blank.", categories=["Secrets", "Family", "Health", "Confession", "Other"], filter=filter_tag)

        if len(selected_categories) > 2:
            return render_template('index.html', messages=messages[-max_messages:], categories=["Secrets", "Family", "Health", "Confession", "Other"], error="You can select up to 2 categories.", filter=filter_tag)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if comment:  
            filter_tag = request.form['filter']
            comment_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            comment_data = {
                'name': name,
                'comment': comment,
                'timestamp': comment_timestamp,
                'categories': categories
            }

            if parent_id is not None:
                parent_id = int(parent_id)
                messages[parent_id]['comments'].append(comment_data)
            return redirect(f'/?filter={filter_tag}')
        else:
            message = {
                'id': get_next_id(),
                'name': name,
                'post': post,
                'timestamp': timestamp,
                'categories': categories,
                'comments': []
            }
            messages.append(message)

        
    
    filtered_messages = [message for message in messages if filter_tag is None or filter_tag == 'all' or filter_tag in message['categories']]
    
    search_query = request.args.get('search')
    if request.method == 'GET':
        if search_query:
            filtered_messages = [message for message in filtered_messages if search_query.lower() in message['post'].lower()]
            if not filtered_messages:
                error_message = "No results found!!!"
            else:
                error_message = ""
                         
            
            
    return render_template('index.html', messages=filtered_messages[-max_messages:], error=error_message, categories=["Secrets", "Family", "Health", "Confession", "Other"], filter=filter_tag, search=search_query)

    #return render_template('index.html', messages=filtered_messages[-max_messages:], error=None, categories=["Secrets", "Family", "Health", "Confession", "Other"], filter=filter_tag)

if __name__ == '__main__':
    app.run()
