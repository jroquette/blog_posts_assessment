"""
File of test
"""
import unittest
import json
import requests_mock

from blog_post import app


class TestBlogPostRoutes(unittest.TestCase):
    """
    Class of test blog post routes
    """

    def setUp(self):
        """
        Setup environment for tests
        """
        self.application = app.test_client()
        self.post_mock_tag_test = {"posts": [
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 1,
                "likes": 9999,
                "popularity": 1.0,
                "reads": 9999,
                "tags": [
                    "test",
                ]
            }, {
                "author": "Test Author",
                "authorId": 999,
                "id": 4,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "second_test"
                ]
            }, {
                "author": "Test Author",
                "authorId": 999,
                "id": 5,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "third_test"
                ]
            },
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 6,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "second_test", "third_test"
                ]
            }
        ]}
        self.post_mock_tag_second_test = {"posts": [
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 2,
                "likes": 10,
                "popularity": 0.1,
                "reads": 10,
                "tags": [
                    "second_test",
                ]
            },
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 4,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "second_test"
                ]
            },
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 6,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "second_test", "third_test"
                ]
            }
        ]}
        self.post_mock_tag_third_test = {"posts": [
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 3,
                "likes": 500,
                "popularity": 0.5,
                "reads": 500,
                "tags": [
                    "third_test",
                ]
            },
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 5,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "third_test"
                ]
            },
            {
                "author": "Test Author",
                "authorId": 999,
                "id": 6,
                "likes": 999,
                "popularity": 0.99,
                "reads": 9999,
                "tags": [
                    "test", "second_test", "third_test"
                ]
            }
        ]}

    def test_ping(self):
        """
        Test Ping route
        """
        ans = self.application.get("/api/ping")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertTrue(response.get('success'), True)

    def test_blog_posts_invalid_direction(self):
        """
        Test invalid direction parameter
        """
        ans = self.application.get("/api/posts?tags=tech&direction=ascending")
        self.assertEqual(ans.status_code, 400)

    def test_blog_posts_invalid_sortBy(self):
        """
        Test invalid sortBy parameter
        """
        ans = self.application.get("/api/posts?tags=tech&sortBy=authorId")
        self.assertEqual(ans.status_code, 400)

    def test_blog_posts_without_tag(self):
        """
        Test invalid tag parameter
        """
        ans = self.application.get("/api/posts")
        self.assertEqual(ans.status_code, 400)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_one_tag(self, **kwargs):
        """
        Test request posts with one tag
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(len(response), 4)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_more_than_one_tag(self, **kwargs):
        """
        Test request posts with more than one tag
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=third_test',
                           text=json.dumps(self.post_mock_tag_third_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test,third_test")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(len(response), 6)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_remove_duplicated(self, **kwargs):
        """
        Test request posts with duplicated values
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(len(response), 5)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_direction_asc(self, **kwargs):
        """
        Test request posts direction ascending sort by id
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=third_test',
                           text=json.dumps(self.post_mock_tag_third_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test,third_test")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(response[0]['id'], 1)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_direction_desc(self, **kwargs):
        """
        Test request posts direction descending sort by id
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=third_test',
                           text=json.dumps(self.post_mock_tag_third_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test,third_test&direction=desc")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(response[0]['id'], 6)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_sortBy_reads(self, **kwargs):
        """
        Test request posts sort by reads
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=third_test',
                           text=json.dumps(self.post_mock_tag_third_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test,third_test&sortBy=reads")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(response[0]['reads'], 10)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_sortBy_likes(self, **kwargs):
        """
        Test request posts sort by likes
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=third_test',
                           text=json.dumps(self.post_mock_tag_third_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test,third_test&sortBy=likes")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(response[0]['likes'], 10)

    @requests_mock.Mocker(kw='mock')
    def test_blog_posts_sortBy_popularity(self, **kwargs):
        """
        Test request posts sort by popularity
        """
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=test',
                           text=json.dumps(self.post_mock_tag_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=second_test',
                           text=json.dumps(self.post_mock_tag_second_test), status_code=200)
        kwargs['mock'].get('https://api.hatchways.io/assessment/blog/posts?tag=third_test',
                           text=json.dumps(self.post_mock_tag_third_test), status_code=200)
        ans = self.application.get("/api/posts?tags=test,second_test,third_test&sortBy=popularity")
        response = json.loads(ans.data)
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(response[0]['popularity'], 0.1)


if __name__ == '__main__':
    unittest.main()
