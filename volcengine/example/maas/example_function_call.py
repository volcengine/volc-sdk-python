import os
from volcengine.maas import MaasService, MaasException, ChatRole


def test_function_call(maas: MaasService):
    req = {
        "model": {"name": "${YOUR_MODEL_NAME}"},
        "messages": [
            {"role": ChatRole.SYSTEM, "content": "如未特殊说明，用户下班时间为下午6点。"},
            {
                "role": ChatRole.SYSTEM,
                "content": "用户ID全部用<<USER_N>>表示，文档ID全部用<<DOC_N>>表示，其中N表示序号1，2，3...",
            },
            {"role": ChatRole.USER, "content": "播放陈奕迅的十年"},
        ],
        "parameters": {"temperature": 0.8, "max_new_tokens": 512},
        "functions": [
            {
                "name": "EntitySearchTool",
                "description": "当用户需要查询办公场景相关实体使用此函数，查询输入的实体对应的信息，实体包括：消息，邮件，文档，待办事项。用户问题里面有id信息优先提取id作为检索条件",
                "parameters": {
                    "properties": {
                        "query": {"description": "表示用户输入查询实体", "type": "string"}
                    },
                    "required": ["query"],
                    "type": "object",
                },
                "examples": ['{"query": "最近3天看过的文档"}'],
            },
            {
                "name": "EntityUnderstandTool",
                "description": "当用户需要对办公实体操作时使用此函数，实体包括：消息，邮件，代办事项",
                "parameters": {
                    "properties": {
                        "entity": {"description": "表示实体对应的id", "type": "string"},
                        "operation": {
                            "description": "表示任务名称，取值有：总结、校对、提取待办事项",
                            "type": "string",
                        },
                    },
                    "required": ["operation", "entity"],
                    "type": "object",
                },
                "examples": ['{"operation": "总结", "entity": "<<DOC_0>>"}'],
            },
            {
                "name": "BookMeetingTool",
                "description": "当用户需要预订会议时使用此函数，根据输入的信息解析出会议主题，参会人，会议时间，并预订会议。如果用户没有指定会议开始时间，则取当前系统时间。如果用户没有指定会议结束时间，会议时长默认为1小时结束",
                "parameters": {
                    "properties": {
                        "end_time": {"description": "表示会议结束时间", "type": "string"},
                        "participant_ids": {
                            "description": "表示参会人id集合，用;隔开，必须有用户本人的id",
                            "type": "string",
                        },
                        "start_time": {"description": "表示会议开始时间", "type": "string"},
                        "timezone": {
                            "default": "Asia/Shanghai",
                            "description": "表示会议所在时区",
                            "type": "string",
                        },
                        "topic": {
                            "default": "",
                            "description": "表示预订会议的主题",
                            "type": "string",
                        },
                    },
                    "required": ["participant_ids", "start_time", "end_time"],
                    "type": "object",
                },
                "examples": [
                    '{"topic": "今天下午5点跟小周周会日程", "participant_ids": "<<USER_0>>;<<USER_1>>", "start_time": "2023-07-18T17:00:00", "end_time": "2023-07-18T18:00:00", "timezone": "Asia/Shanghai"}'
                ],
            },
            {
                "name": "CodeExecutorPlugin",
                "description": "当用户需要执行代码的时候使用此函数，支持go，js，java，python，rust，php，kotlin，dart，c，cpp，c#等编程语言",
                "parameters": {
                    "properties": {
                        "code": {"type": "string"},
                        "language": {"type": "string"},
                    },
                    "required": ["language", "code"],
                    "type": "object",
                },
                "examples": [
                    '{"language": "python3", "code": "print(\'hello word\')"}'
                ],
            },
            {
                "name": "MusicPlayer",
                "description": "歌曲查询Plugin，当用户需要搜索某个歌手或者歌曲时使用此plugin，给定歌手，歌名等特征返回相关音乐",
                "parameters": {
                    "properties": {
                        "artist": {"description": "表示歌手名字", "type": "string"},
                        "description": {"description": "表示描述信息", "type": "string"},
                        "song_name": {"description": "表示歌曲名字", "type": "string"},
                    },
                    "required": [],
                    "type": "object",
                },
                "examples": ['{"artist":"孙燕姿","song_name":"遇见","description":""}'],
            },
        ],
    }

    try:
        resp = maas.chat(req)
        print(resp)
        print(resp.choice.message.content)

        req["messages"].append(
            {
                "role": resp.choice.message.role,
                "content": resp.choice.message.content,
                "name": resp.choice.message.name,
                "function_call": {
                    "name": resp.choice.message.function_call.name,
                    "arguments": resp.choice.message.function_call.arguments,
                },
            }
        )

        if resp.choice.message.function_call.name != "":
            # Note: 用户必须要首先验证模型输出的 function name 和 argument 是否合法
            # 1. Name 不一定是 prompt 给出的 function name；
            # 2. Arguments 不一定是合法的 json；
            # 3. Arguments 即使是合法的 json，也不一定满足 function 的 Parameters 规范。
            function_resp = "通过汽水音乐，为您找到：\n| 歌手 | 歌名 |\n| --- | --- |\n| 陈奕迅 | 十年 (OT: 明年今日) |\n| 陈奕迅 | 富士山下 |\n| 陈奕迅 | 最佳损友 |"
            req["messages"].append(
                {
                    "role": ChatRole.FUNCTION,
                    "content": function_resp,
                    "name": resp.choice.message.function_call.name,
                }
            )
        else:
            # 模型输出的内容可能不是 function call，继续对话即可
            user_input = "播放肖斯塔科维奇最伟大的作品"
            req["messages"].append(
                {
                    "role": ChatRole.USER,
                    "content": user_input,
                }
            )

        resp = maas.chat(req)
        print(resp)
        print(resp.choice.message.content)

    except MaasException as e:
        print(e)


if __name__ == "__main__":
    maas = MaasService("maas-api.ml-platform-cn-beijing.volces.com", "cn-beijing")

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    test_function_call(maas)
