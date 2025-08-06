# 🚀 Enhanced SQL Masker with Dual LLM & Modern Interface

A professional SQL data masking tool with AI-powered features, modern Claude-like interface, and dual LLM smart routing.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Key Features

### 🛡️ Advanced SQL Masking
- **Smart Data Masking**: Automatically mask sensitive data in SQL queries
- **Realistic Name Generation**: Replace masked values with realistic-looking names
- **Syntax Highlighting**: Real-time SQL syntax highlighting with masked value detection
- **Import/Export Mappings**: Save and reuse masking configurations
- **Diff Viewer**: Compare original vs masked SQL with highlighting

### 🤖 AI-Powered Analysis
- **Dual LLM Smart Routing**: 
  - 📝 **Text/Code**: `deepseek-coder-v2:latest` for SQL analysis and optimization
  - 🖼️ **Images**: `llava:latest` for visual analysis and diagrams
- **Code Understanding**: AI explains SQL structure, logic, and purpose
- **Code Modification**: Natural language instructions to modify SQL
- **Multi-Provider Support**: OpenAI, Anthropic, or local models via Ollama

### 🎨 Modern Interface
- **Claude-like Chat Interface**: Professional message bubbles and layout
- **Dark/Light Theme Toggle**: 🌙/☀️ Switch between themes with persistence
- **Zoom Controls**: 🔍+/🔍- Scale entire interface (50%-300%)
- **Image Support**: Upload or paste images directly in chat
- **Dynamic Sizing**: Chat bubbles auto-resize to fit content (up to 60 lines)

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Anonimiser_GUI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **For local LLM support (optional)**:
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull required models
   ollama pull deepseek-coder-v2:latest
   ollama pull llava:latest
   ```

### Running the Application

```bash
python run_sql_masker.py
```

## 🎯 Usage Guide

### Basic SQL Masking

1. **Enter SQL**: Paste your SQL query in the input area
2. **Prepare Masking**: Click "Prepare Masking" to analyze
3. **Configure Mapping**: Review and edit detected tables/columns
4. **Mask SQL**: Generate masked version
5. **Export/Import**: Save configurations for reuse

### AI Features Setup

1. **Enable AI**: Click "🤖 Enable AI Features"
2. **Configure**: Click "⚙️ AI Config"
3. **Choose Setup**:
   
   **Option A: Local Models (Recommended)**
   - API Provider: `local_llm`
   - ✅ Enable Dual LLM (Text + Vision)
   - Text Model: `deepseek-coder-v2:latest`
   - Vision Model: `llava:latest`
   - Base URL: `http://localhost:11434/v1/chat/completions`
   
   **Option B: Cloud APIs**
   - API Provider: `openai` or `anthropic`
   - Enter your API key
   - Choose model (e.g., `gpt-4`, `claude-3-sonnet`)

4. **Test Connection**: Verify setup works
5. **Save Configuration**

### Using AI Features

- **🧠 Understand Code**: AI analyzes SQL structure and provides explanations
- **✏️ Modify Code**: Give natural language instructions to modify SQL
- **🖼️ Image Analysis**: Upload database diagrams or screenshots for analysis
- **💬 Interactive Chat**: Ask follow-up questions in modern chat interface

### Interface Features

- **Theme Toggle**: Click 🌙/☀️ in chat header to switch themes
- **Zoom Controls**: Use 🔍+/🔍- to scale interface
- **Message Navigation**: 
  - **Enter**: Send message
  - **Shift+Enter**: New line in message
  - **Ctrl+Shift+V**: Paste images from clipboard

## 📁 Project Structure

```
Anonimiser_GUI/
├── 🚀 run_sql_masker.py          # Main application launcher
├── 🖥️ sql_mask_gui.py            # Core GUI and masking logic
├── 🤖 ai_config.py               # AI configuration and API handling
├── 🎨 ai_interface.py            # AI interface integration
├── 💬 modern_ai_interface.py     # Modern chat interface
├── 🎨 theme_manager.py           # Theme and zoom management
├── 📋 requirements.txt           # Python dependencies
├── ⚙️ theme_config.json          # Theme settings (auto-generated)
└── 📚 README.md                  # This file
```

## 🔧 Configuration

### Theme & Zoom Settings
Settings are automatically saved to `theme_config.json`:
```json
{
  "theme": "dark",
  "zoom_level": 1.2
}
```

### AI Configuration
AI settings are managed through the GUI and stored securely.

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message in chat |
| `Shift+Enter` | New line in message |
| `Ctrl+Shift+V` | Paste image from clipboard |
| `Ctrl+C` | Copy text |

## 🚨 Requirements

### Python Dependencies
- **Python 3.8+**
- **tkinter** (usually included with Python)
- **requests** - HTTP requests for AI APIs
- **pyperclip** - Clipboard operations
- **sqlparse** - SQL parsing
- **sql-metadata** - SQL metadata extraction
- **Pillow** - Image processing

### Optional Dependencies
- **Ollama** - For local LLM support
- **deepseek-coder-v2** - Local coding model
- **llava** - Local vision model

## 🌟 Advanced Features

### Dual LLM Smart Routing
The application automatically selects the best model for each task:
- **Code questions** → deepseek-coder-v2 (optimized for programming)
- **Image questions** → llava (optimized for vision)
- **Mixed queries** → Intelligent routing based on content

### Modern Interface Design
- **Professional Layout**: Claude-inspired design with proper spacing
- **Dynamic Bubbles**: Messages auto-resize to fit content (up to 60 lines)
- **Theme Persistence**: Remember user preferences
- **Responsive Design**: Works well at different zoom levels

## 🐛 Troubleshooting

### Common Issues

**AI Features Not Working**
- Ensure `requests` is installed: `pip install requests`
- Check API key is correct
- For local LLM, verify Ollama is running: `ollama list`

**Image Upload Issues**
- Ensure `Pillow` is installed: `pip install Pillow`
- Check image format is supported (PNG, JPG, etc.)
- For clipboard paste, use Ctrl+Shift+V

**Interface Issues**
- Theme not switching: Check `theme_config.json` permissions
- Zoom not working: Restart application
- Window not centering: Update display drivers

### Getting Help
1. Check this README
2. Verify all dependencies are installed
3. Test with simple SQL queries first
4. Check console output for error messages

## 📈 Version History

- **v2.0**: Modern interface with dual LLM support and enhanced chat bubbles
- **v1.x**: Basic SQL masking functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama** for local LLM support
- **OpenAI & Anthropic** for cloud AI services
- **Claude** for interface design inspiration
- **SQL parsing libraries** for robust SQL analysis

---

**Ready to mask your SQL data with AI-powered intelligence?** 🚀

Run `python run_sql_masker.py` to get started!