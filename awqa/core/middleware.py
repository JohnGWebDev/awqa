from django.urls import resolve
from django.conf import settings

class HtmxResponseMiddleware(object):
    def __init__(self, get_response):
        """This method requires a get_response argument."""
        self.get_response = get_response

    def __call__(self, request):
        """This method is called every time a request is made."""
        return self.get_response(request)

    def process_template_response(self, request, response):
        """Middleware hook called after a view executes."""
        app_name = resolve(request.path).app_name
        if (app_name in settings.HTMX_APPS or app_name == '') and not response.headers.get("HX-Retarget"):
            response.template_name = f"{response.template_name[0]}{'#page-partial' if request.htmx else ''}"
        print(response.template_name)
        return response