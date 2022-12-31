
import usb.core
import usb.util

dev = usb.core.find(idVendor=0x1504, idProduct=0x0108)

# Detach the kernel driver
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]
ep = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match=lambda e: \
    usb.util.endpoint_direction(e.bEndpointAddress) == \
    usb.util.ENDPOINT_IN
)

# Print a message
ep.write("PI\r\n")

# Release the device
usb.util.dispose_resources(dev)
