import unittest
import requests
import json

class API_Test(unittest.TestCase):
    

    def check_ping(self):
        URL = "http://localhost:5000/api/ping"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)
        print("Test 1 completed")
    
    def check_400_error_for_tag(self):
        URL = "http://localhost:5000/api/posts?tags="
        r = requests.get(URL)
        self.assertEqual(r.status_code, 400)
        print(r._content)
        print("Test 2 completed")

    def check_400_error_for_sort_By(self):
        URL = "http://localhost:5000/api/posts?tags=tech&sortBy=t"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 400)
        print(r._content)
        print("Test 3 completed")

    def check_400_error_for_direction(self):
        URL = "http://localhost:5000/api/posts?tags=tech&direction=des"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 400)
        print(r._content)
        print("Test 4 completed")
    def check_200_for_posts(self):
        URL = "http://localhost:5000/api/posts?tags=tech,tech,history,health&direction=desc&sortBy=popularity"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)
        json_data = json.loads(r.text)
        print(type(json_data))
        print(json_data)
        print("Test 5 completed")
    
if __name__ == "__main__":
    tester = API_Test()
    tester.check_ping()
    tester.check_400_error_for_tag()
    tester.check_400_error_for_sort_By()
    tester.check_400_error_for_direction()
    tester.check_200_for_posts()