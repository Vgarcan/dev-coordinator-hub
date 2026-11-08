from django.contrib import admin

from .models import Repository

# Register your models here.


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    """Manage passive inventory records using Django's standard admin."""

    list_display = ('full_name', 'tracking_status', 'updated_at')
    list_filter = ('tracking_status',)
    search_fields = ('full_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
