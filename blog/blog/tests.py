from django.test import TestCase,Client
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email = 'test@email.com',
            password='secret'
        )

        self.post = Post.objects.create(
            title = 'A good Title',
            body = 'Nice Body Content',
            author = self.user,
        )

    def test_string_representation(self):
        post=Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good Title') 
        self.assertEqual(f'{self.post.author}', 'testuser' )
        self.assertEqual(f'{self.post.body}', 'Nice Body Content')

    def test_post_list_view(self):
        res = self.client.get(reverse('Home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Nice Body Content')
        self.assertTemplateUsed(res, 'home.html')

    def test_post_detail_view(self):
        res = self.client.get('/post/1/')
        no_res = self.client.get('/post/100000/')
        self.assertEqual(no_res.status_code, 404)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'A good Title')
        self.assertTemplateUsed(res, 'post-detail.html')           

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')
    
    def test_post_create_view(self):
        res = self.client.post(reverse('post_new'), {
            'title': 'New Title',
            'body': 'New text',
            'author': self.user
        })
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'New Title')

    def test_post_update_view(self):
        res = self.client.post(reverse('post_edit', args='1'),{
            'title': 'Updated title',
            'body': 'Updayed text'

        })
        self.assertEqual(res.status_code, 302)

    def test_post_delete_view(self):
        res= self.client.get(
            reverse('post_delete', args='1')
        )
        self.assertEqual(res.status_code, 200)