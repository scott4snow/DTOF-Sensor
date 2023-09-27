# Import the modules
import asyncio
import bleak
from bleak import BleakClient, BleakScanner
import tkinter as tk

# Define the address of the BLE device
address = "13:10:90:E8:89:E2"  # Replace with your device address

# Define the UUID of the characteristic to read
# Replace with your characteristic UUID
CHAR_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Define a function to scan for BLE devices

# Define a function to scan for BLE devices
async def scan():
    # Clear the listbox
    listbox.delete(0, tk.END)
    # Create a BleakScanner object
    scanner =  bleak.BleakScanner()
    # Start scanning for 2 seconds
    await scanner.start()
    await asyncio.sleep(2)
    await scanner.stop()
    # Get the scanned devices
    devices = await scanner.get_discovered_devices()
    # Loop through the devices and add them to the listbox
    for d in devices:
        listbox.insert(tk.END, f"{d.name} - {d.address}")

# Define a function to connect to a BLE device
async def connect():
    # Get the selected device from the listbox
    selection = listbox.curselection()
    if selection:
        # Get the device address
        device = listbox.get(selection[0]).split()[-1]

        # Connect to the Device
        async with BleakClient(device.address) as client:
            print(f'Connected to {device.address}')

            # Read the hex value from the characteristic UUID
            hex_value = await client.read_gatt_char(CHAR_UUID)
            print(hex_value)
            # Convert the hex value to decimal
            decimal_value = int(hex_value.hex(), 16)
            # Display the decimal value in the label
            label.config(text=f"Decimal value: {decimal_value}")
            # Disconnect from the device
            await client.disconnect()

    else:
        # No device selected
        label.config(text="Please select a device")


# Define a normal function that disconnects from the BLE device


def disconnect():
    async def close_connection():
        # Create a bleak client object with the address
        client = BleakClient(address)
        await client.disconnect()  # Disconnect from the BLE device
    # Create an asyncio task to run the async function
    asyncio.create_task(close_connection())


# Create a GUI window
window = tk.Tk()
window.title("Bleak GUI")

# Create a button to scan for devices
scan_button = tk.Button(window, text="Scan",
                        command=lambda: asyncio.run(scan()))
scan_button.pack()

# Create a listbox to display the devices
listbox = tk.Listbox(window)
listbox.pack()

# Create a button to connect to a device
connect_button = tk.Button(window, text="Connect",
                           command=lambda: asyncio.run(connect()))
connect_button.pack()

# Create another button widget that calls the disconnect function when clicked
disconnect_button = tk.Button(window, text="Disconnect",
                              command=lambda: asyncio.run(disconnect()))
disconnect_button.pack()  # Pack the button widget into the root window


# Create a label to display the decimal value
label = tk.Label(window, text="Decimal value: ")
label.pack()

# Start the main loop of the GUI
window.mainloop()
