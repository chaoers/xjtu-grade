import sys
import json
from typing import List

from auth.ehall_login import ehall_login
from utils import get_timestamp

session = ehall_login()


def get_grade(num=999) -> List[dict]:
    """获得学生对应的所有学科成绩分析数据

    Args:
        num (int, optional): 最大课程数目. 默认 999.

    Returns:
        dict: 原始学科成绩数据格式
    """
    session.get('http://ehall.xjtu.edu.cn/new/index.html?browser=no')
    session.get(
        'http://ehall.xjtu.edu.cn/portal/html/select_role.html',
        params={
            'appId': 4768574631264620,
        },
    )
    resp = session.get(
        'http://ehall.xjtu.edu.cn/appMultiGroupEntranceList',
        params={
            'r_t': get_timestamp(),
            'appId': 4768574631264620,
            'param': ''
        },
    )
    data = resp.json()
    target_url = ''
    for group in data['data']['groupList']:
        if group['groupName'] == '移动应用学生':
            target_url = group['targetUrl']
    session.get(target_url)
    resp = session.post(
        'http://ehall.xjtu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do',
        data={
            'querySetting': [
                {"name": "SFYX", "caption": "是否有效", "linkOpt": "AND", "builderList": "cbl_m_List",
                    "builder": "m_value_equal", "value": "1", "value_display": "是"},
                {"name": "XNXQDM", "value": "2019-2020-2",
                    "builder": "notEqual", "linkOpt": "and"}
            ],
            'pageSize': num,
            'pageNumber': 1,
        }
    )
    grade = resp.json()['datas']['xscjcx']['rows']
    return grade


def get_subject_rank(subject: dict):
    """这里是成绩分析页面点开单科成绩后的请求，还未做处理，可以进一步分析数据

    Args:
        subject (dict): 查询成绩时得到的一个科目对应的字典
    """
    # 成绩分布
    class_distribution_anl = 'http://ehall.xjtu.edu.cn/jwapp/sys/cjcx/modules/cjcx/jxbcjfbcx.do'
    req = session.get(
        class_distribution_anl,
        data={
            subject['JXBID'],  # 教学班 ID
            subject['XNXQDM'],  # 学年学期代码
            subject['TJLX'],
        })
    # 成绩统计
    class_grade_anl = 'http://ehall.xjtu.edu.cn/jwapp/sys/cjcx/modules/cjcx/jxbcjtjcx.do'
    req = session.get(
        class_grade_anl,
        data={
            subject['JXBID'],  # 教学班 ID
            subject['XNXQDM'],  # 学年学期代码
            subject['TJLX'],
        })
    # 学生排名
    stu_rank = 'http://ehall.xjtu.edu.cn/jwapp/sys/cjcx/modules/cjcx/jxbxspmcx.do'
    req = session.get(
        stu_rank,
        data={
            subject['JXBID'],  # 教学班 ID
            subject['XNXQDM'],  # 学年学期代码
            subject['TJLX'],
            subject['XH'],  # 学号
        }
    )
    # todo analyse data above


def parse_grade() -> List[dict]:
    """分析原始成绩

    Returns:
        List[dict]: 对单个科目的数据进行分析，并转换成人类友好的键值
    """
    grade_list = get_grade()
    grades = [{
        '学期学年': {
            'display': subject['XNXQDM_DISPLAY'],
            'id': subject['XNXQDM'],
        },
        '课程名': subject['KCM'],
        '课程号': subject['KCH'],
        '课序号': subject['KXH'],
        '课程类别': {
            'id': subject['KCLBDM'],
            'display': subject['KCLBDM_DISPLAY'],
        },
        '课程性质': subject['DJCJLXDM_DISPLAY'],
        '学分': subject['XF'],
        '学时': subject['XS'],
        '修读方式': {
            'id': subject['XDFSDM'],
            'display': subject['XDFSDM_DISPLAY'],
        },
        '修读类型': {
            'id': subject['SFZX'],
            'display': subject['SFZX_DISPLAY'],
        },
        '总成绩': subject['ZCJ'],
        '考试日期': subject['KSSJ'],
        '绩点': subject['XFJD'],
        '重修重考': {
            'id': subject['CXCKDM'],
            'display': subject['CXCKDM_DISPLAY'],
        },
        '等级成绩类型': {
            'id': subject['DJCJLXDM'],
            'display': subject['DJCJLXDM_DISPLAY'],
        },
        '考试类型': {
            'id': subject['KSLXDM'],
            'display': subject['KSLXDM_DISPLAY'],
        },
        '开课单位': {
            'id': subject['KKDWDM'],
            'display': subject['KKDWDM_DISPLAY'],
        },
        '是否及格': {
            'id': subject['SFJG'],
            'display': subject['SFJG_DISPLAY'],
        },
        '是否有效': {
            'id': subject['SFYX'],
            'display': subject['SFYX_DISPLAY'],
        },
        # '特殊原因': subject[''],
    } for subject in grade_list]

    return grades
