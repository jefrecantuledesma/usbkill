#!/usr/bin/env python
import pyudev
import subprocess

def device_event(observer, device):
    action = device.action()
    if action == "add":
        print(f"USB Device Plugged In: {device}")
        power_off()
    elif action == "remove":
        print(f"USB Device Unplugged: {device}")
        power_off()

def power_off() -> None:
    print("Powering off the computer.")
    #UNCOMMENT WHEN READY
    subprocess.run(["systemctl", "poweroff"])

def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    observer = pyudev.MonitorObserver(monitor, device_event)
    observer.start()

    try:
        print("Monitoring USB devices. Press Ctrl+C to exit.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()

