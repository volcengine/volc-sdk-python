from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("your ak")
    secretNumberService.set_sk("your sk")

    click2_call_lite_form = {
        "Caller": "137XXXX8257",
        "Callee": "158XXXX9130",
        "NumberPoolNo": "NPXXXXX810901043",
    }
    print(secretNumberService.click2_call_lite(click2_call_lite_form))