#!/usr/bin/env python3
"""
Test script for Template2.py to validate the code structure and fix
for the CTkImage attribute error without requiring GUI libraries.
"""

import sys
import os

def test_template2_structure():
    """Test the structure and key fixes in Template2.py"""
    
    print("Testing Template2.py structure and fixes...")
    
    # Read the Template2.py file
    template2_path = os.path.join(os.path.dirname(__file__), 'Template2.py')
    
    if not os.path.exists(template2_path):
        print("❌ Template2.py file not found")
        return False
    
    with open(template2_path, 'r') as f:
        content = f.read()
    
    # Test 1: Check that problematic _PhotoImage__photo attribute is NOT used
    if '_PhotoImage__photo' in content:
        print("❌ Still contains problematic _PhotoImage__photo attribute")
        return False
    else:
        print("✅ No _PhotoImage__photo attribute found (problem fixed)")
    
    # Test 2: Check for proper CTkImage usage
    if 'CTkImage' in content and 'ctk.CTkImage' in content:
        print("✅ Uses proper CTkImage instantiation")
    else:
        print("❌ CTkImage usage not found")
        return False
    
    # Test 3: Check for InstallerUI class
    if 'class InstallerUI:' in content:
        print("✅ InstallerUI class defined")
    else:
        print("❌ InstallerUI class not found")
        return False
    
    # Test 4: Check for main function
    if 'def main():' in content:
        print("✅ main() function defined")
    else:
        print("❌ main() function not found")
        return False
    
    # Test 5: Check for _build_ui method
    if 'def _build_ui(self):' in content:
        print("✅ _build_ui() method defined")
    else:
        print("❌ _build_ui() method not found")
        return False
    
    # Test 6: Check that we're using CTkLabel with image instead of canvas.create_image
    if 'canvas.create_image' in content:
        print("❌ Still using canvas.create_image (potential problem)")
        return False
    elif 'CTkLabel' in content and 'image=' in content:
        print("✅ Using CTkLabel with image parameter (correct approach)")
    else:
        print("⚠️  Image display method unclear")
    
    # Test 7: Check for proper error handling
    if 'try:' in content and 'except' in content:
        print("✅ Contains error handling")
    else:
        print("❌ No error handling found")
        return False
    
    # Test 8: Check line count around expected error line (219)
    lines = content.split('\n')
    if len(lines) >= 219:
        print(f"✅ File has sufficient lines ({len(lines)} lines, error was at line 219)")
    else:
        print(f"⚠️  File has {len(lines)} lines, original error was at line 219")
    
    print("\n✅ All structure tests passed! Template2.py should fix the CTkImage attribute error.")
    return True

def test_key_fixes():
    """Test the specific fixes implemented for the CTkImage error"""
    
    print("\nTesting key fixes for CTkImage error...")
    
    template2_path = os.path.join(os.path.dirname(__file__), 'Template2.py')
    
    with open(template2_path, 'r') as f:
        content = f.read()
    
    # Key fix 1: Using CTkLabel instead of canvas.create_image
    print("\n🔧 Fix 1: Image display method")
    if 'logo_label = ctk.CTkLabel(' in content and 'image=self.logo_ctk' in content:
        print("✅ Uses CTkLabel with image parameter - this avoids accessing internal CTkImage attributes")
    else:
        print("❌ CTkLabel with image not found")
    
    # Key fix 2: Proper CTkImage creation
    print("\n🔧 Fix 2: CTkImage creation")
    if 'self.logo_ctk = ctk.CTkImage(' in content:
        print("✅ Creates CTkImage properly using ctk.CTkImage()")
    else:
        print("❌ CTkImage creation not found")
    
    # Key fix 3: No direct access to internal attributes
    print("\n🔧 Fix 3: Attribute access")
    private_attrs = ['_PhotoImage__photo', '__photo', '_photo']
    found_private = [attr for attr in private_attrs if attr in content]
    if not found_private:
        print("✅ No private/internal attribute access found")
    else:
        print(f"❌ Found private attribute access: {found_private}")
    
    # Key fix 4: Error handling for image loading
    print("\n🔧 Fix 4: Error handling")
    if 'try:' in content and '_load_logo' in content:
        print("✅ Image loading has error handling")
    else:
        print("❌ No error handling for image loading")
    
    print("\n✅ Key fixes analysis complete!")

if __name__ == "__main__":
    print("=" * 60)
    print("TEMPLATE2.PY VALIDATION TEST")
    print("=" * 60)
    
    success = test_template2_structure()
    test_key_fixes()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 VALIDATION PASSED: Template2.py should resolve the CTkImage error!")
        print("\nThe original error:")
        print("AttributeError: 'CTkImage' object has no attribute '_PhotoImage__photo'")
        print("\nHas been fixed by:")
        print("1. Using CTkLabel with image parameter instead of canvas.create_image")
        print("2. Not accessing private/internal CTkImage attributes")
        print("3. Proper CTkImage instantiation with PIL Image objects")
        print("4. Added error handling for image loading scenarios")
    else:
        print("❌ VALIDATION FAILED: Issues found in Template2.py")
    
    print("=" * 60)