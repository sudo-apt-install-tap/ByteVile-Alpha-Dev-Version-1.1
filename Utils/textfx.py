import os
import platform

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def banner():
    print(r"""
  ____        _        __     _ _      
 | __ ) _   _| |_ ___  \ \   (_) | ___ 
 |  _ \| | | | __/ _ \  \ \  | | |/ _ \
 | |_) | |_| | ||  __/  / /__| | |  __/
 |____/ \__,_|\__\___| /_____|_|_|\___|
    ByteVile Alpha Dev Version 1.1
    """)

