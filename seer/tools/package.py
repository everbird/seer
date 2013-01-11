# -*- coding: utf-8 -*-

import os
import string
import json
from datetime import datetime
from urllib import urlencode

cmd_template = string.Template('wget -O - -c "$url" | gzip > "$target"')

CMD_WGET_WITH_GZIP = 'wget -O - -c "%s" | gzip > "%s"'

def package(target, datenum=None):
    datenum = datenum or datetime.now().strftime('%Y%m%d')

    query = dict(
         filters=[
              dict(
                   name='datenum',
                   op='eq',
                   val=datenum,
            ),
        ],
    )
    payload = dict(
       q=json.dumps(query),
    )
    source = 'http://seer.everbird.net/api/program?' + urlencode(payload)

    fname = 'daily-programs-%s.json.gz' % datenum
    output_path = os.path.join(target, fname)
    cmd = CMD_WGET_WITH_GZIP % (source, output_path)
    r = os.popen(cmd)
    print r
