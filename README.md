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

## 🤖 Dual LLM System - Smart AI Routing

### Overview
The Dual LLM system automatically routes your queries to the most appropriate AI model:
- **📝 Text/Code Questions** → `deepseek-coder-v2:latest` (specialized for coding)
- **🖼️ Image Questions** → `llava:latest` (specialized for vision)

### ✨ Key Benefits

#### 🎯 **Smart Routing**
- **Automatic Detection**: System detects if you've uploaded an image
- **Model Selection**: Chooses the best model for your specific query
- **Seamless Experience**: Works transparently in the background

#### 🔧 **Optimized Performance**
- **deepseek-coder-v2**: Excellent at SQL, code analysis, and technical questions
- **llava**: Superior image understanding and visual analysis
- **Best Results**: Each model handles what it does best

#### 💰 **Cost Efficient**
- **Local Models**: Both models run locally via Ollama
- **No API Costs**: No charges for OpenAI or Anthropic APIs
- **Fast Responses**: Local processing for quick results

### 🛠️ Dual LLM Setup Instructions

#### **Step 1: Install Required Models**
```bash
# Install both models via Ollama
ollama pull deepseek-coder-v2:latest
ollama pull llava:latest
```

#### **Step 2: Enable Dual LLM Mode**
1. Run your application: `python run_sql_masker.py`
2. Click **"🤖 Enable AI Features"**
3. Click **"⚙️ AI Config"**
4. Set **API Provider**: `local_llm`
5. ✅ **Check "Enable Dual LLM (Text + Vision)"**
6. Set **Text/Code Model**: `deepseek-coder-v2:latest`
7. Set **Vision Model**: `llava:latest`
8. Set **Base URL**: `http://localhost:11434/v1/chat/completions`
9. Click **"Save"**

### 🎮 How Dual LLM Works

#### **Smart Detection Logic**
```python
if image_data:
    # Route to vision model
    model = "llava:latest"
    print("🖼️ Using vision model for image analysis")
else:
    # Route to text model  
    model = "deepseek-coder-v2:latest"
    print("📝 Using text model for code/text analysis")
```

#### **Example Scenarios**

**📝 Text Query** (Uses deepseek-coder-v2)
```
User: "Explain this SQL query and optimize it"
Console: 📝 Using text model: deepseek-coder-v2:latest
Response: [Detailed SQL analysis and optimization suggestions]
```

**🖼️ Image Query** (Uses llava)
```
User: Uploads database diagram + "What's in this database diagram?"
Console: 🖼️ Using vision model: llava:latest  
Response: [Detailed analysis of the database schema image]
```

**🤝 Combined Query** (Uses llava for image context)
```
User: Uploads ERD + "Generate SQL for this database design"
Console: 🖼️ Using vision model: llava:latest
Response: [Analyzes image and generates appropriate SQL]
```

### 📋 Configuration Options

#### **Alternative Models**
You can use different models based on your needs:

**For Text/Code:**
- `deepseek-coder-v2:latest` ⭐ (Recommended)
- `codellama:latest`
- `mistral:latest`
- `llama2:latest`

**For Vision:**
- `llava:latest` ⭐ (Recommended)
- `llava:13b`
- `llava:7b` (Faster, less accurate)

#### **API Integration**
The dual LLM system also works with cloud providers:

**OpenAI + Local**
- Text: `gpt-3.5-turbo` (OpenAI)
- Vision: `llava:latest` (Local)

**Mixed Cloud/Local**
- Text: `claude-3-sonnet` (Anthropic) 
- Vision: `llava:latest` (Local)

### 📊 Performance Comparison

| Scenario | Single Model | Dual LLM | Improvement |
|----------|-------------|-----------|-------------|
| **Code Questions** | llava (slow) | deepseek-coder ⚡ | 3x faster |
| **Image Questions** | deepseek (no vision) | llava 👁️ | Vision capability |
| **Mixed Queries** | One size fits all | Best tool for job | Optimal results |

### 🎉 Real-World Examples

#### **Database Design Workflow**
1. **Upload ERD image** → llava analyzes the database structure
2. **Ask for SQL generation** → llava creates tables based on visual analysis
3. **Request optimizations** → deepseek optimizes the generated SQL
4. **Ask for documentation** → deepseek writes comprehensive docs

#### **Code Review Process**  
1. **Text questions** → deepseek provides detailed code analysis
2. **Screenshot of errors** → llava identifies UI issues
3. **Performance questions** → deepseek suggests optimizations
4. **Visual debugging** → llava helps with layout problems

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

**Dual LLM Issues**
- **"Model not found" Error**: `ollama pull deepseek-coder-v2:latest && ollama pull llava:latest`
- **Images Not Working**: Check if vision model is running: `ollama list`
- **Dual LLM Not Active**: Ensure "Enable Dual LLM" is checked in AI Config

### Verification Commands
```bash
# Check Ollama models
ollama list

# Test individual models
ollama run deepseek-coder-v2:latest "Hello"
ollama run llava:latest "Describe this image"

# Check app configuration
python -c "from ai_config import AIConfig; print(AIConfig().config)"
```

### Getting Help
1. Check this README
2. Verify all dependencies are installed
3. Test with simple SQL queries first
4. Check console output for error messages

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

## 🎯 Quick Start Summary

1. **Install models**: `ollama pull deepseek-coder-v2:latest && ollama pull llava:latest`
2. **Run app**: `python run_sql_masker.py`
3. **Enable dual LLM**: AI Config → Check "Enable Dual LLM"
4. **Use it**: Text questions get deepseek, images get llava automatically!

**Ready to mask your SQL data with AI-powered intelligence?** 🚀

**You now have the best of both worlds - specialized AI models working together seamlessly!** ✨