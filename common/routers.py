"""
 Custom routers for job sourcing .
"""
# third party imports
from rest_framework.routers import DefaultRouter, SimpleRouter


class OptionalSlashRouter(SimpleRouter):
    """
    optional slash router class
    """
    def __init__(self):
        """
            explicitly appending '/' in urls if '/' doesn't exists for making common url patterns .
        """
        super(OptionalSlashRouter, self).__init__()
        self.trailing_slash = '/?'
