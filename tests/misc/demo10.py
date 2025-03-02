import json

a_list = [1, 2, 3, 3, 4, 4, 5]  # 所有 request
# b_list = list(set(a_list))

b_list = []  # 用来过滤的列表
for request in a_list:
    if request not in b_list:
        b_list.append(request)
# 寻求请求的特征值

# request -> 定义一个指纹
# 特征1: url（需要）
# 特征2: 参数，get -> 包含着url中（需要）
#            post -> body（需要）
# 特征3: 请求方式 -> get, post（需要）
# 特征4: 请求头（不需要）

from w3lib.url import canonicalize_url

url1 = "www.baidu.com?a=1&b=2&c=3"
url2 = "www.baidu.com?c=3&b=2&a=1"
url3 = canonicalize_url(url1)
url4 = canonicalize_url(url2)

# 需要判断为同一个 url
print(url3 == url4)

url5 = "www.baidu.com"
params1 = {
    "a": 1, "b":2,"c":3
}
params2 = {
    "c": 3, "b":2,"a":1
}

data1 = json.dumps(params1, sort_keys=True)
data2 = json.dumps(params2, sort_keys=True)
print(data1 == data2)
