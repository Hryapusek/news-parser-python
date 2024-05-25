python.exe -m venv env
./env/Scripts/Activate.ps1
pip install -r .\requirements.txt
python -m pytest -p src .\src\gui\test\test_main_window.py