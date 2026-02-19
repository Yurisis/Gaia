@echo off
cd /d "d:\Develop\Gaia"

:: Ensure log directory exists
if not exist "logs" mkdir logs

echo [START] Gaia Auto Generation at %date% %time% >> logs\scheduler.log

:: SQL-like comment: Run main.py in bulk mode with safe count
python main.py --type bulk --count 50 >> logs\scheduler.log 2>&1

echo [END] Finished at %date% %time% >> logs\scheduler.log
echo --------------------------------------------------- >> logs\scheduler.log
