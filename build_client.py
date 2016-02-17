from distutils.core import setup
import py2exe

setup(
    console=[
        {
            "script": "client.py",
            "icon_resources": [(1, "cmd.ico")]
        }
    ],
    requires=['unicurses'],
    data_files=[('.', 'pdcurses.dll')]
)
