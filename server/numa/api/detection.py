from rest_framework import serializers, viewsets

from bills.models import Detection


class DetectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'


class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    # def create(self, request):
    #     print("CREATING")
    #     pass
