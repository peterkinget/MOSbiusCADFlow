import os
import pkg_resources

# Try to access the chip_config_data directory
print("Trying to access chip_config_data...")
try:
    data_path = pkg_resources.resource_filename('commandline', 'chip_config_data')
    print(f"Path: {data_path}")
    print(f"Exists: {os.path.exists(data_path)}")
    
    if os.path.exists(data_path):
        print("Files in chip_config_data:")
        for file in os.listdir(data_path):
            print(f"  - {file}")
    else:
        print("Directory does not exist")
except Exception as e:
    print(f"Error: {e}")

# Try to access the subckt_templates directory
print("\nTrying to access subckt_templates...")
try:
    templates_path = pkg_resources.resource_filename('commandline', 'subckt_templates')
    print(f"Path: {templates_path}")
    print(f"Exists: {os.path.exists(templates_path)}")
    
    if os.path.exists(templates_path):
        print("Files in subckt_templates:")
        for file in os.listdir(templates_path):
            print(f"  - {file}")
    else:
        print("Directory does not exist")
except Exception as e:
    print(f"Error: {e}")
