---
title: NCSU Research Assistant
emoji: 🐺
colorFrom: red
colorTo: red
sdk: streamlit
sdk_version: "1.28.0"
python_version: "3.11"
app_file: app.py
pinned: false
---

# 🐺 NCSU Research Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A clean, deployable version of the NCSU Research Assistant web interface - an AI-powered research tool for NC State University that searches the university website, extracts content, and generates comprehensive answers with citations.

## 📁 File Structure

```
Chatbot_Deploy/
├── user_interface.py              # Main Streamlit web interface
├── ncsu_advanced_config_base.py  # Core research engine
├── requirements.txt               # Python dependencies
├── run_web_interface.bat         # Windows batch launcher
├── run_web_interface.ps1         # PowerShell launcher
├── NC_State_Wolfpack_logo.svg.png # Logo (left header)
├── NC-State-University-Logo.png   # Logo (right header)
├── src/                           # Source modules
│   ├── __init__.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── ncsu_scraper.py       # Website scraper
│   │   ├── content_aggregator.py # Content processor
│   │   └── models.py             # Data models
│   └── utils/
│       ├── __init__.py
│       └── logger.py              # Logging utility
└── results/                       # Output directory
    └── .gitkeep
```

## 🌟 Features

- **🔍 Intelligent Search**: Searches NCSU website using domain-specific search
- **📄 Full Content Extraction**: Extracts 100% content from web pages using MarkItDown
- **🤖 LLM-Based Grading**: Uses AI to score content relevance (0-1 scale)
- **📊 Smart Filtering**: Filters content by relevance threshold
- **🔗 Rich Citations**: Generates answers with clickable source links
- **🎨 Beautiful UI**: NC State branded interface with Wolfpack logos
- **⚙️ Configurable**: Adjustable search depth, relevance threshold, and LLM settings

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium web scraping)
- **Optional**: OpenAI API key, Anthropic API key, or Hugging Face token
  - **Note**: Hugging Face models are **free** and work without any API key!

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ncsu-research-assistant.git
cd ncsu-research-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key (Optional)

**Option A: Use Hugging Face (Free, Recommended)**
- No API key required! Just select "huggingface" as the provider in the interface.
- Optional: Add `HF_TOKEN` for higher rate limits (get from https://huggingface.co/settings/tokens)

**Option B: Use OpenAI or Anthropic**
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-api-key-here
# OR
ANTHROPIC_API_KEY=your-api-key-here
```

Or set it as an environment variable:

```bash
# Windows
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

**Note**: Never commit your `.env` file to Git! It's already in `.gitignore`.

### 3. Launch the Web Interface

**Windows (Batch):**
```cmd
run_web_interface.bat
```

**Windows (PowerShell):**
```powershell
.\run_web_interface.ps1
```

**Manual:**
```bash
streamlit run user_interface.py
```

### 4. Access the Interface

Open your browser and go to:
```
http://localhost:8501
```

## 📋 Requirements

- Python 3.8+
- Chrome browser (for Selenium)
- ChromeDriver (automatically managed by Selenium)

## 🔧 Configuration

All settings can be adjusted in the web interface sidebar:
- LLM Provider (OpenAI/Anthropic/Mock)
- Model selection
- Search parameters
- Relevance threshold

## 📊 Output

All research results are automatically saved to the `results/` directory:
- `answer_[query]_[timestamp].txt` - Human-readable answer
- `data_[query]_[timestamp].json` - Complete research data
- `config_[query]_[timestamp].yaml` - Configuration used

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NC State University for providing the website content
- OpenAI and Anthropic for LLM APIs
- Streamlit for the web framework
- All contributors and users

## 🐺 Go Pack!

Built with ❤️ for NC State University

**Think and Do!**
