# Project Summary - AI Assistant Bot

**Last Updated:** 2026-02-18 (Session 4)
**Status:** ✅ YouTube Download Feature Added - Bot Running & In Active Development
**Version:** 1.4.0

---

## ⚠️ IMPORTANT: Read This File First

**This file is the primary handoff document for AI assistants working on this project.**

When you start a conversation about this codebase:
1. **Read this file completely** - It contains everything you need to understand the project architecture, design decisions, and current state
2. Use other documentation files (SETUP.md, FEATURES.md, DEPENDENCIES.md) for specific implementation details
3. This file is maintained as the single source of truth for project context

**Why this matters:** This bot uses AI at every layer. Understanding the multi-layer AI architecture, context passing, and unified parsing approach is critical before making changes.

---

## Quick Start for New AI Assistant

**TLDR:** This is Alfred, a fully operational Discord bot that creates calendar events, provides fun facts, and handles basic conversation. APIs are set up, bot works, user is actively developing it.

**Current State:**
- ✅ Bot is running locally and tested
- ✅ Named "Alfred" with defined personality (professional, friendly, task-focused)
- ✅ Four features: Calendar (create/modify/view events) + Fun Facts + YouTube Downloader + Conversation
- ✅ All APIs configured (Discord, Gemini, Google Calendar)
- ✅ **Dual OAuth setup complete** - Readonly access to all calendars, write access to bot calendar only
- ✅ **100% AI-native** - Zero hardcoded keywords, all routing and parsing via Gemini
- ✅ YouTube download feature complete (MP3/MP4 support)

**What to Know:**
- User wants this to be a general-purpose assistant (not just calendar)
- Calendar is the first "task feature" - more will be added
- Bot should be conversational but redirect to tasks (not a chatbot)
- DM-first design (personal assistant, not server bot)
- All free APIs, modular architecture

### The Vision

A general-purpose **personal assistant via Discord DMs** that can:
- Understand what you're asking in natural language
- Route to the appropriate feature automatically (via AI, not keywords)
- Handle any task: calendar, email, reminders, weather, todos, file management, etc.
- Work 24/7 from Discord DMs (even when laptop is closed)
- **DM-first design**: Private, one-on-one interaction with the bot

---

## Current State

### ✅ What's Built

**Core Infrastructure:**
- Discord bot framework with AI-powered intent routing
- Google Gemini integration for natural language understanding (gemini-2.5-flash)
- Modular feature system (easy to add new capabilities)
- Google Calendar integration
- **Conversation context system**: Remembers last 10 messages from last 15 minutes (hybrid approach)
  - Enables follow-up messages like "make it 2 hours" or "change that to 3pm" or "actually rename them to..."
  - Per-user context tracking
  - Automatic cleanup of old messages
  - **All features receive context** - passed to Calendar, Fun Facts, and Conversation features
- **Startup notification**: Bot sends "✅ Ready to go!" DM to owner on startup (optional, via DISCORD_OWNER_ID)

**Features Implemented:**
1. **Calendar Feature** - Create and modify Google Calendar events from natural language
   - Location: `src/features/calendar_feature.py`
   - **Unified AI parsing**: Single Gemini call interprets intent and extracts all data
   - No hardcoded keywords - purely meaning-based understanding
   - Automatically determines create vs modify based on context

   **Event Creation:**
   - Supports: recurring events, location, custom notifications/reminders
   - Creates events via Google Calendar API with popup notifications
   - Smart title generation: Creates brief titles with details in description
   - Example: "meeting about buying phone" → Title: "Phone Purchase Meeting", Description: "Discuss buying a new phone"
   - Reminders: "meeting at 3pm with 1 hour notification" → Creates popup reminder 60 minutes before
   - **Formatted output**: Shows readable times (Mon, Feb 17 at 3:00 PM), location, recurrence status
   - Multiple events: Shows full details for each event with indentation

   **Event Modification:**
   - Search existing events by name/keywords
   - Modify: title, description, location, reminders
   - Supports bulk modifications (e.g., "rename all office hours to tutor hours")
   - Add reminders: "add 1 hour notification to CSE 127 office hours"
   - All parsing done by AI - no keyword matching
   - **Formatted output**: Shows modified event name, recurrence status, and all changed properties

   **Schedule Viewing:**
   - View events from ALL calendars (primary, secondary, shared, subscribed)
   - Natural language queries: "what's my schedule today?", "what's on thursday?", "show me next week"
   - AI parses time ranges into actual dates (no hardcoded keywords for "today", "tomorrow", etc.)
   - Reads from all calendars using readonly credentials
   - Deduplicates events across calendars
   - Filters events by actual date (timezone-aware)

