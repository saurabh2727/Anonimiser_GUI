#!/usr/bin/env python3
"""
Debug Image Processing Issue
Identifies why images aren't being processed by the AI
"""

from ai_config import AIConfig
import os


def debug_ai_config():
    """Debug the AI configuration"""
    print("🔍 Debugging AI Configuration...")
    
    ai_config = AIConfig()
    config = ai_config.config
    
    print(f"API Provider: {config['api_provider']}")
    print(f"Model: {config['model']}")
    print(f"Base URL: {config['base_url']}")
    print(f"API Key: {'***' if config['api_key'] != 'local' else 'local'}")
    
    # Check image support
    model_name = config['model'].lower()
    supports_images = False
    
    if config['api_provider'] == 'local_llm':
        if 'llava' in model_name:
            supports_images = True
            print("✅ Model supports images (llava detected)")
        else:
            print("❌ Model does NOT support images (no llava in model name)")
            print(f"   Current model: {config['model']}")
            print(f"   For image support, use: llava:latest")
    elif config['api_provider'] == 'openai':
        if 'gpt-4' in model_name or 'vision' in model_name:
            supports_images = True
            print("✅ Model supports images (GPT-4/vision detected)")
        else:
            print("❌ Model does NOT support images")
            print(f"   Current model: {config['model']}")
            print(f"   For image support, use: gpt-4 or gpt-4-vision-preview")
    elif config['api_provider'] == 'anthropic':
        supports_images = True
        print("✅ Model supports images (Claude supports images)")
    else:
        print("❓ Unknown provider - image support uncertain")
    
    return supports_images


def test_image_processing():
    """Test image processing functions"""
    print("\n🖼️ Testing Image Processing...")
    
    ai_config = AIConfig()
    
    # Test if PIL is available
    try:
        from PIL import Image
        print("✅ PIL (Pillow) is available")
    except ImportError:
        print("❌ PIL (Pillow) is NOT available - install with: pip install Pillow")
        return False
    
    # Test image processing methods
    has_methods = (
        hasattr(ai_config, 'process_image_for_ai') and
        hasattr(ai_config, 'process_image_from_clipboard')
    )
    
    if has_methods:
        print("✅ Image processing methods are available")
    else:
        print("❌ Image processing methods are missing")
        return False
    
    return True


def check_ollama_models():
    """Check available Ollama models"""
    print("\n🤖 Checking Available Ollama Models...")
    
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("Available Ollama models:")
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'llava' in line.lower():
                    print(f"✅ {line.strip()} (supports images)")
                else:
                    print(f"   {line.strip()}")
        else:
            print("❌ Could not list Ollama models - make sure Ollama is running")
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        print("Make sure Ollama is installed and running")


def provide_solutions(supports_images):
    """Provide solutions based on findings"""
    print("\n🛠️ Solutions:")
    
    if not supports_images:
        print("❌ MAIN ISSUE: Your current AI model doesn't support images!")
        print("\n📋 To fix this, choose one of these options:")
        
        print("\n1️⃣ OPTION 1: Use Local llava Model (Recommended)")
        print("   • Run: ollama pull llava:latest")
        print("   • In the app, go to AI Configuration")
        print("   • Set Model to: llava:latest")
        print("   • Set Provider to: local_llm")
        
        print("\n2️⃣ OPTION 2: Use OpenAI GPT-4")
        print("   • In the app, go to AI Configuration")
        print("   • Set Provider to: openai")
        print("   • Set Model to: gpt-4")
        print("   • Add your OpenAI API key")
        
        print("\n3️⃣ OPTION 3: Use Anthropic Claude")
        print("   • In the app, go to AI Configuration")
        print("   • Set Provider to: anthropic")
        print("   • Set Model to: claude-3-sonnet-20240229")
        print("   • Add your Anthropic API key")
    else:
        print("✅ Your model should support images!")
        print("🔍 Let's check if there's another issue...")
        
        print("\n📋 Additional checks:")
        print("1. Make sure the AI service is running")
        print("2. Try a simple text message first")
        print("3. Check if the image file is valid")
        print("4. Try with a different image format")


def main():
    """Main debug function"""
    print("🐛 AI Image Processing Debug Tool")
    print("=" * 50)
    
    # Run all checks
    supports_images = debug_ai_config()
    image_processing_ok = test_image_processing()
    check_ollama_models()
    
    # Provide solutions
    provide_solutions(supports_images)
    
    print("\n" + "=" * 50)
    print("🎯 Quick Fix Summary:")
    if not supports_images:
        print("   Run: ollama pull llava:latest")
        print("   Then change your AI model to: llava:latest")
    else:
        print("   Your configuration looks good - try restarting the app")


if __name__ == "__main__":
    main()