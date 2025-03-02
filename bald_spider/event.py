# bald_spider 中可以触发的关键事件

# spider_error arguments: exception, spider
spider_error = "spider_error"
# spider_open arguments: nothing(spider)
spider_opened = "spider_opened"
# spider_closed arguments: nothing(spider)
spider_closed = "spider_closed"
# ignore_request arguments: exception, request, spider
ignore_request = "ignore_request"
# request_scheduled arguments: request, spider
request_scheduled = "request_scheduled"
# response_received arguments: response, spider
response_received = "response_received"
# item_successful arguments: item, spider
item_successful = "item_successful"
# item_discard arguments: item, exception, spider
item_discard = "item_discard"
