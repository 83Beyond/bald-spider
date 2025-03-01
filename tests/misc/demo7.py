methods = {
    "process_request": ['request_handle1','request_handle2','request_handle3'],
    "process_response": ['response_handle1','response_handle2'],
    "process_exception": ['exception_handle1'],
}

# 订阅系统。
# 博主
# 你 -> 关注
# 博主 -> 发布

# event(关键事件)：ignore_request, spider_error, spider_open

subscriber = {
    "ignore_request": {'ignore_request_handle1', 'ignore_request_handle2', 'ignore_request_handle3'},
    "spider_error": {'spider_error_handle1', 'spider_error_handle2'},
    "spider_open": {'spider_open_handle1'},
}