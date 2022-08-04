# coding:utf-8

from volcengine.sts.StsService import StsService

if __name__ == '__main__':
    stsService = StsService()
    stsService.set_ak("your ak")
    stsService.set_sk("your sk")

    params = {
        "DurationSeconds": "900",
        "RoleSessionName": "just_for_test",
        "RoleTrn": "trn:iam::yourAccountID:role/yourRole"
    }

    print(stsService.assume_role(params))
