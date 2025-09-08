# Zapier Integration Guide
## Constitutional Architecture API for CEREBRUM-1

This guide provides the complete implementation for the three Zapier integrations described in the Constitutional Architecture briefing.

## API Deployment

The API is now implemented and provides the following endpoints required for Zapier integration:

### Base URL
```
https://your-deployed-domain.com
```
(For local testing: http://localhost:8000)

### Authentication
All API endpoints require JWT authentication using the `Authorization: Bearer <token>` header.

To get a token for testing:
```bash
curl -X POST https://your-domain.com/api/auth/token
```

**Important**: In production, implement proper authentication with user credentials.

## Zapier Integration Endpoints

### 1. AEGIS Content Filter - `/api/security/filter`
**Used by**: Zap #1 (Triage Constitutionnel)

```http
POST /api/security/filter
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "content": "Content to be filtered"
}
```

**Response:**
```json
{
  "is_compliant": true,
  "reason": null,
  "confidence": 0.95
}
```

### 2. Task Creation - `/api/tasks`
**Used by**: Zap #1 (Triage Constitutionnel)

```http
POST /api/tasks
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Task name",
  "priority": "💡 Normal",
  "content": "Task description"
}
```

**Priority Options:**
- `🔥 Urgent` (30 minutes)
- `⚡ High` (20 minutes)
- `💡 Normal` (15 minutes)
- `📝 Low` (10 minutes)

### 3. Workload Summary - `/api/tasks/workload`
**Used by**: Zap #2 (Weekly Report)

```http
GET /api/tasks/workload
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "total_minutes": 45,
  "tasks_by_priority": {
    "💡 Normal": 15,
    "⚡ High": 20,
    "📝 Low": 10
  },
  "total_tasks": 3,
  "status_breakdown": {
    "pending": 3
  }
}
```

## Zapier Configuration

### Zap #1: Triage Constitutionnel de l'Inbox

1. **Trigger**: Notion - New Database Item
   - Database: 📥 Inbox

2. **Action**: Webhooks by Zapier - POST
   - URL: `https://your-domain.com/api/security/filter`
   - Headers: `Authorization: Bearer <YOUR_JWT_TOKEN>`
   - Data: `{"content": "{{content_from_notion}}"}`

3. **Filter**: Filter by Zapier
   - Continue only if: `is_compliant` equals `true`

4. **Action**: Webhooks by Zapier - POST
   - URL: `https://your-domain.com/api/tasks`
   - Headers: `Authorization: Bearer <YOUR_JWT_TOKEN>`
   - Data: `{"name": "{{notion_item_name}}", "priority": "💡 Normal", "content": "{{notion_item_content}}"}`

5. **Action**: Notion - Update Database Item
   - Set Status to "Traité"

### Zap #2: Rapport de Charge Hebdomadaire

1. **Trigger**: Schedule by Zapier
   - Every Monday at 9am

2. **Action**: Webhooks by Zapier - GET
   - URL: `https://your-domain.com/api/tasks/workload`
   - Headers: `Authorization: Bearer <YOUR_JWT_TOKEN>`

3. **Action**: Formatter by Zapier - Text
   - Create formatted report:
   ```
   Rapport de Charge CEREBRUM-1
   
   Charge totale: {{total_minutes}} minutes
   Nombre de tâches: {{total_tasks}}
   
   Par priorité:
   🔥 Urgent: {{tasks_by_priority.🔥 Urgent}} min
   ⚡ High: {{tasks_by_priority.⚡ High}} min
   💡 Normal: {{tasks_by_priority.💡 Normal}} min
   📝 Low: {{tasks_by_priority.📝 Low}} min
   ```

4. **Action**: Gmail - Send Email
   - Subject: "Rapport de Charge Hebdomadaire - CEREBRUM-1"
   - Body: Use formatted text from step 3

### Zap #3: Capture d'Email vers l'Inbox

1. **Trigger**: Gmail - New Labeled Email
   - Label: "to-notion"

2. **Action**: Notion - Create Database Item
   - Database: 📥 Inbox
   - Name: Email subject
   - Content: Email body

## Running the API

### Development
```bash
cd /home/runner/work/gdp-dashboard/gdp-dashboard
python -m api.main
```

### Production
```bash
# Using uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Or using gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Environment Variables

Set these environment variables in production:

```bash
export JWT_SECRET_KEY="your-super-secure-secret-key"
```

## Testing the Integration

Use the provided curl examples to test each endpoint:

```bash
# Get authentication token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token | jq -r .access_token)

# Test content filtering
curl -X POST http://localhost:8000/api/security/filter \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"This is a test task"}'

# Create a task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test task","priority":"💡 Normal"}'

# Get workload summary
curl -X GET http://localhost:8000/api/tasks/workload \
  -H "Authorization: Bearer $TOKEN"
```

## AEGIS Security Features

The content filter implements basic constitutional compliance rules:
- Blocks content with "urgent", "asap", "emergency" patterns (anti-rush principle)
- Blocks content with security bypass attempts
- Requires minimum content length for proper assessment
- Returns confidence scores for filtering decisions

## Next Steps

1. Deploy the API to a public URL (Heroku, Railway, Google Cloud Run, etc.)
2. Update JWT_SECRET_KEY with a secure value
3. Configure your Notion databases and share them with Zapier
4. Create the three Zaps following the configuration above
5. Test the complete workflow from Notion → API → Email

The system is now ready to serve as the "Système Nerveux" of your Constitutional Architecture!