from volcengine.verender.VerenderService import  VerenderService


def get_verender_instance():
    # ftrans_client_addr是快传客户端的地址 不配置走S10 传输速度会低于快传客户端
    # ftrans_proxy_addr是代理的管理地址 无代理不需要填
    v = VerenderService(ftrans_client_addr="127.0.0.1:8899", ftrans_proxy_addr="10.1.1.1:30001")
    v.set_ak("your ak")
    v.set_sk("your sk")
    return v