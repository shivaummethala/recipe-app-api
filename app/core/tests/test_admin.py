from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Creating a setup for client as similar to pytest fixtures,
        creating a super user and user for admin UI(manage)"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'shivaadmin@gmail.com',
            password = 'testapp123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'shivaummethala@gmail.com',
            password = 'test123',
            name = 'Test User full name'
        )

    def test_users_listed(self):
        """Test that above users are listed on user page"""
        # generate the url for list user page and reverse is to update url automatically rather
        # changing every time manually
        url = reverse('admin:core_user_changelist')  # admin/core/user
        res = self.client.get(url)
        # check if username and email present in res
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # generate a url as /admin/core/user/id
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Page for adding new user in django admin
        Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)




