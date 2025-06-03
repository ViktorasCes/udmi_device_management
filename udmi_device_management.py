import os # Imports the 'os' module, which provides a way of using operating system dependent functionality, such as reading or writing to the file system.
import json # Imports the 'json' module, which allows working with JSON (JavaScript Object Notation) data.

def find_and_list_devices(base_directory, output_file):
    """
    Searches for device folders that contain a 'gateway_id' in their metadata.json
    and also have key files (ending in .pem or .pkcs8). The results are written to a text file.

    Args:
        base_directory (str): The root directory to start the search from (e.g., 'udmi/devices').
        output_file (str): The path to the text file where the results will be saved.
    """
    # Prints a message indicating the start of the device search.
    print(f"Searching for devices in '{base_directory}'...")
    # Initialises an empty list to store the names of eligible device folders.
    eligible_devices = []

    # Defines the key file extensions to look for when listing devices.
    key_extensions = ('.pem', '.pkcs8')

    # Walks through the directory tree, starting from the base_directory.
    # root: The current directory path.
    # dirs: A list of subdirectories in the current directory.
    # files: A list of files in the current directory.
    for root, dirs, files in os.walk(base_directory):
        # Checks if the current directory is a device folder (i.e., it's not the base_directory itself
        # and it's a direct subdirectory of 'devices').
        if os.path.basename(root) != 'devices' and 'devices' in root.split(os.sep):
            device_name = os.path.basename(root) # Extracts the name of the current device folder.
            metadata_path = os.path.join(root, 'metadata.json') # Constructs the full path to the metadata.json file.
            has_gateway_id = False # Flag to indicate if 'gateway_id' is found in metadata.
            has_keys = False # Flag to indicate if any key files (.pem or .pkcs8) are found.

            # Checks if the metadata.json file exists in the current device folder.
            if os.path.exists(metadata_path):
                try:
                    # Opens and reads the metadata.json file.
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f) # Parses the JSON content of the file.
                        # Checks if 'gateway' and 'gateway_id' keys exist in the metadata.
                        if 'gateway' in metadata and 'gateway_id' in metadata['gateway']:
                            has_gateway_id = True # Sets the flag to True if 'gateway_id' is found.
                except json.JSONDecodeError:
                    # Prints an error message if the metadata.json file is not valid JSON.
                    print(f"Warning: Could not parse '{metadata_path}'. Skipping.")
                except Exception as e:
                    # Catches any other exceptions during file processing.
                    print(f"An error occurred reading '{metadata_path}': {e}")

            # Checks for .pem or .pkcs8 files in the current device folder.
            for file in files:
                if file.endswith(key_extensions): # Checks if the file ends with any of the defined key extensions.
                    has_keys = True # Sets the flag to True if any key file is found.
                    break # Exits the loop once a key file is found as we only need to know if at least one exists.

            # If both conditions are met, adds the device name to the list of eligible devices.
            if has_gateway_id and has_keys:
                eligible_devices.append(device_name)
                print(f"Found eligible device: {device_name}") # Confirms finding an eligible device.

    # Writes the list of eligible devices to the specified output file.
    with open(output_file, 'w', encoding='utf-8') as f:
        for device in eligible_devices:
            f.write(f"{device}\n") # Writes each device name on a new line.

    # Prints a confirmation message about where the results have been saved.
    print(f"\nEligible devices listed in '{output_file}'.")

