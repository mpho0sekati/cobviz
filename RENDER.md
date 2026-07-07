# Deploying `cobviz` to Render.com

This guide provides a detailed walkthrough for hosting your own instance of the COBOL Visualization Tool on [Render](https://render.com/).

## 🚀 Quick Start: Blueprint Deployment

The easiest way to deploy `cobviz` is using the included `render.yaml` Blueprint specification.

1. **Fork the Repository**: Fork this project to your own GitHub account.
2. **Create a Blueprint**:
   - Log in to your [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** and select **Blueprint**.
   - Connect your GitHub account and select your forked repository.
3. **Deploy**:
   - Render will automatically detect the `render.yaml` file.
   - Review the configuration and click **Apply**.
   - Your service will be built (using the `Dockerfile`) and deployed within minutes.

## 🛠️ Manual Configuration

If you prefer to configure the service manually:

1. **New Web Service**: Click **New +** > **Web Service**.
2. **Environment**: Choose **Docker**.
3. **Region**: Select a region close to your users (e.g., `Oregon (US West)`).
4. **Plan**: Select the **Free** tier (or higher if processing very large files).
5. **Advanced Settings**:
   - **Environment Variables**:
     - `PORT`: 5000 (Render usually sets this automatically, but ensure your app listens on `${PORT}`).
   - **Health Check Path**: `/`

## ⚙️ How it works on Render

- **Dockerization**: Render uses the `Dockerfile` in the root directory to build a lightweight Python container.
- **Gunicorn**: The container runs `gunicorn` as the production WSGI server.
- **Port Binding**: The application dynamically binds to the port provided by Render's environment, ensuring smooth traffic routing.

## 🔍 Troubleshooting

- **Build Failures**: Ensure you haven't removed `requirements.txt` or `pyproject.toml`, as both are used during the build.
- **Health Check Errors**: If the service starts but fails health checks, verify that the `CMD` in the `Dockerfile` is correctly using the `${PORT}` variable.
- **Resource Limits**: The Free tier has limited RAM. If you encounter crashes with large COBOL files, consider upgrading your Render plan.

## 🔒 Security Note
When hosting publicly, remember that anyone with the URL can access your tool. Ensure you do not paste highly sensitive or proprietary code into a public instance unless you have configured appropriate access controls (e.g., Render's IP allowlisting or a custom authentication layer).
