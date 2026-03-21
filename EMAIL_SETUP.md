# Email Configuration for Password Reset

## Overview
The Himwatkhanda Vastu application includes a complete password reset system with **database-driven email configuration**. Email settings are managed through the dashboard admin interface, not in code.

## Architecture

### Database-Driven Configuration
- Email settings are stored in the `EmailConfiguration` model
- Active configuration is loaded automatically from the database
- One configuration can be marked as "active" and used system-wide
- No need to edit code or restart server to change email settings

### Default Configuration
- **Development**: Console backend (prints to terminal)
- **Production**: SMTP backend (sends actual emails)

## Setup

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Create Default Configuration
```bash
python manage.py create_default_email_config
```

This creates a default console-based configuration for development.

### 3. Access Email Configuration
Go to: **Dashboard → Settings → Email Configurations**
- URL: `/dashboard/settings/email-config/`

## Configuration Options

### Backend Types
1. **Console** (Development)
   - Prints emails to terminal
   - No actual email sent
   - Use for testing and development

2. **SMTP** (Production)
   - Sends real emails via SMTP server
   - Requires SMTP credentials

### SMTP Settings

#### For Gmail:
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password
   - Use this app password (not your regular password)

**Configuration:**
- SMTP Host: `smtp.gmail.com`
- Port: `587`
- Use TLS: `Yes`
- Username: `your-email@gmail.com`
- Password: `your-app-password`

#### For SendGrid:
- SMTP Host: `smtp.sendgrid.net`
- Port: `587`
- Use TLS: `Yes`
- Username: `apikey`
- Password: `your-sendgrid-api-key`

#### For Amazon SES:
- SMTP Host: `email-smtp.us-east-1.amazonaws.com`
- Port: `587`
- Use TLS: `Yes`
- Username: `your-ses-smtp-username`
- Password: `your-ses-smtp-password`

### Email Settings
- **From Email**: Default sender email (e.g., `noreply@himawatkhandavastu.com`)
- **From Name**: Display name (e.g., `Himwatkhanda Vastu`)
- **Admin Email**: Admin notifications destination

## Managing Email Configuration

### Via Dashboard
1. Navigate to `/dashboard/settings/email-config/`
2. Click "Add Configuration" or edit existing
3. Fill in the required fields
4. Check "Set as Active Configuration" to make it the default
5. Save

### Active Configuration
- Only one configuration can be active at a time
- When you mark a configuration as active, others are automatically deactivated
- The active configuration is used system-wide for all emails

## Password Reset Flow

1. **User Request**: User goes to `/accounts/password-reset/`
2. **Email Sent**: System sends reset link using active email configuration
3. **User Clicks**: User clicks link in email (valid for 3 days)
4. **Reset Password**: User enters new password
5. **Confirmation**: User sees confirmation message

## Access Points

- **Password Reset**: `/accounts/password-reset/`
- **Email Config List**: `/dashboard/settings/email-config/`
- **Create Config**: `/dashboard/settings/email-config/create/`
- **Login Page**: Has "Lost your password?" link

## Testing

### Development (Console Backend)
When using console backend, emails print to the terminal:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Password reset on Himwatkhanda Vastu
From: noreply@localhost
To: user@example.com
Date: ...

Hello,

You're receiving this email because you requested a password reset...
```

### Production (SMTP Backend)
1. Configure SMTP settings in dashboard
2. Send a test password reset email
3. Check recipient's inbox
4. Review logs if issues occur: `logs/django.log`

## Security Notes

- Password reset links expire after 3 days
- Tokens are one-time use only
- SMTP passwords are encrypted in database
- Always use HTTPS in production
- Use app passwords, not regular passwords

## Troubleshooting

### Emails not sending:
1. Verify SMTP credentials are correct
2. Check if configuration is marked as active
3. Review logs in `logs/django.log`
4. Test SMTP connection manually

### Console not showing emails:
- Ensure active configuration uses "Console" backend
- Check you're using the active configuration

### Reset link shows "invalid":
- Link may have expired (3-day limit)
- Link may have already been used
- User's email in database may be incorrect

### Configuration not loading:
- Run migrations: `python manage.py migrate`
- Check dashboard logs for errors
- Verify EmailConfiguration model exists

## Database Migration

A migration file was created: `dashboard/migrations/0014_emailconfiguration.py`

Apply it when database access is available:
```bash
python manage.py migrate dashboard
```

## Templates

All templates are already created and working:
- `templates/accounts/password_reset.html` - Reset request form
- `templates/accounts/password_reset_email.html` - Email template
- `templates/accounts/password_reset_confirm.html` - New password form
- `templates/accounts/password_reset_done.html` - Confirmation after request
- `templates/accounts/password_reset_complete.html` - Final confirmation
- `templates/dashboard/email_config_list.html` - Configuration list
- `templates/dashboard/email_config_form.html` - Configuration form
