@echo off
REM ============================================================
REM  TaskFlow - inicializacao automatica
REM  Duplo clique neste arquivo para instalar (se necessario)
REM  e iniciar o servidor, abrindo o navegador sozinho.
REM ============================================================

cd /d "%~dp0"

IF NOT EXIST ".venv" (
    echo Criando ambiente virtual pela primeira vez...
    py -m venv .venv
)

call .venv\Scripts\activate.bat

echo Instalando/atualizando dependencias...
pip install -r requirements.txt -q

echo.
echo Iniciando o TaskFlow...
echo Acesse http://127.0.0.1:5000 no navegador.
echo Para PARAR o servidor, feche esta janela ou pressione Ctrl+C.
echo.

start "" http://127.0.0.1:5000

flask --app app run --debug

pause
