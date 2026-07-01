from django.contrib import admin
from .models import APIRquestLog

class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "requested_at",
        "response_ms", 
        "status_code",
        "user",
        "view_method",
        "path", 
        "remote_address",
        "host",
        "query_params",
    )

admin.site.register(APIRquestLog, APIRequestLogAdmin)