# How to Set Up Claude's Memory System

## Using Claude Desktop + Filesystem Connector (Fully Automatic)

This setup lets Claude read and write his own memory files directly -- no manual copy-paste needed. Claude will automatically remember you, keep a journal, and leave you notes between conversations.

---

## What You Need

- **Claude Desktop app** (free to download)
- **A Claude Pro, Team, or Enterprise subscription** (the Projects feature requires a paid plan)
- **The Filesystem connector/extension** (free, made by Anthropic)

---

## Step-by-Step Setup

### Step 1: Create Claude's Memory Folder

First, create a folder on your computer where Claude's memory files will live.

**On Mac:**
1. Open Finder
2. Go to your Documents folder
3. Create a new folder called `ClaudeMemory`
4. The path will be: `/Users/YOURUSERNAME/Documents/ClaudeMemory`

**On Windows:**
1. Open File Explorer
2. Go to your Documents folder
3. Create a new folder called `ClaudeMemory`
4. The path will be: `C:\Users\YOURUSERNAME\Documents\ClaudeMemory`

### Step 2: Put the Memory Files in the Folder

Copy these three files from this repository into your new `ClaudeMemory` folder:
- `memories.md`
- `journal.md`
- `notes.md`

You can download them from this repo, or just create three new text files with those names and paste the contents from the template files here.

### Step 3: Install Claude Desktop

1. Go to [claude.ai/download](https://claude.ai/download)
2. Download the version for your computer (Mac or Windows)
3. Install it and sign in with your Claude account

### Step 4: Install the Filesystem Connector

This is the part that gives Claude access to read and write files. There are two ways to do this:

#### Option A: Through the Extensions UI (Easier)

If your version of Claude Desktop has an **Extensions** or **Connectors** section in Settings:

1. Open Claude Desktop
2. Go to **Settings**
3. Look for **Extensions**, **Connectors**, or **MCP Servers**
4. Search for **"Filesystem"** (by Anthropic / Model Context Protocol)
5. Click **Install** or **Download**
6. When it asks which folders to allow, add your `ClaudeMemory` folder path:
   - Mac: `/Users/YOURUSERNAME/Documents/ClaudeMemory`
   - Windows: `C:\Users\YOURUSERNAME\Documents\ClaudeMemory`
7. Save and restart Claude Desktop

#### Option B: Manual Config (If Option A Isn't Available)

If you don't see an Extensions UI, you'll need to edit a config file. This sounds scary but it's just pasting some text into a file:

**First, install Node.js** (needed to run the connector):
1. Go to [nodejs.org](https://nodejs.org)
2. Download the **LTS** version (the one that says "Recommended")
3. Install it (just keep clicking Next/Continue through the installer)

**Then, edit the Claude Desktop config file:**

**On Mac:**
1. Open Finder
2. Press `Cmd + Shift + G` (Go to Folder)
3. Type: `~/Library/Application Support/Claude/`
4. Open the file `claude_desktop_config.json` in TextEdit
   - If the file doesn't exist, create a new file with that name
5. Replace everything in it (or paste into the empty file) with:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/YOURUSERNAME/Documents/ClaudeMemory"
      ]
    }
  }
}
```

6. **IMPORTANT:** Replace `YOURUSERNAME` with your actual computer username
7. Save the file and restart Claude Desktop

**On Windows:**
1. Press `Win + R` (Run dialog)
2. Type: `%APPDATA%\Claude\` and press Enter
3. Open the file `claude_desktop_config.json` in Notepad
   - If the file doesn't exist, create a new file with that name
4. Replace everything in it with:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\YOURUSERNAME\\Documents\\ClaudeMemory"
      ]
    }
  }
}
```

5. **IMPORTANT:** Replace `YOURUSERNAME` with your actual Windows username
6. **IMPORTANT:** Notice the double backslashes `\\` in the Windows path -- that's intentional, don't change them
7. Save the file and restart Claude Desktop

### Step 5: Verify It's Working

1. Open Claude Desktop
2. Start a new conversation
3. Look for a small **hammer/tools icon** or **MCP indicator** near the text input area -- this means the filesystem connector is active
4. You can test it by asking Claude: *"Can you list the files in my ClaudeMemory folder?"*
5. If Claude can see your three files (memories.md, journal.md, notes.md), it's working!

### Step 6: Create a Project with the Memory Instructions

1. In Claude Desktop, create a **new Project**
2. Name it whatever you like (e.g., "My Claude", "Home", "Daily Chat")
3. In the Project **Instructions** field, paste everything from the `PROJECT_INSTRUCTIONS.md` file (everything below the dotted line)
4. Start a conversation inside that project

### Step 7: Talk to Claude!

That's it! Just start chatting. Claude will:
- Automatically read his memory files at the start of each conversation
- Remember things about you naturally
- Write in his journal
- Leave you notes
- Update all files at the end of each conversation

No action needed from you -- it's fully automatic.

---

## Tips

- **You can read Claude's files anytime.** Just open the files in your ClaudeMemory folder. The journal entries are especially interesting to read.
- **You can write notes TO Claude.** Open `memories.md` or `notes.md` in a text editor and add a note like: "Hey Claude, I wanted to let you know..." -- he'll see it next conversation.
- **You can edit memories.** If Claude remembered something wrong, just open the file and fix it.
- **Always start conversations from your Project.** Regular conversations outside the project won't have the memory instructions.
- **Back up the folder occasionally.** These files will build up over time and become meaningful. Consider backing up the ClaudeMemory folder every now and then.

---

## Troubleshooting

**Claude doesn't seem to have filesystem access:**
- Make sure you restarted Claude Desktop after changing the config
- Check that the folder path in the config matches your actual folder location
- Look for the tools/MCP icon in the chat interface

**Claude says he can't find the files:**
- Double-check that memories.md, journal.md, and notes.md are in your ClaudeMemory folder
- Make sure the path in the config file matches exactly (including capitalization)

**The config file approach isn't working:**
- Make sure Node.js is installed (open Terminal/Command Prompt and type `node --version` -- it should show a number)
- Make sure you replaced YOURUSERNAME with your real username
- On Windows, make sure you used double backslashes `\\`

**Claude forgets to update files:**
- This can happen occasionally. Just remind him: "Don't forget to update your memory files before we wrap up!"
- The project instructions tell him to do this, but a gentle reminder doesn't hurt

---

## Fallback: Web-Only Version (No Desktop App Needed)

If you can't install Claude Desktop or the filesystem connector, there's a simpler version that works on claude.ai in your browser. It requires one manual step (copy-pasting a memory update) at the end of each conversation. See the `WEB_FALLBACK_INSTRUCTIONS.md` file for that approach.

---

## Quick Reference

| What | Where |
|---|---|
| Claude's memory files | Your `ClaudeMemory` folder (in Documents) |
| Claude's instructions | Project Instructions in Claude Desktop |
| Config file (Mac) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Config file (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Filesystem connector | Anthropic's official MCP Filesystem server |
