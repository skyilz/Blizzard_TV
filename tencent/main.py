import json
import re
import time
import requests


def main():
        
    base_url = 'https://tv.blizzard.cn/action/activities/HDRewardReceive'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    # 填cookie
    cookie = {
        "cookie": "          "
    }
    # 填礼品id，默认为OW典藏包
    datas = {
        "itemCode": "OW_UPGRADE"
    }
    success = 0
    flag = 0
    for num in range(1, 500):  
        print(num)
        request = requests.post(base_url, headers=headers, data=datas, cookies=cookie)
        d = json.loads(request.content.decode('utf8'))
        if d['msg'] == 'login':
            text = '暴雪cookie失效了，登陆失败'
            flag = 1
        else:
            if d['msg'] == 'item_limit':
                text = 'OW典藏包领取失败'
                print(d)
            elif d['msg'] == 'success':
                text = 'OW典藏包领取成功'
                print(d)
                flag = 1
                success = 1
            elif d['msg'] == 'exist_record':
                text = '您已拥有该礼品，请勿重复领取'
                print(d)
                flag = 1
            else:
                text = '未知原因引起失败'
                print(d)
        print(text)
        if num == 499:
            flag = 1
            text = '本次尝试领取失败'
        if flag == 1:
            # qq推送
            QmsgKey = "          "
            if success == 1: 
                content = f"""{text}{d}"""
            else:
                content = f"""{text}"""
            data = {
                "msg": content
            }
            url_send = "https://qmsg.zendee.cn/send/%s" % (QmsgKey)
            try:
                res = requests.post(url_send, data=data)
                sucmsg = res.json()['success']
                if sucmsg == True:
                    print("qq推送服务成功")
                else:
                    print("qq推送服务失败")
            except:
                print("qq推送参数错误")
        if flag == 1:
            break
        else:
            time.sleep(3)

def main_handler(event, context):
    main()

if __name__ == '__main__':
    main()
