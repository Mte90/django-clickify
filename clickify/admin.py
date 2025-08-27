from django.contrib import admin
from .models import DownloadClick


@admin.register(DownloadClick)
class DownloadClickAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'ip_address', 'country', 'city', 'timestamp')
    search_fields = ('file_name', 'ip_address', 'country', 'city')
    list_filter = ('country', 'timestamp')
    readonly_fields = ('file_name', 'ip_address',
                       'user_agent', 'timestamp', 'country', 'city')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False
