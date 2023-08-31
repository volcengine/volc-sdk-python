import verender_init


def list_dcc_demo():
    v = verender_init.get_verender_instance()

    resp = v.list_dcc()
    print(resp)