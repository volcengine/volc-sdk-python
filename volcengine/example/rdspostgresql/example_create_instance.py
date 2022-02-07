# coding:utf-8
from __future__ import print_function
from volcengine.rdspostgresql.rdspostgresql import RdsPostgreSQL


# test unit : "create_instance" "create_account" "create_white_list" "create_database" "modify_database_owner"
test_unit = "create_instance"
instanceID = "postgres-xxx"


def test_create_instance(cls):
    params = {
        "Region": "cn-north-x",
        "Zone": "cn-north-x-a",
        "DBEngine": "PostgreSQL",
        "DBEngineVersion": "PostgreSQL_12",       # PostgreSQL Version "PostgreSQL_12" "PostgreSQL_11"
        "InstanceType": "HA",                     # Primary isntance should be "HA" Readonly instance should be "Basic"
        "InstanceSpecName": "rds.postgres.1c2g",  # 1c2g mean 1CPU and 2G Memory
        "StorageSpaceGB": 100,                    # storage(GB)
        "Number": 1,                              # instance number
        "StorageType": "LocalSSD",                # storage type should be "LocalSSD"
        "VpcID": "vpc-xxx",
        "ChargeType": "PostPaid",                 # ChargeType currently should be "PostPaid"
        "InstanceCategory": "Primary",            # Primary instance type should be "Primary", readonly instance should be "ReadOnly"
        "RequestSource": "OpenAPI"
    }
    print(cls.create_instance(params))


def test_create_account(cls):
    params = {
        "InstanceId": instanceID,
        "AccountName": "user004",
        "AccountPassword": "xxx",
        "AccountDesc": "",
        "AccountType": "Normal",       # account type "Super" or "Normal"
    }
    print(cls.create_account(params))


def test_create_white_list(cls):
    params = {
        "InstanceId": instanceID,
        "GroupName": "hahaha",
        "IPList": ["1.1.1.2"],
    }
    print(cls.create_instance_white_list(params))


def test_create_database(cls):
    params = {
        "InstanceId":       instanceID,
        "DBName":           "db001",
        "CharacterSetName": "utf8",      # CharacterSet "utf8" "latin1" or "ascii"
        "Collate":          "CUTF8",     # Collate "C" "CUTF8" or "EnUsUtf8"
        "Ctype":            "CUTF8",     # Ctype "C" "CUTF8" or "EnUsUtf8"
        "Owner":            "user001",
    }
    print(cls.create_database(params))


def test_modify_database_owner(cls):
    params = {
        "InstanceId": instanceID,
        "DBName": "db001",
        "Owner": "user001",
    }
    print(cls.modify_database_owner(params))


if __name__ == '__main__':
    service = RdsPostgreSQL("cn-north-1")
    service.set_ak("Your AK")
    service.set_sk("Your SK")

    if test_unit == "create_instance":
        test_create_instance(service)
    elif test_unit == "create_account":
        test_create_account(service)
    elif test_unit == "create_white_list":
        test_create_white_list(service)
    elif test_unit == "create_database":
        test_create_database(service)
    elif test_unit == "modify_database_owner":
        test_modify_database_owner(service)
