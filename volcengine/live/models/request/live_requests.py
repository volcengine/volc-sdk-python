from tokenize import String


class CreateVQScoreTaskRequest:
    MainAddr = ""
    ContrastAddr = ""
    FrameInterval = 0
    Duration = 0
    Algorithm = ""
    def __init__(self):
        self = self

class GeneratePushURLRequest:
    Vhost = ""
    Domain = ""
    App = ""
    Stream = ""
    ValidDuration = 0
    ExpiredTime = ""
    def __init__(self):
        self = self

class GeneratePlayURLRequest:
    Vhost = ""
    Domain = ""
    App = ""
    Stream = ""
    Suffix = ""
    Type = ""
    ValidDuration = 0
    ExpiredTime = ""
    def __init__(self):
        self = self

class CreatePullToPushTaskRequest:
    Title = ""
    StartTime = 0
    EndTime = 0
    CallbackURL = ""
    Type = 0
    CycleMode = 0
    DstAddr = ""
    SrcAddr = ""
    SrcAddrS = []
    def __init__(self):
        self = self

class UpdatePullToPushTaskRequest:
    Title = ""
    StartTime = 0
    EndTime = 0
    CallbackURL = ""
    Type = 0
    CycleMode = 0
    DstAddr = ""
    SrcAddr = ""
    SrcAddrS = []
    TaskId = ""
    def __init__(self):
        self = self

class ListVQScoreTaskRequest:
    StartTime = ""
    EndTime = ""
    PageNum = 0
    PageSize = 0
    Status = 0
    def __init__(self):
        self = self