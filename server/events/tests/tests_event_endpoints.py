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
            start="2025-06-30T20:30:00Z",
            end="2025-06-30T22:30:00Z"
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
            "start": "2025-06-30T20:38:00Z",
            "end": "2025-06-30T22:38:00Z"
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
        self.user_id = jwt.decode(self.access_token, settings.SECRET_KEY, algorithms=["HS256"])["user_id"]

        self.event_user_1 = Event.objects.create(
            creator=self.user_1,
            description="Realizando teste automatizado",
            start="2026-12-12T20:30:00Z",
            end="2026-12-12T22:30:00Z"
        )
        self.event_user_2 = Event.objects.create(
            creator=self.user_2,
            description="Realizando teste automatizado",
            start="2026-12-14T20:30:00Z",
            end="2026-12-14T22:30:00Z"
        )

        self.general_header = {'Authorization': f'Bearer {self.access_token}'}
    
    def test_if_creator_is_an_readonly_attribute(self):
        url = reverse("event-list")

        response = self.client.get(url, headers=self.general_header)
        event = response.data[0]

        with self.assertRaisesMessage(KeyError, "creator"):
            event["creator"]
    
    def test_get_all_the_user_events(self):
        all_the_user_events = Event.objects.filter(creator__id=self.user_id)

        url = reverse("event-list")

        response = self.client.get(url, headers=self.general_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(all_the_user_events), len(response.data))
    
    def test_get_event_of_the_user(self):
        event_id = Event.objects.filter(creator__id=self.user_id)[0].id

        url = reverse("event-detail", kwargs={"pk": event_id})

        response = self.client.get(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_event_of_another_user(self):
        event_id = Event.objects.exclude(creator__id=self.user_id)[0].id

        url = reverse("event-detail", kwargs={"pk": event_id})

        response = self.client.get(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_event_without_passing_user_id(self):
        data = {
            "description": "Criando evento sem passar id do usuário",
            "start": "2026-08-14T20:30:00Z",
            "end": "2026-08-14T22:30:00Z"
        }
        url = reverse("event-list")

        response = self.client.post(url, json.dumps(data), content_type='application/json', headers=self.general_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_create_event_passing_user_id(self):
        data = {
            "creator": self.user_id,
            "description": "Criando evento passando id do usuário",
            "start": "2026-08-14T22:40:00Z",
            "end": "2026-08-14T23:00:00Z"
        }
        url = reverse("event-list")

        response = self.client.post(url, json.dumps(data), content_type='application/json', headers=self.general_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_event_passing_another_user_id(self):
        """
        Regardless of whether the user ID is passed or not, and whether the ID of the authenticated user or another user is passed, the event created must belong to the authenticated user.

        This test verifies that the API works this way when the other user's ID is passed.
        """

        another_user_id = User.objects.exclude(id=self.user_id)[0].id

        data = {
            "creator": another_user_id,
            "description": "Criando evento passando id de outro usuário",
            "start": "2026-08-15T22:40:00Z",
            "end": "2026-08-15T23:00:00Z"
        }
        url = reverse("event-list")

        response = self.client.post(url, json.dumps(data), content_type='application/json', headers=self.general_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.get(id=response.data["id"]).creator.id, self.user_id)


    def test_update_event_of_the_user(self):
        event = Event.objects.filter(creator__id=self.user_id)[0]

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
        event = Event.objects.exclude(creator__id=self.user_id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        data = {
            "creator": event.creator.id,
            "description": "Testando edição de eventos passando Access Token",
            "start": event.start.isoformat(),
            "end": event.end.isoformat()
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json', headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_the_creator_id_of_a_event_of_the_user(self):
        """
        Users can not change the creator id of their events to ensure they can not pass their event to another.

        This test verifies that the API works this way.
        """

        another_user_id = User.objects.exclude(id=self.user_id)[0].id

        event = Event.objects.filter(creator__id=self.user_id)[0]

        data = {
            "creator": another_user_id,
            "description": "Testando edição de eventos passando Access Token",
            "start": event.start.isoformat(),
            "end": event.end.isoformat()
        }
        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.patch(url, json.dumps(data), content_type='application/json', headers=self.general_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(id=response.data["id"]).creator.id, self.user_id)
    
    def test_delete_event_of_the_user(self):
        event = Event.objects.filter(creator__id=self.user_id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.delete(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_event_of_another_user(self):
        event = Event.objects.exclude(creator__id=self.user_id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.delete(url, headers=self.general_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class RestrictingAccessAndManipulationToOnlyTheVerifiedUserResourcesTestCase(APITestCase):
    def setUp(self):
        url = reverse("auth-login")
        self.JWT_authenticator = JWTAuthentication()


        self.user_verified_data = {}

        self.user_verified_data["instance"] = User.objects.create_user(name="user_verified", email="teste@teste123.com.br", password='test')
        self.user_verified_data["instance"].have_email_verified = True
        self.user_verified_data["instance"].save()

        response = self.client.post(url, json.dumps({"email": "teste@teste123.com.br", "password": "test"}), content_type='application/json')
        self.user_verified_data["access_token"] = response.data["access_token"]
        self.user_verified_data["header"] = {'Authorization': f'Bearer {self.user_verified_data["access_token"]}'} 

        self.user_verified_data["event"] = Event.objects.create(
            creator=self.user_verified_data["instance"],
            description="Realizando teste automatizado",
            start="2026-12-12T20:30:00Z",
            end="2026-12-12T22:30:00Z"
        )


        self.user_unverified_data = {}

        self.user_unverified_data["instance"] = User.objects.create_user(name="user_unverified", email="teste@teste453.com.br", password='test')
        self.user_unverified_data["instance"].save()

        response = self.client.post(url, json.dumps({"email": "teste@teste453.com.br", "password": "test"}), content_type='application/json')
        self.user_unverified_data["access_token"] = response.data["access_token"]
        self.user_unverified_data["header"] = {'Authorization': f'Bearer {self.user_unverified_data["access_token"]}'} 

        self.user_unverified_data["event"] = Event.objects.create(
            creator=self.user_unverified_data["instance"],
            description="Realizando teste automatizado",
            start="2026-12-12T20:30:00Z",
            end="2026-12-12T22:30:00Z"
        )
    
    def test_get_all_the_user_verified_events(self):
        all_the_user_events = Event.objects.filter(creator__id=self.user_verified_data["instance"].id)

        url = reverse("event-list")

        response = self.client.get(url, headers=self.user_verified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(all_the_user_events), len(response.data))
    
    def test_get_all_the_user_unverified_events(self):
        url = reverse("event-list")

        response = self.client.get(url, headers=self.user_unverified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_event_of_the_user_verified(self):
        event_id = Event.objects.filter(creator__id=self.user_verified_data["instance"].id)[0].id

        url = reverse("event-detail", kwargs={"pk": event_id})

        response = self.client.get(url, headers=self.user_verified_data["header"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_event_of_user_unverified(self):
        event_id = Event.objects.filter(creator__id=self.user_unverified_data["instance"].id)[0].id

        url = reverse("event-detail", kwargs={"pk": event_id})

        response = self.client.get(url, headers=self.user_unverified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event_of_the_verified_user(self):
        data = {
            "creator": self.user_verified_data["instance"].id,
            "description": "Criando evento sem passar id do usuário",
            "start": "2026-08-14T20:30:00Z",
            "end": "2026-08-14T22:30:00Z"
        }
        url = reverse("event-list")

        response = self.client.post(url, json.dumps(data), content_type='application/json', headers=self.user_verified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_create_event_of_the_unverified_user(self):
        data = {
            "creator": self.user_unverified_data["instance"].id,
            "description": "Criando evento passando id do usuário",
            "start": "2026-08-14T22:40:00Z",
            "end": "2026-08-14T23:00:00Z"
        }
        url = reverse("event-list")

        response = self.client.post(url, json.dumps(data), content_type='application/json', headers=self.user_unverified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_of_the_verified_user(self):
        event = Event.objects.filter(creator__id=self.user_verified_data["instance"].id)[0]

        data = {
            "creator": event.creator.id,
            "description": "Testando edição de eventos de usuário verificado",
            "start": event.start.isoformat(),
            "end": event.end.isoformat()
        }
        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.patch(url, json.dumps(data), content_type='application/json', headers=self.user_verified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_update_event_of_the_unverified_user(self):
        event = Event.objects.filter(creator__id=self.user_unverified_data["instance"].id)[0]

        data = {
            "creator": event.creator.id,
            "description": "Testando edição de eventos de usuário verificado",
            "start": event.start.isoformat(),
            "end": event.end.isoformat()
        }
        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.patch(url, json.dumps(data), content_type='application/json', headers=self.user_unverified_data["header"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_of_the_verified_user(self):
        event = Event.objects.filter(creator__id=self.user_verified_data["instance"].id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.delete(url, headers=self.user_verified_data["header"])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_event_of_the_unverified_user(self):
        event = Event.objects.filter(creator__id=self.user_unverified_data["instance"].id)[0]

        url = reverse("event-detail", kwargs={"pk": event.id})

        response = self.client.delete(url, headers=self.user_unverified_data["header"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)