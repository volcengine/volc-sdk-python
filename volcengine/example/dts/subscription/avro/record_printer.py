MYSQL_TYPE_TIMESTAMP = 7
MYSQL_TYPE_DATE = 10
MYSQL_TYPE_TIME = 11
MYSQL_TYPE_DATETIME = 12
MYSQL_TYPE_YEAR = 13
MYSQL_TYPE_DATE_NEW = 14


def print_record(record):
    operation = record["operation"]
    print("Operation[{}] ObjectName[{}] SourceTimestamp[{}] ID[{}]".format(record["operation"], record["objectName"],
                                                                           record["sourceTimestamp"], record["id"]))
    if operation == "DDL":
        print("DDL[{}]".format(record["afterImages"]))
    elif operation == "INSERT":
        for i in range(len(record["afterImages"])):
            print("Field[{}] After[{}]".format(record["fields"][i]["name"],
                                               getDataValue(record["fields"][i]["dataTypeNumber"],
                                                            record["afterImages"][i])))
    elif operation == "DELETE":
        for i in range(len(record["afterImages"])):
            print("Field[{}] BEFORE[{}]".format(record["fields"][i]["name"],
                                                getDataValue(record["fields"][i]["dataTypeNumber"],
                                                             record["beforeImages"][i])))
    elif operation == "UPDATE":
        for i in range(len(record["afterImages"])):
            print("Field[{}] BEFORE[{}] After[{}]".format(record["fields"][i]["name"],
                                                          getDataValue(record["fields"][i]["dataTypeNumber"],
                                                                       record["beforeImages"][i]),
                                                          getDataValue(record["fields"][i]["dataTypeNumber"],
                                                                       record["afterImages"][i])))
    else:
        print(record)


def getDataValue(dataType, data) -> str:
    if dataType == MYSQL_TYPE_TIMESTAMP:
        return "%d.%d" % (data["timestamp"], data["millis"])
    elif dataType in (MYSQL_TYPE_DATE, MYSQL_TYPE_DATE_NEW):
        return "%d-%d-%d" % (data["year"], data["month"], data["day"])
    elif dataType == MYSQL_TYPE_TIME:
        return "%02d:%02d:%02d" % (data["hour"], data["minute"], data["second"])
    elif dataType == MYSQL_TYPE_DATETIME:
        return "%04d-%02d-%02d %02d:%02d:%02d" % (data["year"], data["month"], data["day"],
                                            data["hour"], data["minute"], data["second"])
    elif dataType == MYSQL_TYPE_YEAR:
        return data["year"]
    else:
        return data["value"]
