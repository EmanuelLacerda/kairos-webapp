from django.urls import reverse
from django.conf import settings
from authentication.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

import json
import jwt

from events.models import Event

class RestrictingAccessAndManipulationToResourcesByAccessTokenTestCase(APITestCase):
    """
    The user cannot nether access, nor create/edit/delete any event without pass their current access token.  
    """

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

class RestrictingAccessAndManipulationToOnlyTheAuthenticatedUserResourcesTestCase(APITestCase):
    """
    The user can only access and create/edit/delete their events.
    """

    def setUp(self):
        self.JWT_authenticator = JWTAuthentication()


        self.user_1 = User.objects.create_user(name="user2", email="teste@teste9238.com.br", password='test')
        self.user_2 = User.objects.create_user(name="user3", email="teste@teste9138.com.br", password='test')

        self.user_1.have_email_verified = True
        self.user_1.save()

        url = reverse("auth-login")
        data = {
            "email": "teste@teste9238.com.br",
            "password": "test"
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.access_token = response.data["access_token"]

        self.event_user_1 = Event.objects.create(
            creator=self.user_1,
            description="Realizando teste automatizado",
            start="2025-08-12 20:30",
            end="2025-08-12 22:30"
        )
        self.event_user_2 = Event.objects.create(
            creator=self.user_2,
            description="Realizando teste automatizado",
            start="2025-08-14 20:30",
            end="2025-08-14 22:30"
        )

        self.general_header = {'Authorization': f'Bearer {self.access_token}'}
    
    def test_get_all_the_user_events(self):
        url = reverse("event-list")

        response = self.client.get(url, headers=self.general_header)

        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]

        any(event["id"] != user_id  for event in response.data)

        self.assertFalse(any(event["id"] != user_id  for event in response.data))
    
    def test_get_event_of_the_user(self):
        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        event_id = Event.objects.filter(creator__id=user_id)[0].id

        url = reverse("event-detail", kwargs={"pk": event_id})

        response = self.client.get(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_event_of_another_user(self):
        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        event_id = Event.objects.exclude(creator__id=user_id)[0].id

        url = reverse("event-detail", kwargs={"pk": event_id})

        response = self.client.get(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_event_of_the_user(self):
        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        event = Event.objects.filter(creator__id=user_id)[0]

        data = {
            "creator": event.creator.id,
            "description": "Testando edição de eventos passando Access Token",
            "start": event.start.isoformat(),
            "end": event.end.isoformat()
        }
        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.patch(url, json.dumps(data), content_type='application/json', headers=self.general_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_event_of_another_user(self):
        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        event = Event.objects.exclude(creator__id=user_id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        data = {
            "creator": event.creator.id,
            "description": "Testando edição de eventos passando Access Token",
            "start": event.start.isoformat(),
            "end": event.end.isoformat()
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json', headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_event_of_the_user(self):
        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        event = Event.objects.filter(creator__id=user_id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.delete(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_event_of_another_user(self):
        user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]
        event = Event.objects.exclude(creator__id=user_id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.delete(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

