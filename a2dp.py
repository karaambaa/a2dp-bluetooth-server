from bluetoothctl import Bluetoothctl
from subprocess import call

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
            call(["pulseaudio", "--start"])
            print('connected')
        else:
            print('not yet connected')
        info = False

    while not bl.is_connected():
        call(["pulseaudio", "--kill"])
        bl.child.expect('Request confirmation', timeout=None)
        bl.child.sendline('yes')
        for _ in range(3):
            bl.child.expect('Authorize service', timeout=8)
            bl.child.sendline('yes')
        info = True
