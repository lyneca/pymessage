from distutils.core import setup
import py2exe

setup(
    console=[
        {
            "script": "server.py",
            "icon_resources": [(1, "cmd.ico")]
        }
    ],
)
