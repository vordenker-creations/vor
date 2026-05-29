import os

with open('pages/profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"Portfolio View"', '"AI Academic Plan"')
content = content.replace('"My Profile / Portfolio"', '"AI Academic Plan"')
content = content.replace('"View Portfolio"', '"View Plan"')
content = content.replace('"Save your profile context and click Generate Plan to build your dynamic AI Portfolio timeline."', '"Save your profile context and click Generate Plan to build your dynamic AI Academic Plan."')
content = content.replace('"Your portfolio is ready. Update your profile info to recalculate insights."', '"Your plan is ready. Update your profile info to recalculate insights."')
content = content.replace('"Portfolio V2 Launch"', '"Academic Plan V2"')

with open('pages/profile.py', 'w', encoding='utf-8') as f:
    f.write(content)
