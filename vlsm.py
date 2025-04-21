import ipaddress
import math

def get_prefix_from_mask(mask_str):
    try:
        return ipaddress.IPv4Network(f"0.0.0.0/{mask_str}").prefixlen
    except ValueError:
        print("Invalid subnet mask.")
        return None

def calculate_vlsm(base_ip, subnet_mask, host_requirements):
    prefix = get_prefix_from_mask(subnet_mask)
    if prefix is None:
        return []

    try:
        network = ipaddress.IPv4Network(f"{base_ip}/{prefix}", strict=False)
    except ValueError as e:
        print("Invalid base IP or subnet mask.")
        return []

    host_requirements.sort(reverse=True)
    subnets = []
    current_ip = network.network_address

    for hosts in host_requirements:
        needed_hosts = hosts + 2  # inclui endereço de rede e de broadcast
        subnet_prefix = 32 - math.ceil(math.log2(needed_hosts))
        try:
            subnet = ipaddress.IPv4Network((current_ip, subnet_prefix), strict=False)
        except ValueError:
            print(f"Unable to create subnet for {hosts} hosts.")
            break

        # verifica se a subrede cabe dentro do range
        if subnet.network_address not in network or subnet.broadcast_address > network.broadcast_address:
            print(f"Subnet {subnet} does not fit in the base network.")
            break

        subnets.append(subnet)
        current_ip = subnet.broadcast_address + 1

    return subnets

# --- Main Program ---
if __name__ == "__main__":
    base_ip = input("Enter the base IP address (e.g., 192.168.0.0): ")
    subnet_mask = input("Enter the subnet mask (e.g., 255.255.255.0): ")
    host_input = input("Enter host requirements separated by commas (e.g., 50,20,10): ")

    try:
        host_requirements = [int(h.strip()) for h in host_input.split(",")]
    except ValueError:
        print("Invalid host requirements. Please enter numbers separated by commas.")
        exit(1)

    result = calculate_vlsm(base_ip, subnet_mask, host_requirements)

    if result:
        print("\nVLSM Subnet Allocation:")
        for i, subnet in enumerate(result, start=1):
            usable_hosts = list(subnet.hosts())
            print(f"Subnet {i}: {subnet}")
            print(f"  Usable IPs: {usable_hosts[0]} - {usable_hosts[-1]}")
            print(f"  Subnet Mask: {subnet.netmask}")
            print(f"  Broadcast Address: {subnet.broadcast_address}\n")
