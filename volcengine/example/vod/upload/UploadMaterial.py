# coding:utf-8
from __future__ import print_function

import json

from volcengine.util.Functions import Function
from volcengine.vod.VodService import VodService
from volcengine.const.Const import *
from volcengine.vod.models.request.request_vod_pb2 import VodUploadMaterialRequest

if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    space_name = 'your space name'
    file_path = 'your file path'

    get_meta_function = Function.get_meta_func()
    snapshot_function = Function.get_snapshot_func(2.3)
    add_option_function = Function.get_add_material_option_info_func(title='素材测试视频', tags='test',
                                                                     description='素材测试，视频文件',
                                                                     category=CATEGORY_VIDEO, record_type=2,
                                                                     format_input='MP4')

    try:
        req = VodUploadMaterialRequest()
        req.FileType = FILE_TYPE_MEDIA
        req.SpaceName = space_name
        req.FilePath = file_path
        req.Functions = json.dumps([get_meta_function, snapshot_function, add_option_function])
        req.CallbackArgs = ''
        req.FileExtension = '.mp4'
        req.UploadHostPrefer = ''

        resp = vod_service.upload_material(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Mid)
            print(resp.Result.Data.PosterUri)
            print(resp.Result.Data.SourceInfo.FileName)
            print(resp.Result.Data.SourceInfo.Height)
            print(resp.Result.Data.SourceInfo.Width)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    space_name = 'your space name'
    file_path = 'your file path'

    get_meta_function = Function.get_meta_func()
    snapshot_function = Function.get_snapshot_func(0)
    add_option_function = Function.get_add_material_option_info_func(title='素材测试图片', tags='test',
                                                                     description='素材测试，图片文件',
                                                                     category=CATEGORY_IMAGE, record_type=2,
                                                                     format_input='jpg')

    try:
        req = VodUploadMaterialRequest()
        req.FileType = FILE_TYPE_IMAGE
        req.SpaceName = space_name
        req.FilePath = file_path
        req.Functions = json.dumps([get_meta_function, snapshot_function, add_option_function])
        req.CallbackArgs = ''
        req.FileName = ''
        req.FileExtension = '.jpg'
        req.UploadHostPrefer = ''

        resp = vod_service.upload_material(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Mid)
            print(resp.Result.Data.PosterUri)
            print(resp.Result.Data.SourceInfo.FileName)
            print(resp.Result.Data.SourceInfo.Height)
            print(resp.Result.Data.SourceInfo.Width)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    space_name = 'your space name'
    file_path = 'your file path'

    get_meta_function = Function.get_meta_func()
    add_option_function = Function.get_add_material_option_info_func(title='素材测试字幕', tags='test',
                                                                     description='素材测试，字幕文件',
                                                                     category=CATEGORY_FONT, record_type=2,
                                                                     format_input='vtt')

    try:
        req = VodUploadMaterialRequest()
        req.FileType = FILE_TYPE_OBJECT
        req.SpaceName = space_name
        req.FilePath = file_path
        req.Functions = json.dumps([get_meta_function, add_option_function])
        req.CallbackArgs = ''
        req.FileName = ''
        req.FileExtension = '.vtt'
        req.UploadHostPrefer = ''

        resp = vod_service.upload_material(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Mid)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
