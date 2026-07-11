# Hosting `cobviz` for Free on Render.com

This guide explains how to set up the COBOL Visualization Tool on [Render](https://render.com/) using their **Free Tier**.

## 🚀 Option 1: Blueprint Deployment (Easiest)

The included `render.yaml` file is pre-configured for the Free plan using Docker.

1. **Fork the Repository**: Fork this project to your GitHub account.
2. **Create a Blueprint**:
   - In Render, click **New +** > **Blueprint**.
   - Connect your fork.
3. **Deploy**: Review and click **Apply**.

## 🛠️ Option 2: Native Python Deployment (No Docker)

If you prefer not to use Docker, you can deploy `cobviz` as a native Python Web Service. This is often faster to build.

1. **New Web Service**: Click **New +** > **Web Service**.
2. **Select Repository**: Connect your GitHub fork.
3. **Configure Settings**:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install .`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT cobviz.web:app`
4. **Select Plan**: Choose the **Free** instance type.
5. **Deploy**: Click **Create Web Service**.

## ⚠️ Understanding the Render Free Tier

- **Spinning Down**: The service pauses after 15 minutes of inactivity.
- **Cold Starts**: Initial load may take **30-60 seconds** while the instance wakes up.
- **Resources**: You have 512MB RAM, which is plenty for analyzing most COBOL files.

## 🔒 Security Note
Hosted instances are public. Do not paste sensitive or proprietary code into a public URL unless you have secured it.
