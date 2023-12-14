import re
import json
from django.conf import settings
from django.urls import reverse

from .models import ViewTrack
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class UserTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return None
    
    def process_response(self, request, response):
        if self.should_log_view_track(request,response):
            self.log_view_track(request,response)
        return response
    
    def should_log_view_track(self, request, response):
        if not getattr(settings, "DJANGO_VIEW_TRACKING_ENABLED", True):
            return False

        allow_anonymous = getattr(settings, "DJANGO_VIEW_TRACKING_ANONYMOUS_USER", True)

        blacklist = getattr(
            settings,
            "DJANGO_VIEW_TRACKING_BLACKLIST",
            [
                reverse("admin:index"),
            ],
        )

        if allow_anonymous or not request.user.is_anonymous:
            if blacklist and re.match(
                rf"({'|'.join([re.escape(_prefix) for _prefix in blacklist])})",
                request.path,
            ):
                return False

            return True

        return False
    
    def log_view_track(self, request, response):
        # 请求IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]  # 如果有代理，获取真实IP
        else:
            ip = request.META.get("REMOTE_ADDR")

        ViewTrack.objects.create(
            user=None if request.user.is_anonymous else request.user,
            ip=ip,
            request_method=request.method,
            request_url=request.get_full_path(),
            response_status_code=response.status_code,
        )

