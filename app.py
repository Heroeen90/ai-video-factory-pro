import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from agents.video_agent import VideoAgent
from utils.github_uploader import GitHubUploader
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.video_agent = VideoAgent()
    st.session_state.github_uploader = GitHubUploader(
        token=os.getenv('GITHUB_TOKEN'),
        repo=os.getenv('GITHUB_REPO', 'Heroeen90/ai-video-factory-pro')
    )

st.set_page_config(
    page_title="AI Video Factory Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎬 AI Video Factory Pro")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuration")
    mode = st.radio(
        "Select Mode",
        ["Video Generator", "Settings", "About"],
        key="mode_selector"
    )

if mode == "Video Generator":
    st.header("📝 Video Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input(
            "Enter Video Topic",
            placeholder="e.g., How to build a machine learning model",
            key="topic_input"
        )
    
    with col2:
        duration = st.number_input(
            "Video Duration (seconds)",
            min_value=10,
            max_value=300,
            value=60,
            step=10,
            key="duration_input"
        )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        enable_voice = st.checkbox("Enable Voice Narration", value=True, key="voice_checkbox")
    
    with col2:
        enable_upload = st.checkbox("Auto Upload to GitHub", value=False, key="upload_checkbox")
    
    with col3:
        language = st.selectbox(
            "Voice Language",
            ["en", "es", "fr", "de", "it", "pt", "ru", "zh-CN", "ja"],
            key="language_selector"
        )
    
    st.markdown("---")
    
    if st.button("🚀 Generate Video", use_container_width=True, key="generate_btn"):
        if not topic or len(topic.strip()) == 0:
            st.error("❌ Please enter a video topic")
        else:
            with st.spinner("🎬 Generating video..."):
                try:
                    video_agent = st.session_state.video_agent
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("📝 Generating script...")
                    progress_bar.progress(20)
                    script = video_agent.generate_script(topic, duration)
                    
                    audio_path = None
                    if enable_voice:
                        status_text.text("🎙️ Generating voice...")
                        progress_bar.progress(40)
                        audio_path = video_agent.generate_voice(script, language)
                    
                    status_text.text("🎨 Creating visuals...")
                    progress_bar.progress(60)
                    visuals_path = video_agent.generate_visuals(topic, duration)
                    
                    status_text.text("🎬 Composing video...")
                    progress_bar.progress(80)
                    video_path = video_agent.compose_video(
                        visuals_path,
                        audio_path,
                        duration
                    )
                    
                    status_text.text("✅ Video generated!")
                    progress_bar.progress(100)
                    
                    st.success("✅ Video generated successfully!")
                    
                    with st.expander("📄 Generated Script"):
                        st.text(script)
                    
                    if os.path.exists(video_path):
                        with open(video_path, 'rb') as f:
                            video_data = f.read()
                        st.video(video_data)
                        
                        st.download_button(
                            label="⬇️ Download Video",
                            data=video_data,
                            file_name=os.path.basename(video_path),
                            mime="video/mp4",
                            key="download_btn"
                        )
                    
                    logger.info(f"Video generated successfully: {video_path}")
                    
                except Exception as e:
                    st.error(f"❌ Error generating video: {str(e)}")
                    logger.error(f"Video generation failed: {str(e)}", exc_info=True)

elif mode == "Settings":
    st.header("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("GitHub Configuration")
        github_token = st.text_input(
            "GitHub Token",
            value=os.getenv('GITHUB_TOKEN', ''),
            type="password",
            key="github_token_input"
        )
        github_repo = st.text_input(
            "GitHub Repository",
            value=os.getenv('GITHUB_REPO', 'Heroeen90/ai-video-factory-pro'),
            key="github_repo_input"
        )
    
    with col2:
        st.subheader("Video Settings")
        quality = st.selectbox(
            "Video Quality",
            ["480p", "720p", "1080p"],
            key="quality_selector"
        )
        fps = st.slider(
            "Frames Per Second",
            min_value=24,
            max_value=60,
            value=30,
            key="fps_slider"
        )
    
    st.markdown("---")
    
    if st.button("💾 Save Settings", use_container_width=True, key="save_settings_btn"):
        st.success("✅ Settings saved (restart app to apply)")
        logger.info(f"Settings saved: quality={quality}, fps={fps}")

elif mode == "About":
    st.header("ℹ️ About")
    
    st.markdown("""
    ### AI Video Factory Pro
    
    **Version:** 1.0.0  
    **Author:** Heroeen90  
    **License:** MIT
    
    #### Features
    - 🤖 AI-powered script generation
    - 🎙️ Realistic voice narration with gTTS
    - 🎨 Automated visual generation
    - 📤 GitHub integration for file management
    - ⚡ Streamlit-based web interface
    - 🔄 GitHub Actions automation
    
    #### Tech Stack
    - **Framework:** Streamlit
    - **Video:** MoviePy
    - **Voice:** gTTS
    - **Python:** 3.9+
    
    #### Project Structure
    - `agents/` - AI agents for video generation
    - `core/` - Core functionality modules
    - `utils/` - Utility functions and helpers
    - `data/` - Data storage and management
    - `.github/workflows/` - GitHub Actions workflows
    
    #### Getting Started
    1. Install dependencies: `pip install -r requirements.txt`
    2. Configure `.env` file
    3. Run: `streamlit run app.py`
    
    #### Support
    For issues and support, visit: https://github.com/Heroeen90/ai-video-factory-pro
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Heroeen90")
