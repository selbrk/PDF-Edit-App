# **PDF Edit App**

A Python-based GUI application that allows users to view, edit, merge, and manipulate PDF files using an intuitive interface built with **Tkinter**. The app provides essential PDF editing capabilities, including page rotation, zooming, and merging multiple PDFs into one.

---

##  **Features**
- **View PDF Files:** Displays PDF pages as images with scrollable navigation.
- **Page Rotation:** Rotate selected pages or all pages clockwise or counterclockwise.
- **Zoom In/Out:** Dynamically adjust the size of displayed PDF pages.
- **Page Selection:** Select pages to create a new PDF from chosen or unchosen pages.
- **Merge PDFs:** Combine multiple PDF files into a single PDF.
- **Save/Download PDFs:** Export the edited PDF to a new file.

---

##  **Requirements**

Make sure you have the following installed:

- **Python 3.8+**
- Required Python libraries:
  - `pypdf`
  - `pdf2image`
  - `Pillow`
  - `tkinter` (comes pre-installed with most Python distributions)

You can install the dependencies with:

```bash
pip install -r requirements.txt
```



---

## **Installation and Setup**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/selbrk/PDF-Edit-App.git
   cd PDF-Edit-App
   ```

2. **Create a Virtual Environment (Recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   .\venv\Scripts\activate   # On Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Poppler** (For `pdf2image` to work):
   - **macOS**:  
     ```bash
     brew install poppler
     ```
   - **Linux (Ubuntu/Debian)**:  
     ```bash
     sudo apt-get install poppler-utils
     ```
   - **Windows**:  
     Download [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)  
     Add the path to the `bin` directory to your system’s PATH environment variable.

---

##  **Usage**

1. Run the application:
   ```bash
   python main.py
   ```

2. Use the graphical interface to:
   - Open and view PDF files.
   - Select pages to create a new PDF or remove unwanted pages.
   - Rotate individual or all pages.
   - Zoom in/out for better visibility.
   - Merge multiple PDFs into one file.

---

## ️ **Features in Detail**

| **Feature**              | **Description**                                                                 |
|-------------------------|---------------------------------------------------------------------------------|
| **View PDF**             | Opens and displays all pages of a selected PDF as scrollable images.           |
| **Page Rotation**        | Rotate selected or all pages in 90° increments clockwise or counterclockwise.  |
| **Zoom In/Out**          | Adjusts the zoom level dynamically to fit pages within the window.             |
| **Page Selection**       | Select pages to export a subset of the original PDF or remove unwanted pages.  |
| **Merge PDFs**           | Select and merge multiple PDFs into a single output file.                      |
| **Download Edited PDF**  | Save the final edited/merged PDF file to a location of your choice.            |




