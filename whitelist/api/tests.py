from django.test import TestCase
from django.contrib.auth.models import User
from .models import ChannelWhitelist
from django.db import IntegrityError, transaction
from django.utils import timezone
import time

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
        # test that the channel can be created created successfully
        self.assertEqual(self.channel.channel_id, 'idtest')
        self.assertEqual(self.channel.channel_name, 'channeltestname')
        self.assertTrue(self.channel.is_active)
        self.assertEqual(self.channel.user, self.user)
        self.assertIsNotNone(self.channel.date_added)
        
    def test_channel_str_method(self):
        # test the __str__ method returns the correct format
        expected = f'{self.channel.channel_name} : {self.user.username}'
        self.assertEqual(str(self.channel), expected)

    def test_same_channel_id(self):
        # test if duplicates can be created
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ChannelWhitelist.objects.create(
                    channel_id='idtest',
                    channel_name='Duplicate Channel',
                    thumbnail_url='https://example.com/thumb2.jpg',
                    user=self.user
                )
    
    def test_reverse_relationship(self):
        # test if we can accesss channels from user
        channels = self.user.whitelisted_channels.all()
        self.assertEqual(channels.count(), 1)
        self.assertEqual(channels.first(), self.channel)
    
    def test_multiple_channels(self):
        # test if multiple channels are created
        channel2 = ChannelWhitelist.objects.create(
            channel_id = 'idtest2',
            channel_name = 'channeltestname',
            channel_url = 'https://testchannel.com/test',
            thumbnail_url = 'https://testimages/thumnail.jpg',
            subscriber_count = 100,
            videos_count = 100,
            user = self.user,
            is_active = True,
        )
        
        self.assertEqual(self.user.whitelisted_channels.count(), 2)
        self.assertIn(self.channel, self.user.whitelisted_channels.all())
        self.assertIn(channel2, self.user.whitelisted_channels.all())
    
    def test_mark_checked(self):
        # test if mark_checked function works
        oldtime = self.channel.last_updated
        time.sleep(0.01)
        self.channel.mark_checked()
        self.channel.refresh_from_db()
        
        self.assertIsNotNone(self.channel.last_updated)
        self.assertNotEqual(self.channel.last_updated, oldtime)
        
    def test_Cascase_delete(self):
        # test if channels are deleted
        channel_id = self.channel.id
        self.user.delete()
        
        with self.assertRaises(ChannelWhitelist.DoesNotExist):
            ChannelWhitelist.objects.get(id=channel_id)
    
    def test_date_added(self):
        # test if channels are ordered by latest
        
        channel2 = ChannelWhitelist.objects.create(
            channel_id = 'idtest2',
            channel_name = 'channeltestname',
            channel_url = 'https://testchannel.com/test',
            thumbnail_url = 'https://testimages/thumnail.jpg',
            subscriber_count = 100,
            videos_count = 100,
            user = self.user,
            is_active = True,
        )
        
        channels = ChannelWhitelist.objects.all()
        self.assertEqual(channels[0], channel2)
        self.assertEqual(channels[1], self.channel)
        
    def test_blank_fields(self):
        # test optional fields if they are blank
        minimalChannel = ChannelWhitelist.objects.create(
            channel_id = 'minimalid',
            channel_name = 'minimalname',
            channel_url = 'https://minimalurl.com/test',
            user = self.user
        )
        
        self.assertIsNone(minimalChannel.subscriber_count)
        self.assertIsNone(minimalChannel.videos_count)
        self.assertEqual(minimalChannel.thumbnail_url, '')
        
    def test_filter_by_active(self):
        # test active and inactive channels
        inactiveChannel = ChannelWhitelist.objects.create(
            channel_id = 'minimalid',
            channel_name = 'minimalname',
            channel_url = 'https://minimalurl.com/test',
            user = self.user,
            is_active = False
        )
        
        inactiveChannels = self.user.whitelisted_channels.filter(is_active=False)
        activeChannels = self.user.whitelisted_channels.filter(is_active=True)
        
        self.assertEqual(activeChannels.count(), 1)
        self.assertEqual(inactiveChannels.count(), 1)
        self.assertIn(inactiveChannel, inactiveChannels)
        self.assertIn(self.channel, activeChannels)
        