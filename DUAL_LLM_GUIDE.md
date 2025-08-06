# 🚀 Dual LLM System - Smart AI Routing

## Overview
The Dual LLM system automatically routes your queries to the most appropriate AI model:
- **📝 Text/Code Questions** → `deepseek-coder-v2:latest` (specialized for coding)
- **🖼️ Image Questions** → `llava:latest` (specialized for vision)

## ✨ Key Benefits

### 🎯 **Smart Routing**
- **Automatic Detection**: System detects if you've uploaded an image
- **Model Selection**: Chooses the best model for your specific query
- **Seamless Experience**: Works transparently in the background

### 🔧 **Optimized Performance**
- **deepseek-coder-v2**: Excellent at SQL, code analysis, and technical questions
- **llava**: Superior image understanding and visual analysis
- **Best Results**: Each model handles what it does best

### 💰 **Cost Efficient**
- **Local Models**: Both models run locally via Ollama
- **No API Costs**: No charges for OpenAI or Anthropic APIs
- **Fast Responses**: Local processing for quick results

## 🛠️ Setup Instructions

### **Step 1: Install Required Models**
```bash
# Install both models via Ollama
ollama pull deepseek-coder-v2:latest
ollama pull llava:latest
```

### **Step 2: Enable Dual LLM Mode**
1. Run your application: `python run_sql_masker.py`
2. Click **"🤖 Enable AI Features"**
3. Click **"⚙️ AI Config"**
4. Set **API Provider**: `local_llm`
5. ✅ **Check "Enable Dual LLM (Text + Vision)"**
6. Set **Text/Code Model**: `deepseek-coder-v2:latest`
7. Set **Vision Model**: `llava:latest`
8. Set **Base URL**: `http://localhost:11434/v1/chat/completions`
9. Click **"Save"**

## 🎮 How It Works

### **Smart Detection Logic**
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

### **Example Scenarios**

#### 📝 **Text Query** (Uses deepseek-coder-v2)
```
User: "Explain this SQL query and optimize it"
Console: 📝 Using text model: deepseek-coder-v2:latest
Response: [Detailed SQL analysis and optimization suggestions]
```

#### 🖼️ **Image Query** (Uses llava)
```
User: Uploads database diagram + "What's in this database diagram?"
Console: 🖼️ Using vision model: llava:latest  
Response: [Detailed analysis of the database schema image]
```

#### 🤝 **Combined Query** (Uses llava for image context)
```
User: Uploads ERD + "Generate SQL for this database design"
Console: 🖼️ Using vision model: llava:latest
Response: [Analyzes image and generates appropriate SQL]
```

## 📋 Configuration Options

### **Dual LLM Settings**
```python
config = {
    'dual_llm_enabled': True,           # Enable/disable dual mode
    'text_model': 'deepseek-coder-v2:latest',  # For code/text
    'vision_model': 'llava:latest',     # For images
    'smart_routing': True,              # Auto-select model
    'api_provider': 'local_llm'         # Use local Ollama
}
```

### **Alternative Models**
You can use different models based on your needs:

#### **For Text/Code:**
- `deepseek-coder-v2:latest` ⭐ (Recommended)
- `codellama:latest`
- `mistral:latest`
- `llama2:latest`

#### **For Vision:**
- `llava:latest` ⭐ (Recommended)
- `llava:13b`
- `llava:7b` (Faster, less accurate)

## 🎯 Visual Indicators

### **In Chat Interface**
- **AI Assistant (Smart Routing)** - Shows dual LLM is active
- **Console Messages**: 
  - `📝 Using text model: deepseek-coder-v2:latest`
  - `🖼️ Using vision model: llava:latest`

### **Configuration Dialog**
- ✅ **"Enable Dual LLM (Text + Vision)"** checkbox
- **Separate fields** for text and vision models
- **Help text** explaining the benefits

## 🔧 Troubleshooting

### **Common Issues**

#### **❌ "Model not found" Error**
```bash
# Solution: Install missing models
ollama pull deepseek-coder-v2:latest
ollama pull llava:latest
```

#### **❌ Images Not Working**
1. Check if vision model is running: `ollama list`
2. Verify llava is installed
3. Ensure Pillow is installed: `pip install Pillow`

#### **❌ Dual LLM Not Active**
1. Open AI Configuration
2. Ensure "Enable Dual LLM" is checked
3. Verify both models are set correctly
4. Restart the application

### **Verification Commands**
```bash
# Check Ollama models
ollama list

# Test individual models
ollama run deepseek-coder-v2:latest "Hello"
ollama run llava:latest "Describe this image"

# Check app configuration
python -c "from ai_config import AIConfig; print(AIConfig().config)"
```

## 🚀 Advanced Usage

### **Custom Model Combinations**
You can mix and match models for specific use cases:

#### **For Coding Focus**
- Text: `deepseek-coder-v2:latest`
- Vision: `llava:latest`

#### **For General Use**
- Text: `mistral:latest`  
- Vision: `llava:latest`

#### **For Performance**
- Text: `llama2:7b`
- Vision: `llava:7b`

### **API Integration**
The dual LLM system also works with cloud providers:

#### **OpenAI + Local**
- Text: `gpt-3.5-turbo` (OpenAI)
- Vision: `llava:latest` (Local)

#### **Mixed Cloud/Local**
- Text: `claude-3-sonnet` (Anthropic) 
- Vision: `llava:latest` (Local)

## 📊 Performance Comparison

| Scenario | Single Model | Dual LLM | Improvement |
|----------|-------------|-----------|-------------|
| **Code Questions** | llava (slow) | deepseek-coder ⚡ | 3x faster |
| **Image Questions** | deepseek (no vision) | llava 👁️ | Vision capability |
| **Mixed Queries** | One size fits all | Best tool for job | Optimal results |

## 🎉 Real-World Examples

### **Database Design Workflow**
1. **Upload ERD image** → llava analyzes the database structure
2. **Ask for SQL generation** → llava creates tables based on visual analysis
3. **Request optimizations** → deepseek optimizes the generated SQL
4. **Ask for documentation** → deepseek writes comprehensive docs

### **Code Review Process**  
1. **Text questions** → deepseek provides detailed code analysis
2. **Screenshot of errors** → llava identifies UI issues
3. **Performance questions** → deepseek suggests optimizations
4. **Visual debugging** → llava helps with layout problems

---

## 🎯 Quick Start Summary

1. **Install models**: `ollama pull deepseek-coder-v2:latest && ollama pull llava:latest`
2. **Run app**: `python run_sql_masker.py`
3. **Enable dual LLM**: AI Config → Check "Enable Dual LLM"
4. **Use it**: Text questions get deepseek, images get llava automatically!

**You now have the best of both worlds - specialized AI models working together seamlessly!** 🚀✨