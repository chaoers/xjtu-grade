import base64
import json
import requests


from config import config
from utils import get_timestamp, encrypt_passward


def ehall_login() -> requests.Session:
    """利用 request 库模拟登陆 ehall

    Returns:
        requests.Session: 得到一个登陆认证的 session
    """
    session = requests.session()
    session.cookies.set(
        'cur_appId_', 'GRt5IN2Ni3M=',
    )
    resp = session.get(
        'https://org.xjtu.edu.cn/openplatform/oauth/authorize',
        data={
            'appID': '1030',
            'redirectUri': 'http://ehall.xjtu.edu.cn/amp-auth-adapter/loginSuccess',
            'scope': 'user_info',
        })

    resp = session.get(
        'https://org.xjtu.edu.cn/openplatform/g/admin/getIsShowJcaptchaCode',
        data={
            'userName': config.net_id,
            '_': get_timestamp()
        }
    )

    data = json.loads(resp.text)
    captcha = ''
    if data['data']:
        resp = session.post(
            'https://org.xjtu.edu.cn/openplatform/g/admin/getJcaptchaCode',
            headers={
                'Content-Type': 'application/json;charset=UTF-8'
            }
        )
        data = json.loads(resp.text)
        img = base64.b64decode(data['data'])
        with open('captcha.png', 'wb') as file:
            file.write(img)
        print(' ..... done')

        captcha = input('Captcha:')

    resp = session.post(
        'https://org.xjtu.edu.cn/openplatform/g/admin/login',
        data=json.dumps({
            'username': config.net_id,
            'pwd': encrypt_passward(config.password),
            'loginType': 1,
            'jcaptchaCode': captcha
        }),
        headers={
            'Content-Type': 'application/json;charset=utf-8',
        }
    )

    data = json.loads(resp.text)
    if data['code'] != 0:
        return False

    session.cookies.set('open_Platform_User', str(data['data']['tokenKey']))
    session.cookies.set('memberId', str(data['data']['orgInfo']['memberId']))

    resp = session.get(
        'https://org.xjtu.edu.cn/openplatform/g/admin/getUserIdentity',
        params={
            'memberId': data['data']['orgInfo']['memberId'],
            '_': get_timestamp()
        }
    )
    data = json.loads(resp.text)

    resp = session.get(
        'https://org.xjtu.edu.cn/openplatform/oauth/auth/getRedirectUrl',
        params={
            'userType': data['data'][0]['userType'],
            'personNo': data['data'][0]['personNo'],
            '_': get_timestamp()
        }
    )
    data = json.loads(resp.text)

    if data['code'] != 0:
        return False

    response = session.get(data['data'])
    data = response.text

    return session
