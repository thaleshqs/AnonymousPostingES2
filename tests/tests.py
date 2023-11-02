import unittest
import sys
sys.path.append('../')  # Adiciona o diretório do projeto ao sys.path
from main import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
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

    def test_submit_message(self):
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
            
    def test_too_many_categories_error(self):
        data = {
            'name': 'Test User',
            'post': 'This message must not be inside the resulting page.',
            'categories': ['Secrets', 'Family', 'Health'],
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
            
if __name__ == '__main__':
    unittest.main()
