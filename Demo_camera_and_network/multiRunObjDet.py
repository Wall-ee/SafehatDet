import time
import multiprocessing as mp
import cv2

def read_cam(imgQ,detQ):
    cap = cv2.VideoCapture(0)

    while True:
        frame = cap.read()[1]
        imgQ.put(frame)
        imgQ.get() if imgQ.qsize() > 1 else time.sleep(0.01)
    
        detQ.put(frame)
        detQ.get() if detQ.qsize() > 1 else time.sleep(0.01)

def show_img_from_queue(imgQ,window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = imgQ.get()
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

def det_safehat_from_queue(detQ,window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = detQ.get()
        cv2.imshow(window_name, frame)
        cv2.waitKey(0)

def run_single_camera():
    # user_name, user_pwd, camera_ip = "admin", "admin123456", "172.20.114.196"
    # user_name, user_pwd, camera_ip = "admin", "admin123456", "[fe80::3aaf:29ff:fed3:d260]"

    camera_name = 'cam1'
    det_camera_name = 'det_cam1'
    mp.set_start_method(method='spawn')  # init
    imageQueue = mp.Queue(maxsize=2)
    detObjQueue = mp.Queue(maxsize=2)
    processes = [mp.Process(target=image_put, args=(imageQueue,detObjQueue)),
                 mp.Process(target=image_get, args=(imageQueue,camera_name)),
                 mp.Process(target=image_get, args=(detObjQueue,det_camera_name))]

    [process.start() for process in processes]
    [process.join() for process in processes]


# def run_multi_camera():
#     user_name, user_pwd = "admin", "admin123456"
#     camera_ip_l = [
#         "172.20.114.196",  # ipv4
#         "[fe80::3aaf:29ff:fed3:d260]",  # ipv6
#     ]

#     mp.set_start_method(method='spawn')  # init
#     queues = [mp.Queue(maxsize=4) for _ in camera_ip_l]

#     processes = []
#     for queue, camera_ip in zip(queues, camera_ip_l):
#         processes.append(mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)))
#         processes.append(mp.Process(target=image_get, args=(queue, camera_ip)))

#     for process in processes:
#         process.daemon = True
#         process.start()
#     for process in processes:
#         process.join()


# def image_collect(queue_list, camera_ip_l):
#     import numpy as np

#     """show in single opencv-imshow window"""
#     window_name = "%s_and_so_no" % camera_ip_l[0]
#     cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
#     while True:
#         imgs = [q.get() for q in queue_list]
#         imgs = np.concatenate(imgs, axis=1)
#         cv2.imshow(window_name, imgs)
#         cv2.waitKey(1)

#     # """show in multiple opencv-imshow windows"""
#     # [cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
#     #  for window_name in camera_ip_l]
#     # while True:
#     #     for window_name, q in zip(camera_ip_l, queue_list):
#     #         cv2.imshow(window_name, q.get())
#     #         cv2.waitKey(1)


# def run_multi_camera_in_a_window():
#     user_name, user_pwd = "admin", "admin123456"
#     camera_ip_l = [
#         "172.20.114.196",  # ipv4
#         "[fe80::3aaf:29ff:fed3:d260]",  # ipv6
#     ]

#     mp.set_start_method(method='spawn')  # init
#     queues = [mp.Queue(maxsize=4) for _ in camera_ip_l]

#     processes = [mp.Process(target=image_collect, args=(queues, camera_ip_l))]
#     for queue, camera_ip in zip(queues, camera_ip_l):
#         processes.append(mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)))

#     for process in processes:
#         process.daemon = True  # setattr(process, 'deamon', True)
#         process.start()
#     for process in processes:
#         process.join()


def run():
    # run_opencv_camera()  # slow, with only 1 thread
    run_single_camera()  # quick, with 2 threads
    # run_multi_camera() # with 1 + n threads
    # run_multi_camera_in_a_window()  # with 1 + n threads
    pass


if __name__ == '__main__':
    run()
