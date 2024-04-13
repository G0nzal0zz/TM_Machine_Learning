## Copy Plugin Script

This script is designed to copy the `Plugin.as` file from a GitHub repository to the `TmInterface\Plugins` folder. It automates the process of updating the `Plugin.as` file in the `TmInterface\Plugins` folder with the latest version from the repository.

### Usage

1. **Setting up the Environment:**
   - Create a file named `.env` in the same directory as the script (`copy_plugin.bat`).
   - In `.env`, specify the source path of the `Plugin.as` file in the GitHub repository and the destination path of the `TmInterface` folder in the following format (**see .env.example**):
     ```
     SOURCE_PATH=C:\path\to\github\repository\Plugin.as
     DESTINATION_PATH=C:\path\to\TmInterface\
     ```
   - Ensure that the paths are correctly formatted and point to valid files and directories.

2. **Running the Script:**
   - Execute the `copy_plugin.bat` script.
   - The script will read the paths from `.env`, copy the `Plugin.as` file from the source path to the destination path (`TmInterface` folder), and then attempt to open the copied file.

### Note

- Ensure that the script (`copy_plugin.bat`) is located in the same directory as the `.env` file.
- The script assumes that the `TmInterface\Plugins` folder already exists in the specified destination path.
- Make sure to update the `SOURCE_PATH` in `.env` with the correct path to the `Plugin.as` file in your GitHub repository.
- It's recommended to run this script periodically to keep the `Plugin.as` file in the `TmInterface` folder up-to-date with the latest changes from the repository.