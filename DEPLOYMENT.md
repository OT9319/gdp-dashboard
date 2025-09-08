# Production Deployment Guide

This guide explains how to deploy the Constitutional Architecture system to production.

## Prerequisites

1. A hosting platform (Heroku, Railway, Google Cloud Run, etc.)
2. Domain name for your API endpoints
3. Notion workspace with databases set up
4. Zapier account
5. Gmail account for email integration

## Deployment Options

### Option 1: Heroku (Recommended)

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set JWT_SECRET_KEY="your-super-secure-secret-key-here"
   ```

3. **Create Procfile**
   ```
   web: uvicorn api.main:app --host=0.0.0.0 --port=${PORT:-8000}
   streamlit: streamlit run streamlit_app.py --server.port=${PORT:-8501}
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy Constitutional Architecture system"
   git push heroku main
   ```

### Option 2: Railway

1. Connect your GitHub repository to Railway
2. Set environment variable: `JWT_SECRET_KEY`
3. Railway will automatically detect and deploy both services

### Option 3: Google Cloud Run

1. **Build and push container**
   ```bash
   gcloud run deploy constitutional-api --source . --port 8000
   ```

2. **Set environment variables**
   ```bash
   gcloud run services update constitutional-api --set-env-vars JWT_SECRET_KEY="your-secret"
   ```

## Configuration After Deployment

### 1. Update API Base URL

Once deployed, note your API base URL (e.g., `https://your-app.herokuapp.com`)

### 2. Notion Setup

1. Create these databases in Notion:
   - **📥 Inbox**: Properties include Name (title), Content (text), Status (select)
   - **🚀 Projets**: For project tracking
   - **👥 Contacts CRM**: For contact management

2. Create a Notion integration:
   - Go to https://www.notion.so/my-integrations
   - Create new integration
   - Copy the integration token
   - Share your databases with the integration

### 3. Zapier Configuration

Configure the three Zaps using your deployed API URL:

#### Zap #1: Inbox Triage
- **Step 2 URL**: `https://your-app.herokuapp.com/api/security/filter`
- **Step 4 URL**: `https://your-app.herokuapp.com/api/tasks`

#### Zap #2: Weekly Report  
- **Step 2 URL**: `https://your-app.herokuapp.com/api/tasks/workload`

### 4. Authentication

For production, get your JWT token:
```bash
curl -X POST https://your-app.herokuapp.com/api/auth/token
```

Use this token in all Zapier webhook configurations.

### 5. Gmail Labels

Create a Gmail label called "to-notion" for Zap #3.

## Testing Production Deployment

Run the test script against your production URL:

```bash
# Update test_api.py API_BASE to your production URL
# API_BASE = "https://your-app.herokuapp.com"

python test_api.py
```

## Monitoring

- Check Heroku logs: `heroku logs --tail`
- Monitor API health: `curl https://your-app.herokuapp.com/`
- Test Zapier integrations with sample data

## Security Considerations

1. **JWT Secret**: Use a long, random secret key
2. **HTTPS**: Ensure all API calls use HTTPS
3. **Rate Limiting**: Consider implementing rate limits for production
4. **Authentication**: Implement proper user authentication instead of simple tokens

## Troubleshooting

### Common Issues

1. **API not accessible**: Check firewall settings and port configuration
2. **JWT token expired**: Tokens expire after 24 hours, generate new ones
3. **CORS errors**: Ensure CORS is properly configured in the API
4. **Notion integration fails**: Verify database sharing and integration permissions

### Debugging Steps

1. Check application logs
2. Verify environment variables are set
3. Test API endpoints individually
4. Validate Notion database structure
5. Check Zapier error logs

The system is now production-ready and should handle the three Zapier integrations as specified in the Constitutional Architecture briefing!