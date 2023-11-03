import unittest
import sys
from bs4 import BeautifulSoup

sys.path.append('../')  
from main import app, messages, filtered_messages, previous_search

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False  


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        
    def tearDown(self):
        messages.clear()
        previous_search = None
        filtered_messages.clear()

    
    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_politics_page(self):
        response = self.app.get('/policies')
        self.assertEqual(response.status_code, 200)

    def test_submit_message(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 200) 

    def test_submit_two_messages(self):
        data1 = {
            'name': 'Test User 1',
            'post': 'Test Message 1',
        }
        response1 = self.app.post('/', data=data1)
        self.assertEqual(response1.status_code, 200)
        
        data2 = {
            'name': 'Test User 1',
            'post': 'Test Message 1',
        }
        
        response2 = self.app.post('/', data=data2)
        self.assertEqual(response2.status_code, 200) 

    def test_submit_two_messages_and_check_content(self):
        data1 = {
            'name': 'Test User 1',
            'post': 'Test Message 1',
        }
        response1 = self.app.post('/', data=data1, follow_redirects=True)
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b'Test User 1', response1.data)
        self.assertIn(b'Test Message 1', response1.data)
       
        data2 = {
            'name': 'Test User 2',
            'post': 'Test Message 2',
        }
        
        response2 = self.app.post('/', data=data2, follow_redirects=True)
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Test User 2', response2.data)
        self.assertIn(b'Test Message 2', response2.data)


    def test_submit_message_and_check_content(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)
        self.assertIn(b'Test Message', response.data)
       
    def test_user_name_on_page(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_filter_all_works_with_category_post(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
            'categories': 'Secrets',
        }
        self.app.post('/', data=data, follow_redirects=True)

        response = self.app.get('/?filter=all')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Message', response.data)

    def test_filter_hides_other_posts(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
            'categories': 'Secrets',
        }
        self.app.post('/', data=data, follow_redirects=True)

        response = self.app.get('/?filter=Health')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Message', response.data)
            
    def test_too_many_categories_error_three(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health'],
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        
        response = self.app.get('/')
        self.assertNotIn(b'This message must not be inside the resulting page.', response.data)

    def test_too_many_categories_error_four(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health', 'Confession'],
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        
        response = self.app.get('/')
        self.assertNotIn(b'This message must not be inside the resulting page.', response.data)

    def test_too_many_categories_error_five(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health', 'Confession', 'Other'],
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        
        response = self.app.get('/')
        self.assertNotIn(b'This message must not be inside the resulting page.', response.data)
    
    def test_max_post_limit(self):
        max_posts = 10 

        for i in range(max_posts + 1):
            data = {
                'name': 'Test User',
                'post': f'Test Message {i}',
            }

            response = self.app.post('/', data=data, follow_redirects=True)

        response = self.app.get('/')
        self.assertNotIn(b'Test Message 0', response.data)

        response = self.app.get('/')
        self.assertIn(b'Test Message 10', response.data)
    
    
    def test_post_comment(self):
        response = self.app.post('/', data={
            'name': 'Test User',
            'post': 'Test Message',
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        response = self.app.post('/', data={
            'name': 'Test User',
            'comment': 'Test Comment',
            'parent_id': 0, 
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'Test Comment', response.data)  

    def test_post_comment_with_categories(self):
        data = {
            'name': 'Test User',
            'post': 'Test Message',
            'categories': 'Health',
        }

        self.app.post('/', data=data, follow_redirects=True)

        response = self.app.post('/', data={
            'name': 'Test User',
            'comment': 'Test Comment',
            'parent_id': 0,
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'Test Comment', response.data) 

    def test_search_with_results(self):
        data = {
            'name': 'Test User',
            'post': 'This is a sample post with a unique keyword',
        }
        self.app.post('/', data=data, follow_redirects=True)

        response = self.app.get('/?search=unique')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a sample post with a unique keyword', response.data)

    def test_search_with_no_results(self):
        data = {
            'name': 'Test User',
            'post': 'This post should not match the search query',
        }
        self.app.post('/', data=data, follow_redirects=True)

        response = self.app.get('/?search=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'This post should not match the search query', response.data)

    def test_search_with_empty_query(self):
        data = {
            'name': 'Test User',
            'post': 'This post should not match the search query',
        }
        self.app.post('/', data=data, follow_redirects=True)

        response = self.app.get('/?search=')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'This post should not match the search query', response.data)

    def test_search_multiple_results(self):
        data1 = {
            'name': 'Test User',
            'post': 'This is the first post matching the search query',
        }
        self.app.post('/', data=data1, follow_redirects=True)

        data2 = {
            'name': 'Test User',
            'post': 'This is the second post matching the search query',
        }
        self.app.post('/', data=data2, follow_redirects=True)

        response = self.app.get('/?search=matching the search query')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the first post matching the search query', response.data)
        self.assertIn(b'This is the second post matching the search query', response.data)
    
    def test_combination_search_and_filter(self):
        data1 = {
            'name': 'Test User',
            'post': 'Post with Health',
            'categories': 'Health',
        }
        self.app.post('/', data=data1, follow_redirects=True)

        data2 = {
            'name': 'Test User',
            'post': 'Post with Other',
            'categories': 'Other',
        }
        self.app.post('/', data=data2, follow_redirects=True)

        response = self.app.get('/?filter=Health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post with Health', response.data)
        self.assertNotIn(b'Post with Other', response.data)
    
    def test_comment_without_parent(self):
        data = {
            'name': 'Test User',
            'comment': 'This comment should not have a parent',
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(b'This comment should not have a parent', response.data)

    def test_comment_with_invalid_parent(self):
        data = {
            'name': 'Test User',
            'comment': 'This comment should not have a parent',
            'parent_id': 12345, 
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(b'This comment should not have a parent', response.data)
    
    def test_comment_twice(self):
        self.app = app.test_client()
        data1 = {
            'name': 'Test User',
            'post': 'Original Message',
        }
        response = self.app.post('/', data=data1, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        data2 = {
            'name': 'Test User',
            'comment': 'First Comment',
            'filter': 'all',
            'parent_id': 0,  
        }
        response = self.app.post('/', data=data2, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        self.assertIn(b'First Comment', response.data)
        
        data3 = {
            'name': 'Test User',
            'comment': 'Second Comment',
            'filter': 'all',
            'parent_id': 0, 
        }
        response = self.app.post('/', data=data3, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Second Comment', response.data)
        
    def test_comment_on_deleted_message(self):
        data1 = {
            'name': 'Test User',
            'post': 'Original Message',
        }
        self.app.post('/', data=data1, follow_redirects=True)

        data2 = {
            'name': 'Test User',
            'comment': 'Comment on Original Message',
            'parent_id': 0,
        }
        response = self.app.post('/', data=data2, follow_redirects=True)

        messages.clear()

        data3 = {
            'name': 'Test User',
            'comment': 'Comment on Deleted Message',
            'parent_id': 0,
        }
        response = self.app.post('/', data=data3, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Comment on Deleted Message', response.data)
    
        
if __name__ == '__main__':
    unittest.main()