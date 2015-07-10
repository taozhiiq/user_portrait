# -*- coding: UTF-8 -*-
'''
compute the user attribute about text
'''
import re
import csv
import sys
import time
# read weibo bulk from api
from weibo_api import read_user_weibo
reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

cx_dict = ['a', 'n', 'nr', 'ns', 'nz', 'v', '@', 'd']
sw = load_scws()

#liwc_dict = get_liwc_dict()
#emoticon_dict = get_emoticon_dict()

def get_emoticon_dict():
    results = dict()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/emoticons.txt', 'rb')
    for line in f:
        line_list = line.split(':')
        emoticon = line_list[0]
        #print 'emoticon:', type(emoticon), emoticon
        emo_class = line_list[1]
        try:
            results[emo_class].append(emoticon.decode('utf-8'))
        except:
            results[emo_class] = [emoticon.decode('utf-8')]
    return results

emoticon_dict = get_emoticon_dict()

def get_liwc_dict():
    results = dict()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/extract_word.csv', 'rb')
    reader = csv.reader(f)
    for line in reader:
        num = line[0]
        word = line[1]
        try:
            results[num].append(word)
        except:
            results[num] = [word]
    return results

liwc_dict = get_liwc_dict()

# read uid_list from user portrait
def read_uid_list():
    uid_list = []
    return uid_list

def attr_text_len(weibo_list):
    len_list = [len(weibo['text']) for weibo in weibo_list]
    max_len = max(len_list)
    min_len = min(len_list)
    ave_len = float(sum(len_list)) / len(len_list)
    #print 'len_list:', len_list
    return [min_len, max_len, ave_len]

'''
def attr_punc(weibo_list):
    results = {}   
    return results
'''

def attr_hash(weibo_list):
    results = {}
    for weibo in weibo_list:
        text = weibo['text']
        if isinstance(text, str):
            text = text.decode('utf-8', 'ignore')
        RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
        hashtag_list = RE.findall(text)
        # there all use unicode 
        for hashtag in hashtag_list:
            try:
                results[hashtag] += 1
            except:
                results[hashtag] = 1
    return results

def attr_emoticon(weibo_list):
    results = {}
    for weibo in weibo_list:
        text = weibo['text']
        for emo_class in emoticon_dict:
            emoticons = emoticon_dict[emo_class]
            for emoticon in emoticons:
                #print 'emoticon:', emoticon.encode('utf-8'), type(emoticon)
                #print 'text:', type(text)
                if isinstance(text, str):
                    text = text.decode('utf-8')
                count = text.count(emoticon)
                if count != 0:
                    try:
                        results[emoticon] += count
                    except:
                        results[emoticon] = count
    
    return results

# {class_num:{word:count}}
def attr_liwc(weibo_list):
    results = {}
    for weibo in weibo_list:
        text = weibo['text']
        cut_text = sw.participle(text.encode('utf-8'))
        cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
        for num in liwc_dict:
            for liwc_word in liwc_dict[num]:
                if liwc_word in cut_word_list:
                    if num in results:
                        try:
                            results[num][liwc_word] += 1
                        except:
                            results[num][liwc_word] = 1
                    else:
                        results[num] = {liwc_word: 1}
    # test
    '''
    for num in results:
        for word in results[num]:
            print 'num, word, count:', num, word, results[num][word]
    '''
    return results


def attr_link(weibo_list):
    count = []
    for weibo in weibo_list:
        text = weibo['text']
        pat = re.compile('http://')
        urls = re.findall(pat, text)
        if len(urls)!=0:
            count.append(len(urls))
    if count:
        all_count = sum(count)    
        ave_count = float(all_count) / len(weibo_list)
        max_count = max(count)
        min_count = min(count)
        return [min_count, max_count, ave_count, all_count]
    else:
        return None

def compute_text_attribute(user, weibo_list):
    result = {}
    # text attr1: len
    result['text_len'] = attr_text_len(weibo_list)
    # text attr2: punctuation
    #result['punc'] = attr_punc(weibo_list)
    # text attr3: emoticon
    result['emoticon'] = attr_emoticon(weibo_list)
    # text attr4: hashtag
    result['hashtag'] = attr_hash(weibo_list)
    # text attr5: liwc word
    result['emotion_words'] = attr_liwc(weibo_list)
    # text attr6: web link
    result['link'] = attr_link(weibo_list)
    return result

def main():
    # read the uid list
    uid_list = read_uid_list()
    # get user weibo 7day {user:[weibos]}
    user_weibo_dict = read_user_weibo(uid_list)
    # compute text attribute
    user_results = {}
    for user in user_weibo_dict:
        weibo_list = user_weibo_dict[user]
        results = compute_text_attribute(user, weibo_list)
        user_results[user] = results 
    return user_results # save by bulk
    
if __name__=='__main__':
    user_results = main()
    print 'user_result:', user_results