import verender_init


def upload_file_demo():
    v = verender_init.get_verender_instance()
    workspace_id = 1935
    src = "D:\\tests\\test_upload_file\\test_upload_file.txt"
    des = "D:\\tests\\test_upload_file\\test_upload_file.txt"
    isp = "ct" # ct: 电信 un: 联通 cm: 移动
    f = v.upload_file(workspace_id, src, des, isp)
    print(f.name, f.size, f.mtime, f.md5)