2. **Fun Fact Feature** - Provide interesting random facts
   - Location: `src/features/fun_fact_feature.py`
   - Uses Gemini to generate interesting, accurate fun facts
   - Responds to: "tell me a fun fact", "share something interesting", etc.
   - Brief, engaging responses (2-3 sentences)
   - Context-aware: Can provide related facts based on conversation topic

3. **YouTube Download Feature** - Download YouTube videos as MP3 or MP4
   - Location: `src/features/youtube_feature.py`
   - Download YouTube videos as audio (MP3) or video (MP4)
   - Supports multiple URLs in a single request (up to 5 at once)
   - AI-powered intent detection (no keyword matching)
   - Smart format detection based on user request context
   - File size validation (Discord 25MB limit)
   - Automatic cleanup of temporary files
   - Example requests:
     - "download this as mp3: [youtube link]"
     - "convert to mp4: [youtube link]"
     - "get me the audio from these: [link1] [link2]"
   - Uses yt-dlp for downloading, ffmpeg for conversion
   - Files sent directly via Discord DM

4. **Conversation Feature** - Handle greetings, small talk, and general questions
   - Location: `src/features/conversation_feature.py`
   - Provides friendly, brief responses to non-task messages
   - Gently redirects to task-oriented help
   - Fallback for messages that don't match other features

**Bot Personality (Alfred):**
- Named "Alfred" - a professional but friendly AI assistant
- Location: `src/config/bot_context.py`
- Defined personality: Professional, concise, helpful, task-oriented
- Can engage in brief small talk (1-2 exchanges) before redirecting to tasks
- Politely declines deep/philosophical conversations
- Consistent tone across all features

**Key Components:**
- `src/bot.py` - Main entry point, starts the Discord bot
- `src/config/bot_context.py` - Alfred's personality and context configuration
- `src/services/discord_handler.py` - Discord bot + AI routing logic + conversation logging + context management
  - Per-user conversation history tracking
  - Hybrid context filtering (10 messages / 15 minutes)
  - Context passed to router and features
- `src/services/intent_router.py` - AI-powered intent classification with context awareness (gemini-2.5-flash)
- `src/services/gemini_parser.py` - Parses natural language → event data with smart titles (gemini-2.5-flash)
- `src/services/calendar_service.py` - Google Calendar API integration
  - Event creation (recurrence, reminders, location)
  - Event search by keywords
  - Event modification (title, description, location, time)
- `src/features/calendar_feature.py` - Calendar feature module
  - Context-aware event creation
  - Event modification detection and handling
  - Enhanced response formatting
- `src/features/fun_fact_feature.py` - Fun fact generator
  - Uses Gemini to generate interesting facts (gemini-2.5-flash)
  - Brief, accurate, engaging responses
- `src/features/conversation_feature.py` - Conversation/small talk handler
  - Context-aware responses (gemini-2.5-flash)
  - Remembers recent conversation flow
- `src/utils/auth.py` - Auth utilities (minimal)

### ✅ Setup Status

**Completed:**
1. ✅ Python dependencies installed
2. ✅ Google Gemini API key configured
3. ✅ Google Calendar API OAuth credentials set up
4. ✅ Discord bot created and configured
5. ✅ `.env` file configured with all API keys
6. ✅ Google Calendar authenticated
7. ✅ Bot running locally and tested

**Bot is operational and responding to messages!**

### 🔮 Potential Future Enhancements

