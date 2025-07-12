# Green Credits MP

## Overview
Green Credits MP is a platform designed to help farmers manage their carbon credits. It provides features such as user authentication, personal information management, cultivation details tracking, and a dashboard for monitoring activities.

## Features
- **Login and Registration**: Secure login and registration for farmers.
- **Farmer Dashboard**: A central hub for managing personal information, cultivation details, and carbon credit scores.
- **Personal Information Management**: Update and manage personal details.
- **Cultivation Details**: Add and track cultivation-related information, including crop type, area size, and geo-location.
- **Information Preview**: show all personal and cultivation details .

## Installation

### Poetry
Poetry is used for dependency management and packaging.

1. Install Poetry:
   ```sh
   pip install poetry
   ```
2. Create a new project:
   ```sh
   poetry new myproject
   ```
3. Initialize in an existing project:
   ```sh
   poetry init
   ```
4. Activate the virtual environment:
   ```sh
   poetry env activate
   ```
5. Install packages:
   ```sh
   poetry add package_name
   ```

## Generate EXE
************
To generate an executable file, use PyInstaller with the following command:
```sh
poetry run pyinstaller --onefile --windowed main.py
```


## Streamlit
*********
To run the Streamlit app, use the following command:
```sh
streamlit run first_app.py

