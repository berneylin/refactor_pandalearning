#!/usr/bin/env python3
# encoding: utf-8

import time
from utils import user
from utils import func
from utils import threads


def main():
    start_time = time.time()
    username = user.get_user()
    cookies, a_log, v_log = func.user_helper(username)
    total, each = func.score_helper(cookies)
    article_thread = threads.ArticleThread(cookies, a_log, each, username)
    video_thread = threads.VideoThread(cookies, v_log, each, username)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()
    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")


if __name__ == "__main__":
    main()
