import atexit
from multiprocessing import Process, JoinableQueue
from pathlib import Path

from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
import time

# from bills.algo.detect_flow import DetectFlowImageSearch
from bills.algo.poc_detector import POCDetector
from bills import detection_worker
from bills.models import Detection, Bill
from bills.models.common import read_from_file_stream


class DetectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'


detector = _queue = _process = None
_stop = False

def load_detector():
    global detector, _queue, _process
    print("loading detector")
    detector = POCDetector()
    # get all bills
    # preprocess the library
    bills = Bill.objects.all()
    for bill in bills:
        front = bill.read_front_image()
        print(front)
        if front is None:
            print("ERROR: bill front image is empty " + str(bill.id))
            continue
        back = bill.read_back_image()
        detector.add_bill_to_library(bill.id, front, back, bill)

    # from django import db
    # db.connections.close_all()
    # _queue = JoinableQueue()
    # _process = Process(target= detection_worker.detection_worker, name='worker', kwargs={'queue':_queue})
    # atexit.register(_cleanup)
    # _process.start()

def _cleanup():
    global _queue
    if _queue is None:
        return
    print("empty worker queue")
    _queue.join()
    print("empty worker queue, Done")
    _queue = None

def prevent_file_close(upload_file):
    upload_file.file.unlink = lambda name: print("not really closing " + name)


class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer


    def save_created_deferred(self, validated_data, detection_response, elapsed):
        instance = Detection()
        instance.time = int(round(elapsed * 1000))
        instance.front.save("front.jpg", validated_data['front'].file)
        instance.back.save("back.jpg", validated_data['back'].file)
        instance.result = detection_response
        instance.save()
        # global _queue
        # prevent_file_close(validated_data["front"])
        # prevent_file_close(validated_data["back"])
        # _queue.put((validated_data["front"].file.name, validated_data["back"].file.name, detection_response, elapsed))

    def create(self, request):
        print("running detection")
        try:
            for value in request.FILES.values():
                if Path(value.name).suffix[1:] == "":
                    value.name = value.name + ".jpg"
            # do the validation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print("request valid")
            # do the detection
            validated_data = serializer.validated_data
            instance = Detection()
            instance.front.save("front.jpg", validated_data['front'].file)
            instance.back.save("back.jpg", validated_data['back'].file)
            instance.save()

            front = instance.read_front_image()#read_from_file_stream(validated_data['front'])
            back = instance.read_back_image()#read_from_file_stream(validated_data['back'])
            if detector is None:
                load_detector()
            start = time.time()
            try:
                print("detect")
                detection_response = detector.predict(front, back)
                elapsed = time.time() - start
                print("detect done in " + str(elapsed))
                print(detection_response)
                #self.save_created_deferred(validated_data, detection_response, elapsed)
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
            except Exception as detectionE:
                elapsed = time.time() - start
                print(detectionE)
                self.save_created_deferred(validated_data, {'error': str(detectionE)}, elapsed)
                return Response("Detection internal error", status=status.HTTP_201_CREATED,
                                headers={'Content-Type': 'text/plain'})
        except Exception as e:
            print(e)
            return Response("Backend internal error", status=status.HTTP_201_CREATED, headers={'Content-Type': 'text/plain'})
