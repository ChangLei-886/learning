#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '02/08/2018'
"""

import hashlib
import json
import collections

#返回字符串的md5值
def get_md5(str = None):
    if not str:
        return None

    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))

    return hl.hexdigest()

#返回序列化的json
def json_response(request=None, response=None, message='', status=0):

    ret_json = collections.OrderedDict()
    if request is not None:
        ret_json['request'] = request

    if response is not None:
        ret_json['response'] = response

    ret_json['message'] = message
    ret_json['status'] = status

    return json.dumps(ret_json, indent=4, separators=(',', ':'), ensure_ascii=False)
