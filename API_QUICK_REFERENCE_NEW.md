# Financial Services API Quick Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints (except `/support` POST) require the `access_token` cookie or Authorization header:
```javascript
// In fetch calls:
fetch(url, {
  credentials: 'include',  // Include cookies
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

---

## Financial Planning

### Budgets

#### Create Budget
```
POST /financial/budgets
Body: {
  "category": "groceries",
  "limit": 500.00,
  "spent": 150.00,
  "month": "2025-01"
}
```

#### Get All Budgets
```
GET /financial/budgets?month=2025-01
Response: [{ id, category, limit, spent, month, created_at, ... }]
```

#### Get Budget
```
GET /financial/budgets/{id}
```

#### Update Budget
```
PUT /financial/budgets/{id}
Body: { "spent": 200.00 }
```

#### Delete Budget
```
DELETE /financial/budgets/{id}
```

### Goals

#### Create Goal
```
POST /financial/goals
Body: {
  "goal_name": "Save for vacation",
  "target_amount": 5000.00,
  "current_amount": 1500.00,
  "deadline": "2025-12-31T23:59:59",
  "status": "active"
}
```

#### Get All Goals
```
GET /financial/goals?skip=0&limit=100
```

#### Get Goal
```
GET /financial/goals/{id}
```

#### Update Goal
```
PUT /financial/goals/{id}
Body: { "current_amount": 2500.00 }
```

#### Delete Goal
```
DELETE /financial/goals/{id}
```

---

## Insurance

### Policies

#### Create Policy
```
POST /insurance/policies
Body: {
  "policy_number": "POL-123456",
  "policy_type": "health",
  "coverage_amount": 100000.00,
  "premium": 250.00,
  "start_date": "2024-01-01T00:00:00",
  "renewal_date": "2025-01-01T00:00:00",
  "status": "active"
}
```

#### Get All Policies
```
GET /insurance/policies
```

#### Get Policy
```
GET /insurance/policies/{id}
```

#### Update Policy
```
PUT /insurance/policies/{id}
Body: { "status": "active" }
```

#### Delete Policy
```
DELETE /insurance/policies/{id}
```

### Claims

#### Submit Claim
```
POST /insurance/policies/{policy_id}/claims
Body: {
  "claim_number": "CLM-789123",
  "amount": 5000.00,
  "status": "pending",
  "description": "Medical treatment claim"
}
```

#### Get Policy Claims
```
GET /insurance/policies/{policy_id}/claims
```

#### Get Claim
```
GET /insurance/claims/{id}
```

#### Update Claim (Admin)
```
PUT /insurance/claims/{id}
Body: { "status": "approved" }
```

---

## Notifications

#### Get Notifications
```
GET /notifications?skip=0&limit=50
Response: [{ id, title, message, notification_type, is_read, created_at }]
```

#### Get Unread Count
```
GET /notifications/unread/count
Response: { "unread_count": 5 }
```

#### Create Notification
```
POST /notifications
Body: {
  "title": "Payment Received",
  "message": "Your deposit has been processed",
  "notification_type": "transaction",
  "is_read": false
}
```

#### Get Notification
```
GET /notifications/{id}
```

#### Mark As Read
```
PUT /notifications/{id}/mark-as-read
```

#### Mark All As Read
```
PUT /notifications/mark-all-as-read
```

#### Delete Notification
```
DELETE /notifications/{id}
```

---

## Settings

#### Get Settings
```
GET /settings
Response: {
  "id": 1,
  "user_id": 1,
  "two_factor_enabled": false,
  "email_notifications": true,
  "sms_notifications": false,
  "phone_number": "+1234567890",
  "address": "123 Main St",
  "preferences": null
}
```

#### Update Settings
```
PUT /settings
Body: {
  "email_notifications": true,
  "sms_notifications": false
}
```

#### Update Profile
```
PUT /settings/profile
Body: {
  "full_name": "John Doe"
}
```

#### Change Password
```
PUT /settings/password
Body: {
  "old_password": "current_password",
  "new_password": "new_password_min_8_chars"
}
```

#### Enable 2FA
```
PUT /settings/2fa/enable
```

#### Disable 2FA
```
PUT /settings/2fa/disable
```

---

## Support Tickets

### Public Endpoints (No Auth Required)

#### Submit Ticket
```
POST /support
Body: {
  "subject": "Account Issue",
  "message": "I cannot reset my password",
  "priority": "high"
}
Response: { "id": 1, "ticket_number": "TKT-ABC123", ... }
```

### User Endpoints

#### Get My Tickets
```
GET /support/my-tickets?skip=0&limit=100
```

#### Get Ticket
```
GET /support/{id}
```

### Admin Endpoints

#### Get All Tickets
```
GET /support/admin/all?skip=0&limit=100&status=open
```

#### Update Ticket (Status, Priority)
```
PUT /support/{id}
Body: { "status": "in_progress", "priority": "high" }
```

#### Delete Ticket
```
DELETE /support/{id}
```

---

## Projects

#### Create Project
```
POST /projects
Body: {
  "project_name": "Home Renovation",
  "description": "Kitchen and bathroom upgrade",
  "status": "planning",
  "budget": 25000.00,
  "start_date": "2025-06-01T00:00:00",
  "end_date": "2025-12-31T23:59:59"
}
```

#### Get Projects
```
GET /projects?skip=0&limit=100
```

#### Get Project
```
GET /projects/{id}
```

#### Update Project
```
PUT /projects/{id}
Body: { "status": "in_progress" }
```

#### Delete Project
```
DELETE /projects/{id}
```

---

## User Profile (Existing)

#### Get Profile
```
GET /user/profile
Response: {
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": true,
  "account_number": "ACC-123456"
}
```

#### Get Dashboard Data
```
GET /user/dashboard
Response: {
  "total_balance": 10000.00,
  "total_investments": 25000.00,
  "total_loans": 15000.00,
  "recent_transactions": [...]
}
```

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message"
}
```

