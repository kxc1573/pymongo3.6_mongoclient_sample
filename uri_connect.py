# uri方式连接
# author: mona_alyn
# date:   2018/03/07

import sys
import urllib.parse

import pymongo
from pymongo.errors import ConnectionFailure

from config import MONGODB


# mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
params = []
host_info = ''
# 处理replicaSet设置
if MONGODB['replicaSet']['name']:
    host_opt = []
    for m in MONGODB['replicaSet']['members']:
        host_opt.append('%s:%s' % (m['host'], m['port']))
    host_info = (',').join(host_opt)
    replicaSet_str = 'replicaSet=%s' % MONGODB['replicaSet']['name']
    params.append(replicaSet_str)
else:
    host_info = '%s:%s' % (MONGODB['host'], MONGODB['port'])

# 处理密码校验
if MONGODB['user'] and MONGODB['pwd']:
    # py2中为urllib.quote_plus
    username = urllib.parse.quote_plus(MONGODB['user'])
    password = urllib.parse.quote_plus(MONGODB['pwd'])
    auth_str = '%s:%s@' % (username, password)
    params.append('authMechanism=SCRAM-SHA-1')
else:
    auth_str = ''

if params:
    param_str = '?' + '&'.join(params)
else:
    param_str = ''

uri = 'mongodb://%s%s/%s%s' % (auth_str, host_info, MONGODB['db'], param_str)
client = pymongo.MongoClient(uri)


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
