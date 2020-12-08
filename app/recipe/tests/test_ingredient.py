from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):
    """Test the publicly available ingredient API"""

    def setUp(self):
        self.client = APIClient()

    # From here INGREDIENT_URL testing
    def test_login_required(self):
        """Test that login required"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the privatly available ingredient API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='myemail@look.com',
            password='Password123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieving_ingredient_list(self):
        """Test retrieving ingredients"""
        Ingredient.objects.create(user=self.user, name='Potato')
        Ingredient.objects.create(user=self.user, name='Soy Sauce')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limit_to_user(self):
        """Test that return ingredients to authenticated user"""
        otherUser = get_user_model().objects.create_user(
            email='django@look.com',
            password='Test123'
        )

        Ingredient.objects.create(user=otherUser, name='Pepper')
        ing = Ingredient.objects.create(user=self.user, name='butter')
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing.name)

    def test_create_ingredient_successful(self):
        """Test create a new ingredient"""
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENT_URL, payload)

        exist = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exist)

    def test_create_invalid_ingredient(self):
        """Test providing invalid ingredient"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
