:: SETUP THE VIRTUAL ENVIRONEMENTS
python -m venv .venv
:: ACTIVATE THE VENV 
call .\.venv\Scripts\activate
:: INSTALL REQUIREMENTS
@REM pip install wheel
@REM pip install -r .\requirements.txt
@REM @echo off
:: Install the Hello Package
python setup.py install
