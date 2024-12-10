from django.test import TestCase
from django.contrib.auth.models import User
from .models import OneTimeCode

class OneTimeCodeTest(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_and_verify_code(self):
        # Create a new one-time code
        test_code = "abcde12345"
        one_time_code = OneTimeCode.objects.create(
            code=test_code,
            user=self.test_user
        )

        # Check if code exists in database
        self.assertTrue(OneTimeCode.objects.filter(user=self.test_user).exists())
        
        # Verify that the code was hashed and can be verified
        retrieved_code = OneTimeCode.objects.get(user=self.test_user)
        self.assertTrue(retrieved_code.check_code(test_code))

    def tearDown(self):
        # Clean up test data
        self.test_user.delete()
        