from django.db import models
from django.conf import settings
from django.utils import timezone

class ChannelWhitelist(models.Model):
    #Channel Info
    channel_id = models.CharField(max_length=100, unique=True)
    channel_name = models.CharField(max_length=200)
    channel_url = models.URLField(max_length=100, blank=True)
    
    #Visual Info
    thumbnail_url = models.URLField()
    
    #Channel Metadata
    subscriber_count = models.IntegerField(blank=True, null=True)
    videos_count = models.CharField(blank=True, null=True)
    
    #User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='whitelisted_channels')
    
    #Status & Timestamps
    is_active = models.BooleanField(default=False)
    last_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    checked_api = models.DateTimeField(blank=True, null=True, help_text='Last time channel was check with youtbe API')
    
    class Meta:
        ordering = ['-date_added']
        verbose_name = ['Whitelisted_Channel']
        verbose_name_plural =  ['Whitelisted_Channels']
        unique_together = ['user', 'channel_id']
        indexex = [
            models.Index(fields=['channel_id']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['date_added'])
        ]
    
    def __str__(self):
        return f'{self.channel_name} : {self.user.username}'
    
    def mark_checked(self):
        self.last_updated = timezone.now()
        self.save(update_fields=['last_updated'])