import unittest
from django.urls import reverse

class testapp(unittest.TestCase):
    
    def htmltest():
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        print("PASSED")
        
        


