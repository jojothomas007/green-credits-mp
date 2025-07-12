# 🌾 Farmer Data Management Portal

This is a Streamlit-based web application for managing farmer data. The app allows users to upload farmer data in JSON format, search for farmers by name, and verify geo-location details for crops.

## Features

1. **Login System**:
   - Secure login with username and password.

2. **Upload Farmer Data**:
   - Upload a JSON file containing farmer details.
   - Displays personal and cultivation information.

3. **Search Farmer**:
   - Search for a farmer by name.
   - Displays personal and cultivation information if a match is found.
   - If no match is found, dummy data is displayed.

4. **Geo-Location Verification**:
   - Verify geo-location for each crop.
   - Displays a green "✅ Verified" status upon verification.
   - Includes a "Quarterly Check-in" button to reset the status to "⚠️ Not Verified."


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/farmer-data-portal.git
   cd farmer-data-portal
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

- Access the application in your web browser at `http://localhost:8501`.
- Log in using the credentials 
- Upload a JSON file with farmer data 
- Search for farmers and verify geo-location details as needed.

## Development

- This project is built using Python, Streamlit, and other open-source libraries.
- Contributions are welcome! Please submit a pull request or open an issue for discussion.


## Acknowledgments

- Inspired by the need for efficient farmer data management and accessibility.
- Built with passion for empowering farmers and enhancing agricultural productivity.