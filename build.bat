@echo off
c:/python34/python.exe build_server.py py2exe
echo.
c:/python34/python.exe build_client.py py2exe
echo.
echo Copying PDCurses...
copy pdcurses.dll dist
echo Copying server start...
copy linux0.bat dist
echo Removing redundant files...
cd dist
del -v _bz2.pyd _hashlib.pyd _ssl.pyd
echo Done.
cd ..