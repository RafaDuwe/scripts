from napalm import get_network_driver

routers = {
    "R1": {"hostname": "192.168.1.1", "username": "admin", "password": "rafa"},
    "R2": {"hostname": "192.168.1.2", "username": "admin", "password": "rafa"},
    "R3": {"hostname": "192.168.1.3", "username": "admin", "password": "rafa"}
}

def get_router_info(router_name, router_data):
    driver = get_network_driver("ios")  
    device = driver(
        hostname=router_data["hostname"],
        username=router_data["username"],
        password=router_data["password"]
    )
    
    try:
        device.open()
        info = device.get_facts()
        print(f"{router_name} ({router_data['hostname']}):")
        print(f"  Modelo: {info['model']}")
        print(f"  Versão do IOS: {info['os_version']}")
        print(f"  Uptime: {info['uptime']} segundos")
        print(f"  Número de interfaces: {len(info['interface_list'])}")
        print("-" * 40)
        device.close()
    except Exception as e:
        print(f"Erro ao conectar no {router_name}: {e}")

for name, data in routers.items():
    get_router_info(name, data)
