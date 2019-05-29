import time
from os import unlink


def detection_worker(queue=None):
    print('start worker')
    import django
    django.setup()
    from django.core.mail import mail_admins
    from bills.models import Detection

    def delete_file_wait(file):
        tries = 0
        while True:
            try:
                unlink(file)
                return
            except PermissionError:
                if tries > 60:
                    print("Giving up")
                    return
                time.sleep(1)
                tries += 1

    def save_created_sync(front_url, back_url, detection_response, elapsed):
        print("perform save to db")
        instance = Detection()
        with open(front_url, "rb") as front_fp:
            with open(back_url, "rb") as back_fp:
                instance.time = int(round(elapsed * 1000))
                instance.front.save("front.jpg", front_fp)
                instance.back.save("back.jpg", back_fp)
                instance.result = detection_response
                print("save to db")
                instance.save()
        print("really deleting file")
        delete_file_wait(front_url)
        delete_file_wait(back_url)
        print("really deleting file done")

    while True:
        (front_url, back_url, detection_response, elapsed) = queue.get()
        try:
            save_created_sync(front_url, back_url, detection_response, elapsed)
        except:
            import traceback
            details = traceback.format_exc()
            print("error in worker", details)
            mail_admins('Background process exception', details)
        finally:
            queue.task_done()  # so we can join at exit




