@echo off
call datalakes-final-project-venv\Scripts\activate.bat
start cmd /k "cd api && python app.py"
cd scripts
streamlit run streamlit_main.py
call deactivate