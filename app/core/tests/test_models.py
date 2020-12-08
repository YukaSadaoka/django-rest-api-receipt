from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='myemail@look.com', password='Password123'):
    """Create a sample user"""
    return get_user_model().objects.create_superuser(email, password)


class ModelTests(TestCase):

    # From here User model testing
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

    # From here Tag model testing
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    # From here Ingredient model testing
    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ing = models.Ingredient.objects.create(
            user=sample_user(),
            name='Tomato'
        )

        self.assertEqual(str(ing), ing.name)

    # From here Recipe object model testing
    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Tomato soup with garlic breads',
            time_minutes=15,
            price=3.50
        )

        self.assertEqual(str(recipe), recipe.title)
