import os
import re
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="YT Summarizer",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }

    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid #ffffff15;
    }

    .hero h1 {
        font-size: 2.8em;
        font-weight: 700;
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero p {
        color: #aaaaaa;
        font-size: 1.1em;
    }

    .url-card {
        background: #1a1a1a;
        border-radius: 16px;
        padding: 25px;
        border: 1px solid #2a2a2a;
        margin-bottom: 20px;
    }

    .stat-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #0f3460;
        margin: 5px;
    }

    .stat-number {
        font-size: 2em;
        font-weight: 700;
        color: #ff416c;
    }

    .stat-label {
        color: #888888;
        font-size: 0.85em;
        margin-top: 5px;
    }

    .summary-card {
        background: #1a1a1a;
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #2a2a2a;
        margin-top: 20px;
        line-height: 1.8;
        color: #e0e0e0;
    }

    .summary-card h2 {
        color: #ff416c;
        border-bottom: 2px solid #ff416c30;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    .badge {
        display: inline-block;
        background: #ff416c20;
        color: #ff416c;
        border: 1px solid #ff416c50;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8em;
        font-weight: 600;
        margin: 3px;
    }

    .type-card {
        background: #1a1a1a;
        border: 2px solid #2a2a2a;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }

    .type-card:hover {
        border-color: #ff416c;
    }

    .stButton > button {
        background: linear-gradient(135deg, #ff416c, #ff4b2b) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 65, 108, 0.4) !important;
    }

    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #2a2a2a !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 1em !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ff416c !important;
    }

    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #2a2a2a !important;
        border-radius: 12px !important;
    }

    div[data-testid="stExpander"] {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
    }

    .step-box {
        background: #1a1a1a;
        border-left: 3px solid #ff416c;
        border-radius: 0 10px 10px 0;
        padding: 10px 15px;
        margin: 8px 0;
        color: #cccccc;
        font-size: 0.9em;
    }

    .footer {
        text-align: center;
        color: #444444;
        font-size: 0.8em;
        padding: 20px;
        border-top: 1px solid #1a1a1a;
        margin-top: 40px;
    }

    label {
        color: #aaaaaa !important;
    }
</style>
""", unsafe_allow_html=True)


# ── HELPER FUNCTIONS ──────────────────────────────────────
def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id)
        transcript_list = list(fetched)
        full_text = " ".join([t.text for t in transcript_list])
        return full_text, len(transcript_list)
    except TranscriptsDisabled:
        return None, "Transcripts disabled for this video"
    except NoTranscriptFound:
        return None, "No transcript found"
    except Exception as e:
        return None, f"Error: {str(e)}"


def summarize_transcript(transcript, summary_type):
    prompts = {
        "⚡ Quick Summary": f"""Analyze this transcript and provide:
1. **Topic** (1 line)
2. **Summary** (2-3 sentences)
3. **Key Points** (5 bullet points)
4. **Best For** (who should watch - 1 line)
Transcript: {transcript[:8000]}""",

        "📋 Detailed Summary": f"""Analyze this transcript and provide:
1. **Topic** (1 line)
2. **Overview** (3-4 sentences)
3. **Main Points** (detailed bullets)
4. **Key Takeaways** (3-5 actionable insights)
5. **Conclusion** (1-2 sentences)
Transcript: {transcript[:8000]}""",

        "📚 Study Notes": f"""Convert this transcript into study notes:
1. **Topic**
2. **Core Concepts** (with explanations)
3. **Key Terms** (vocabulary)
4. **Summary Points** (numbered)
5. **Review Questions** (3 questions)
Transcript: {transcript[:8000]}"""
    }

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert content summarizer. Create clear, structured summaries."
            },
            {
                "role": "user",
                "content": prompts[summary_type]
            }
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content


# ── HERO SECTION ──────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 YouTube Summarizer</h1>
    <p>Transform any YouTube video into a clear, structured summary using AI</p>
    <br>
    <span class="badge">⚡ Instant</span>
    <span class="badge">🤖 AI Powered</span>
    <span class="badge">📎 3 Summary Types</span>
    <span class="badge">📥 Downloadable</span>
</div>
""", unsafe_allow_html=True)

# ── TWO COLUMN LAYOUT ─────────────────────────────────────
left_col, right_col = st.columns([2, 1])

with left_col:
    # st.markdown('<div class="url-card">', unsafe_allow_html=True)
    st.markdown("#### 🔗 Enter YouTube URL")
    url_input = st.text_input(
        "url",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

    st.markdown("#### 📊 Summary Type")
    summary_type = st.selectbox(
        "type",
        ["⚡ Quick Summary", "📋 Detailed Summary", "📚 Study Notes"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    summarize_btn = st.button("🚀 Generate Summary")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class="url-card">
        <h4 style="color:#ff416c;">📋 How It Works</h4>
        <div class="step-box">1️⃣ Paste YouTube URL</div>
        <div class="step-box">2️⃣ Choose summary type</div>
        <div class="step-box">3️⃣ Click Generate</div>
        <div class="step-box">4️⃣ Read & Download!</div>
        <br>
        <h4 style="color:#ff416c;">✅ Supported</h4>
        <div class="step-box">youtube.com/watch?v=...</div>
        <div class="step-box">youtu.be/...</div>
        <br>
        <h4 style="color:#ff416c;">⚠️ Requirements</h4>
        <div class="step-box">Video must have captions</div>
        <div class="step-box">English works best</div>
    </div>
    """, unsafe_allow_html=True)

# ── PROCESS ───────────────────────────────────────────────
if summarize_btn:
    if not url_input.strip():
        st.warning("⚠️ Please enter a YouTube URL!")
    else:
        video_id = extract_video_id(url_input.strip())
        if not video_id:
            st.error("❌ Invalid YouTube URL!")
        else:
            with st.spinner("📥 Fetching transcript..."):
                transcript, result = get_transcript(video_id)

            if transcript is None:
                st.error(f"❌ {result}")
                st.info("💡 Try a video with captions enabled.")
            else:
                word_count = len(transcript.split())

                # Stats row
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{word_count:,}</div>
                        <div class="stat-label">Total Words</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{result:,}</div>
                        <div class="stat-label">Segments</div>
                    </div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{word_count // 130}</div>
                        <div class="stat-label">Est. Minutes</div>
                    </div>""", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{min(word_count, 8000):,}</div>
                        <div class="stat-label">Words Analyzed</div>
                    </div>""", unsafe_allow_html=True)

                # Generate summary
                with st.spinner("🤖 Generating summary..."):
                    summary = summarize_transcript(transcript, summary_type)

                # Display summary
                st.markdown(f"### 📋 {summary_type}")
                st.markdown("---")
                st.markdown(summary)
                st.markdown("---")
                
                # Actions row
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    with st.expander("📜 View Full Transcript"):
                        st.text_area("", transcript, height=250)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    YouTube Summarizer — Powered by Llama 3.3 70B via Groq API
</div>
""", unsafe_allow_html=True)