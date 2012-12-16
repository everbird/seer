# -*- coding: utf-8 -*-

import sys
from os.path import dirname
SEER_PATH = dirname(dirname(__file__))
if SEER_PATH not in sys.path[0]:
    sys.path.insert(0, SEER_PATH)

from unittest2 import TestCase

from seer.helper import normallize_name

class HelperTestCase(TestCase):

    def test_normallize_name(self):
        names = [
                ('故事片:蜘蛛侠', '蜘蛛侠'),
                ('电影情报站 (1) ', ''),
                ('醉拳3', '醉拳3'),
                ('格斗之夜(224)', '格斗之夜'),
                ('八辈子学吃（1）', '八辈子学吃'),
                ('2012我要上春晚特别节目-直通春晚(4)1/3', '-我要上春晚特别节目-直通春晚'),
                ('电视剧：加油妈妈17/35', '加油妈妈'),
                ('消费主张周末版45', '消费主张周末版45'),
                ('故事片：东成西就2011', '东成西就2011'),
                ('新闻1+1（重播）', '新闻-+1'),
                ('电视剧：铁齿铜牙纪晓岚4（11）', '铁齿铜牙纪晓岚-'),
                ('电视剧：新都市人（9、10）', '新都市人'),
                ('电视剧：媳妇的美好宣言（28-32）', '媳妇的美好宣言'),
                ('午间360', '午间360'),
                ('热门影院2012年11月30日3', '热门影院-年-月-日3'),
                ('发现中国（123)', '发现中国'),
                ('刷新3+7', '刷新-+7'),
                ('回看  父子神探之神秘数字', '父子神探之神秘数字'),
                ('回看 故事片: 民警故事', '民警故事')
                ]
        for i, (name, expect) in enumerate(names):
            result = normallize_name(name)
            print i, expect, result, name
            self.assertEquals(expect, result)
