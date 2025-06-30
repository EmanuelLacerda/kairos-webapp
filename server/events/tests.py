from django.urls import reverse
from events.models import Event
from authentication.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class EventAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='user1', email="teste@teste9038.com.br", password='test')
        self.event = Event.objects.create(
            creator=self.user,
            description="Realizando teste automatizado",
            start="2025-06-30 20:30",
            end="2025-06-30 22:30"
        )
    
    def test_get_all_events_without_JWT_token(self):
        url = reverse("event-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_event_without_JWT_token(self):
        url = reverse("event-detail", kwargs={"pk": self.event.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_event_without_JWT_token(self):
        url = reverse("event-list")

        data = {
            "creator": self.user,
            "description": "Realizando teste automatizado",
            "start": "2025-06-30 20:38",
            "end": "2025-06-30 22:38"
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_event_without_JWT_token(self):
        url = reverse("event-detail", kwargs={"pk": self.event.id})

        data = {
            "description": "Teste automatizado"
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_event_without_JWT_token(self):
        url = reverse("event-detail", kwargs={"pk": self.event.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)