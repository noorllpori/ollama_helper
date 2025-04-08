pyinstaller --onefile --windowed --name="olala" --icon="./nikuniku.ico" main.py
del .\olala.exe
copy .\dist\olala.exe .\olala.exe