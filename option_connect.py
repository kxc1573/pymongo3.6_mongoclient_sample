# option方式连接
# author: mona_alyn
# date:   2018/03/07

import sys
import urllib.parse

import pymongo
from pymongo.errors import ConnectionFailure

from config import MONGODB


# replicaSet设置
if MONGODB['replicaSet']['name']:
    host_opt = []
    for m in MONGODB['replicaSet']['members']:
        host_opt.append('%s:%s' % (m['host'], m['port']))
    replicaSet = MONGODB['replicaSet']['name']
else:
    host_opt = '%s:%s' % (MONGODB['host'], MONGODB['port'])
    replicaSet = None

option = {
    'host': host_opt,
    'authSource': MONGODB['db'] or 'admin',    # 指定db,默认为'admin'
    'replicaSet': replicaSet,
}
if MONGODB['user'] and MONGODB['pwd']:
    # py2中为urllib.quote_plus
    option['username'] = urllib.parse.quote_plus(MONGODB['user'])
    option['password'] = urllib.parse.quote_plus(MONGODB['pwd'])
    option['authMechanism'] = MONGODB['authMechanism']

client = pymongo.MongoClient(**option)


# 验证连接成功，假设db中有collection名为TEST_COL
try:
    # 涉及权限问题
    # client.run.command({'count': 'source'})     # 查询命令
    # 不支持多个host
    # client.admin.command('ismaster')
    database = client[MONGODB['db']]
    print(database.TEST_COL.count())
except ConnectionFailure:
    raise ConnectionFailure
    print("Server not available")
    sys.exit()
