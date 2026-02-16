$Action = New-ScheduledTaskAction -Execute "C:\Users\Yurisis\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe" -Argument "`"d:\Develop\Gaia\main.py`"" -WorkingDirectory "d:\Develop\Gaia"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 3650)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -TaskName "GaiaContentGenerator" -Description "Automatically generates and posts blog content via Gaia." -Force
Write-Host "Task 'GaiaContentGenerator' has been registered successfully. It will run daily at 09:00 AM."
