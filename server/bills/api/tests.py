import tempfile

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class DetectionTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        # Set the mode to binary and read so it can be decoded as binary
        with open('test_set\\788\\fr 788.jpg', 'rb') as fp_front:
            with open('test_set\\788\\fr 788 d.jpg', 'rb') as fp_back:
                response = self.client.post("/api/detection/", {'front': fp_front, 'back': fp_back}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "Detection failed")
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')