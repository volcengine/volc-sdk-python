import verender_init


def get_current_user_demo():
    v = verender_init.get_verender_instance()

    resp = v.get_current_user()
    print(resp)