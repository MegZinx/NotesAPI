from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Note

# Create your tests here.


class NoteAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="sana", password="testpass123")
        self.user2 = User.objects.create_user(username="harris", password="testpass123")
        self.note1 = Note.objects.create(
            owner=self.user1, title="Sana Note", content="secret"
        )

    def authenticate(self, user):
        response = self.client.post(
            "/api/token/", {"username": user.username, "password": "testpass123"}
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_unauthenticated_request_rejected(self):
        response = self.client.get("/api/notes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_notes(self):
        Note.objects.create(owner=self.user2, title="Harris Note", content="private")
        self.authenticate(self.user1)
        response = self.client.get("/api/notes/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Sana Note")

    def test_user_cannot_access_others_note_detail(self):
        self.authenticate(self.user2)
        response = self.client.get(f"/api/notes/{self.note1.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_note_sets_user_automatically(self):
        self.authenticate(self.user1)
        response = self.client.post(
            "/api/notes/", {"title": "New Note", "content": "body text"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], "sana")

    def test_empty_title_rejected(self):
        self.authenticate(self.user1)
        response = self.client.post("/api/notes/", {"title": "   ", "content": "body"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
