import usb.core
import usb.util

# Encontre o dispositivo USB pelo ID do fornecedor e do produto
vendor_id = 0x046d   # Substitua XXXX pelo ID do fornecedor do seu dispositivo
product_id = 0xc077  # Substitua XXXX pelo ID do produto do seu dispositivo

# Tente encontrar o dispositivo
device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

# Verifique se o dispositivo foi encontrado
if device is None:
    raise ValueError("Dispositivo USB não encontrado")

try:
    # Verifique se o kernel do sistema operacional tem o dispositivo
    if device.is_kernel_driver_active(0):
        device.detach_kernel_driver(0)

    # Reclame a interface
    usb.util.claim_interface(device, 0)

    # Agora que temos acesso ao dispositivo, leia dados brutos
    endpoint = device[0][(0, 0)][0]  # Endpoint de leitura

    while True:
        try:
            data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            print("Dados recebidos:", data)
            # Faça o que for necessário com os dados recebidos aqui
        except usb.core.USBError as e:
            if e.args == ('Operation timed out',):
                continue
finally:
    # Libere a interface e reverta quaisquer mudanças feitas no kernel
    usb.util.release_interface(device, 0)
    usb.util.dispose_resources(device)
