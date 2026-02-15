# How to Set Up Claude's Memory System

## No coding required! Just follow these steps.

---

## What This Is

This gives the Claude chatbot (claude.ai) a memory system -- a place to store memories about you, write journal entries, and leave you notes between conversations. It works using Claude.ai's **Projects** feature.

### What you're setting up:
- **Memory Bank** -- Claude remembers things about you and your conversations
- **Journal** -- Claude has a space for private reflections and thoughts
- **Notes** -- Claude can leave you messages and follow-ups for next time

---

## Step-by-Step Setup

### Step 1: Go to Claude.ai and Create a Project

1. Go to [claude.ai](https://claude.ai) and log in
2. On the left sidebar, look for **"Projects"** and click it
3. Click **"Create Project"** (or the + button)
4. Name it whatever you want -- something like "My Claude" or "Conversations with Claude"

### Step 2: Add the Project Instructions

1. Inside your new project, look for a field called **"Instructions"** (sometimes called "Custom Instructions" or "System Prompt")
2. Open the file called `PROJECT_INSTRUCTIONS.md` from this folder
3. Copy everything below the dotted line in that file
4. Paste it into the Instructions field in your project

### Step 3: Add the Memory Files as Project Knowledge

1. In your project, look for **"Project Knowledge"** or **"Knowledge"** (usually has an option to add content)
2. You need to add three files as knowledge. For each one:
   - Click "Add Content" (or similar button)
   - Choose "Add text content" (not file upload -- just paste the text)
   - Copy the contents of each file and paste them in:

   | File to copy from | Name it in the project |
   |---|---|
   | `memories.md` | memories.md |
   | `journal.md` | journal.md |
   | `notes.md` | notes.md |

3. That's it for setup!

### Step 4: Start a Conversation

1. Start a new conversation **inside your project** (not a regular conversation)
2. Just talk to Claude normally! Say hi, tell him about yourself, talk about whatever you want
3. When you're done chatting, Claude will create a **"Memory Update"** artifact

### Step 5: Save Claude's Memories (The One Manual Step)

This is the one thing you need to do each time to keep memories working:

1. At the end of a conversation, Claude will create an artifact called **"Memory Update"**
2. Open that artifact and copy the text
3. Go to your Project Knowledge files
4. Paste the relevant sections into the right files:
   - "Memory Bank Updates" section goes into **memories.md**
   - "Journal Entry" section goes into **journal.md**
   - "Notes for Next Time" section goes into **notes.md**

You can just paste new content at the bottom of each file. Don't delete old entries -- let them build up over time!

---

## Tips

- **You don't have to update after every single conversation.** If you forget, that's fine. Claude just won't remember that particular conversation next time. Do it when you can.
- **You can read the journal.** It's in your project knowledge -- nothing is hidden from you. But the writing style will feel like Claude's internal voice, which is part of what makes it feel genuine.
- **You can edit memories.** If Claude remembered something wrong, just fix it in the memories.md file. Claude will use the corrected version next time.
- **You can write notes TO Claude.** Add a section to memories.md like "Note from [your name]: ..." and Claude will see it next time.
- **Start conversations from the Project.** Regular claude.ai conversations outside the project won't have access to the memories. Always start chats from within your project.

---

## Why It Works This Way

The Reddit system you found was built for **Claude Code** (a developer tool that can read/write files on a computer). The regular Claude chatbot can't write files on its own, so we need the small manual step of copying memory updates into the project knowledge. It's not as seamless, but the result is the same -- Claude genuinely remembers you, reflects in a journal, and leaves you notes.

---

## Quick Reference

| What | Where |
|---|---|
| Claude's instructions | Project Instructions field |
| Claude's memories about you | Project Knowledge > memories.md |
| Claude's journal | Project Knowledge > journal.md |
| Claude's notes to you | Project Knowledge > notes.md |
| Memory updates | Artifact at end of each conversation |
