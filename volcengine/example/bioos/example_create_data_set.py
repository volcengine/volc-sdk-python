# coding:utf-8
from __future__ import print_function

import datetime
import time
from typing import List

import pytz
import yaml

from volcengine.bioos.BioOsService import BioOsService


class YamlConverter:
    class Publications:
        def __init__(self, title: str, authors: List[str], access_url: str = None,
                     quotation: str = None):
            self.Name = title
            self.Authors = authors
            if access_url is not None:
                self.AccessURL = access_url
            if quotation is not None:
                self.Quotation = quotation

    def __init__(self, yaml_file: str):
        with open(yaml_file, "r", encoding="UTF-8") as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
            self.Name = yaml_dict.get("Name", None)
            self.Description = yaml_dict.get("Description", None)
            self.DocURL = yaml_dict.get("Documentation", None)
            self.Email = yaml_dict.get("Contact", None)
            self.Owners = yaml_dict.get("Owners", None)
            self.Licence = yaml_dict.get("Licence", None)

            self.Category = yaml_dict.get("Relevance", None)
            createDate = yaml_dict.get("CreateDate", None)
            if createDate:
                self.check_time_format(str(createDate))
                utc_date = datetime.datetime.combine(createDate, datetime.datetime.min.time())
                utc_date = pytz.utc.localize(utc_date)
                self.CreateTime = int(time.mktime(utc_date.timetuple()))
            updateDate = yaml_dict.get("UpdateDate", None)
            if updateDate:
                self.check_time_format(str(updateDate))
                utc_date = datetime.datetime.combine(updateDate, datetime.datetime.min.time())
                utc_date = pytz.utc.localize(utc_date)
                self.UpdateTime = int(time.mktime(utc_date.timetuple()))
            self.Catalogue = yaml_dict.get("Catalogue", None)

            project_type = yaml_dict.get("ProjectType", None)
            if project_type:
                self.ProjectDataTypes = project_type.get("ProjectDataTypes", None)
                self.SampleScope = project_type.get("SampleScope", None)

            self.Labels = yaml_dict.get("Labels", None)

            other_info = yaml_dict.get("Other", None)
            if other_info:
                self.ExternalLink = other_info.get("ExternalLink", None)
                self.ExternalLinkDescription = other_info.get("ExternalLinkDescription", None)
                self.ExampleTutorial = other_info.get("Tutorial", None)
                self.Tools = other_info.get("Tools&applications", None)
            self.Publications = []
            publications = yaml_dict.get("Publications", None)
            if publications is not None:
                for publication in publications:
                    self.Publications.append(YamlConverter.Publications(
                        publication.get("Title", None),
                        publication.get("Authors", None),
                        publication.get("URL", None),
                        publication.get("Citation", None)
                    ).__dict__)

            self.DataFilesAccessURL = yaml_dict.get("DataFilesURL", None)
            self.DataFileSamplesAccessURL = yaml_dict.get("DataFileSamplesURL", None)
            self.DataFileAccessMethodURL = yaml_dict.get("DataFileMethodURL", None)

    def build_create_params(self):
        return self.__dict__

    @staticmethod
    def check_time_format(t):
        try:
            datetime.datetime.strptime(t, "%Y-%m-%d")
        except Exception as e:
            print("time format %Y-%m-%d not matched")
            raise e


if __name__ == '__main__':
    # set endpoint/region here if the default value is unsatisfied
    bioos_service = BioOsService(endpoint='endpoint', region='region')

    # call below method if you don't set ak and sk in $HOME/.volc/config
    bioos_service.set_ak('ak')
    bioos_service.set_sk('sk')

    params = YamlConverter("example_dataset.yaml").build_create_params()

    resp = bioos_service.create_data_set(params)
    print(resp)
