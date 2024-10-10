## Configuration File

The application uses a JSON configuration file to define the services to be managed. This file specifies the folder containing NSSM, the destination folder for batch files, and an array of services with their respective details.

### Configuration File Structure

The configuration file should be named `config.json` and should be structured as follows:

```json
{
    "nssm_folder": "files/",
    "dest_folder": "C:\\laragon\\www\\your-project-name",
    "services": [
        {
            "service_name": "service_one",
            "source_bat_path": "files/server1.bat"
        },
        {
            "service_name": "service_two",
            "source_bat_path": "files/server2.bat"
        },
        {
            "service_name": "service_three",
            "source_bat_path": "files/server3.bat"
        }
    ]
}

```
 `run` code
```cmd
python main.py

