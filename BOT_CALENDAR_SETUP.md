# Bot Calendar Setup Guide

## Overview

Alfred uses a **dual authentication** approach for maximum security:

1. **User credentials** (readonly) - Reads from ALL your calendars
2. **Bot credentials** (write) - Only writes to a dedicated bot calendar

This means Alfred can VIEW your work calendar, personal calendar, etc., but can ONLY CREATE/MODIFY events in the bot calendar.

---

## Step 1: Create Bot Calendar

1. Go to [Google Calendar](https://calendar.google.com/)
2. On the left sidebar, click the **+** next to "Other calendars"
3. Select **"Create new calendar"**
4. Name it: **"Alfred Bot"** (or any name you like)
5. Description: "Calendar managed by Alfred assistant bot"
6. Click **"Create calendar"**

---

## Step 2: Get Bot Calendar ID

1. In Google Calendar, find your new "Alfred Bot" calendar in the left sidebar
2. Click the **⋮** (three dots) next to it
3. Select **"Settings and sharing"**
4. Scroll down to **"Integrate calendar"**
5. Copy the **Calendar ID** (looks like: `abc123def456@group.calendar.google.com`)
6. Save this - you'll need it for `.env`

---

## Step 3: Set Up Two OAuth Credentials (Same Google Account)

You need TWO separate OAuth credentials, but both will use YOUR Google account.

### 3A. User Credentials (Readonly)

**Purpose:** Read all calendars

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create new one)
3. Enable **Google Calendar API**
4. Go to **APIs & Services → Credentials**
5. Click **"Create Credentials" → "OAuth client ID"**
6. Application type: **Desktop app**
7. Name: **"Alfred User (Readonly)"**
8. Click **Create**
9. Download the JSON file
10. Rename it to: `user_credentials.json`
11. Move to: `credentials/user_credentials.json`

**Important:** Configure OAuth consent screen if prompted. Add yourself as test user.

### 3B: Bot Credentials (Write)

**Purpose:** Write to bot calendar only

1. In the same Google Cloud Console project
2. Click **"Create Credentials" → "OAuth client ID"** again
3. Application type: **Desktop app**
4. Name: **"Alfred Bot (Write)"**
5. Click **Create**
6. Download the JSON file
7. Rename it to: `bot_credentials.json`
8. Move to: `credentials/bot_credentials.json`

**Note:** Both credentials are for YOUR Google account. Security comes from calendar ACLs, not separate accounts.

---

## Step 4: Verify Bot Calendar Permissions

**No action needed!** Since you're using your own Google account for both credentials, you automatically have write permission to your own bot calendar.

The security works like this:
- Your account created the "Alfred Bot" calendar
- Your account owns it and has full permissions
- When you authenticate with bot credentials, you'll grant calendar scope
- But the bot code ONLY uses bot credentials to write to GOOGLE_CALENDAR_ID
- Your primary calendar is safe because the code never writes to it

---

## Step 5: Update .env File

```bash
# Bot calendar ID (where Alfred creates events)
GOOGLE_CALENDAR_ID=abc123def456@group.calendar.google.com

# Existing variables
DISCORD_BOT_TOKEN=your_token
GOOGLE_GEMINI_API_KEY=your_key
DISCORD_OWNER_ID=your_user_id
```

---

## Step 6: Authenticate Both Services

Run the bot - it will prompt for authentication TWICE:

```bash
cd src
python bot.py
```

**First prompt:** User authentication (readonly)
- Browser opens
- Log in with your Google account
- Grant readonly calendar permissions
- Creates `user_token.pickle`

**Second prompt:** Bot authentication (write)
- Browser opens again
- Log in with **the same Google account**
- Grant full calendar permissions
- Creates `bot_token.pickle`

**Both use YOUR account** - security comes from which calendar the code writes to, not different accounts.

---

## Step 7: Verify Setup

Test in Discord:

```
You: Create meeting tomorrow at 3pm
Alfred: ✓ **Meeting**
        📅 Tomorrow at 3:00 PM → 4:00 PM
```

Check Google Calendar:
- ✅ Event should appear in "Alfred Bot" calendar
- ✅ Event should NOT appear in your primary calendar
- ✅ Both calendars should be visible side-by-side

---

## Security Summary

**What Alfred CAN do:**
- ✅ Read events from ALL your calendars (work, personal, shared)
- ✅ Create/modify events in "Alfred Bot" calendar only

**What Alfred CANNOT do:**
- ❌ Create/modify events in your primary calendar
- ❌ Create/modify events in any calendar except bot calendar
- ❌ Delete calendars
- ❌ Share calendars

**Why this is secure:**
- Code explicitly writes to GOOGLE_CALENDAR_ID (bot calendar) only
- Even if code has bugs, worst case is bot calendar gets messed up
- Your primary calendar is protected by code logic, not ACLs (since you own both)
- Separation of read/write credentials makes intent clear in code

---

## Troubleshooting

**"FileNotFoundError: user_credentials.json not found"**
- Make sure both credential files are in `credentials/` folder
- Check filenames: `user_credentials.json` and `bot_credentials.json`

**"Bot can't create events"**
- Make sure bot calendar is shared with bot identity
- Check GOOGLE_CALENDAR_ID in .env matches bot calendar ID
- Verify bot_token.pickle exists

**"Can't see events in primary calendar when asking schedule"**
- Check user_token.pickle exists
- Verify user credentials have calendar.events.readonly scope
- Re-run authentication if needed (delete user_token.pickle)

**"Bot creates events in primary calendar instead"**
- Check GOOGLE_CALENDAR_ID in .env is set to bot calendar ID
- Should be like: abc123@group.calendar.google.com
- NOT "primary"

---

## File Structure

After setup, you should have:

```
auto-calendar/
├── credentials/
│   ├── user_credentials.json     # Readonly credentials
│   └── bot_credentials.json      # Write credentials
├── user_token.pickle             # Readonly token (auto-generated)
├── bot_token.pickle              # Write token (auto-generated)
└── .env                          # Contains GOOGLE_CALENDAR_ID
```

---

## Next Steps

Once setup is complete:
1. Test event creation: "Schedule meeting tomorrow at 3pm"
2. Test schedule viewing: "What's my schedule today?" (coming soon)
3. Your primary calendar remains protected!
