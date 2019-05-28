from pathlib import Path
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
import time

# from bills.algo.detect_flow import DetectFlowImageSearch
from bills.algo.poc_detector import POCDetector
from bills.models import Detection, Bill


class DetectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'


detector = None


def load_detector():
    global detector
    print("loading detector")
    detector = POCDetector()
    # get all bills
    # preprocess the library
    bills = Bill.objects.all()
    for bill in bills:
        front = bill.read_front_image()
        if front is None:
            print("ERROR: bill front image is empty " + str(bill.id))
            continue
        back = bill.read_back_image()
        detector.add_bill_to_library(bill.id, front, back, bill)


class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def create(self, request):
        for value in request.FILES.values():
            if Path(value.name).suffix[1:] == "":
                value.name = value.name + ".jpg"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        front = instance.read_front_image()
        back = instance.read_back_image()
        if detector is None:
            load_detector()
        start = time.time()
        detection_response = detector.predict(front, back)
        elapsed = time.time() - start
        instance.time = int(round(elapsed * 1000))
        instance.result = detection_response
        instance.save()
        first_detection = detection_response[0]
        first_detection_id = first_detection[0]
        if first_detection[1] < 0.7 or first_detection_id == 0:
            return Response("Detection failed", status=status.HTTP_201_CREATED, headers={'Content-Type': 'text/plain'})
        else:
            bill = Bill.objects.get(id=first_detection_id)
            return Response(bill.name, status=status.HTTP_201_CREATED, headers={'Content-Type': 'text/plain'})
