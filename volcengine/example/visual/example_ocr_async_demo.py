# coding:utf-8
from __future__ import print_function
import base64
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    # visual_service.set_host('host')
    submit_action = "OCRPdfSubmitTask"
    query_action = "OCRPdfQueryTask"
    version = "2021-08-23"
    visual_service.set_api_info(submit_action, version)
    visual_service.set_api_info(query_action, version)

    # below shows the sdk usage for all common apis,
    # if you cannot find the needed one, please check other example files in the same dir
    # or contact us for further help  
    
    # PDF识别
    # req_key=ocr_pdf
    # OCRPdfSubmitTask
    # OCRPdfQueryTask


    submit_form = {
        "req_key": "ocr_pdf",
        "image_base64": base64.b64encode(open('local.pdf','rb').read()).decode(),
        "image_url": "http://image.jpeg",
    }

    submit_resp = visual_service.ocr_async_api(submit_action, submit_form)

    query_form = {
        "req_key": "ocr_pdf",
        "task_id": "12345678"
    }

    query_resp = visual_service.ocr_async_api(query_action, query_form)
    print(query_resp)