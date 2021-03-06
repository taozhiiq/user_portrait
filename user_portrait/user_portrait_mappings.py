# -*- coding: utf-8 -*-

import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

index_info = {
    "settings":{
        "analysis":{
            "analyzer":{
                "my_analyzer":{
                    "type": "pattern",
                    "pattern": "&"
                }
            }
        }
    },

    "mappings":{
        "user":{
            "properties":{
                "domain":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "uname":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "geo_activity_dict":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "hashtag":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "keywords":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "psycho_status":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "topic":{
                    "type": "string",
                    "index": "not_analyzed"
                },


                "geo_activity":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "keywords_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "psycho_status_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "topic_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },

                "importance": {
                    "type": "long"
                },
                "influence": {
                    "type": "long"
                },
                "activeness": {
                    "type": "long"
                },

                "emoticon": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "online_pattern":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "link": {
                    "type": "long",
                    "index": "not_analyzed"
                },
                "fansnum": {
                    "type": "long"
                },
                "text_len": {
                    "type": "long"
                },
                "photo_url": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "verified": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "statusnum": {
                    "type": "long"
                },
                "gender": {
                    "type": "long"
                },
                "location": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "emotion_words": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "friendsnum": {
                    "type": "long"
                }
            }
        }
    }
}


es = Elasticsearch('219.224.135.93')

es.indices.create(index="user_portrait", body=index_info, ignore=400)

#es.index(index="test_mapping_index", doc_type="user", id="1917335617",body={"uid":"1917335617", "hashtag_string":"中国好声音&急速前进&花千骨", "hashtag":"中国好声音&急速前进&花千骨", "geo_activity":"中国		北京	北京&中国	上海	上海", "geo_activity_string":"北京&上海"})