**User may request (not currently planned):**
- Additional task features: reminders, todos, weather, email, notes
- Calendar enhancements: delete events, list upcoming events, multi-calendar support
- Deployment to cloud hosting (Render/Railway for 24/7)
- Persistent context storage (across bot restarts)
- Timezone handling improvements
- More sophisticated natural language handling

**Already Implemented (Session 2 - 2026-02-17):**
- ✅ Recurring events (daily, weekly, monthly with RRULE)
- ✅ Location support
- ✅ Custom notifications/reminders
- ✅ Smart title & description generation
- ✅ Modify/rename existing events
- ✅ Search calendar events by keywords
- ✅ Conversation context (hybrid: 10 messages / 15 minutes)
- ✅ Follow-up message support (context-aware)
- ✅ Per-user context tracking
- ✅ Console logging with context indicators

**Don't proactively suggest features - wait for user to request**

---

## Architecture Deep Dive

### How It Works

```
User sends Discord message
    ↓
Discord Bot receives message
    ↓
AI Intent Router (Gemini)
    ├─ Analyzes user intent
    ├─ Compares against all feature capabilities
    └─ Selects best matching feature (confidence score)
    ↓
Selected Feature Handler
    ├─ Processes the request
    └─ Returns response
    ↓
Bot replies to user
```

### Key Design Decisions

**1. AI-Powered Intent Detection (Zero Hardcoded Keywords)**
- **Feature-level routing**: Gemini routes messages to correct feature (Calendar, Fun Facts, Conversation)
- **Sub-intent detection**: Calendar feature uses AI to detect create vs modify intent
- No hardcoded keyword matching - fully meaning-based
- Each feature describes its capabilities in natural language
- AI understands intent regardless of phrasing
- Easy to extend: just add new features and describe what they do

**2. Modular Feature System**
- Each feature is independent module in `src/features/`
- Features implement: `get_capabilities()` and `handle()`
- Register feature → AI automatically learns to route to it
- No changes to core bot logic needed

**3. AI-Powered Personality (Alfred)**
- Bot has consistent personality defined in `bot_context.py`
- Named "Alfred" - professional, friendly, task-oriented assistant
- Conversation feature handles small talk while staying focused
- Can engage briefly (1-2 exchanges) before redirecting to tasks
- All features use the same personality context

**4. Streamlined AI Pipeline** (Model: gemini-2.5-flash)
- **Call 1**: Route message to correct feature (Calendar, Fun Facts, Conversation)
- **Call 2** (if calendar): Single unified parse - detects intent (create/modify) AND extracts all structured data in one call
- **Call 2** (if conversation/fun facts): Generate contextual response
- Cost: 2 Gemini API calls per user message (well within free tier)
- All features use gemini-2.5-flash model
- Fully AI-driven - zero hardcoded keyword matching
- Calendar feature uses comprehensive prompt that handles all cases in one request

**5. Discord DMs as Interface**
- Personal assistant via Discord DMs (DM-first design)
- Works on phone, desktop, web
- Can run 24/7 on free cloud hosting
- Bot responds to DMs automatically (no @mention needed)
- Can also respond if @mentioned in servers, but designed for personal DM use
- No need for local Mac/laptop to stay on

### Technology Stack

