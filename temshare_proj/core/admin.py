from django.contrib import admin
from .models import FileShare, URLShare


@admin.register(FileShare)
class FileShareAdmin(admin.ModelAdmin):
    list_display = ('token', 'file', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('token',)
    readonly_fields = ('token', 'created_at')
    ordering = ('-created_at',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired?'


@admin.register(URLShare)
class URLShareAdmin(admin.ModelAdmin):
    list_display = ('token', 'original_url', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('token', 'original_url')
    readonly_fields = ('token', 'created_at')
    ordering = ('-created_at',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired?'
