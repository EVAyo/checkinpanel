# -*- coding: utf-8 -*-
"""
cron: 23 14 * * *
new Env('芒果 TV');
"""

import json, os, requests, time
from urllib import parse
from utils import get_data
from notify_mtr import send 


class MgtvCheckIn:
    def __init__(self, mgtv_params_list):
        self.mgtv_params_list = mgtv_params_list

    @staticmethod
    def sign(params):
        url = "https://credits.bz.mgtv.com/user/creditsTake"
        user_params = {
            "abroad": params.get("abroad"),
            "ageMode": "0",
            "appVersion": params.get("appVersion"),
            "artistId": params.get("uuid"),
            "device": params.get("device"),
            "did": params.get("did"),
            "mac": params.get("did"),
            "osType": params.get("osType"),
            "src": "mgtv",
            "testversion": "",
            "ticket": params.get("ticket"),
            "uuid": params.get("uuid"),
        }
        try:
            user_info = requests.get(url="https://homepage.bz.mgtv.com/v2/user/userInfo", params=user_params).json()
            username = user_info.get("data", {}).get("nickName")
        except Exception as e:
            print("获取用户信息失败", e)
            username = params.get("uuid")
        res = requests.get(url=url, params=params)
        res_json = json.loads(res.text.replace(f"{params.get('callback')}(", "").replace(");", ""))
        if res_json["code"] == 200:
            cur_day = res_json["data"]["curDay"]
            _credits = res_json["data"]["credits"]
            msg = f"帐号信息: {username}\n签到积分: +{_credits}积分\n已经签到: {cur_day}天/21天"
        else:
            msg = f"帐号信息: {username}\n签到状态: 已完成签到 or 签到失败"
        return msg

    def main(self):
        msg_all = ""
        for mgtv_cookie in self.mgtv_params_list:
            mgtv_params = mgtv_cookie.get("mgtv_params")
            params = parse.parse_qs(mgtv_params)
            params["timestamp"] = [round(time.time())]
            params = {key: value[0] for key, value in params.items()}
            msg = self.sign(params=params)
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _mgtv_params_list = data.get("MGTV_PARAMS_LIST", [])
    res = MgtvCheckIn(mgtv_params_list=_mgtv_params_list).main()
    print(res)
    send("芒果 TV", res)