import os
import shutil
import platform
import subprocess
import time
import logging
import json


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def is_nssm_installed():
    """Check if NSSM is already installed by looking for its executable in System32."""
    nssm_path = os.path.join(os.environ['windir'], 'System32', 'nssm.exe')
    return os.path.isfile(nssm_path)

def install_nssm(nssm_folder):
    """Copy the correct version of NSSM to System32 based on the Windows architecture."""
    if is_nssm_installed():
        logging.info("NSSM is already installed. Skipping installation.")
        return

    system32_path = os.path.join(os.environ['windir'], 'System32')


    architecture = platform.architecture()[0]
    
    if architecture == '64bit':
        nssm_executable = os.path.join(nssm_folder, 'win64', 'nssm.exe')
    else:
        nssm_executable = os.path.join(nssm_folder, 'win32', 'nssm.exe')


    shutil.copy(nssm_executable, system32_path)
    logging.info(f"Installed NSSM to System32 from {nssm_executable}.")

def copy_bat_file(source_bat_path, dest_folder):
    """Copy the BAT file to the specified destination folder."""
    try:
        shutil.copy(source_bat_path, dest_folder)
        logging.info(f"Copied '{source_bat_path}' to '{dest_folder}'.")
    except Exception as e:
        logging.error(f"Error copying BAT file: {e}")

def create_service(service_name, bat_file_path):
    """Check if a Windows service exists, stop it if running, remove it, and create a new service to run the specified BAT file using NSSM."""
    try:

        nssm_path = os.path.join(os.environ['windir'], 'System32', 'nssm.exe')

        query_command = [nssm_path, 'status', service_name]
        result = subprocess.run(query_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            status_output = result.stdout.decode().strip()
            if "RUNNING" in status_output:
                logging.info(f"Stopping service '{service_name}'...")
                stop_command = ['sc', 'stop', service_name]
                stop_result = subprocess.run(stop_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


            remove_command = ['sc', 'delete', service_name]
            remove_result = subprocess.run(remove_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if remove_result.returncode == 0:
                logging.info(f"Service '{service_name}' removed successfully.")
            else:
                logging.error(f"Failed to remove service '{service_name}'. Error: {remove_result.stderr.decode().strip()}")
        time.sleep(4)
        
        command = [
            nssm_path, 'install', service_name,
            bat_file_path
        ]
        
        subprocess.run(command, check=True)
        logging.info(f"Service '{service_name}' created successfully to run '{bat_file_path}'.")

        subprocess.run([nssm_path, 'start', service_name], check=True)
        logging.info(f"Service '{service_name}' started successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating or starting service '{service_name}': {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    config_file = "config.json"
    config = load_config(config_file)

    extracted_nssm_folder = config['nssm_folder']

    dest_folder = config['dest_folder']

    for service in config['services']:
        service_name = service['service_name']
        source_bat_path = service['source_bat_path']
        
        try:
            install_nssm(extracted_nssm_folder)


            copy_bat_file(source_bat_path, dest_folder)

            bat_file_path = os.path.join(dest_folder, os.path.basename(source_bat_path))
            create_service(service_name, bat_file_path)

        except Exception as e:
            logging.error(f"An error occurred while creating service '{service_name}': {e}")

if __name__ == "__main__":
    main()
