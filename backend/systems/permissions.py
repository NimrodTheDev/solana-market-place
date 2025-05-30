from rest_framework.permissions import BasePermission
from dotenv import load_dotenv
import os
import logging
load_dotenv()
logger = logging.getLogger(__name__)
class IsCronjobRequest(BasePermission):
    def has_permission(self, request, view):
        cron_key_env = os.getenv('CRON_KEY')
        cron_key_req = request.META.get("HTTP_X_CRON_SECRET")
        logger.info(f"Env CRON_KEY: {repr(cron_key_env)}")
        logger.info(f"Request CRON_SECRET: {repr(cron_key_req)}")
        is_match = cron_key_req == cron_key_env
        logger.info(f"Permission check result: {is_match}")
        return is_match

