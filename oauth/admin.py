from django.contrib import admin

# Register your models here.
from oauth.models import OauthUserProfile

class OauthUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'access_token', 'refresh_token', 'expires_timestamp')


admin.site.register(OauthUserProfile, OauthUserAdmin)