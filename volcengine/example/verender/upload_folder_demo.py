import verender_init


def upload_folder_demo():
    v = verender_init.get_verender_instance()
    workspace_id = 1935
    src_path = "D:\\tests\\test_upload_folder"
    des_path = "D:\\tests\\test_upload_folder"
    isp = "un" # ct: 电信 un: 联通 cm: 移动

    v.upload_folder(workspace_id, src_path, des_path, isp)