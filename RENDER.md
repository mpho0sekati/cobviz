# Hosting `cobviz` for Free on Render.com

This guide explains how to set up the COBOL Visualization Tool on [Render](https://render.com/) using their **Free Tier**.

## 🚀 Option 1: One-Click Blueprint (Recommended)

The easiest way to stay on the free tier is to use the included `render.yaml` file, which is already configured for the Free plan.

1. **Fork the Repository**: Click the "Fork" button at the top of this GitHub repository to create a copy in your own account.
2. **Create a Blueprint**:
   - Log in to your [Render Dashboard](https://dashboard.render.com/).
   - Click the **New +** button and select **Blueprint**.
   - Connect your GitHub account and select your forked `cobviz` repository.
3. **Deploy**:
   - Render will show you the resources defined in `render.yaml`.
   - Ensure the **Service Plan** says `Free`.
   - Click **Apply**. Render will build the Docker image and deploy your web interface automatically.

## 🛠️ Option 2: Manual Setup (Step-by-Step)

If you prefer to configure the service manually through the Render UI, follow these detailed steps to ensure you remain on the Free tier:

1. **Start a New Web Service**:
   - Click **New +** and select **Web Service**.
2. **Select Repository**:
   - Connect your GitHub repository.
3. **Configure Service Settings**:
   - **Name**: `cobviz`
   - **Region**: Choose the one closest to you (e.g., `Oregon (US West)`).
   - **Branch**: `main` (or your primary branch).
   - **Language**: Select **Docker**.
4. **Select the Free Plan**:
   - Scroll down to the **Instance Type** section.
   - **Crucial**: Select the **Free** tier. It offers 512MB RAM and 0.1 CPU, which is sufficient for `cobviz`.
5. **Advanced Settings**:
   - **Environment Variables**: Render handles the `PORT` automatically for Docker services, but you can explicitly add `PORT` = `5000` if needed.
   - **Health Check Path**: Set this to `/`.
6. **Deploy**: Click **Create Web Service**.

## ⚠️ Understanding the Render Free Tier

Since you are using the Free tier, please keep these points in mind:

- **Spinning Down**: If the web service is inactive for 15 minutes, Render will "spin it down" (pause it).
- **Cold Starts**: When you visit the URL after the service has spun down, it may take **30-60 seconds** to wake up and load the page. This is normal for the Free plan.
- **Resource Limits**: The 512MB RAM limit is enough for most COBOL files. However, if you paste an extremely large file that exceeds this memory, the service might restart.

## 🔍 Verifying the Setup

Once the deployment status turns to `Live`:
1. Click the URL provided by Render (e.g., `https://cobviz.onrender.com`).
2. Wait for the initial load (cold start).
3. Paste some COBOL code and test the **Visualize** and **Explain** features!

## 🔒 Security Note
Your hosted instance is public. Avoid pasting sensitive proprietary code unless you have restricted access to your Render URL.
