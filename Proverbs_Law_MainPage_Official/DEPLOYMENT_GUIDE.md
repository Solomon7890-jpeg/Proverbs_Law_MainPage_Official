# 🚀 Deployment Guide: ProVerBs Legal AI

This guide provides instructions for deploying the 'ProVerBs Legal AI' application to Hugging Face Spaces.

## 1. Prerequisites

Before you begin, make sure you have the following:

*   **Hugging Face Account**: If you don't have one, create it for free at [https://huggingface.co/join](https://huggingface.co/join).
*   **Hugging Face Access Token**:
    *   Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
    *   Click "New token" and select "Write" access.
    *   Copy the token. You will need it during deployment.
*   **Space Name**: Choose a name for your Hugging Face Space. It should be in the format `your-username/your-space-name` (e.g., `Solomon7890/proverbs-law-ai`).

## 2. Quick Deploy (Recommended Method)

This is the easiest and recommended way to deploy your application.

### Step 1: Run the Deployment Script

Open a terminal or command prompt in the `Proverbs_Law_MainPage_Official` directory and run the following command:

*   **On Windows:**
    ```bash
    python quick_deploy_hf.py
    ```
    (You can also double-click the `QUICK_DEPLOY.bat` file.)

*   **On macOS/Linux:**
    ```bash
    python3 quick_deploy_hf.py
    ```

### Step 2: Provide Your Information

The script will prompt you to enter:

1.  **Your Space Name**: The name you chose in the prerequisites (e.g., `your-username/your-space-name`).
2.  **Your Hugging Face Token**: Paste the token you copied.

### Step 3: Wait for Deployment

The script will automate the deployment process, which may take 2-5 minutes. Once it's done, your application will be live.

### Step 4: Access Your Application

You can access your deployed application at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`.

## 3. Manual Deployment (For Advanced Users)

If you prefer more control, you can use one of these manual methods:

*   **Method 1: Using Git**: Use `git` commands to initialize a repository, add your files, and push them to your Hugging Face Space.
*   **Method 2: Using the Hugging Face Python API**: Write a Python script using the `huggingface_hub` library to create and upload your Space.
*   **Method 3: Using the Web Interface**: Create a new Space on the Hugging Face website and upload your files (`app.py`, `requirements.txt`, `assets/` folder, etc.) through the browser.

For detailed instructions on these manual methods, please refer to the `DEPLOYMENT_GUIDE_WITH_LOGOS.md` file in your project.

## 4. After Deployment

### Verification

After the deployment is complete and the Space is running, check the following:

*   **Logo Display**: The rotating logos should appear at the top of the page.
*   **Functionality**: Test the AI features and ensure all tabs and sections are working correctly.
*   **Performance**: The page should load quickly without any broken images or console errors.

### Troubleshooting

If you encounter any issues, such as logos not appearing or the Space build failing, refer to the **Troubleshooting** section in the `DEPLOYMENT_GUIDE_WITH_LOGOS.md` file for solutions.
