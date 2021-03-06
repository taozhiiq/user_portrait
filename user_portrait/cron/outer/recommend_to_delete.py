# -*- coding: utf-8 -*-

"""
based on user activity, recommend to delete the user in portrait database

"""

import sys
import time
import json
import redis
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1, R_RECOMMENTATION_OUT
from filter_uid import all_delete_uid

es = ES_CLUSTER_FLOW1
recommend_redis = R_RECOMMENTATION_OUT

threshould = 4
index_destination = "copy_user_portrait"
index_destination_doctype = "user"

def search_low_number(low_range, index_name=index_destination, index_type=index_destination_doctype):
    query_body = {
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                 },
                "filter": {
                    "range": {
                        "low_number":{
                            "gt": low_range
                        }
                    }
                }
            }
        }
    }

    results = es.search(index=index_name, doc_type=index_type, body=query_body)["hits"]["hits"]

    user_list = []
    for item in results:
        user_list.append(item['_id'])

    return user_list


def main():
    filter_uid = all_delete_uid()
    record_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    recommend_list = search_low_number(threshould) # recommended user to delete in portrait database
    print len(recommend_list)
    if recommend_list:
        recommend_list = list(set(recommend_list).difference(filter_uid))
        recommend_redis.hset("recommend_delete_list", record_time, json.dumps(recommend_list)) # lpush uid into a redis

        former_time = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
        recommend_redis.hdel("recommend_delete_list", former_time)
        return 1
    else:
        print "no one to recommend"
        return 0

if __name__ == "__main__":
    main()
