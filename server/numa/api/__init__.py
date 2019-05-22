from rest_framework import routers

# Serializers define the API representation.
from numa.api.detection import DetectionViewSet




# Routers provide an easy way of automatically determining the URL conf.
ApiRouter = routers.DefaultRouter()
ApiRouter.register(r'detection', DetectionViewSet)
