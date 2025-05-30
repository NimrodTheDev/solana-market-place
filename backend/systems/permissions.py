from rest_framework.permissions import BasePermission
from dotenv import load_dotenv
import os
load_dotenv()

class IsCronjobRequest(BasePermission):
    def has_permission(self, request, view):
        print(request.META.get("HTTP_X_CRON_SECRET") == os.getenv('CRON_KEY'), os.getenv('CRON_KEY')[3:]+"...")
        return request.META.get("HTTP_X_CRON_SECRET") == os.getenv('CRON_KEY')