**Core Dependencies:**
- **Python 3.14** (user's current version)
- **discord.py >=2.6.4** - Discord bot framework
- **google-genai >=0.3.0** - Google Gemini AI SDK (new package, replaces google-generativeai)
- **google-auth >=2.37.0** - Google authentication
- **google-auth-oauthlib >=1.2.1** - OAuth2 flow for Google Calendar
- **google-api-python-client >=2.155.0** - Google Calendar API client
- **python-dotenv >=1.0.1** - Environment variable management
- **protobuf >=5.29.2,<6.0.0** - Required for google-genai
- **grpcio >=1.68.1** - gRPC support
- **yt-dlp >=2026.2.4** - YouTube video/audio downloader
- **ffmpeg** (system dependency) - Audio/video conversion

**AI Model:**
- **Google Gemini 2.5 Flash** - AI for routing & parsing (FREE tier)

**APIs Used:**
- **Google Calendar API** - Calendar integration (FREE)
  - **Dual OAuth Setup**: Two separate credential files for security
    - `user_credentials.json` → readonly scope (`calendar.readonly`) - reads ALL calendars
    - `bot_credentials.json` → full scope (`calendar`) - writes ONLY to bot calendar
  - Both use same Google account, security via scopes and code logic
- **Discord API** - Bot communication (FREE)
- **OAuth 2.0** - Google Calendar authentication

**Important Notes:**
- All dependencies are Python 3.14 compatible
- Using `google-genai` (new SDK) instead of deprecated `google-generativeai`
- Free tier quotas vary by Gemini model - check https://ai.google.dev/pricing

---

## File Structure

```
auto-calendar/
├── src/
│   ├── bot.py                          # Main entry point, starts the bot
│   ├── config/                         # Bot configuration
│   │   └── bot_context.py              # Alfred's personality & context
│   ├── features/                       # Feature modules (add new features here)
│   │   ├── __init__.py
│   │   ├── calendar_feature.py         # Calendar event creation & modification
│   │   ├── fun_fact_feature.py         # Fun fact generator
│   │   └── conversation_feature.py     # Greetings & small talk
│   ├── services/                       # Core services
│   │   ├── discord_handler.py          # Discord bot + routing + context management
│   │   ├── intent_router.py            # AI-powered intent classification
│   │   ├── gemini_parser.py            # Natural language → event parsing
│   │   └── calendar_service.py         # Google Calendar API (create/search/modify)
│   └── utils/
│       └── auth.py                     # Auth utilities (minimal)
├── credentials/                         # Git-ignored
│   ├── user_credentials.json           # Readonly Google OAuth (all calendars)
│   └── bot_credentials.json            # Write Google OAuth (bot calendar only)
├── user_token.pickle                   # Git-ignored - User OAuth token
├── bot_token.pickle                    # Git-ignored - Bot OAuth token
├── .env                                # Git-ignored - API keys
├── .env.example                        # Template for .env
├── .gitignore
├── requirements.txt                    # Python dependencies with versions
├── runtime.txt                         # Python version (3.14.0)
├── README.md                           # Project overview
├── SETUP.md                            # Detailed setup instructions
├── FEATURES.md                         # Guide for adding new features
├── DEPENDENCIES.md                     # Complete dependency documentation
└── PROJECT_SUMMARY.md                  # This file (for AI assistants)
```

---

## How to Add a New Feature (Quick Reference)

**Pattern used:**
1. Create `src/features/feature_name.py` with class that has:
   - `__init__`: Set `self.name` and `self.description`
   - `get_capabilities()`: Return detailed string describing what it handles
   - `async handle(message, message_text)`: Process request, return string response

2. Register in `src/services/discord_handler.py` in `_load_features()`:
   ```python
   from features.feature_name import FeatureName
   feature = FeatureName()
   self.router.register_feature(feature)
   ```

3. AI automatically learns to route to it based on capabilities description

**Important:** Task features should be registered BEFORE conversation feature (order matters for routing priority)

**See existing features as examples:**
- `calendar_feature.py` - Complex feature with external API
- `conversation_feature.py` - Simple feature with AI response generation

**Full guide:** FEATURES.md

---

## Environment Variables

Required in `.env`:

```bash
# Discord Bot
DISCORD_BOT_TOKEN=your_discord_bot_token

# Google Gemini AI (for routing + parsing)
GOOGLE_GEMINI_API_KEY=your_gemini_api_key

# Google Calendar
GOOGLE_CALENDAR_ID=primary  # or specific calendar ID for testing
# For testing, you can use a separate calendar ID like:
# GOOGLE_CALENDAR_ID=abc123@group.calendar.google.com
```

**Security:** Never commit `.env`, `credentials/`, or `token.pickle` to git!

**Note on Calendar ID:**
- `primary` = your main Google Calendar (recommended for production)
- Use a specific calendar ID (from Calendar Settings → Integrate calendar) for testing
- Format: `[long-hash]@group.calendar.google.com` for sub-calendars
- Switching between calendars just requires updating `.env` and restarting the bot

---

## API Costs (All FREE)

| Service | Cost | Limit | Usage |
|---------|------|-------|-------|
| Discord Bot | FREE | Unlimited messages | Bot interface |
| Google Gemini | FREE | 1,500 req/day | 1-2 calls per user message |
| Google Calendar API | FREE | Generous quotas | Event creation |
| Hosting (Render/Railway) | FREE | 750 hours/month | 24/7 bot hosting |

**Total:** $0/month for personal use

---

## Common Issues & Solutions (For Debugging)

**Setup Issues (Already Resolved for This Bot):**
- ✅ "No module named 'services'" → Run from `src/` directory
- ✅ Credentials → Already configured
- ✅ Discord intents → Already enabled
- ✅ Can't DM bot → Already in private server

**Potential Runtime Issues:**

**AI Routing Problems:**
- Wrong feature handling message → Check `intent_router.py` confidence threshold (default: 0.6)
- Improve feature's `get_capabilities()` description with more examples
- Check console logs to see which feature was selected and why

**Calendar Parsing Issues:**
- Events created with wrong time/date → Check `gemini_parser.py` prompt
- No events created → User's message might be too ambiguous, check Gemini response in logs
- Check timezone settings in `calendar_service.py`

**Conversation Issues:**
- Alfred too chatty → Adjust prompt in `conversation_feature.py`
- Alfred too rigid → Adjust personality in `bot_context.py`
- Not redirecting to tasks → Check conversation guidelines in `bot_context.py`

**Debug Approach:**
1. Check console logs (shows which feature was selected)
2. Check Gemini API responses (shows what AI understood)
3. Test with very explicit messages first
4. Gradually test more natural language

---

## Key Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run bot locally
cd src && python bot.py

# Authenticate Google Calendar (one-time)
cd src && python -c "from services.calendar_service import get_calendar_service; get_calendar_service()"
```

### Bot Commands (in Discord)
- `!help` - Show help and available features
- `!ping` - Check bot responsiveness
- `!features` - List all registered features

---

## Design Philosophy (Why It's Built This Way)

**AI Routing Instead of Keywords:**
- Uses Gemini to understand "what does user want to do?"
- Features describe their own capabilities
- AI matches user intent → best feature
- Scales infinitely (just add features, AI learns them)
- No brittle keyword matching

**Modular Features:**
- Each feature is independent file
- Drop in new feature → register it → AI routes to it automatically
- Easy to test, disable, or remove features
- Features can be shared across projects

**Conversation as Fallback:**
- Conversation feature registered LAST (lower priority)
- Task features get first chance at routing
- Only non-task messages go to conversation
- Keeps bot task-focused while still being friendly

**Alfred's Personality:**
- Single source of truth in `bot_context.py`
- All features can use same personality context
- Consistent tone across all interactions
- Professional but friendly, concise, helpful

---

## For New Claude Chat Session

**FIRST: Read this entire file to understand current state**

**TL;DR for New Session:**
- ✅ Bot is 100% operational - all APIs working
- ✅ Four features: Calendar (create/modify/view), Fun Facts, YouTube Download, Conversation
- ✅ 100% AI-native architecture (ZERO keyword matching - this is critical!)
- ✅ Dual OAuth for calendar (readonly for viewing, write for bot calendar only)
- ✅ Uses Gemini 2.5 Flash for all AI routing and parsing
- 🎯 User is actively iterating and adding features
- 🚨 **CRITICAL:** Never add keyword matching - all intent via AI

**Key Files to Reference:**
1. `PROJECT_SUMMARY.md` - This file (overall project state)
2. `src/features/` - All feature implementations (calendar, youtube, fun_fact, conversation)
3. `src/services/intent_router.py` - AI-powered routing (no keywords!)
4. `src/services/discord_handler.py` - Main bot logic and feature registration
5. `src/config/bot_context.py` - Alfred's personality
6. `requirements.txt` - Python dependencies with versions

**Bot is Operational - APIs Already Set Up:**
- Discord bot token: configured ✅
- Google Gemini API: configured ✅
- Google Calendar API: authenticated (dual OAuth) ✅
- YouTube downloads: yt-dlp + ffmpeg ready ✅
- Bot runs with: `cd src && python bot.py`

**Likely Next Tasks (User May Request):**
- Add more features (web search, reminders, todos, weather, translation, notes, etc.)
- Refine existing features (improve prompts, handle edge cases)
- Deploy to cloud hosting (Fly.io recommended for 24/7)
- Debug routing or parsing issues
- Test YouTube download feature

**What NOT to Suggest:**
- ❌ Don't suggest redoing API setup (already done)
- ❌ Don't add keyword matching (100% AI-native philosophy)
- ❌ Don't make it overly chatty (task-focused, not chatbot)
- ❌ Don't suggest server features (this is DM-first personal assistant)
- ❌ Don't over-engineer simple requests

---

## Critical Context for AI Assistant (READ THIS)

**User's Priorities:**
1. **Natural language first** - Users should phrase things naturally, not use keywords
2. **Extensible architecture** - Easy to add unlimited features without changing core
3. **Task-focused personality** - Can do small talk but redirects to being helpful
4. **Completely free** - All APIs must be free tier
5. **DM-first design** - Personal assistant via Discord DMs, not server bot
6. **Simple, clean code** - Don't over-engineer

**Architecture Principles:**
- **AI routing** over keyword matching (using Gemini to understand intent)
- **Modular features** - each feature is independent, drop-in module
- **Consistent personality** - Alfred's context defined once, used everywhere
- **Features register themselves** - AI learns capabilities automatically

**User's Development Style:**
- Actively developing with you in iterative sessions
- Wants you to update PROJECT_SUMMARY.md as changes are made
- Values working code over documentation
- Prefers simple solutions over complex ones

**What NOT to Do:**
- ❌ **NEVER add hardcoded keywords or keyword matching** - This is 100% AI-native
  - No `keywords = [...]` lists
  - No `can_handle()` methods with keyword checks
  - No `if "word" in text.lower()` patterns
  - No regex fallbacks for parsing
  - All routing and parsing is via Gemini AI interpreting meaning
  - User will ALWAYS call this out if you add keywords (it's happened multiple times)
- ❌ Don't make Alfred overly chatty (he's task-focused)
- ❌ Don't make calendar-specific suggestions (this is general assistant)
- ❌ Don't suggest paid APIs or services
- ❌ Don't over-engineer simple requests
- ❌ Don't forget to update this file when making significant changes

**Common Mistakes to Avoid (Learned from Past Sessions):**
- Adding keyword fallbacks "just in case" → User wants pure AI, no fallbacks
- Suggesting features without checking if already implemented
- Missing timezone handling (user is in PST/PDT - America/Los_Angeles)
- Using wrong Gemini model (it's 2.5 Flash, not 2.0 or 1.5)
- Forgetting to update PROJECT_SUMMARY.md after changes

**When User Says "update project summary":**
- They mean this file (PROJECT_SUMMARY.md)
- Update it to reflect current state accurately
- This file is FOR YOU (future Claude sessions) to get up to speed quickly
- Focus on actionable info, not marketing copy
- Include: what's built, what's working, known issues, next steps, lessons learned

**User's Communication Style:**
- Direct and concise
- Will correct you if you misunderstand (e.g., "we are on 2.5 flash. don't get confused")
- Values quick iteration over perfect documentation
- Appreciates when you proactively use tools (TodoWrite, etc.)
- Wants PROJECT_SUMMARY.md updated regularly as a handoff document

**Development History:**
- **Session 1 (Initial):** Built core architecture, calendar feature, AI routing
- **Session 2 (2026-02-17 AM):**
  - Added bot personality (Alfred) in `bot_context.py`
  - Added conversation feature for greetings/small talk
  - Set up all APIs (Discord, Gemini, Google Calendar)
  - Fixed Gemini model name (changed from gemini-1.5-flash → gemini-2.5-flash)
  - Enhanced calendar feature:
    - Smart title & description generation
    - Recurring events support (daily, weekly, monthly with RRULE)
    - Location support
    - Custom notifications/reminders
    - Event modification/rename capability
    - Search existing events by keywords
    - Bulk modifications (rename all matching events)
  - Implemented conversation context system:
    - Hybrid approach: last 10 messages from last 15 minutes
    - Per-user context tracking
    - Enables follow-up messages and references
    - Context passed to AI router and features
  - Added console logging for user/Alfred conversation flow
  - Bot tested and operational

- **Session 3 (2026-02-17 PM):**
  - **MAJOR: Implemented dual OAuth calendar setup**
    - Split credentials: `user_credentials.json` (readonly) + `bot_credentials.json` (write)
    - User scope: `calendar.readonly` - reads from ALL calendars
    - Bot scope: `calendar` (full) - writes ONLY to bot calendar
    - Physical security via scopes, not just code logic
  - **Added schedule viewing feature**
    - New action: `view` (alongside `create` and `modify`)
    - Queries ALL user calendars (primary, secondary, shared, subscribed)
    - AI parses natural language time ranges → actual dates
    - Deduplicates events across calendars
    - Timezone-aware date filtering
  - **Removed ALL hardcoded keywords**
    - Deleted `can_handle()` methods from all features
    - Removed keyword lists from calendar, conversation, fun fact features
    - Removed keyword fallback logic from intent_router
    - 100% AI-native routing and parsing
  - **Fixed dependency issues**
    - Installed `python-dotenv` in venv
    - Moved credential files to correct `credentials/` directory
    - Re-authenticated with new OAuth scopes
  - **Fixed schedule viewing completely**
    - Timezone issues: Query with local timezone (PST/PDT) boundaries
    - Date calculation: Improved prompt to help Gemini calculate relative dates correctly
    - All-day events: Now sort first, then timed events chronologically
    - Deduplication: Events with same title + time deduplicated across calendars
    - Debug logging: Comprehensive tracking of event processing

- **Session 4 (2026-02-18):**
  - **Verified Gemini model version**
    - Confirmed all code uses `gemini-2.5-flash` (not 2.0)
    - Updated documentation to reflect correct model version
  - **MAJOR: Implemented YouTube Download Feature**
    - Download YouTube videos as MP3 (audio) or MP4 (video)
    - Support for multiple URLs per request (up to 5)
    - 100% AI-native parsing (no keyword fallbacks)
    - Smart format detection based on user intent
    - File size validation (Discord 25MB limit)
    - Uses yt-dlp + ffmpeg for downloads/conversion
    - Automatic temp file cleanup
    - Files sent directly via Discord DM
  - **Maintained AI-native architecture**
    - Removed regex/keyword fallbacks from YouTube feature
    - All parsing via Gemini 2.5 Flash
    - Consistent with zero-keyword philosophy

**Current Session Status (2026-02-18):**
- ✅ Gemini model version verified (2.5 Flash)
- ✅ Documentation updated to reflect correct model
- ✅ YouTube download feature implemented and ready
  - MP3 and MP4 support
  - Multiple URL handling (up to 5 per request)
  - 100% AI-native (no keyword matching)
  - Integrated into discord_handler.py
  - Added to requirements.txt
- ✅ All features maintain zero-keyword philosophy
- 🎯 YouTube feature complete, ready for testing
- 📝 PROJECT_SUMMARY.md updated with comprehensive handoff info

**Next Session Should Know:**
- YouTube feature is untested - may need debugging
- User interested in adding more general assistant features
- Keep maintaining AI-native architecture (no keywords!)
- Update this file after significant changes

## 🚨 Known Issues & Important Notes

### **Issue #1: Gemini API Rate Limits (KNOWN, HANDLED)**

**Problem:**
- Free tier has daily request limits (varies by model)
- gemini-2.5-flash currently in use
- Can hit quota during heavy testing

**Current Status:**
- ⚠️ May encounter rate limits during development
- Error handling in place (user-friendly messages)
- Not a blocker - just need to be aware

**If Rate Limits Hit:**
1. Wait for quota reset (daily)
2. Consider paid tier if user wants ($0.50-$1.00 per 1M tokens)
3. Could switch to different model/provider if needed

### **Issue #2: YouTube Downloads - Discord File Size Limit**

**Problem:**
- Discord free users: 25MB file size limit
- Longer YouTube videos may exceed this

**Current Handling:**
- Feature checks file size before sending
- Warns user if >25MB
- Files are downloaded but not sent

**Potential Solutions (if user requests):**
- Upload to cloud storage and send link instead
- Compress files more aggressively
- Split large files

### **Issue #3: YouTube Feature - Untested**

**Status:**
- Feature implemented but not tested in production
- May have bugs with:
  - URL extraction edge cases
  - Format detection accuracy
  - yt-dlp errors
  - ffmpeg conversion issues

**Action:** Test thoroughly before relying on it

### **Working Well - No Issues:**
- ✅ Calendar feature (create/modify/view) - fully tested
- ✅ Fun Facts feature - working
- ✅ Conversation feature - working
- ✅ AI routing - working well (0.6 confidence threshold)
- ✅ Dual OAuth calendar setup - working
- ✅ Timezone handling (PST/PDT) - fixed and working

**Conversation Context Features:**
- Remembers last 10 messages per user
- Only keeps messages from last 15 minutes
- Enables follow-up requests:
  - "Make it 2 hours instead"
  - "Change that to 3pm"
  - "Actually, move it to Friday"
- Context passed to AI router and all features
- Per-user tracking (different users have separate contexts)
- Automatic cleanup of old messages

**Logging Features:**
- Console logs now show conversation flow:
  - 👤 USER messages
  - 📚 Context indicator (shows how many messages in memory)
  - 🤖 AI routing decisions
  - 🤵 ALFRED responses
- Helps with debugging and understanding bot behavior during local development

**Known Technical Details:**
- Bot must be in a Discord server to enable DMs (Discord limitation)
- User created private server for the bot
- Actual usage is via DMs (server is just for Discord's technical requirement)
- Testing with separate calendar ID before using primary calendar
- Discord "user installation" doesn't work for bots - must use server installation

**Deployment Plan:**
- **Platform**: Fly.io (recommended)
  - Free tier: 3 small VMs (256MB RAM each) forever
  - Always-on, no spin-down (critical for reminders feature)
  - Persistent storage included
  - No credit card required for free tier
- **Why not Railway**: Removed free tier, now $5/month minimum
- **Why not Render**: Free tier spins down after 15min inactivity (bad for reminders)

**If User Reports Issues:**
- Likely related to routing (messages going to wrong feature)
- Or parsing (calendar events extracted incorrectly)
- Or conversation boundaries (Alfred too chatty or too rigid)
- Or context not working (follow-ups not understood)
- Ask for specific examples to debug

**Context System Notes:**
- Context is in-memory only (resets on bot restart)
- 15-minute window means conversations "expire" after inactivity
- 10-message limit prevents infinite memory growth
- Each user has separate context (no cross-user contamination)
- Context cleanup happens automatically on each message

---

## Testing Status

- ✅ **Local testing:** Complete - bot running and responding
- ✅ **Calendar feature:** Tested - creating events successfully
- ✅ **AI routing:** Tested - routing between calendar and conversation features
- ✅ **Conversation feature:** Tested - Alfred responding with personality
- ⏳ **Deployment:** Not yet deployed to cloud hosting
- ⏳ **Edge cases:** Ongoing testing and refinement

**Next Testing Goals:**
- Test more complex calendar scenarios (multiple events, various time formats)
- Test conversation boundaries (when to chat vs redirect to tasks)
- Test routing edge cases (ambiguous messages)

---

## Maintenance Notes

### When Adding a New Feature:
1. Create feature file in `src/features/`
2. Register in `discord_handler.py`
3. Update FEATURES.md with example
4. Update this file's "Features Implemented" section
5. Update README.md if it's a major feature

### When Modifying Core Logic:
1. Update this file's "Architecture" section
2. Update SETUP.md if setup process changes
3. Update FEATURES.md if feature interface changes

### When Changing APIs/Dependencies:
1. Update `requirements.txt`
2. Update SETUP.md with new setup steps
3. Update this file's "Technology Stack" section
4. Update `.env.example` if new env vars needed

---

**End of Summary**

This file should be updated whenever significant changes are made to the project. A new Claude chat should read this file first to understand the full context and current state.
