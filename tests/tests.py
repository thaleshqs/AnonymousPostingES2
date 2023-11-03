import unittest
import sys
from flask import Flask
sys.path.append('../')  # Adiciona o diretório do projeto ao sys.path
from main import app, messages, previous_search, filtered_messages, create_app
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection in testing
#from flask_caching import Cache


class TestApp(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        self.client = self.app.test_client()
    
    @classmethod
    def tearDown(self):        
        messages.clear()
        filtered_messages.clear()
        previous_search = None

        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None
        self.client = None
        
    
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_politics_page(self):
        response = self.client.get('/policies')
        self.assertEqual(response.status_code, 200)

    def test_submit_message(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_submit_two_messages(self):
        data1 = {
            'name': 'Test User 1',
            'post': 'Test Message 1',
        }
        response1 = self.client.post('/', data=data1)
        self.assertEqual(response1.status_code, 302)

        data2 = {
            'name': 'Test User 1',
            'post': 'Test Message 2',
        }

        response2 = self.client.post('/', data=data2)
        self.assertEqual(response2.status_code, 302)

#    def test_submit_two_messages_and_check_content(self):
#        data1 = {
#            'name': 'Test User 1',
#            'post': 'Test Message 1',
#        }
#        response1 = self.client.post('/', data=data1, follow_redirects=True)
#        self.assertEqual(response1.status_code, 200)
#        self.assertIn(b'Test User 1', response1.data)
#        self.assertIn(b'Test Message 1', response1.data)
#
#        data2 = {
#            'name': 'Test User 2',
#            'post': 'Test Message 2',
#        }
#
#        response2 = self.client.post('/', data=data2, follow_redirects=True)
#        self.assertEqual(response2.status_code, 200)
#        self.assertIn(b'Test User 2', response2.data)
#        self.assertIn(b'Test Message 2', response2.data)

#    def test_submit_message_and_check_content(self):
#        data = {
#            'name': 'Test User',
#            'post': 'Test Message',
#        }
#        response = self.client.post('/', data=data, follow_redirects=True)
#        self.assertEqual(response.status_code, 200)
#        self.assertIn(b'Test User', response.data)
#        self.assertIn(b'Test Message', response.data)

    def test_user_name_on_page(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }
        response = self.client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_post_empty_message(self):
        data = {
            'name': 'Test User',
            'post': '',
        }
        response = self.client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message or comment cannot be blank.', response.data)
        self.assertNotIn(b'Test User', response.data)

    def test_post_message_and_empty_comment(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }
        response = self.client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Message', response.data)
        
        data = {
            'name': 'Test User Comment',
            'comment': '',
        }
        response = self.client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message or comment cannot be blank.', response.data)
        self.assertNotIn(b'Test User Comment', response.data)

    def test_filter_all_works_with_category_post(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
            'categories': 'Health',
        }
        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/?filter=all')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Message', response.data)

    def test_filter_hides_other_posts(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
            'categories': 'Health',
        }
        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/?filter=Family')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Message', response.data)

    def test_too_many_categories_error_three(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health'],
        }
        response = self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/')
        self.assertNotIn(b'This message must not be inside the resulting page.', response.data)

    def test_too_many_categories_error_four(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health', 'Confession'],
        }
        response = self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/')
        self.assertNotIn(b'This message must not be inside the resulting page.', response.data)

    def test_too_many_categories_error_five(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health', 'Confession', 'Other'],
        }
        response = self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/')
        self.assertNotIn(b'This message must not be inside the resulting page.', response.data)
    

    def test_search_with_results(self):
        data = {
            'name': 'Test User',
            'post': 'This is a sample post with a unique keyword',
        }
        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/?search=unique')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a sample post with a unique keyword', response.data)

    def test_search_with_no_results(self):
        data = {
            'name': 'Test User',
            'post': 'This post should not match the search query',
        }
        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/?search=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'This post should not match the search query', response.data)

    def test_search_with_empty_query(self):
        data = {
            'name': 'Test User',
            'post': 'This post should not match the search query',
        }
        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.get('/?search=')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'This post should not match the search query', response.data)

    def test_search_multiple_results(self):
        data1 = {
            'name': 'Test User',
            'post': 'This is the first post matching the search query',
        }
        self.client.post('/', data=data1, follow_redirects=True)

        data2 = {
            'name': 'Test User',
            'post': 'This is the second post matching the search query',
        }
        self.client.post('/', data=data2, follow_redirects=True)

        response = self.client.get('/?search=matching the search query')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the first post matching the search query', response.data)
        self.assertIn(b'This is the second post matching the search query', response.data)
    
    
    def test_combination_search_and_filter(self):
        data1 = {
            'name': 'Test User',
            'post': 'Post with category A',
            'categories': 'Health',
        }
        self.client.post('/', data=data1, follow_redirects=True)

        data2 = {
            'name': 'Test User',
            'post': 'Post with category B',
            'categories': 'Other',
        }
        self.client.post('/', data=data2, follow_redirects=True)

        response = self.client.get('/?filter=Health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post with category A', response.data)
        self.assertNotIn(b'Post with category B', response.data)    

    def test_post_one_comment(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }

        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.post('/', data={
            'name': 'Test User',
            'comment': 'Test Comment',
            'parent_id': 0,
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'Test Comment', response.data)  
    
    
    def test_post_two_comments(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }

        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.post('/', data={
            'name': 'Test User',
            'comment': 'Test Comment',
            'parent_id': 0,  # Replace with the message ID you want to comment on
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Check for a successful response
        
        self.assertIn(b'Test Comment', response.data)  # Assert that the comment is present in the response content
    
        response = self.client.post('/', data={
            'name': 'Test User',
            'comment': 'Test Comment 2',
            'parent_id': 0,  # Replace with the message ID you want to comment on
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertIn(b'Test Comment 2', response.data)

    def test_post_message_with_one_category_and_post_one_comment(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
            'categories': 'Health',
        }

        self.client.post('/', data=data, follow_redirects=True)

        response = self.client.post('/', data={
            'name': 'Test User',
            'comment': 'Test Comment',
            'parent_id': 0,  # Replace with the message ID you want to comment on
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Check for a successful response    
        self.assertIn(b'Test Comment', response.data)  # Assert that the comment is present in the response content
                        
    def test_comment_without_parent(self):
        data = {
            'name': 'Test User',
            'comment': 'This comment should not have a parent',
        }
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(b'This comment should not have a parent', response.data)
    
    def test_comment_with_invalid_parent(self):
        data = {
            'name': 'Test User',
            'comment': 'This comment should not have a parent',
            'parent_id': 12345,  # Invalid parent ID
        }
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(b'This comment should not have a parent', response.data)
    

    def test_comment_on_deleted_message(self):
        data1 = {
            'name': 'Test User',
            'post': 'Original Message',
        }
        self.client.post('/', data=data1, follow_redirects=True)

        data2 = {
            'name': 'Test User',
            'comment': 'Comment on Original Message',
            'parent_id': 0,  # Comment on the original message
        }
        response = self.client.post('/', data=data2, follow_redirects=True)

        messages.clear()  # Clear all messages (simulate message deletion)

        data3 = {
            'name': 'Test User',
            'comment': 'Comment on Deleted Message',
            'parent_id': 0,  # Comment on the original message (now deleted)
        }
        response = self.client.post('/', data=data3, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Comment on Deleted Message', response.data)
    

if __name__ == '__main__':
    unittest.main()
