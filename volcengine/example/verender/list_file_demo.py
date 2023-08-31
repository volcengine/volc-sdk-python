import verender_init


def list_file_demo():
    v = verender_init.get_verender_instance()

    workspace_id = 1935
    prefix = "D/tests"
    filter_in = ""
    order_type = "asc" # asc or desc
    order_field = "name" # name or mtime
    page_num = 1
    page_size = 10
    isp = "ct" # ct: 电信 un: 联通 cm: 移动
    total, file_info_list = v.list_file(workspace_id, prefix, filter_in, order_type, order_field, page_num, page_size, isp)
    print(total)
    print(file_info_list)