# AI Video Factory Pro

A production-ready AI-powered video generation platform built with Streamlit.

## Features

- Automated video script generation from topics
- AI voice narration using gTTS
- Video composition with MoviePy
- GitHub integration for file uploads
- Scheduled automation via GitHub Actions
- Complete project structure with agents and utilities

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Project Structure

```
.
├── agents/               # AI agents for video generation
├── core/                 # Core functionality modules
├── utils/                # Utility functions
├── data/                 # Data storage
├── .github/workflows/    # GitHub Actions workflows
├── app.py                # Main Streamlit application
└── requirements.txt      # Python dependencies
```

## Configuration

Create a `.env` file with:

```
GITHUB_TOKEN=your_token_here
GITHUB_REPO=owner/repo
```
