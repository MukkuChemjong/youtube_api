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
        
class UserProfile(models.Model):
    #User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='whitelisted_channels')
    
    #Extension Settings
    strict_mode = models.BooleanField(default=False, help_text='If true hide all whiteslited channels, if false highlight them')
    auto_sync = models.BooleanField(default=True, help_text='Automatically sync whitelist with browser')
    
    #Prefrences
    default = models.CharField(
        max_length=50,
        choices=[
            ('grid', 'Grid'),
            ('list', 'List'),
        ],
        default='grid',
    )
    
    theme = models.CharField(
        max_length=50,
        choices=[
            ('auto', 'Auto'),
            ('black', 'Black'),
            ('white', 'White')
        ],
        default='auto'
    )
    
    #Statistics
    total_channels_added = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ['User Profile']
        verbose_name_plural = ['User Profiles']
    
    def updatedTotalChannelsAdded(self):
        self.total_channels_added = self.user.whitelisted_channels.filter(is_active==True).count()
        self.save(update_fields=['total_channels_added'])
    
    