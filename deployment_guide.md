# Deployment Guide for VizAI

## Do I need a Cloud Platform?
**Short Answer:** It depends on who needs to use your app.

| **Scenario** | **Deployment Type** | **Cost** | **Difficulty** |
| :--- | :--- | :--- | :--- |
| **Just for me** | **Local (Your PC)** | Free | Easy |
| **Share with team/friends** | **Cloud (Streamlit Cloud, Hugging Face)** | Free (usually) | Easy/Medium |
| **Business/Production** | **Cloud (AWS, Azure, GCP)** | Paid | Hard |

---

## Option 1: Streamlit Cloud (Best for Free Sharing)
*Requires a GitHub account.*
1.  Push your code to a GitHub repository.
2.  Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Click "New app".
4.  Select your repository, branch, and main file path (`app.py`).
5.  Click "Deploy".
6.  **Important**: Go to "App Settings" -> "Secrets" and add your `GROQ_API_KEY`.
    ```toml
    GROQ_API_KEY = "your-key-here"
    ```

## Option 2: Hugging Face Spaces (Great for AI Apps)
*Running on free CPU hardware.*
1.  Create a [Hugging Face account](https://huggingface.co/join).
2.  Create a new **Space**.
3.  Select **Streamlit** as the SDK.
4.  Upload your files (`app.py`, `requirements.txt`, etc.) directly or via Git.
5.  Go to **Settings** -> **Variables and secrets** and add `GROQ_API_KEY`.

## Option 3: Docker (Containerized)
1.  **Build the Image**:
    Open your terminal in the project directory and run:
    ```bash
    docker build -t vizai-app .
    ```

2.  **Run the Container**:
    Run the following command, replacing `your_groq_api_key_here` with your actual key:
    ```bash
    docker run -p 8501:8501 -e GROQ_API_KEY="your_groq_api_key_here" vizai-app
    ```

3.  **Access the App**:
    Open your browser and go to `http://localhost:8501`.

## Option 4: Local Execution
Simply run:

## How to Update your GitHub Repo
If you have already deployed this app and want to push the latest changes (UI upgrade + Dockerfile):

1.  Open your terminal in the project folder.
2.  Stop the app if it's running (Ctrl+C).
3.  Run these commands:
    ```bash
    git add .
    git commit -m "Upgrade UI: Dark theme and Docker support"
    git push origin main
    ```
4.  If you are using **Streamlit Cloud**, it will **automatically detect the changes and redeploy** your app within minutes!

## Is this Production Ready?
**Yes, for a Portfolio or Internal Tool.**
-   ✅ **Secure**: Secrets are managed via environment variables (not hardcoded).
-   ✅ **Portable**: Docker makes it run anywhere.
-   ✅ **User Friendly**: Error handling and loading states are implemented.

**Considerations for Enterprise Scale**:
-   **Concurrency**: Streamlit is not designed for thousands of simultaneous users.
-   **Authentication**: The current app has basic auth; enterprise apps need OAuth/SSO.
-   **Data Privacy**: Ensure you comply with data laws if users upload sensitive CSVs.
