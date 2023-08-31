import verender_init


def list_account_dcc_plugins_demo():
    v = verender_init.get_verender_instance()

    params = {
        "SpecTemplateId": 15,
        "Dcc": "maya",
        "DccVersion": "2022.3"
    }

    resp = v.list_account_dcc_plugin(params=params)
    print(resp)