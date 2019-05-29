import tempfile

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from bills.models import Bill
from bills.models.common import set_storage_test


class DetectionTests(APITestCase):
    def setUp(self):
        set_storage_test(True)
        with open('test_set\\catalog\\us1\\front.jpg', 'rb') as fp_front:
            with open('test_set\\catalog\\us1\\back.jpg', 'rb') as fp_back:
                bill = Bill()
                bill.name = bill.catalog = bill.image_id = "usd1"
                bill.front.save('image1.jpg', fp_front)
                bill.back.save('image2.jpg', fp_back)
                bill.save()
        with open('test_set\\catalog\\il50\\front.jpg', 'rb') as fp_front:
            with open('test_set\\catalog\\il50\\back.jpg', 'rb') as fp_back:
                bill = Bill()
                bill.name = bill.catalog = bill.image_id = "il50"
                bill.front.save('image1.jpg', fp_front)
                bill.back.save('image2.jpg', fp_back)
                bill.save()

    def tearDown(self):
        set_storage_test(False)

    def test_detection(self):
        """
        Ensure we can use the detection API
        """
        # Set the mode to binary and read so it can be decoded as binary
        with open('test_set\\us1\\1\\front.jpg', 'rb') as fp_front:
            with open('test_set\\us1\\1\\back.jpg', 'rb') as fp_back:
                response = self.client.post("/api/detection/", {'front': fp_front, 'back': fp_back}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "usd1")

