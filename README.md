# Green Credits MP

## Overview

Green Credits MP is a Python-based application designed to facilitate the management and trading of carbon credits. It provides an interactive dashboard for users to track their credits, view marketplace statistics, and explore projects to offset their carbon emissions.

---

## Technical Details

### **Core Technologies**
- **Python**: The primary programming language for the application.
- **Streamlit**: Used to build an interactive web-based dashboard.
- **Poetry**: For dependency management and packaging.
- **PyPDF**: For extracting text from PDF files.
- **python-docx**: For extracting text from `.docx` files.

### **File Structure**
- **`Home.py`**: The main dashboard page for the application.
- **`content_util.py`**: Utility functions for extracting text from various file formats (PDF, DOCX, plain text).
- **`streamlit_app.py`**: (If applicable) Manages the Streamlit application and routes.
- **`tests/`**: Contains unit tests for validating the functionality of the application.

---

## Home Page Functionality

The `Home.py` file serves as the landing page for the Carbon Credit Marketplace application. It provides the following features:

1. **Dashboard Overview**:
   - Displays a welcoming message and introduces the purpose of the platform.

2. **Key Metrics**:
   - Highlights important statistics such as:
     - Total credits owned.
     - Total credits purchased.
     - Total CO₂ offset (with an equivalent in trees planted).

3. **Recent Transactions**:
   - Shows a table of recent credit purchases, including details like date, project name, credits purchased, and cost.

4. **Marketplace Statistics**:
   - Provides an overview of the marketplace, including:
     - Total verified projects.
     - Average price per credit.
     - Number of global participants.

5. **Call-to-Action**:
   - Encourages users to explore more projects and offset additional emissions.

---

## Utility Functions

The `content_util.py` file contains the `ContentManager` class, which provides the following functionalities:

1. **Extract Content from Files**:
   - Supports PDF, plain text, and DOCX file formats.
   - Uses libraries like `pypdf` and `python-docx` for text extraction.

2. **Dynamic Content Handling**:
   - Determines the file type and delegates extraction to the appropriate method.
   - Logs warnings for unsupported file types.

3. **Methods**:
   - `extract_from_pdf_bytes`: Extracts text from PDF files.
   - `extract_from_text_bytes`: Extracts text from plain text files.
   - `extract_from_docx_bytes`: Extracts text from DOCX files.

---

## Usage

1. **Set up the environment**:
   - Install Poetry using `pip install poetry`.
   - Initialize or activate the Poetry environment in your project.

2. **Install dependencies**:
   - Add required packages using `poetry add package_name`.

3. **Run the application**:
   - Start the Streamlit app using:
     ```bash
     streamlit run Home.py
     ```

4. **Generate an executable**:
   - Use `poetry run pyinstaller --onefile --windowed main.py` to create a standalone `.exe` file.

---

## Future Enhancements

1. **Dynamic Data Integration**:
   - Replace hardcoded values in `Home.py` with data fetched from a database or API.

2. **Enhanced Visualizations**:
   - Add charts or graphs to visualize trends in credit purchases or offsets over time.

3. **User Authentication**:
   - Implement user-specific dashboards based on login credentials.

---

This project is designed to simplify carbon credit management while providing an intuitive user experience through its interactive dashboard.