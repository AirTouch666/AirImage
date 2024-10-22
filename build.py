import PyInstaller.__main__
import os

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'run.py',
    '--name=AirImage',
    '--onefile',
    '--add-data=templates:templates',
    '--hidden-import=PIL._tkinter_finder'
])
