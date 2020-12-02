# NGFW - Azure SD-WAN connector

Service to automatically deploy IPSec tunnels between NGFW engines and Azure 

# Prerequisites
* Azure SD-WAN config
* SMC details
* Docker

# Installation
### Logging in to the registry
* ```docker login forcepoint-bd-docker.jfrog.io ```

*Use your full @forcepoint.com username along with the API token provided in your user section in artifactory*
### Getting from the registry
* ```docker pull forcepoint-bd-docker.jfrog.io/ngfw-azure-sdwan```
###  Build locally with source (if not using registry image)
* ```docker build -t ngfw-azure-sdwan .```
### To run with your config:
* ```docker run -v "/path/to/local/folder:/app/config" -e CONFIG_URL=<URL-TO-YOUR>/config.yaml -e AZURE_CONFIG_URL=<URL-TO-YOUR>/azure-config.json ngfw-azure-sdwan```
---
*The local volume is used to persist the config file after download, if not added in the run command it will pull the config every time.*

*config.yaml and azure-config.json must be supplied as an ENV_VAR's as seen here and follow the example in the repo, any malformed fields or any missing mandatory fields will cause the connector to throw an exception*

# Example Config

```
smc-host: <SMC-IP-ADDRESS>
smc-port: <SMC-PORT>
smc-api-key: <SMC-API-KEY>>
smc-api-version: 6.7
gateway-profile:
ngfw-azure-locations:
  - {'NGFW EMEA 1': 'North Europe'}
  - {'NGFW US 1': 'East US'}
  - {'NGFW APAC 1': 'Japan West'}
ngfw-external-interface-ip: {'NGFW EMEA 1': '192.168.122.100','NGFW US 1': '192.168.122.200', 'NGFW APAC 1': '192.168.122.150'}
ngfw-external-address-space: {'NGFW EMEA 1': '192.168.122.0/24','NGFW US 1': '192.168.122.0/24', 'NGFW APAC 1': '192.168.122.0/24'}
ngfw-internal-vpn-interface-ip: {'NGFW EMEA 1': '172.16.16.1','NGFW US 1': '172.16.16.1', 'NGFW APAC 1': '172.16.16.1'}
ngfw-internal-vpn-address-space: {'NGFW EMEA 1': '172.16.16.1/32','NGFW US 1': '172.16.16.1/32','NGFW APAC 1': '172.16.16.1/32'}
```

# Results
The tool will print completion to the console, you can then see the results in the SMC