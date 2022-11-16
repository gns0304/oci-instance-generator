import requests
import configparser
import os
import json
from oci.config import from_file
from oci.signer import Signer


class OCI:
    def __init__(self, url, conf_path, key_file_path, metadata):

        if key_file_path:
            self.__set_key_file_config(conf_path, key_file_path)

        self.__config = from_file(conf_path, "DEFAULT")
        self.__auth = Signer(
            tenancy=self.__config['tenancy'],
            user=self.__config['user'],
            fingerprint=self.__config['fingerprint'],
            private_key_file_location=self.__config['key_file']
        )
        self.__url = url
        self.__metadata = self.__set_metadata(metadata)

    @staticmethod
    def __set_key_file_config(conf_path, key_file_path):
        config = configparser.ConfigParser()
        config.read(conf_path)
        config.set("DEFAULT", 'key_file', key_file_path)
        with open(conf_path, 'w') as conf_file:
            config.write(conf_file)

    @staticmethod
    def __set_metadata(metadata):
        if os.path.isfile(metadata):
            with open(metadata, 'r') as file:
                return json.load(file)
        else:
            return metadata

    def get_instances(self):
        params = {"compartmentId": self.__metadata["compartmentId"]}
        response = requests.get(self.__url, params=params, auth=self.__auth)
        return response.json()

    def create_instance(self):
        response = requests.post(self.__url, json=self.__metadata, auth=self.__auth)
        return response.json()
