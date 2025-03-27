# coding:utf-8
from volcengine.imagex.v2.imagex_service import ImagexService

if __name__ == '__main__':
    service = ImagexService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    service.set_ak('ak')
    service.set_sk('sk')

    query = {}
    body = {}

    resp = service.describe_imagex_heif_encode_file_in_size_by_time(query, body)
    print(resp)
