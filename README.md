## Summary of Workflow

This section outlines the typical workflow for using your PDF Analyzer project.


### To begin working with the PDF Analyzer project, you'll first need to **clone the model repository** from GitHub.

 1. **Open your terminal or command prompt and run the following command:

```bash
git clone https://github.com/huridocs/pdf-document-layout-analysis.git
+```
 
 This section outlines the typical workflow for using your PDF Analyzer project.

### To Start Working on Your Project

1.  **Start the HURIDOCS Docker Container:**
    * Open your terminal or command prompt.
    * You can run this command from any directory.
    * **First Time Run / After System Restart:** If this is your **very first time running** the project, or if you have previously run `docker rm huridocs_analyzer` (deleted the container), you will need to **build and run** it:
        ```bash
        # Navigate to the HURIDOCS directory first: cd pdf-document-layout-analysis
        docker build -t huridocs-pdf-analyzer .
        docker run -d -p 5060:5060 --name huridocs_analyzer --platform linux/amd64 huridocs-pdf-analyzer
        ```
    * **Subsequent Runs (Container Already Built and Exists):** If you've previously built the image and the container exists (you just stopped it), you only need to start it:
        ```bash
        docker start huridocs_analyzer
        ```
    * **Important:** After running the `docker run` or `docker start` command, wait for about 10-20 seconds for the service inside the container to fully initialize and become ready to process requests.

2.  **Activate Your Python Virtual Environment:**
    * Open a **separate terminal window** (keep the Docker terminal open).
    * Navigate to your project directory (`pdf_analyzer_huridocs`).
    ```bash
    cd /path/to/your/pdf_analyzer_huridocs # Replace with your actual path
    ```
    * Activate the virtual environment:
        * **On macOS / Linux:**
            ```bash
            source venv/bin/activate
            ```
        * **On Windows (Command Prompt):**
            ```cmd
            .\venv\Scripts\activate
            ```
        * **On Windows (PowerShell):**
            ```powershell
            .\venv\Scripts\Activate.ps1
            ```

3.  **Run Your Analysis Script:**
    * With the virtual environment active, execute your Python script to process PDFs in the `input/` folder.
    ```bash
    python pdf_processor.py
    ```

### To Stop Working

1.  **Deactivate Your Python Virtual Environment:**
    * In the terminal where your Python environment is active:
    ```bash
    deactivate
    ```

2.  **Stop the HURIDOCS Docker Container:**
    * In the terminal where your Docker container is running (or any terminal):
    ```bash
    docker stop huridocs_analyzer
    ```