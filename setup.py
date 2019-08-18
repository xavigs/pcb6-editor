from distutils.core import setup
import py2exe

setup(console = ['main.py'],
    windows = [{
            "script":"main.py",
            "icon_resources": [(1, "editor.ico")]
            }],
)
