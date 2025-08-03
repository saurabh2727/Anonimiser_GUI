# 🎭 Enhanced SQL Masker Tool v2.0 - Modular

A powerful GUI application for masking sensitive information in SQL queries with **AI-enhanced semantic mapping** and **comprehensive zoom functionality**.

## 🚀 Key Features

### **Core Masking Capabilities**
- **Intelligent SQL Analysis**: Automatically detects tables, columns, strings, functions, and aliases
- **Smart Masking**: Replace sensitive names with anonymized equivalents
- **Reversible Operations**: Unmask SQL back to original form using saved mappings
- **Mapping Management**: Save/load mapping configurations for consistency

### **🧠 AI-Enhanced Masking (NEW!)**
- **Semantic Preservation**: AI generates meaningful masked names instead of random strings
- **Domain Awareness**: Automatically detects business context (telecom, finance, retail, etc.)
- **Consistent Relationships**: Maintains logical connections between related entities
- **Toggle Mode**: Switch between traditional random and AI-enhanced semantic masking

### **🔍 Advanced Zoom & Readability**
- **Global Zoom Controls**: Zoom all sections simultaneously
- **Individual Section Zoom**: Fine-tune each text area independently  
- **Keyboard Shortcuts**: `Ctrl+Plus/Minus` for quick zoom, `Ctrl+0` to reset
- **Expandable Interface**: Drag-to-resize sections for optimal viewing

### **🤖 AI Assistant Features**
- **Code Understanding**: Get detailed SQL analysis and explanations
- **Natural Language Modifications**: Describe changes in plain English
- **Interactive Conversations**: Follow-up questions about your SQL
- **Multiple AI Providers**: OpenAI, Anthropic, Local LLM (Ollama), Custom APIs

## 📋 Requirements

### Python Dependencies
```bash
pip install tkinter sqlparse requests pyperclip
```

### Optional AI Requirements
- **Local LLM**: Install [Ollama](https://ollama.ai) with `deepseek-coder-v2:latest` model
- **Cloud AI**: API keys for OpenAI or Anthropic (optional)

## 🎯 Quick Start

1. **Launch the Application**:
   ```bash
   python sql_mask_gui_modular.py
   ```

2. **Basic Masking Workflow**:
   - Enter or load SQL in the "Original SQL" section
   - Click "Mask SQL" (auto-analyzes if no mappings exist)
   - View anonymized result in "Masked SQL" section
   - Save mappings for future use

3. **AI-Enhanced Masking**:
   - Click "Enable AI Features"
   - Configure AI provider in "AI Config"
   - Toggle "AI Masking: ON" for semantic masking
   - Enjoy meaningful masked names instead of random strings

## 🎨 Interface Overview

### **Main Sections**
- **📝 SQL Editor**: Original and masked SQL with individual zoom controls
- **🗺️ Mappings**: View and manage entity mappings
- **❓ Help**: Complete documentation and shortcuts

### **Control Panel**
- **File Operations**: Load/Save files and mappings
- **Masking Operations**: Analyze, Edit, Mask, Unmask SQL
- **AI Features**: Enable/Configure AI, Understanding, Modifications

## 🔧 AI Configuration

### **Supported Providers**
1. **Local LLM (Recommended for Privacy)**:
   - Base URL: `http://localhost:11434/v1/chat/completions`
   - Model: `deepseek-coder-v2:latest`
   - API Key: Any value (or leave empty)

2. **OpenAI**:
   - Models: `gpt-3.5-turbo`, `gpt-4`, etc.
   - Requires valid API key

3. **Anthropic**:
   - Models: `claude-3-sonnet-20240229`, etc.
   - Requires valid API key

4. **Custom API**:
   - Configure your own endpoint and model

## 📊 Masking Comparison

### **Traditional Random Masking**
```sql
-- Before
SELECT customer_id, billing_date FROM customer_accounts;

-- After
SELECT col_001, fld_002 FROM table_003;
```

### **AI-Enhanced Semantic Masking**
```sql
-- Before  
SELECT customer_id, billing_date FROM customer_accounts;

-- After
SELECT client_ref, invoice_timestamp FROM account_data;
```

## ⌨️ Keyboard Shortcuts

### **Main Application**
- `Ctrl+O`: Load file
- `Ctrl+S`: Save mappings
- `F5`: Analyze SQL
- `F6`: Mask SQL
- `F7`: Unmask SQL

### **Zoom Controls**
- `Ctrl+Plus`: Zoom in
- `Ctrl+Minus`: Zoom out
- `Ctrl+0`: Reset zoom

### **AI Understanding Window**
- `Ctrl+Enter`: Submit question
- `Ctrl+Plus/Minus`: Zoom all sections
- `Ctrl+0`: Reset all zoom levels

## 🎯 Use Cases

### **Development & Testing**
- Anonymize SQL for external code reviews
- Create realistic test data scenarios
- Share queries without exposing sensitive schemas

### **Documentation & Training**
- Generate training materials with masked examples
- Create documentation with anonymized SQL
- Maintain readability while ensuring privacy

### **Compliance & Security**
- Meet data privacy requirements
- Secure sensitive database information
- Audit-friendly anonymization process

## 🔍 Advanced Features

### **Smart Domain Detection**
- **Telecom**: Recognizes network, call, mobile patterns
- **Finance**: Detects account, payment, transaction terms
- **Retail**: Identifies product, order, customer entities
- **HR**: Spots employee, department, payroll references

### **Conversation Interface**
- **Quick Questions**: Pre-built queries about SQL structure
- **Custom Questions**: Ask anything about your SQL code
- **Follow-up Support**: Continue conversations for deeper analysis

### **Enhanced Readability**
- **Expandable Sections**: Resize any part of the interface
- **Multiple Zoom Levels**: Perfect text size for any screen
- **Professional Layout**: Color-coded controls and clear organization

## 🛠️ Technical Details

### **Architecture**
- **Modular Design**: Separate components for masking, AI, and GUI
- **Extensible**: Easy to add new AI providers or masking strategies
- **Error Handling**: Graceful fallbacks and user-friendly error messages

### **Performance**
- **Local Processing**: Core masking works without internet
- **Optimized AI Calls**: Intelligent prompt management for large queries
- **Responsive UI**: Non-blocking operations with progress indicators

## 📝 File Structure

```
Anonimiser_GUI/
├── sql_mask_gui_modular.py      # Main application
├── sql_masker.py                # Core masking logic
├── ai_config.py                 # AI configuration
├── ai_interface.py              # AI interaction windows
├── syntax_highlighter.py       # SQL syntax highlighting
├── test_ai_masking.py          # Masking comparison demo
├── test_understanding_zoom.py   # Understanding window demo
└── *.md                        # Documentation files
```

## 🎉 What's New in v2.0

### **🧠 AI-Enhanced Masking**
- Semantic preservation instead of random strings
- Business domain awareness
- Consistent relationship mapping

### **🔍 Comprehensive Zoom**
- Global and individual section zoom controls
- Keyboard shortcuts for all zoom operations
- Perfect accessibility for any screen size

### **🎨 Improved Interface**
- 20% larger default window size
- Expandable and resizable sections
- Better button layouts and spacing
- Meaningful quick question buttons

### **⚡ Enhanced Workflow**
- Auto-analysis when masking (no manual "Analyze" step)
- Improved error handling and user feedback
- Professional tooltips and visual cues

---

**🎭 Transform your SQL masking workflow with intelligent AI assistance and professional-grade zoom functionality!**