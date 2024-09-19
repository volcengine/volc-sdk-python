# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import *

if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    try:
        req8 = VodGetSubtitleInfoListRequest()
        req8.Vid = 'vid'
        req8.FileIds = 'fileIds'
        req8.Formats = 'format'
        req8.Languages = 'language'
        req8.LanguageIds = 'languageIds'
        req8.SubtitleIds = 'subtitleIds'
        req8.Status = 'Published' #Published/Unpublished
        req8.Title = 'title'
        req8.Tag = 'tag'
        req8.Ssl = 'ssl'
        req8.Offset = 'offset'
        req8.PageSize = 'pageSize'

        resp8 = vod_service.get_subtitle_info_list(req8)
    except Exception:
        raise
    else:
        print(resp8)
        if resp8.ResponseMetadata.Error.Code == '':
            print('get subtitle info list success')
        else:
            print(resp8.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req9 = VodUpdateSubtitleStatusRequest()
        req9.Vid = 'vid'
        req9.FileIds = 'fileId1,fileId2'
        req9.Formats = 'format1,format2'
        req9.Languages = 'language1,language2'
        req9.Status = 'Published'          #Published/Unpublished

        resp9 = vod_service.update_subtitle_status(req9)
    except Exception:
        raise
    else:
        print(resp9)
        if resp9.ResponseMetadata.Error.Code == '':
            print('update subtitle status success')
        else:
            print(resp9.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req10 = VodUpdateSubtitleInfoRequest()
        req10.Vid = 'vid'
        req10.FileId = 'fileIds'
        req10.Format = 'format'
        req10.Language = 'language'
        req10.Title.value = 'title'
        req10.Tag.value = 'tag'

        resp10 = vod_service.update_subtitle_info(req10)
    except Exception:
        raise
    else:
        print(resp10)
        if resp10.ResponseMetadata.Error.Code == '':
            print('update subtitle info success')
        else:
            print(resp10.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req11 = VodGetSubtitleInfoListRequest()
        req11.Vid = 'vid'

        token = vod_service.get_subtitle_auth_token(req11, 60)
    except Exception:
        raise
    else:
        print(token)

    print('*' * 100)