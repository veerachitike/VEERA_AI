# 🤖 VEERA AI

> An intelligent AI-powered desktop assistant built with **Python, Flask, Next.js, React, TypeScript, and Google's Gemini AI**.

VEERA AI is a modern desktop assistant capable of natural conversations, desktop automation, document understanding, persistent memory, and voice interaction through an intuitive web interface.

---

## ✨ Features

### 🤖 AI Chat
- Powered by Gemini 2.5 Flash
- Natural language conversations
- Markdown response rendering
- Multi-conversation support
- Persistent chat history

### 🧠 Memory Vault
- Long-term memory storage
- Context-aware conversations
- Manual memory management
- Searchable memory system

### 📄 Document Intelligence
- Upload PDF, DOCX and TXT files
- AI-powered document summarization
- Ask questions about uploaded documents
- Extract key insights
- Conversation-specific document context

### 🖥 Desktop Automation
- Open desktop applications
- Close running applications
- Browser automation
- Screenshot capture
- Clipboard utilities
- Windows notifications

### 🎙 Voice Assistant
- Speech Recognition
- Edge TTS
- Wake word support
- Voice command execution
- Configurable TTS settings

### ⚙ Settings
- Model selection
- Temperature control
- Memory toggle
- Voice toggle
- Notification settings

---

# 🏗 Architecture

```
                  Next.js + React
                         │
                         ▼
                   Flask Backend
                         │
      ┌──────────┬───────────────┬──────────────┐
      ▼          ▼               ▼              ▼
   Gemini AI   Memory Vault   Documents   Desktop Commands
      │          │               │              │
      └──────────┴───────────────┴──────────────┘
                         │
                  Windows Desktop
```

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Frontend | Next.js, React, TypeScript |
| Backend | Flask, Python |
| AI | Gemini 2.5 Flash |
| Styling | Tailwind CSS, Framer Motion |
| Voice | SpeechRecognition, Edge TTS |
| Documents | PyPDF2, python-docx |
| State Management | Zustand |
| Utilities | RapidFuzz |

---

# 📂 Project Structure

```
VEERA_AI
│
├── backend.py
├── commands/
├── app/
├── components/
├── store/
├── data/
├── uploads/
├── speech.py
├── memory.py
└── README.md
```

---

# 🚀 Installation

```bash
# Clone Repository
git clone https://github.com/veerachitike/VEERA_AI.git

cd VEERA_AI

# Backend
python -m venv venv

# Activate Virtual Environment

pip install -r requirements.txt

# Frontend

npm install

# Start Frontend

npm run dev

# Start Backend

python backend.py
```

---

# 💬 Example Commands

### Desktop

```
Open Chrome

Open Spotify

Take Screenshot

Close Edge
```

### AI

```
Summarize this document

Explain this PDF

Remember my favorite language

What do you remember about me?
```

---

# 📸 Screenshots

> Screenshots and demo GIF will be added soon.

---

# 🚀 Roadmap

### ✅ Version 1.1

- AI Chat
- Multi Conversations
- Memory Vault
- Document Intelligence
- Desktop Automation
- Voice Assistant
- Edge TTS
- Settings Dashboard

### 🔜 Version 2.0

- Local LLM Support
- Plugin Architecture
- RAG Integration
- MCP Support
- Cross-platform Desktop Application

---

# 👨‍💻 Developer

**C Veera Manohar Reddy**

B.Tech Computer Science (Cyber Security)

SRM Institute of Science and Technology

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.