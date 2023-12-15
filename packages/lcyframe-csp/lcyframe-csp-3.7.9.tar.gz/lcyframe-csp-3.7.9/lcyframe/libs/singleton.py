import json

import redis

from scanner.configs import Scaner_Config, out
from scheduler.common import keys

"""
收集最终结果
"""


class RedisCon(object):
    """单例"""

    _redis = None

    @classmethod
    def get_connection(cls):
        if cls._redis is None:
            cls._redis = redis.Redis(
                host=Scaner_Config.REDIS_HOST,
                port=Scaner_Config.REDIS_PORT,
                db=7,
                password=Scaner_Config.REDIS_PASSWORD,
            )
        return cls._redis


class CacheData(object):
    redis = RedisCon.get_connection()

    @classmethod
    def add_domain(cls, task_id, domain):
        """
        域名记录
        """
        return cls.redis.setex(keys.scan_task_domain % task_id, Scaner_Config.EXPIRE, domain)

    @classmethod
    def add_subdomains(cls, task_id, *datas):
        """
        子域名记录
        Returns:
            subdomains: [
                {
                    "subdomainname": "sub.domain.com",  # 必须，其他的中间逻辑依赖该值
                    "ip": "10.10.10.10",
                    "city": "南宁",
                    "country": "中国",
                    "province": "广西",
                    "ips": "电信",
                    "cdn": "True",
                    "domain_id": 10
                },
                ...
            ]
        """
        key = keys.scan_task_subdomains % task_id
        set_res = cls.redis.sadd(key, *[json.dumps(d) for d in datas])
        cls.redis.expire(key, Scaner_Config.EXPIRE)
        return set_res

    @classmethod
    def add_ports(cls, task_id, *datas):
        """
        端口记录
        Returns:
            datas: [
                {
                    "ip": "10.0.0.1",
                    "port": 80,
                    "service": "service",
                    "protocol": "http",
                    "version": "2.0",
                    "subdomainname": "sub.domain.com",
                    "subdomain_id": 20,     # 若为空，则业务内需自行查库；来源：sudomain.id,相同ip可能存在多条不同的子域，取最后一条
                    "company_id": 1,
                    "domain_id": 0,
                    "task_id": 31
                }
            ]
        """
        key = keys.scan_task_ports % task_id
        set_res = cls.redis.sadd(key, *[json.dumps(d) for d in datas])
        cls.redis.expire(key, Scaner_Config.EXPIRE)
        return set_res

    @classmethod
    def get_domain(cls, task_id):
        key = keys.scan_task_domain % task_id
        dms = (cls.redis.get(key) or b"").decode()
        # cls.redis.expire(key, 3600)
        return dms

    @classmethod
    def get_subdomains(cls, task_id):
        key = keys.scan_task_subdomains % task_id
        sdm_list = [json.loads(d) for d in cls.redis.smembers(key)]
        # cls.redis.expire(key, 3600)
        return sdm_list

    @classmethod
    def get_ports(cls, task_id):
        key = keys.scan_task_ports % task_id
        pts = [json.loads(d) for d in cls.redis.smembers(key)]
        # cls.redis.expire(key, 3600)
        return pts

    @classmethod
    def get_result(cls, task_id):
        """
        搜集本次任务的结果
        Args:
            task_id:
        Returns:
        """
        domain = cls.get_domain(task_id)
        subdomains = cls.get_subdomains(task_id)
        ports = cls.get_ports(task_id)
        return {"domain": domain, "subdomains": subdomains, "ports": ports}

    @classmethod
    def __del__(cls):
        # cls.redis.delete('task_domain*')
        # cls.redis.delete('task_ports*')
        # cls.redis.delete('task_subdomains*')
        pass


if __name__ == "__main__":
    cache = CacheData()
    tk_id = "task_id"
    # cache.add_domain(task_id, "domain")
    # print(cache.get_domain(task_id))
    #
    # cache.add_subdomains(task_id, *[
    #             {
    #                 "subdomainname": "sub.domain.com",
    #                 "ip": "10.10.10.10",
    #                 "city": "南宁",
    #                 "country": "中国",
    #                 "province": "广西",
    #                 "ips": "电信",
    #                 "cdn": "True",
    #                 "domain_id": 10
    #             }
    #         ])
    # print(cache.get_subdomains(task_id))
    #
    # cache.add_ports(task_id, *[dict(
    #                 port=80,
    #                 service="service",
    #                 protocol="http",
    #                 version='2.0',
    #                 subdomain_id=20,
    #                 company_id=1,
    #                 domain_id=10,
    #                 task_id=31
    #             )])
    # print(cache.get_ports(task_id))

    out(cache.get_result(tk_id))
