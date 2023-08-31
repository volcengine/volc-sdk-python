import verender_init


def remove_file_demo():
    v = verender_init.get_verender_instance()

    workspace_id = 1935
    filename = "D/tests/test_upload_file/test_upload_file.txt"
    isp = "ct" # ct: 电信 un: 联通 cm: 移动
    v.remove_file(workspace_id, filename, isp)