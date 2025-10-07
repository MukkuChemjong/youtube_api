from django.db import models

class ChannelWhitelist(models.Model):
    #Channel Info
    channel_id = models.CharField(max_length=100, unique=True)
    channel_name = models.CharField(max_length=200)
    channel_url = models.URLField()
    
    #Visual Info
    thumbnail_url = models.URLField()
    
    #Channel Metadata
    subscriber_count = models.CharField(max_length=200)
    videos_count = models.CharField(max_length=200)
    
    #User
    
    #Status & Timestamps
    is_active = models.BooleanField(default=False)
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()
    checked_api = models.DateTimeField()