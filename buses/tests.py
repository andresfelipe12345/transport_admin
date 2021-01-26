from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Bus
from .serializers import BusSerializer


class BusesViewTestCases(APITestCase):

    def setUp(self):
        bus = Bus(seats=10, operative=True)
        bus.save()
        self.bus = bus

    def test_buses_list_view(self):
        response = self.client.get("/buses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buses_new_bus_view(self):
        data = {"seats": 9, "operative": True}
        response = self.client.post("/buses/new/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_buses_detail_bus_view_get(self):
        response = self.client.get("/buses/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buses_detail_bus_view_get_404(self):
        response = self.client.get("/buses/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_buses_detail_bus_view_put(self):
        data = {"seats": 2}
        response = self.client.put("/buses/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buses_detail_bus_view_put_bad(self):
        data = "data"
        response = self.client.put("/buses/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buses_detail_bus_view_delete(self):
        response = self.client.delete("/buses/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
