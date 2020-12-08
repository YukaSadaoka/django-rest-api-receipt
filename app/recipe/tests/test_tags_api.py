from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class publicTagsApiTests(TestCase):
    """Test the public available tags API"""

    def setUp(self):
        self.client = APIClient()

    # From here TAGS_URL testing
    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='email@look.com',
            password='Password123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # From here TAGS_URL testing
    def test_retrieve_tags(self):
        """Test that retrieving tags with authenticated user"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Meat')

        res = self.client.get(TAGS_URL)

        tag = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tag, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated users"""
        otherUser = get_user_model().objects.create_user(
            email='django@look.com',
            password='Test123'
        )

        Tag.objects.create(user=otherUser, name='Dessert')
        tag = Tag.objects.create(user=self.user, name='Chinese foods')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
