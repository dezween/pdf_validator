
## PDF Validator App

This is a PDF validation application using a GUI created with PyQt5 and a backend server for processing files, deployed on Railway.

### Requirements

- Python 3.9 or later
- PyQt5
- requests

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/dezween/pdf_validator.git
   cd pdf_validator
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

1. **Run the application:**

   ```sh
   python client.py
   ```

### P.S. After you run the file and click the button in the application window, wait for the client to send a request to the server and receive a response. This may take about 5 seconds. After that you will get a pop-up window with the message “Файл соответствует эталону.” if the request was successful and the server was able to process the pdf file and it was valid or another message - an error message indicating that the pdf file does not match the benchmark.


### Files

- `client.py` — The client file to run the client application.
- `server.py` — The server file for processing PDF files (deployed on Railway). (not in this repo)
- `task2.py` — Additional script for data processing.
- `requirements.txt` — All project requirements.
- `test_task.pdf` — the ile to test the project.
- `test_task — копия.pdf` — Another file to test the project.


### Additional Information

Make sure the server is correctly deployed and accessible at `https://pdfvalidator.up.railway.app/validate`.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.