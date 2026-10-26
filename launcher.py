import os
import subprocess

os.chdir(r"E:\AI-Server\runtime")

subprocess.Popen(
    ["python", "AI-LAB-Runtime.py"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)