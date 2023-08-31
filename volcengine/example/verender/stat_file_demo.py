import verender_init


def stat_file_demo():
    v = verender_init.get_verender_instance()

    workspace_id = 1935
    filename = "D/tests/test_upload_file/test_upload_file.txt"
    isp = "un" # ct: 电信 un: 联通 cm: 移动
    f = v.stat_file(workspace_id, filename, isp)
    print(f.name, f.size, f.mtime, f.md5)