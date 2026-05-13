from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin


PROTECTED_PREFIXES = (
    '/dashboard/',
    '/accounts/profile',
)


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Require login for /dashboard/* and /accounts/profile*.
    All other paths are fully public (including blog, pages, etc.)
    so external crawlers like facebookexternalhit can access them.
    """
    def process_request(self, request):
        if any(request.path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)


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
