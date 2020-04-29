from threading import Thread
from threading import Lock
from .func import video, article

threadLock = Lock()
threads = []


class MyThread(Thread):
    def __init__(self, name, func, *args, lock=False):
        Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.lock = lock

    def run(self):
        print("开启： " + self.name)
        if self.lock:
            threadLock.acquire()
            self.func(*self.args)
            threadLock.release()
        else:
            self.func(*self.args)


class ArticleThread(MyThread):
    def __init__(self, cookies, a_log, each, username):
        super(ArticleThread, self).__init__("文章学习", article, cookies, a_log, each, username)


class VideoThread(MyThread):
    def __init__(self, cookies, v_log, each, username):
        super(VideoThread, self).__init__("视频学习", video, cookies, v_log, each, username)
