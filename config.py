# replicaSet的name为空则不使用集群配置
# user和pwd为空则不需要进行密码校验
# db不给出则默认为“admin”
MONGODB = {
    'host': '127.0.0.1',
    'port': '27017',
    'user': '',
    'pwd': '',
    'db': 'test',
    'replicaSet': {
        'name': 'abc',
        "members": [
            {
                "host": "localhost",
                "port": "27017"
            },
            {
                "host": "localhost",
                "port": "27027"
            },
            {
                "host": "localhost",
                "port": "27037"
            }
        ]
    }
}
