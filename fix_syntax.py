#!/usr/bin/env python3
"""
🔧 AspirePath - Syntax Error Fix Script
=====================================
This script fixes the indentation error in app.py at line 556
"""

import os
import shutil

def fix_syntax_error():
    print("🔧 Fixing AspirePath syntax error...")
    
    # Read the problematic file
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find and fix the problematic section
    fixed_lines = []
    skip_mode = False
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Start skipping at the problematic legacy navigation section
        if '# page = st.sidebar.radio(' in line:
            fixed_lines.append('# Legacy navigation commented out - replaced with option menu\n')
            skip_mode = True
            continue
            
        # End skipping when we reach the clean section
        if skip_mode and '# Clean up the page variable for logic consistency' in line:
            skip_mode = False
            fixed_lines.append('# Clean up the page variable for logic consistency\n')
            continue
            
        # Skip problematic lines
        if skip_mode:
            continue
            
        # Keep all other lines
        fixed_lines.append(line)
    
    # Write the fixed file
    with open('app_fixed.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("✅ Fixed file created as app_fixed.py")
    print("🔄 Replacing original app.py...")
    
    # Backup and replace
    shutil.copy('app.py', 'app_broken_backup.py')
    shutil.copy('app_fixed.py', 'app.py')
    
    print("✅ app.py has been fixed!")
    print("📁 Backup saved as app_broken_backup.py")

if __name__ == "__main__":
    fix_syntax_error()
