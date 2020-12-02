from smc.elements.network import Network
from smc.core.engine import Engine
from smc.vpn.elements import GatewayProfile, ExternalGateway
from smc.vpn.route import RouteVPN, TunnelEndpoint


def build_vpn_smc(smc_engine_name, gateway_profile, tunnel_config, external_network_address_space,
                  internal_vpn_endpoint_ip, internal_vpn_address_space):
    engine = Engine(smc_engine_name)

    try:
        tunnel_if = engine.tunnel_interface.get(1000)
    except:
        tunnel_if = None
        print("Interface doesn't exist, creating it now...")

    if tunnel_if:
        print("tunnel interface already exists")
    else:
        engine.tunnel_interface.add_layer3_interface(
            interface_id=1000,
            address=internal_vpn_endpoint_ip,
            network_value=internal_vpn_address_space)

    # Enable VPN on the 'Internal Endpoint' interface
    vpn_endpoint = engine.vpn_endpoint.get_contains(tunnel_config[2])
    vpn_endpoint.update(enabled=True)

    tunnel_if = engine.tunnel_interface.get(1000)

    local_endpoint = TunnelEndpoint.create_ipsec_endpoint(engine.vpn.internal_gateway, tunnel_if)

    # Create the remote side network elements
    Network.get_or_create(
        name=smc_engine_name + ' Azure-vpn-internal-net',
        ipv4_network=external_network_address_space)

    # TODO add gatewayProfile name to config and default to 'Default (all capabilities)' if empty
    if gateway_profile:
        print("Using gateway profie: " + gateway_profile)
        gw_profile = GatewayProfile(gateway_profile)
    else:
        print("Using gateway profie: Default (all capabilities)")
        gw_profile = GatewayProfile("Default (all capabilities)")

    gw = ExternalGateway.get_or_create(
        name=smc_engine_name + ' Azure-vpn-gw',
        gateway_profile=gw_profile)

    try:
        gw.external_endpoint.create(
            name=smc_engine_name + ' Azure-vpn-endpoint-1',
            address=tunnel_config[0][0])

        gw.external_endpoint.create(
            name=smc_engine_name + ' Azure-vpn-endpoint-2',
            address=tunnel_config[0][1])
    except:
        print("Endpoints already exist")

    try:
        gw.vpn_site.create(
            name=smc_engine_name + ' Azure-vpn-site',
            site_element=[Network(smc_engine_name + ' Azure-vpn-internal-net')])
    except:
        print("Azure-vpn-site already exists")

    remote_endpoint = TunnelEndpoint.create_ipsec_endpoint(gw)

    try:
        ipsec_tunnel = RouteVPN().get(name=smc_engine_name + ' Azure-VPN')
    except:
        print("IPSEC tunnels don't exist, creating them now...")
        ipsec_tunnel = None

    if ipsec_tunnel:
        print("IPSEC tunnel already exists")
    else:
        RouteVPN.create_ipsec_tunnel(
            name=smc_engine_name + ' Azure-VPN',
            preshared_key=tunnel_config[1],
            local_endpoint=local_endpoint,
            remote_endpoint=remote_endpoint)
