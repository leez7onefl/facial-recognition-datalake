@echo off
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%\datalakes-final-project-venv"
set "REQUIREMENTS_FILE=%PROJECT_DIR%\requirements.txt"
IF NOT EXIST "%VENV_DIR%" (
echo Creating virtual environment...
python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate"
pip install --upgrade pip
pip install -r "%REQUIREMENTS_FILE%"
call deactivate
) ELSE (
echo Virtual environment already exists.
)
echo Script execution finished. Press any key to exit.
pause