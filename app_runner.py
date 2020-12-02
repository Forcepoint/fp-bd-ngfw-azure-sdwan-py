from smc import session

from config import Config
from create_vpn import build_vpn_smc

# # Open config files
config = Config()
config.load_azure_config()
config.load_smc_config()
azure_config = config.azure_data

# Pull SMC details from config and build url
smc_host = config.get_smc('smc-host')
smc_port = config.get_smc('smc-port')
smc_api_key = config.get_smc('smc-api-key')
smc_api_version = config.get_smc('smc-api-version')
gateway_profile = config.get_smc('gateway-profile')

smc_url = f"http://{smc_host}:{smc_port}"

azure_remote_ips = {}

for gateway_config in azure_config:
    for vpn_site_connection in gateway_config['vpnSiteConnections']:

        azure_region = vpn_site_connection['hubConfiguration']['Region']
        psk = vpn_site_connection['connectionConfiguration']['PSK']

        ip_addrs = []

        for ip in vpn_site_connection['gatewayConfiguration']['IpAddresses'].values():
            ip_addrs.append(ip)

        azure_remote_ips[azure_region] = (ip_addrs, psk)

session.login(url=smc_url, api_key=smc_api_key, api_version=str(smc_api_version))

ngfw_external_endpoint_ips = config.get_smc('ngfw-external-interface-ip')
ngfw_internal_vpn_endpoint_ips = config.get_smc('ngfw-internal-vpn-interface-ip')
ngfw_external_network_address_space = config.get_smc('ngfw-external-address-space')
ngfw_internal_vpn_address_space = config.get_smc('ngfw-internal-vpn-address-space')

for ngfw_azure_location in config.get_smc('ngfw-azure-locations'):
    for key in ngfw_azure_location.keys():
        build_vpn_smc(
            key,
            gateway_profile,
            azure_remote_ips[ngfw_azure_location[key]] + (ngfw_external_endpoint_ips[key],),
            ngfw_external_network_address_space[key],
            ngfw_internal_vpn_endpoint_ips[key],
            ngfw_internal_vpn_address_space[key]
        )

print("Completed. Please verify success in the SMC console as per the instructions in the guide...")

session.logout()
