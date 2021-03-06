# seer.tools.init_channels
# -*- coding: utf-8 -*-


from seer.extensions import db
from seer.models.channel import Channel
from seer.models.external import External
from seer.models.candidate import (Candidate, K_CANDIDATE_KANDIANSHI,
        K_CANDIDATE_TVMAO, CANDIDATE_NAMES)

CHANNEL_DATA = {
        1: ('CCTV-1 综合', 8),
        2: ('CCTV-2 财经', 8),
        3: ('CCTV-3 综艺', 8),
        4: ('CCTV-4 中文国际(亚)', 1),
        7: ('CCTV-5 体育', 8),
        8: ('CCTV-6 电影', 10),
        9: ('CCTV-7 军事·农业', 1),
        10: ('CCTV-8 电视剧', 1),
        11: ('CCTV-纪录', 8),
        13: ('CCTV-10 科教', 1),
        14: ('CCTV-11 戏曲', 1),
        15: ('CCTV-12 社会与法', 1),
        16: ('CCTV-13 新闻', 1),
        17: ('CCTV-14 少儿', 1),
        18: ('CCTV-15 音乐', 1),
        19: ('CCTV-NEWS', 1),
        25: ('北京卫视', 4),
        26: ('东方卫视', 4),
        27: ('黑龙江卫视', 4),
        28: ('江苏卫视', 4),
        31: ('四川卫视', 4),
        35: ('重庆卫视', 4),
        37: ('BTV影视', 7),
        38: ('广东卫视', 4),
        41: ('湖北卫视', 4),
        42: ('湖南卫视', 4),
        44: ('辽宁卫视', 4),
        45: ('陕西卫视', 4),
        47: ('云南卫视', 4),
        48: ('浙江卫视', 4),
        49: ('安徽卫视', 4),
        53: ('甘肃卫视', 4),
        55: ('吉林卫视', 4),
        57: ('贵州卫视', 4),
        59: ('青海卫视', 4),
        60: ('宁夏卫视', 4),
        61: ('新疆卫视', 4),
        66: ('兵团卫视', 4),
        75: ('CCTV风云足球', 1),
        76: ('CCTV风云音乐', 1),
        77: ('CCTV第一剧场', 1),
        78: ('CCTV风云剧场', 1),
        79: ('CCTV世界地理', 1),
        #80: ('CCTV电视指南', 1),
        81: ('CCTV怀旧剧场', 1),
        82: ('CCTV国防军事', 1),
        #83: ('CCTV女性时尚', 1),
        84: ('CCTV娱乐', 1),
        85: ('CCTV戏曲', 1),
        86: ('CCTV电影', 1),
        #87: ('CCTV高尔夫网球', 1),
        #88: ('CCTV央视文化精品', 1),
        #89: ('彩民在线', 1),
        #90: ('法律服务', 1),
        #91: ('高尔夫', 1),
        #92: ('靓妆', 1),
        #93: ('梨园', 1),
        #94: ('汽摩', 1),
        #95: ('老年福', 1),
        #96: ('留学世界', 1),
        #97: ('青年学苑', 1),
        #98: ('摄影', 1),
        #99: ('天元围棋', 1),
        100: ('先锋纪录', 3),
        #101: ('现代女性', 1),
        #102: ('英语辅导', 1),
        103: ('游戏竞技', 1),
        #104: ('孕育指南', 1),
        #105: ('早期教育', 1),
        #106: ('证券资讯', 1),
        #107: ('CCTV中学生', 1),
        #108: ('CCTV央视台球', 1),
        109: ('CCTV发现之旅', 1),
        110: ('环球奇观', 3),
        #111: ('书画', 1),
        #112: ('说文解字', 1),
        #113: ('文物宝库', 1),
        #114: ('武术世界', 1),
        115: ('CCTV新科动漫', 1),
        #116: ('幼儿教育', 1),
        117: ('CHC动作电影', 10),
        118: ('CHC家庭影院', 10),
        119: ('CHC高清电影', 10),
        }

