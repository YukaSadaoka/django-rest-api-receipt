from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user(self):
        """Test creating a new user with an email is successful"""
        email = 'myemail@look.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email(self):
        """Test the email for a new user is normalized"""
        email = 'myemail@LOOK.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user who doesn't have email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Pass123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'myemail@LOOK.COM'
        user = get_user_model().objects.create_superuser(email, 'test123')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
