from rest_framework.permissions import BasePermission
from dotenv import load_dotenv
import os
load_dotenv()
class IsCronjobRequest(BasePermission):
    def has_permission(self, request, view):
        cron_key_env = os.getenv('CRON_KEY')
        cron_key_req = request.META.get("HTTP_X_CRON_SECRET")
        return cron_key_req == cron_key_env
