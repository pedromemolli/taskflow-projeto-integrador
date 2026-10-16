@echo off
setlocal
cd /d "%~dp0"

IF NOT EXIST ".venv" (
    echo Criando ambiente virtual pela primeira vez...
    py -m venv .venv
    IF ERRORLEVEL 1 goto :erro
)

call .venv\Scripts\activate.bat
IF ERRORLEVEL 1 goto :erro

echo Instalando/atualizando dependencias...
python -m pip install -r requirements.txt
IF ERRORLEVEL 1 goto :erro

echo.
echo Iniciando o TaskFlow...
echo Acesse http://127.0.0.1:5000 no navegador.
echo Para parar o servidor, pressione Ctrl+C.
echo.

start "" http://127.0.0.1:5000
python app.py
goto :fim

:erro
echo.
echo Ocorreu um erro ao preparar ou iniciar o TaskFlow.
echo Verifique se o Python 3 esta instalado e disponivel pelo comando "py".
pause

:fim
endlocal
