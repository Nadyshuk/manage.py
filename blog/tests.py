from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Post, Comment

class BlogTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.admin = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword'
        )
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'author': self.user,
            'category': 'Test Category'
        }

    def test_post_list_create_view(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail_view(self):
        post = Post.objects.create(**self.post_data)
        response = self.client.get(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user)
        updated_data = {'title': 'Updated Post', 'content': 'Updated Content'}
        response = self.client.put(f'/api/posts/{post.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_list_create_view(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/', {'content': 'Test Comment', 'post': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_detail_view(self):
        comment = Comment.objects.create(content='Test Comment', post_id=1)
        response = self.client.get(f'/api/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user)
        updated_data = {'content': 'Updated Comment'}
        response = self.client.put(f'/api/comments/{comment.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_login_view(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_registration_view(self):
        response = self.client.post('/api/register/', {'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_id', response.data)

    def test_admin_only_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/admin-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/admin-only/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

