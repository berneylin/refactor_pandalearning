import time
import requests
import re
import random
from . import mydriver
from . import user
from . import score


def user_helper(username):
    driver_login = mydriver.Mydriver(nohead=False)
    cookies = driver_login.login()
    a_log = user.get_a_log(username)
    v_log = user.get_v_log(username)
    return cookies, a_log, v_log


def score_helper(cookies):
    total, each = score.get_score(cookies)
    print("当前学习总积分：" + str(total))
    print("阅读文章:{}/6,观看视频:{}/6,登陆:{}/1,文章时长:{}/6,视频时长:{}/6".format(*each))
    return total, each


def get_article_links():
    try:
        t_str = int(time.time()/60)
        s_str = "https://www.xuexi.cn/lgdata/u1ght1omn2.json?_st="
        url = s_str + str(t_str)
        a_str = requests.get(url)
        str_list = a_str.json()
        links = []
        for i in str_list:
            links.append(i['url'])
        return links
    except Exception:
        print("=" * 120)
        print("get_article_links获取失败")
        print("=" * 120)
        raise


def get_video_links():
    try:
        video = requests.get("https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js").content.decode("utf8")
        pattern = r'https://www.xuexi.cn/[^,"]*html'
        link = re.findall(pattern, video, re.I)
        link.reverse()
        return link
    except Exception:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise


def article(cookies, a_log, each, username):
    if each[0] < 6 or each[3] < 8:
        driver_article = mydriver.Mydriver(nohead=True)
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = get_article_links()
        try_count = 0
        while True:
            if each[0] < 6 and try_count < 10:
                a_num = 6 - each[0]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(120):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, 120 - j), end="")
                        time.sleep(1)
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = score_helper(cookies)
                    if each[0] >= 6:
                        print("检测到文章数量分数已满,退出学习")
                        break
                a_log += a_num
            else:
                with open("./user/{}/a_log".format(username), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                break
        try_count = 0
        while True:
            if each[3] < 6 and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log-1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each[3]) * 4 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (120) == 0 and i != remaining:
                        total, each = score_helper(cookies)
                        if each[3] >= 6:
                            print("检测到文章时长分数已满,退出学习")
                            break
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = score_helper(cookies)
            else:
                break
        if try_count < 10:
            print("文章学习完成")
        else:
            print("文章学习出现异常，请检查用户名下a_log文件记录数")
        driver_article.quit()
    else:
        print("文章之前学完了")


def video(cookies, v_log, each, username):
    if each[1] < 6 or each[4] < 10:
        driver_video = mydriver.Mydriver(nohead=True)
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = get_video_links()
        try_count = 0
        while True:
            if each[1] < 6 and try_count < 10:
                v_num = 6 - each[1]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(180):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, 180 - j), end="")
                        time.sleep(1)
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = score_helper(cookies)
                    if each[1] >= 6:
                        print("检测到视频数量分数已满,退出学习")
                        break
                v_log += v_num
            else:
                with open("./user/{}/v_log".format(username), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                break
        try_count = 0
        while True:
            if each[4] < 6 and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log-1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each[4]) * 3 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % 180 == 0 and i != remaining:
                        total, each = score_helper(cookies)
                        if each[4] >= 6:
                            print("检测到视频时长分数已满,退出学习")
                            break
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = score_helper(cookies)
            else:
                break
        if try_count < 10:
            print("视频学习完成")
        else:
            print("视频学习出现异常，请检查用户名下v_log文件记录数")
        driver_video.quit()
    else:
        print("视频之前学完了")
