from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    click2_call_form = {
        "Caller": "137XXXX8257",
        "Callee": "158XXXX9130",
        "CallerNumberPoolNo": "NP163517154204092175",
        "CalleeNumberPoolNo": "NP163517154204092175",
    }
    print(vms_service.click2_call(click2_call_form))