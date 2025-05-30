from rest_framework.permissions import BasePermission
from dotenv import load_dotenv
import os
import logging
load_dotenv()
logger = logging.getLogger(__name__)
class IsCronjobRequest(BasePermission):
    def has_permission(self, request, view):
        logger.info(str(request.META.get("HTTP_X_CRON_SECRET") == os.getenv('CRON_KEY'))+ ": "+ os.getenv('CRON_KEY')+" "+ str(request.META))
        print(request.META.get("HTTP_X_CRON_SECRET") == os.getenv('CRON_KEY'), os.getenv('CRON_KEY')[:3]+"...", request.META)
        return request.META.get("HTTP_X_CRON_SECRET") == os.getenv('CRON_KEY')
