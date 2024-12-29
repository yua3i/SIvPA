@echo off
chcp 65001
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python yüklü degil. Lutfen Python otomatik olarak yuklenecek...
    echo Python yukleniyor...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Python yuklemesi basarisiz oldu.
        pause
        exit /b
    )
    echo Python yüklendi!
) else (
    echo Python zaten yüklü.
)
for /f "delims=" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Mevcut Python surumu: %PYTHON_VERSION%
echo Kütüphaneler yukleniyor...
pip install psutil >nul 2>&1 && echo psutil yuklendi. || echo psutil yuklenemedi.
pip install Pillow >nul 2>&1 && echo Pillow yuklendi. || echo Pillow yuklenemedi.
pip install colorama >nul 2>&1 && echo colorama yuklendi. || echo colorama yuklenemedi.
pip install pynvml >nul 2>&1 && echo pynvml yuklendi. || echo pynvml yuklenemedi.
pip install matplotlib >nul 2>&1 && echo matplotlib yuklendi. || echo matplotlib yuklenemedi.
pip install requests >nul 2>&1 && echo requests yuklendi. || echo requests yuklenemedi.
pip install textblob >nul 2>&1 && echo textblob yuklendi. || echo textblob yuklenemedi.
pip install SpeechRecognition >nul 2>&1 && echo SpeechRecognition yuklendi. || echo SpeechRecognition yuklenemedi.
pip install numpy >nul 2>&1 && echo numpy yuklendi. || echo numpy yuklenemedi.
pip install sounddevice >nul 2>&1 && echo sounddevice yuklendi. || echo sounddevice yuklenemedi.
echo Kütüphaneler başarıyla yüklendi veya hata mesajlarını kontrol edin.
pause
