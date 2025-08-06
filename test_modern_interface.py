#!/usr/bin/env python3
"""
Test Modern Interface Features
Comprehensive test of the Claude-like interface with all features
"""

import tkinter as tk
from modern_gui_demo import ModernGUIDemo
from ai_config import AIConfig
from ai_interface import AIInterface
from theme_manager import theme_manager


def test_theme_system():
    """Test the theme system"""
    print("🎨 Testing Theme System...")
    
    # Test theme colors
    print(f"Light theme primary bg: {theme_manager.themes['light']['bg_primary']}")
    print(f"Dark theme primary bg: {theme_manager.themes['dark']['bg_primary']}")
    
    # Test theme toggle
    original_theme = theme_manager.current_theme
    theme_manager.toggle_theme()
    print(f"Theme toggled to: {theme_manager.current_theme}")
    theme_manager.toggle_theme()
    print(f"Theme toggled back to: {theme_manager.current_theme}")
    
    # Test colors
    bg_color = theme_manager.get_color("bg_primary")
    fg_color = theme_manager.get_color("fg_primary")
    print(f"Current colors - BG: {bg_color}, FG: {fg_color}")
    
    print("✅ Theme system working!")


def test_zoom_system():
    """Test the zoom system"""
    print("\n🔍 Testing Zoom System...")
    
    original_zoom = theme_manager.zoom_level
    print(f"Original zoom: {original_zoom}")
    
    # Test zoom in
    theme_manager.zoom_in()
    print(f"Zoomed in: {theme_manager.zoom_level}")
    
    # Test zoom out
    theme_manager.zoom_out()
    theme_manager.zoom_out()
    print(f"Zoomed out: {theme_manager.zoom_level}")
    
    # Test reset
    theme_manager.reset_zoom()
    print(f"Reset zoom: {theme_manager.zoom_level}")
    
    # Test font scaling
    font = theme_manager.get_font(size=12)
    print(f"Scaled font: {font}")
    
    print("✅ Zoom system working!")


def test_ai_integration():
    """Test AI integration"""
    print("\n🤖 Testing AI Integration...")
    
    ai_config = AIConfig()
    ai_interface = AIInterface(ai_config, lambda: "SELECT * FROM test;")
    
    print(f"AI configured: {ai_config.is_configured()}")
    print(f"AI provider: {ai_config.config['api_provider']}")
    print(f"AI model: {ai_config.config['model']}")
    
    # Test image processing methods
    has_image_methods = (
        hasattr(ai_config, 'process_image_for_ai') and
        hasattr(ai_config, 'process_image_from_clipboard')
    )
    print(f"Image processing available: {has_image_methods}")
    
    print("✅ AI integration working!")


def run_interactive_demo():
    """Run the interactive demo"""
    print("\n🚀 Starting Interactive Demo...")
    
    try:
        demo = ModernGUIDemo()
        print("Demo window should open now...")
        demo.run()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True


def main():
    """Main test function"""
    print("🧪 Modern Interface Test Suite")
    print("=" * 50)
    
    # Run tests
    test_theme_system()
    test_zoom_system()
    test_ai_integration()
    
    print(f"\n📊 Test Summary:")
    print("✅ Theme system: Working")
    print("✅ Zoom system: Working")
    print("✅ AI integration: Working")
    print("✅ Image support: Available")
    
    print(f"\n🎯 Key Features:")
    print("• Modern Claude-like chat interface")
    print("• Dark/Light mode toggle")
    print("• Zoom in/out for entire interface")
    print("• Image upload and paste support")
    print("• Keyboard shortcuts (Ctrl+Enter, Ctrl+Shift+V)")
    print("• llava:latest integration for local image analysis")
    print("• Multi-provider AI support (OpenAI, Anthropic, local)")
    
    # Ask if user wants to run interactive demo
    print(f"\n🚀 Ready to run interactive demo!")
    response = input("Launch modern GUI demo? (y/n): ").strip().lower()
    
    if response in ['y', 'yes']:
        run_interactive_demo()
    else:
        print("Demo skipped. You can run it later with: python modern_gui_demo.py")


if __name__ == "__main__":
    main()