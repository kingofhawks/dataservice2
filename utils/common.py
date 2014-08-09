'''
Created on 2013-6-5

@author: YUWANG
'''

def get_currentId(url):
    currentUrl = url.get_full_path()
    id = currentUrl.split('/')[-1]
    return id