import os
import re

directory = 'd:/hau/vku/doancs1/GUI/vor/pages'

shadow_pattern = re.compile(r'(\w+)\s*=\s*QGraphicsDropShadowEffect.*?(\1\.setBlurRadius\(\d+\).*?)?\1\.setColor\(QColor\([^)]+\)\)', re.DOTALL)

def replace_shadows(match):
    var_name = match.group(1)
    return f"""{var_name}.setBlurRadius(30)
        {var_name}.setXOffset(0)
        {var_name}.setYOffset(8)
        {var_name}.setColor(QColor(18, 55, 105, 20))"""

for filename in os.listdir(directory):
    if filename.endswith('.py'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update shadow settings:
        # Instead of complex regex, let's just do line by line replacements for standard patterns.
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if '.setBlurRadius(' in line:
                line = re.sub(r'\.setBlurRadius\(\d+\)', '.setBlurRadius(30)', line)
            if '.setYOffset(' in line:
                line = re.sub(r'\.setYOffset\(\d+\)', '.setYOffset(8)', line)
            if '.setColor(QColor(' in line:
                line = re.sub(r'\.setColor\(QColor\([^)]+\)\)', '.setColor(QColor(18, 55, 105, 20))', line)
            if 'border-radius: 20px;' in line:
                line = line.replace('border-radius: 20px;', 'border-radius: 22px;')
            new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