CHANNEK_KANDIANSHI_ID = {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: '11',
        13: '13',
        14: '14',
        15: '15',
        16: '16',
        17: '17',
        18: '18',
        19: '19',
        25: '25',
        26: '26',
        27: '27',
        28: '28',
        31: '31',
        35: '35',
        37: '37',
        38: '38',
        41: '41',
        42: '42',
        44: '44',
        45: '45',
        47: '47',
        48: '48',
        49: '49',
        53: '53',
        55: '55',
        57: '57',
        59: '59',
        60: '60',
        61: '61',
        66: '66',
        75: '75',
        76: '76',
        77: '77',
        78: '78',
        79: '79',
        80: '80',
        81: '81',
        82: '82',
        83: '83',
        84: '84',
        85: '85',
        86: '86',
        87: '87',
        88: '88',
        89: '89',
        90: '90',
        91: '91',
        92: '92',
        93: '93',
        94: '94',
        95: '95',
        96: '96',
        97: '97',
        98: '98',
        99: '99',
        100: '100',
        101: '101',
        102: '102',
        103: '103',
        104: '104',
        105: '105',
        106: '106',
        107: '107',
        108: '108',
        109: '109',
        110: '110',
        111: '111',
        112: '112',
        113: '113',
        114: '114',
        115: '115',
        116: '116',
        }

