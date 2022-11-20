import os
from tempfile import TemporaryFile
from unittest.mock import Mock

import cloudinary.uploader
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .helpers import create_test_user


class LoginViewSetTests(TestCase):
    def setUp(self) -> None:
        self.web_client = Client()
        self.user = create_test_user(username="usernameabc", password="testpassword")
        return super().setUp()

    def test_login_success(self) -> None:
        response = self.web_client.post(
            path="/api/v1/token/login",
            data={"username": self.user.username, "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("auth_token" in response.json())

    def test_login_only_post(self) -> None:
        response = self.web_client.get("/api/v1/token/login")
        self.assertEqual(response.status_code, 405)


class RegistrationViewSetTests(TestCase):
    def setUp(self) -> None:
        self.web_client = Client()
        self.user = create_test_user("usernameabc", "testpassword")
        return super().setUp()

    def test_register_new_user(self):
        response = self.web_client.post(
            path="/api/v1/users/",
            data={"username": "newguy", "password": "testpassword"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_fails_if_user_exists(self) -> None:
        response = self.web_client.post(
            "/api/v1/users/",
            {
                "username": self.user.username,
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)


class TestUploadImage(TestCase):
    def setUp(self) -> None:
        self.user = create_test_user(username="username", password="password")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.web_client = Client(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_upload_image_to_cloudinary_succeeds(self):

        cloudinary_mock_response = {
            "public_id": "public-id",
            "secure_url": "http://hello.com/here",
        }
        cloudinary.uploader.upload = Mock(
            side_effect=lambda *args: cloudinary_mock_response
        )

        with TemporaryFile() as temp_image_obj:
            for line in open(os.path.dirname(__file__) + "/mock-image.png", "rb"):
                temp_image_obj.write(line)

            response = self.web_client.post(
                "/api/v1/upload-image",
                {"picture": temp_image_obj},
                format="multipart",
            )

            response_data = response.data

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["status"], "success")
            self.assertEqual(response_data["data"], cloudinary_mock_response)
            # self.assertEqual(cloudinary.uploader.upload.called)
