from multiprocessing import Queue
import cv2
import numpy as np
from datetime import datetime
from filter import Frame
from processing import BnWFilter, ResizeFilter, SaveFilter
from PIL import Image

file = Image.open('img.jpg')

sink_pipe = Queue()

save = SaveFilter(outputs=[])
bnw = BnWFilter(outputs=[save.input, sink_pipe])
resize = ResizeFilter(outputs=[bnw.input])

source_pipe = resize.input

def run_source():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)
        cv2.imshow("input", frame)
        image = Image.fromarray(frame)

        source_pipe.put(Frame(image=image, created_at=datetime.now()))

        frame = sink_pipe.get()
        open_cv_image = np.float32(np.array(frame.image))
        # Convert RGB to BGR
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
        cv2.imshow("output", open_cv_image)

        # press escape to exit
        if (cv2.waitKey(33) == ord('f')):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    filters = [save, bnw, resize]
    for filter in filters:
        filter.start()

    run_source()

    for filter in filters:
        filter.join()