Common Status Codes:
- `200` - Success
- `201` - Created
- `204` - No Content (for DELETE/update operations with no response)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (not authenticated)
- `403` - Forbidden (authenticated but not authorized)
- `404` - Not Found
- `422` - Unprocessable Entity (validation error)
- `500` - Internal Server Error

---

## Example: Complete Workflow

### 1. User Views Budget & Goals Dashboard
```javascript
const budgets = await fetch('/api/v1/financial/budgets?month=2025-01', {
  credentials: 'include'
}).then(r => r.json());

const goals = await fetch('/api/v1/financial/goals', {
  credentials: 'include'
}).then(r => r.json());

// Render budgets and goals with progress bars
```

### 2. User Creates New Goal
```javascript
const newGoal = await fetch('/api/v1/financial/goals', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    goal_name: "New Car",
    target_amount: 30000,
    current_amount: 0,
    deadline: "2026-12-31T23:59:59"
  })
}).then(r => r.json());

console.log('Goal created:', newGoal.id);
```

### 3. User Views Insurance Policies
```javascript
const policies = await fetch('/api/v1/insurance/policies', {
  credentials: 'include'
}).then(r => r.json());

// Display renewal dates, coverage amounts, premiums
```

### 4. User Submits Support Ticket
```javascript
const ticket = await fetch('/api/v1/support', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    subject: "Transaction Not Processed",
    message: "My transfer from Dec 5 is still pending",
    priority: "normal"
  })
}).then(r => r.json());

alert(`Support ticket created: ${ticket.ticket_number}`);
```

---

## Testing with cURL

### Get Budgets
```bash
curl -b "access_token=YOUR_TOKEN" \
  http://localhost:8000/api/v1/financial/budgets
```

### Create Budget
```bash
curl -X POST http://localhost:8000/api/v1/financial/budgets \
  -b "access_token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "groceries",
    "limit": 500,
    "spent": 150,
    "month": "2025-01"
  }'
```

### Submit Support Ticket (No Auth)
```bash
curl -X POST http://localhost:8000/api/v1/support \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Help",
    "message": "I need assistance",
    "priority": "normal"
  }'
```

---

## Browser Console Examples

### Fetch All User Notifications
```javascript
fetch('/api/v1/notifications', { credentials: 'include' })
  .then(r => r.json())
  .then(console.log);
```

### Update User Settings
```javascript
fetch('/api/v1/settings', {
  method: 'PUT',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email_notifications: true,
    phone_number: "+1234567890"
  })
}).then(r => r.json()).then(console.log);
```

### Change Password
```javascript
fetch('/api/v1/settings/password', {
  method: 'PUT',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    old_password: "oldpass123",
    new_password: "newpass456"
  })
}).then(r => {
  if (r.ok) console.log('Password changed successfully');
  else r.json().then(e => console.error(e.detail));
});
```

---

Generated: December 9, 2025
