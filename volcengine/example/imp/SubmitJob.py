# coding:utf-8
from __future__ import print_function

from volcengine.imp.ImpService import ImpService
from volcengine.imp.models.business.imp_common_pb2 import *
from volcengine.imp.models.request.request_imp_pb2 import *

if __name__ == '__main__':
    imp_service = ImpService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    imp_service.set_ak('your ak')
    imp_service.set_sk('your sk')

    # SubmitJob
    try:
        req = ImpSubmitJobRequest()
        req.InputPath.Type = 'VOD'
        req.InputPath.VodSpaceName = 'your space'
        req.InputPath.FileId = 'your vid'
        req.TemplateId = 'your template id'
        req.CallbackArgs = 'your callback args'
        # SmartEraseOverrideParams
        smart_erase = SmartEraseOverrideParams()
        watermark_detect = DetectRect()
        watermark_detect.X1 = 0
        watermark_detect.X2 = 1
        watermark_detect.Y1 = 0
        watermark_detect.Y2 = 1
        ocr_detect = DetectRect()
        ocr_detect.X1 = 0
        ocr_detect.X2 = 1
        ocr_detect.Y1 = 0
        ocr_detect.Y2 = 1
        smart_erase.ActivityId.append("*")
        smart_erase.Watermark.DetectRect.append(watermark_detect)
        smart_erase.OCR.DetectRect.append(ocr_detect)
        req.Params.OverrideParams.SmartErase.append(smart_erase)
        # OutputOverrideParams
        output = OutputOverrideParams()
        output.ActivityId.append("*")
        output.OutputPath.Type = "your storage type"
        output.OutputPath.VodSpaceName = "your vod spaceName"
        output.OutputPath.TosBucket = "your tos bucketName"
        output.OutputPath.FileName = "output FileName"
        req.Params.OverrideParams.Output.append(output)

        resp = imp_service.submit_job(req)
    except Exception:
        raise
    else:
        print("resp:\n ", resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)