CHANNEK_TVMAO_ID = {
        1: ('CCTV', 'CCTV1'), #'CCTV-1 综合',
        2: ('CCTV','CCTV2'), #'CCTV-2 财经',
        3: ('CCTV', 'CCTV3'), #'CCTV-3 综艺',
        4: ('CCTV', 'CCTV4'), #'CCTV-4 中文国际(亚)',
        7: ('CCTV', 'CCTV5'), #'CCTV-5 体育',
        8: ('CCTV', 'CCTV6'), #'CCTV-6 电影',
        9: ('CCTV', 'CCTV7'), #'CCTV-7 军事·农业',
        10: ('CCTV', 'CCTV8'), #'CCTV-8 电视剧',
        11: ('CCTV', 'CCTV9'), #'CCTV-纪录',
        13: ('CCTV', 'CCTV10'), #'CCTV-10 科教',
        14: ('CCTV', 'CCTV11'), #'CCTV-11 戏曲',
        15: ('CCTV', 'CCTV12'), #'CCTV-12 社会与法',
        16: ('CCTV', 'CCTV13'), #'CCTV-13 新闻',
        17: ('CCTV', 'CCTV15'), #'CCTV-14 少儿',
        18: ('CCTV', 'CCTV16'), #'CCTV-15 音乐',
        19: ('CCTV', 'CCTV19'), #'CCTV-NEWS',
        25: ('BTV', 'BTV1'), #'北京卫视',
        26: ('SHHAI', 'DONGFANG1'), #'东方卫视',
        27: ('HLJTV', 'HLJTV1'), #'黑龙江卫视',
        28: ('JSTV', 'JSTV1'), #'江苏卫视',
        31: ('SCTV', 'SCTV1'), #'四川卫视',
        35: ('CCQTV', 'CCQTV1'), #'重庆卫视',
        37: ('BTV', 'BTV4'), #'BTV影视',
        38: ('GDTV', 'GDTV1'), #'广东卫视',
        41: ('HUBEI', 'HUBEI1'), #'湖北卫视',
        42: ('HUNANTV', 'HUNANTV1'), #'湖南卫视',
        44: ('LNTV', 'LNTV1'), #'辽宁卫视',
        45: ('SHXITV', 'SHXITV1'), #'陕西卫视',
        47: ('YNTV', 'YNTV1'), #'云南卫视',
        48: ('ZJTV', 'ZJTV1'), #'浙江卫视',
        49: ('AHTV', 'AHTV1'), #'安徽卫视',
        53: ('GSTV', 'GSTV1'), #'甘肃卫视',
        55: ('JILIN', 'JILIN1'), #'吉林卫视',
        57: ('GUIZOUTV', 'GUIZOUTV1'), #'贵州卫视',
        59: ('QHTV', 'QHTV1'), #'青海卫视',
        60: ('NXTV', 'NXTV1'), #'宁夏卫视',
        61: ('XJTV', 'XJTV1'), #'新疆卫视',
        66: ('BINGTUAN', 'BINGTUAN'), #'兵团卫视',
        75: ('CCTVPAYFEE', 'CCTVPAYFEE1'), #'CCTV风云足球',
        76: ('CCTVPAYFEE', 'CCTVPAYFEE2'), #'CCTV风云音乐',
        77: ('CCTVPAYFEE', 'CCTVPAYFEE3'), #'CCTV第一剧场',
        78: ('CCTVPAYFEE', 'CCTVPAYFEE4'), #'CCTV风云剧场',
        79: ('CCTVPAYFEE', 'CCTVPAYFEE5'), #'CCTV世界地理',
        80: ('CCTVPAYFEE', 'CCTVPAYFEE6'), #'CCTV电视指南',
        81: ('CCTVPAYFEE', 'CCTVPAYFEE7'), #'CCTV怀旧剧场',
        82: ('CCTVPAYFEE', 'CCTVPAYFEE8'), #'CCTV国防军事',
        83: ('CCTVPAYFEE', 'CCTVPAYFEE9'), #'CCTV女性时尚',
        84: ('CCTVPAYFEE', 'CCTVPAYFEE10'), #'CCTV娱乐',
        85: ('CCTVPAYFEE', 'CCTVPAYFEE11'), #'CCTV戏曲',
        86: ('CCTVPAYFEE', 'CCTVPAYFEE12'), #'CCTV电影',
        87: ('CCTVPAYFEE', 'CCTVPAYFEE13'), #'CCTV高尔夫网球',
        88: ('CCTVPAYFEE', 'CCTVPAYFEE14'), #'CCTV央视文化精品',
        89: ('CCTVPAYFEE', 'CCTVPAYFEE16'), #'彩民在线',
        90: ('CCTVPAYFEE', 'CCTVPAYFEE17'), #'法律服务',
        91: ('CCTVPAYFEE', 'GOLF'), #'高尔夫',
        92: ('CCTVPAYFEE', 'CCTVPAYFEE19'), #'靓妆',
        93: ('CCTVPAYFEE', 'CCTVPAYFEE20'), #'梨园',
        94: ('CCTVPAYFEE', 'CCTVPAYFEE22'), #'汽摩',
        95: ('CCTVPAYFEE', 'CCTVPAYFEE23'), #'老年福',
        96: ('CCTVPAYFEE', 'CCTVPAYFEE24'), #'留学世界',
        97: ('CCTVPAYFEE', 'CCTVPAYFEE25'), #'青年学苑',
        98: ('CCTVPAYFEE', 'PHOTOGRAPHY-CHANNEL'), #'摄影',
        99: ('CCTVPAYFEE', 'TIANYUANWEIQI'), #'天元围棋',
        100: ('CCTVPAYFEE', 'DOCUMENTARY-CHANNEL'), #'先锋纪录',
        101: ('CCTVPAYFEE', 'CCTVPAYFEE29'), #'现代女性',
        102: ('CCTVPAYFEE', 'ENGLISH-TEACHING'), #'英语辅导',
        103: ('CCTVPAYFEE', 'GTV-YOUXI'), #'游戏竞技',
        104: ('CCTVPAYFEE', 'CCTVPAYFEE32'), #'孕育指南',
        105: ('CCTVPAYFEE', 'CCTVPAYFEE33'), #'早期教育',
        106: ('CCTVPAYFEE', 'CCTVCJ'), #'证券资讯',
        107: ('CCTVPAYFEE', 'CCTVPAYFEE35'), #'CCTV中学生',
        108: ('CCTVPAYFEE', 'CCTVPAYFEE36'), #'CCTV央视台球',
        109: ('CCTVPAYFEE', 'CCTVFXZL'), #'CCTV发现之旅',
        110: ('CCTVPAYFEE', 'HUANQIUQIGUAN'), #'环球奇观',
        111: ('CCTVPAYFEE', 'CCTVPAYFEE37'), #'书画',
        112: ('CCTVPAYFEE', 'SHUOWENJIEZI'), #'说文解字',
        114: ('CCTVPAYFEE', 'WUSHUSHIJIE'), #'武术世界',
        115: ('CCTVPAYFEE', 'XINKEDONGMAN'), #'CCTV新科动漫',
        116: ('CCTVPAYFEE', 'YOUERJIAOYU'), #'幼儿教育',
        117: ('CHC', 'CHC1'), #'CHC动作电影',
        118: ('CHC', 'CHC2'), #'CHC家庭影院',
        119: ('CHC', 'CHC3'), #'CHC高清电影',
        }

def init():
    for channel_id, (name, priority) in CHANNEL_DATA.iteritems():
        tv_id, c_id = CHANNEK_TVMAO_ID.get(channel_id, ('', ''))
        kandianshi_id = CHANNEK_KANDIANSHI_ID.get(channel_id, '')
        external = External(
                kandianshi_id=kandianshi_id,
                tvmao_tv_id=tv_id,
                tvmao_channel_id=c_id)
        c = Channel(
                id=channel_id,
                name=name,
                priority=priority,
                external=external)
        db.session.add(c)

    # Also use this as priority for candidate programs online
    candidate_uids = [
            K_CANDIDATE_KANDIANSHI,
            K_CANDIDATE_TVMAO,
            ]
    for uid in candidate_uids:
        candidate = Candidate(
                uid=uid,
                name=CANDIDATE_NAMES[uid])
        db.session.add(candidate)

    db.session.commit()
