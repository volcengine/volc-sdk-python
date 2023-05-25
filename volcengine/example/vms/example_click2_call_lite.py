from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    click2_call_lite_form = {
        "Caller": "137XXXX8257",
        "Callee": "158XXXX9130",
        "NumberPoolNo": "NPXXXXX810901043",
    }
    print(vms_service.click2_call_lite(click2_call_lite_form))