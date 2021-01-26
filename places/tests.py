from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Place
from .serializers import PlaceSerializer


class PlacesViewTestCases(APITestCase):

    def setUp(self):
        place = Place(name="my place")
        place.save()
        self.place = place

    def test_places_list_view(self):
        response = self.client.get("/places/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_places_new_place_view(self):
        data = {"name": "my new place"}
        response = self.client.post("/places/new/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_places_new_place_view_bad(self):
        data = "data"
        response = self.client.post("/places/new/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_places_detail_place_view_get(self):
        response = self.client.get("/places/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_places_detail_place_view_get_bad(self):
        response = self.client.get("/places/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_places_detail_place_view_put(self):
        data = {"name": "new name"}
        response = self.client.put("/places/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_places_detail_place_view_delete(self):
        response = self.client.delete("/places/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
