import json
import os
import requests
import yaml

smc_config_path = './config/config.yaml'
azure_config_path = './config/azure-config.json'


def download(config_key):
    # Retrieve URL for config file
    url = os.environ[config_key]

    # Download config file
    print("downloading: " + config_key)
    file_content = requests.get(url=url)
    if config_key == 'SMC_CONFIG_URL':
        with open(smc_config_path, 'wb') as config:
            config.write(file_content.content)
    elif config_key == 'AZURE_CONFIG_URL':
        with open(azure_config_path, 'wb') as config:
            config.write(file_content.content)


class Config:
    """
    Class representing configuration for the program.
    """

    smc_data = {}
    azure_data = {}

    def load_smc_config(self):
        # Check if config file exists, download if not.
        if not os.path.isfile(smc_config_path):
            download('SMC_CONFIG_URL')

        # Load in config file details
        with open(smc_config_path) as config:
            self.smc_data = yaml.load(config, Loader=yaml.FullLoader)

    def load_azure_config(self):
        # Check if config file exists, download if not.
        if not os.path.isfile(azure_config_path):
            download('AZURE_CONFIG_URL')

        # Load in config file details
        with open(azure_config_path) as config:
            self.azure_data = json.load(config)

    def get_smc(self, key):
        return self.smc_data.get(key, None)

    def get_azure(self, key):
        return self.azure_data.get(key, None)
