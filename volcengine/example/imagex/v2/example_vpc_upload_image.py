# coding:utf-8
from __future__ import print_function
from volcengine.imagex.v2.imagex_service import ImagexService

if __name__ == '__main__':
    imagex_service = ImagexService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    request = dict()
    request["ServiceId"] = "service id"      # 服务 ID
    request["FilePath"] = "your file path"   # 文件路径，与Data二选一
    request["Data"] = 'your data'            # 文件二进制数据，与FilePath二选一
    request["StoreKey"] = "your store key"   # 文件存储名
    request["Prefix"] = "your prefix"        # 文件前缀
    request["FileExtension"] = "your file extension"    # 文件后缀
    request["ContentType"] = "your content type"    # 文件Content-Type
    request["StorageClass"] = "your storage class"  # 文件存储类型
    request["PartSize"] = 0                         # 偏好分片大小，单位为字节(0表示按照默认规则分片)
    request["Overwrite"] = False                    # 是否覆盖已有文件
    request["SkipMeta"] = False                     # 是否跳过元信息
    try:
        resp = imagex_service.vpc_upload_image(request)
        print(resp)
    except Exception as e:
        print(e)
