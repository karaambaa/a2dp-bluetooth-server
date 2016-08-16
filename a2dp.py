from bluetoothctl import Bluetoothctl

print("Init bluetooth...")
bl = Bluetoothctl()
bl.start_agent()
bl.default_agent()
bl.make_discoverable()
print("Ready!")
info = True
while True:
    if info:
        if bl.is_connected():
            print('connected')
        else:
            print('not yet connected')
        info = False

    while not bl.is_connected():
        bl.child.expect('Request confirmation', timeout=None)
        bl.child.sendline('yes')
        for _ in range(3):
            bl.child.expect('Authorize service', timeout=8)
            bl.child.sendline('yes')
        info = True
