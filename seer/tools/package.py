# -*- coding: utf-8 -*-

import os
import string
import json
from datetime import datetime
from urllib import urlencode

from configs import config

cmd_template = string.Template('wget -O - -c "$url" | gzip > "$target"')

CMD_WGET_WITH_GZIP = 'wget -O - -c "%s" | gzip > "%s"'

def package(target=None, datenum=None, days=1):
    target = target or os.path.join(config.VAR_PATH, config.SITE_PORT,
            'www/packages')
    datenum = datenum or datetime.now().strftime('%Y%m%d')

    for i in range(days):
        _datenum = str(int(datenum)+i)
        query = dict(
             filters=[
                  dict(
                       name='datenum',
                       op='eq',
                       val=_datenum,
                ),
            ],
        )
        payload = dict(
           q=json.dumps(query),
        )
        source = config.SHOWN_HOME + '/api/program?' + urlencode(payload)

        fname = 'daily-programs-%s.json.gz' % _datenum
        output_path = os.path.join(target, fname)
        cmd = CMD_WGET_WITH_GZIP % (source, output_path)
        os.system(cmd)
        print '[%s] done.'%i, output_path
