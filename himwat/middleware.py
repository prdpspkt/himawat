from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class DisableBrowserCachingMiddleware(MiddlewareMixin):
    """
    Middleware to disable browser caching in development.
    Adds cache-control headers to prevent browser caching.
    Only active when DEBUG=True.
    """
    def process_response(self, request, response):
        # Only disable caching in DEBUG mode
        if settings.DEBUG:
            if 'Cache-Control' not in response:
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            if 'Pragma' not in response:
                response['Pragma'] = 'no-cache'
            if 'Expires' not in response:
                response['Expires'] = '0'
        return response
