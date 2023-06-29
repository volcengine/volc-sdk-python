from volcengine.maas import MaasService


def test_chat(maas, req):
    try:
        resp = maas.chat(req)
        print(resp)
        print(resp.choice.message.content)
    except Exception as e:
        print(e)

    
def test_stream_chat(maas, req):
    try:
        resps = maas.stream_chat(req)
        for resp in resps:
            print(resp)
            print(resp.choice.message.content)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')
    
    req = {
        "model": {
            "name": "chatglm-130b"
        },
        "parameters": {
            "max_tokens": 2000,
            "temperature": 0.8
        },
        "messages": [
            {
                "role": "user",
                "content": "天为什么这么蓝"
            }
        ]
    }
    
    # test_chat(maas, req)
    test_stream_chat(maas, req)

    