from django.db import models
from django.conf import settings
from django.utils import timezone

class ChannelWhitelist(models.Model):
    #Channel Info
    channel_id = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=200)
    channel_url = models.URLField(max_length=100, blank=True)
     
    #Visual Info
    thumbnail_url = models.URLField(blank=True)
    
    #Channel Metadata
    subscriber_count = models.IntegerField(blank=True, null=True)
    videos_count = models.IntegerField(blank=True, null=True)
    
    #User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='whitelisted_channels')
    
    #Status & Timestamps
    is_active = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Whitelisted_Channel'
        verbose_name_plural =  'Whitelisted_Channels'
        unique_together = ['user', 'channel_id']
        indexes= [
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='whitelist_profile')
    
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
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def updatedTotalChannelsAdded(self):
        self.total_channels_added = self.user.whitelisted_channels.filter(is_active=True).count()
        self.save(update_fields=['total_channels_added'])
    
class ChannelCategory(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channel_category')
    channels = models.ManyToManyField(ChannelWhitelist, related_name='categories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Channel Category'
        verbose_name_plural = 'Channel Categories'
        unique_together = ['name', 'user']
        ordering = ['name']
        
    def __str__(self):
        return f'{self.name} - {self.user.username}'
    
    def TotalChannels(self):
        return self.channels.filter(is_active=True).count()

class SyncLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='synclogs')
    
    sync_type = models.CharField(
        max_length=50, 
        choices=[
            ('full', 'Fully Sync'),
            ('partial', 'Partially Sync'),
            ('pull_extension', 'Pull Extension'),
            ('push_extentsion', 'Push Extension'),
            ('api_update', 'Api Update')
        ])
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('pending', 'Pending'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    channels_synced = models.IntegerField(default=0)
    channels_added = models.IntegerField(default=0)
    channels_deleted = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Sync Log'
        verbose_name_plural =  'Sync Logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['status'])
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.sync_type} - {self.status}'