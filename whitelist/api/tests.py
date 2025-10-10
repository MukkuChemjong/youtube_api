from django.test import TestCase
from django.contrib.auth.models import User
from .models import ChannelWhitelist
from django.db import IntegrityError

class ChannelWhitelistTest(TestCase):
    
    # test the step up
    def setUp(self):
        
        self.user = User.objects.create_user(
            username= 'testname',
            email = 'test@gmail.com',
            password = 'testpassword',
        )
        
        self.channel = ChannelWhitelist.objects.create(
            channel_id = 'idtest',
            channel_name = 'channeltestname',
            channel_url = 'https://testchannel.com/test',
            thumbnail_url = 'https://testimages/thumnail.jpg',
            subscriber_count = 100,
            videos_count = 100,
            user = self.user,
            is_active = True,
        )
        
    def test_channel_creation(self):
        self.assertEqual(self.channel.channel_id, 'idtest')
        self.assertEqual(self.channel.channel_name, 'channeltestname')
        self.assertTrue(self.channel.is_active)
        self.assertEqual(self.channel.user, self.user)
        self.assertIsNotNone(self.channel.date_added)
        
    def test_channel_str_method(self):
        expected = f'{self.channel.channel_name} : {self.user.username}'
        self.assertEqual(str(self.channel), expected)
    
    def test_same_channel_id(self):
    
        with self.assertRaises(IntegrityError):
            ChannelWhitelist.objects.create(
                channel_id='idtest',  # Same channel
                channel_name='Duplicate Channel',
                thumbnail_url='https://example.com/thumb2.jpg',
                user=self.user  # Same user
            )
    
        
        