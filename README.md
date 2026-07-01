# 🎬 YouTube AI Summarizer

An AI-powered YouTube video summarization application built with **Python**, **Streamlit**, and **Llama 3.3 70B (Groq API)**. The application automatically extracts transcripts from YouTube videos and generates structured summaries using Large Language Models (LLMs).

---

## 🚀 Features

- 🔗 Accepts YouTube video URLs
- 📝 Automatically extracts video transcripts
- 🤖 Generates AI-powered summaries using Llama 3.3 70B
- ⚡ Supports multiple summary formats:
  - Quick Summary
  - Detailed Summary
  - Study Notes
- 📊 Displays transcript statistics
- 📥 Download summaries as text files
- 📜 View the complete transcript
- 🎨 Modern responsive Streamlit UI

---

## 🛠️ Tech Stack

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python

### AI & APIs
- Groq API
- Llama 3.3 70B Versatile
- Prompt Engineering

### Libraries
- youtube-transcript-api
- python-dotenv
- streamlit
- groq
- re
- os

---

# 🏗️ Architecture

```
                User
                  │
                  ▼
        Streamlit Web Interface
                  │
                  ▼
          YouTube URL Parser
                  │
                  ▼
     YouTube Transcript API
                  │
                  ▼
        Transcript Extraction
                  │
                  ▼
     Prompt Engineering Layer
                  │
                  ▼
       Groq Llama 3.3 70B API
                  │
                  ▼
      AI Generated Summary
                  │
                  ▼
     Display & Download Result
```

---

# ✨ Summary Types

## ⚡ Quick Summary

- Topic
- Short overview
- Key points
- Best suited audience

---

## 📋 Detailed Summary

- Topic
- Complete overview
- Detailed explanations
- Key takeaways
- Conclusion

---

## 📚 Study Notes

- Topic
- Core concepts
- Important terms
- Numbered notes
- Review questions

---

# 📸 Application Workflow

1. Paste a YouTube URL.
2. Select the desired summary type.
3. Fetch the video transcript.
4. Send transcript to the Llama 3.3 model.
5. Receive structured AI-generated summary.
6. View, copy, or download the summary.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/jojotjo/youtube_summarizer.git
cd youtube_summarizer
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📂 Project Structure

```
youtube_summarizer/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
└── screenshots/
```

---

# 🧠 AI Workflow

1. Extract transcript using **youtube-transcript-api**
2. Clean transcript
3. Generate prompt based on selected summary type
4. Send prompt to **Llama 3.3 70B** via **Groq API**
5. Receive structured response
6. Display summary in Streamlit

---

# 📊 Example Output

### Input

```
https://www.youtube.com/watch?v=XXXXXXXXXXX
```

### Output

```
Topic:
Introduction to System Design

Summary:
...

Key Points:
• ...
• ...
• ...

Conclusion:
...
```

---

# 💡 Key Highlights

- AI-powered summarization using Large Language Models
- Prompt engineering for multiple summary formats
- Automatic transcript extraction
- Interactive Streamlit dashboard
- Downloadable summaries
- Responsive dark-themed UI
- Error handling for invalid URLs and unavailable transcripts

---

# 🔮 Future Improvements

- Multi-language transcript support
- Video title and thumbnail preview
- Timestamp-based summaries
- PDF and DOCX export
- Keyword extraction
- Mind map generation
- Quiz generation from videos
- Speaker identification
- Chat with video functionality (RAG)
- Support for longer videos through transcript chunking

---

# 👨‍💻 Author

**Prabhjot Kaur**

- LinkedIn: https://linkedin.com/in/prabhjot-kaur
- GitHub: https://github.com/jojotjo

---

# ⭐ If you found this project useful, consider giving it a star!
