# UDMI Device Management

This Python script provides utilities for managing device key files within a specified directory structure, focusing on devices that are associated with a `gateway_id` in their `metadata.json` files.

## Features

* **List Eligible Devices**: Identify and list device folders that contain both a `gateway_id` in their `metadata.json` and also have `.pem` or `.pkcs8` key files present. The output is saved to a text file.
* **Clean Unnecessary Key Files**: Based on a provided list of device names, remove all `.pem` and `.pkcs8` key files from device folders that have a `gateway_id` in their `metadata.json`.

## File Structure Assumption

The script assumes a directory structure similar to the following, where device folders (e.g., `ADY-1`, `AHU-14`) are direct subdirectories of a `devices` folder:

```bash
udmi/
└── devices/
├── ADY-1/
│   ├── metadata.json
│   ├── rsa_private.pem
│   └── rsa_public.pem
├── AHU-14/
│   ├── metadata.json
│   ├── rsa_private.pem
│   └── rsa_public.pem
└── ...
```

## Usage

The script can be run from the command line with different arguments to perform its two main functions.

### Prerequisites

* Python 3.x installed on your system.

### Running the Script

1.  **Clone the Repository**
2.  **Navigate to the directory**: Open your terminal or command prompt and change your current directory to where you have cloned the UDMI Device Management repository.

#### 1. Listing Eligible Devices

To find and list devices that have a `gateway_id` in their `metadata.json` and also contain `.pem` or `.pkcs8` key files, use the `list` mode:

```bash
python3 udmi_device_management.py list --directory udmi/devices --output_file eligible_devices.txt
```

- `list`: Specifies the operation mode to list devices.
- `--directory udmi/devices`: (Optional) Specifies the base directory where your device folders are located. Defaults to `udmi/devices`
- `--output_file eligible_devices.txt`: (Optional) Specifies the name of the file where the list of eligible device names will be saved. Defaults to `eligible_devices.txt`

#### 2. Cleaning Unnecessary Key Files

To remove `.pem` and `.pkcs8` key files from devices that were identified as eligible (i.e., those with a `gateway_id` in their `metadata.json`), use the `clean` mode. It is highly recommended to run the list command first to generate the `eligible_devices.txt` file before running the `clean` command.

```bash
python3 udmi_device_management.py clean --directory udmi/devices --devices_file eligible_devices.txt
```

- `clean`: Specifies the operation mode to clean key files.
- `--directory udmi/devices`: (Optional) Specifies the base directory containing your device folders. Defaults to `udmi/devices`.
- `--devices_file eligible_devices.txt`: (Optional) Specifies the name of the file containing the list of device names to process for key removal. Defaults to `eligible_devices.txt`.

This command will iterate through the devices listed in `eligible_devices.txt` and remove all `.pem` and `.pkcs8` files from their respective folders if their metadata.json confirms the presence of a `gateway_id`.