def remove_unnecessary_key_files(base_directory, devices_file):
    """
    Reads a list of device names from a file and, for each device,
    removes all .pem and .pkcs8 key files if its metadata.json contains a 'gateway_id'.

    Args:
        base_directory (str): The root directory containing the device folders.
        devices_file (str): The path to the text file containing the list of device names.
    """
    # Prints a message indicating the start of the key file removal process.
    print(f"Starting key file removal for devices listed in '{devices_file}'...")
    devices_to_process = [] # Initialises an empty list to store device names from the input file.

    # Checks if the devices file exists.
    if not os.path.exists(devices_file):
        # Prints an error and exits if the file is not found.
        print(f"Error: Devices file '{devices_file}' not found. Aborting key removal.")
        return

    # Reads the device names from the provided file.
    with open(devices_file, 'r', encoding='utf-8') as f:
        for line in f:
            devices_to_process.append(line.strip()) # Adds each device name, removing leading/trailing whitespace.

    # Defines the file extensions to be removed.
    extensions_to_remove = ('.pem', '.pkcs8')

    # Iterates through each device name that needs processing.
    for device_name in devices_to_process:
        device_path = os.path.join(base_directory, device_name) # Constructs the full path to the device folder.
        metadata_path = os.path.join(device_path, 'metadata.json') # Constructs the full path to the metadata.json.
        has_gateway_id = False # Flag to check for 'gateway_id'.

        # Checks if the device folder exists.
        if not os.path.isdir(device_path):
            print(f"Warning: Device folder '{device_path}' not found. Skipping.")
            continue # Skips to the next device if the folder doesn't exist.

        # Checks if metadata.json exists and contains 'gateway_id'.
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    if 'gateway' in metadata and 'gateway_id' in metadata['gateway']:
                        has_gateway_id = True
            except json.JSONDecodeError:
                print(f"Warning: Could not parse '{metadata_path}'. Skipping key removal for this device.")
                continue # Skips if metadata is malformed.
            except Exception as e:
                print(f"An error occurred reading '{metadata_path}': {e}")
                continue # Skips on other errors.

        # If 'gateway_id' is found, proceeds to remove .pem and .pkcs8 files.
        if has_gateway_id:
            print(f"Processing device '{device_name}' (has gateway_id).")
            # Iterates through all files in the device directory.
            for file_name in os.listdir(device_path):
                # Checks if the file ends with any of the specified extensions.
                if file_name.endswith(extensions_to_remove):
                    file_to_remove = os.path.join(device_path, file_name) # Constructs the full path to the file.
                    try:
                        os.remove(file_to_remove) # Attempts to delete the file.
                        print(f"  Removed: {file_to_remove}") # Confirms successful removal.
                    except OSError as e:
                        # Prints an error if the file could not be removed.
                        print(f"  Error removing '{file_to_remove}': {e}")
        else:
            # Informs if a device is skipped because it lacks a 'gateway_id'.
            print(f"Skipping device '{device_name}' (no gateway_id found in metadata.json).")

    # Prints a message indicating the completion of the key file removal process.
    print("\nKey file removal process completed.")

if __name__ == "__main__":
    import argparse # Imports the 'argparse' module for parsing command-line arguments.

    # Creates an ArgumentParser object to handle command-line arguments.
    parser = argparse.ArgumentParser(
        description="Manages device key files based on metadata.json content."
    )

    # Defines the 'mode' argument, which is mandatory and determines the script's operation.
    parser.add_argument(
        'mode',
        choices=['list', 'clean'], # Specifies the allowed values for 'mode'.
        help="Operation mode: 'list' to find and list devices, 'clean' to remove key files."
    )

    # Defines the 'directory' argument, specifying the base directory for device folders.
    parser.add_argument(
        '--directory',
        default='udmi/devices', # Sets a default value for the directory.
        help="Base directory containing device folders (default: 'udmi/devices')."
    )

    # Defines the 'output_file' argument, used when in 'list' mode.
    parser.add_argument(
        '--output_file',
        default='eligible_devices.txt', # Sets a default output file name.
        help="Output file for eligible device names (used with 'list' mode, default: 'eligible_devices.txt')."
    )

    # Defines the 'devices_file' argument, used when in 'clean' mode.
    parser.add_argument(
        '--devices_file',
        default='eligible_devices.txt', # Sets a default input file name.
        help="Input file containing device names to clean (used with 'clean' mode, default: 'eligible_devices.txt')."
    )

    args = parser.parse_args() # Parses the command-line arguments provided by the user.

    # Checks the 'mode' argument and calls the appropriate function.
    if args.mode == 'list':
        find_and_list_devices(args.directory, args.output_file) # Calls the function to find and list devices.
    elif args.mode == 'clean':
        remove_unnecessary_key_files(args.directory, args.devices_file) # Calls the function to remove key files.
