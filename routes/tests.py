from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Route
from .serializers import RouteSerializer
from places.models import Place


class RoutesViewTestCases(APITestCase):

    def setUp(self):
        place_origin = Place(name="my place origin")
        place_origin.save()
        place_destination = Place(name="my place destination")
        place_destination.save()
        place_new = Place(name="my new place")
        place_new.save()
        route = Route(place_origin=place_origin,
                      place_destination=place_destination)
        route.save()
        self.place_origin = place_origin
        self.place_destination = place_destination
        self.place_new = place_new
        self.route = route

    def test_routes_list_view(self):
        response = self.client.get("/routes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_new_route_view(self):
        data = {"place_origin": 2, "place_destination": 1}
        response = self.client.post("/routes/new/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_routes_new_route_view_bad(self):
        data = {"place_origin": 2}
        response = self.client.post("/routes/new/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routes_detail_route_view_get(self):
        response = self.client.get("/routes/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_detail_route_view_get_bad(self):
        response = self.client.get("/routes/3/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_routes_detail_route_view_put(self):
        data = {"place_origin": 1, "place_destination": 3}
        response = self.client.put("/routes/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_detail_route_view_put_bad(self):
        data = {"place_origin": 1, "place_destination": 1}
        response = self.client.put("/routes/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routes_detail_route_view_delete(self):
        response = self.client.delete("/routes/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
