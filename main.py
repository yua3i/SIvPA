import psutil
import platform
from datetime import datetime
import os
import sys
from colorama import Fore, init
import socket
import pynvml
import subprocess
import matplotlib.pyplot as plt
import time
from PIL import ImageGrab
import requests
from textblob import TextBlob
import speech_recognition as sr
import numpy as np
import sounddevice as sd
import os
import sys
import ctypes

init(autoreset=True)

def change_console_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\033]0;{title}\007")

change_console_title("SİSTEM İZLEME VE PERFORMANS ARACI - made by simsek66")

def get_system_info():
    system_info = platform.uname()
    return (
        f"Sistem: {system_info.system}\n"
        f"Node Name: {system_info.node}\n"
        f"Sürüm: {system_info.release}\n"
        f"Sürüm Detayları: {system_info.version}\n"
        f"Mimari: {system_info.machine}\n"
        f"İşlemci: {system_info.processor}"
    )

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"CPU Kullanımı: %{cpu_usage}"

def get_cpu_usage_live():
    print(Fore.CYAN + "Gerçek Zamanlı CPU Kullanımı (Çıkmak için 'Ctrl+C' tuşlayın):")
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            print(Fore.YELLOW + f"Anlık CPU Kullanımı: %{cpu_usage}\n", end="\r")
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Gerçek zamanlı izleme durduruldu.")

def get_memory_info():
    memory = psutil.virtual_memory()
    return (
        f"Toplam RAM: {memory.total // (1024**3)} GB\n"
        f"Kullanılan RAM: {memory.used // (1024**3)} GB\n"
        f"Boş RAM: {memory.available // (1024**3)} GB\n"
        f"RAM Kullanımı: %{memory.percent}"
    )

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return (
        f"Disk Toplam: {disk.total // (1024**3)} GB\n"
        f"Disk Kullanılan: {disk.used // (1024**3)} GB\n"
        f"Disk Boş: {disk.free // (1024**3)} GB\n"
        f"Disk Kullanımı: %{disk.percent}"
    )

def get_network_info():
    net = psutil.net_io_counters()
    return (
        f"Gönderilen Veri: {net.bytes_sent // (1024**2)} MB\n"
        f"Alınan Veri: {net.bytes_recv // (1024**2)} MB"
    )

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_system_info():
    with open("log.txt", "a") as log_file:
        log_file.write(f"=== Sistem İzleme Logu - {datetime.now()} ===\n")
        log_file.write(get_system_info() + "\n")
        log_file.write(get_cpu_usage() + "\n")
        log_file.write(get_memory_info() + "\n")
        log_file.write(get_disk_usage() + "\n")
        log_file.write(get_network_info() + "\n")
        log_file.write(get_uptime() + "\n")
        log_file.write(get_battery_status() + "\n")
        log_file.write(get_temperatures() + "\n")
        log_file.write(get_gpu_info() + "\n")
        log_file.write(get_process_count() + "\n")
        log_file.write(get_top_processes() + "\n")
        log_file.write(get_current_time() + "\n")
        log_file.write(get_network_status() + "\n")
        log_file.write(get_gpu_usage() + "\n")
        log_file.write(get_ping_status() + "\n")
        log_file.write(get_update_status() + "\n")
        log_file.write(get_storage_devices() + "\n")
        log_file.write(check_file_system_health() + "\n")
        log_file.write(get_wifi_info() + "\n")
        log_file.write(list_power_plans() + "\n")
        log_file.write(get_temperature_info() + "\n")
        log_file.write(list_bluetooth_devices() + "\n")
        log_file.write(get_saved_wifi_passwords() + "\n")
    print(Fore.GREEN + "Log dosyasına yazıldı: log.txt")

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time
    return f"Sistem Açık Kalma Süresi: {uptime}"

def get_battery_status():
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return (
                f"Batarya Seviyesi: %{battery.percent}\n"
                f"Şarj Durumu: {'Takılı' if battery.power_plugged else 'Takılı Değil'}\n"
                f"Kalan Süre: {battery.secsleft // 60} dakika"
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Bilinmiyor"
            )
        else:
            return "Batarya Bilgisi Bulunamadı (Bu cihaz masaüstü olabilir)."
    else:
        return "Batarya desteği yok."

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def show_processes():
    processes = list_processes()
    print(Fore.CYAN + "PID\tİsim\t\tCPU Kullanımı\tRAM Kullanımı")
    for proc in processes[:10]:
        print(Fore.YELLOW + f"{proc['pid']}\t{proc['name'][:15]}\t{proc['cpu_percent']}%\t{proc['memory_percent']}%")

def get_temperatures():
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps:
            output = []
            for name, entries in temps.items():
                for entry in entries:
                    output.append(f"{entry.label or name}: {entry.current}°C")
            return "\n".join(output)
        else:
            return "Sıcaklık bilgisi alınamıyor."
    else:
        return "Bu özellik sisteminiz tarafından desteklenmiyor."

def get_gpu_info():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "GPU bilgisi alınamıyor. Bu sistemde GPU olmayabilir."
        output = []
        for gpu in gpus:
            output.append(
                f"GPU Adı: {gpu.name}\n"
                f"GPU Bellek Kullanımı: {gpu.memoryUsed}/{gpu.memoryTotal} MB\n"
                f"GPU Sıcaklığı: {gpu.temperature}°C\n"
            )
        return "\n".join(output)
    except ImportError:
        return "GPU bilgisi için 'GPUtil' modülünü yükleyin (pip install gputil)."

def get_process_count():
    return f"Sistemde Çalışan Toplam İşlem Sayısı: {len(psutil.pids())}"

def get_top_processes():
    processes = list_processes()
    sorted_by_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    sorted_by_memory = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]

    cpu_output = "En Çok CPU Kullanan İşlemler:\n"
    for proc in sorted_by_cpu:
        cpu_output += f"{proc['name']} (PID: {proc['pid']}) - %{proc['cpu_percent']} CPU\n"

    memory_output = "En Çok RAM Kullanan İşlemler:\n"
    for proc in sorted_by_memory:
        memory_output += f"{proc['name']} (PID: {proc['pid']}) - %{proc['memory_percent']} RAM\n"

    return cpu_output + "\n" + memory_output

def get_current_time():
    now = datetime.now()
    return f"Güncel Tarih ve Saat: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def get_network_status():
    addresses = psutil.net_if_addrs()
    status = []
    for iface, addr in addresses.items():
        for a in addr:
            if a.family == socket.AF_INET:
                status.append(f"Arayüz: {iface} - IP: {a.address}")
    return "\n".join(status) if status else "Ağ durumu bilgisi alınamadı."

def get_gpu_usage():
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return (f"GPU Bellek Kullanımı: {memory_info.used // (1024**2)} MB / {memory_info.total // (1024**2)} MB\n"
                f"GPU Kullanımı: {gpu_usage.gpu}%")
    except Exception as e:
        return f"GPU bilgisi alınamadı: {str(e)}"

def get_ping_status():
    try:
        response = subprocess.check_output("ping -n 1 google.com", shell=True)
        return "Ağ bağlantısı başarılı!"
    except subprocess.CalledProcessError:
        return "Ağ bağlantısı başarısız."

def plot_system_usage():
    times = []
    cpu_usages = []
    memory_usages = []
    
    for i in range(60):
        times.append(i)
        cpu_usages.append(psutil.cpu_percent(interval=1))
        memory_usages.append(psutil.virtual_memory().percent)

    plt.plot(times, cpu_usages, label="CPU Kullanımı")
    plt.plot(times, memory_usages, label="RAM Kullanımı")
    plt.xlabel('Zaman (saniye)')
    plt.ylabel('Kullanım (%)')
    plt.legend()
    plt.title('Sistem Performansı')
    plt.show()

def get_update_status():
    try:
        result = subprocess.check_output("wmic qfe list", shell=True, text=True)
        updates = result.strip().split("\n")[1:]
        return f"Yüklü Güncellemeler:\n{''.join(updates[:5])}\n(Not: Sadece ilk 5 güncelleme gösteriliyor.)"
    except Exception as e:
        return f"Güncelleme bilgisi alınamadı: {str(e)}"

def get_storage_devices():
    try:
        partitions = psutil.disk_partitions()
        output = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            output.append(
                f"{partition.device} - {partition.mountpoint}\n"
                f"Toplam: {usage.total // (1024**3)} GB, Kullanılan: {usage.used // (1024**3)} GB, Boş: {usage.free // (1024**3)} GB\n"
            )
        return "\n".join(output)
    except Exception as e:
        return f"Depolama aygıtı bilgisi alınamadı: {str(e)}"

def monitor_application_performance(process_name):
    print(Fore.CYAN + f"{process_name} uygulaması için gerçek zamanlı izleme başlatılıyor... (Çıkmak için Ctrl+C tuşlayın)")
    try:
        while True:
            found = False
            for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                    print(Fore.YELLOW + f"CPU: %{proc.info['cpu_percent']}, RAM: %{proc.info['memory_percent']}\n", end="\r")
                    found = True
            if not found:
                print(Fore.RED + f"{process_name} bulunamadı.", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "İzleme durduruldu.")

def critical_alerts():
    print(Fore.CYAN + "Kritik durumlar izleniyor. Çıkmak için 'Ctrl+C' tuşlayın.")
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            if cpu_usage > 90:
                print(Fore.RED + f"Kritik Uyarı: CPU kullanımı %{cpu_usage}!")
            if memory_usage > 90:
                print(Fore.RED + f"Kritik Uyarı: RAM kullanımı %{memory_usage}!")
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Kritik durum izleme durduruldu.")

def check_file_system_health():
    try:
        result = subprocess.check_output("chkdsk", shell=True, text=True)
        return f"Dosya Sistemi Sağlık Durumu:\n{result}"
    except Exception as e:
        return f"Dosya sistemi sağlık bilgisi alınamadı: {str(e)}"

def get_wifi_info():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
        return f"Wi-Fi Bilgileri:\n{result}"
    except Exception as e:
        return f"Wi-Fi bilgisi alınamadı: {str(e)}"

def monitor_network_traffic():
    print(Fore.CYAN + "Ağ Trafiği İzleme Başlatıldı (Çıkmak için Ctrl+C)")
    try:
        old_sent = psutil.net_io_counters().bytes_sent
        old_recv = psutil.net_io_counters().bytes_recv
        while True:
            time.sleep(1)
            new_sent = psutil.net_io_counters().bytes_sent
            new_recv = psutil.net_io_counters().bytes_recv
            sent = (new_sent - old_sent) / 1024
            recv = (new_recv - old_recv) / 1024
            print(Fore.YELLOW + f"Gönderilen: {sent:.2f} KB/sn | Alınan: {recv:.2f} KB/sn", end="\r")
            old_sent, old_recv = new_sent, new_recv
    except KeyboardInterrupt:
        print(Fore.RED + "\nAğ Trafiği İzleme Durduruldu.")

def monitor_disk_performance():
    print(Fore.CYAN + "Disk Performansı İzleme Başlatıldı (Çıkmak için Ctrl+C)")
    try:
        old_read = psutil.disk_io_counters().read_bytes
        old_write = psutil.disk_io_counters().write_bytes
        while True:
            time.sleep(1)
            new_read = psutil.disk_io_counters().read_bytes
            new_write = psutil.disk_io_counters().write_bytes
            read_speed = (new_read - old_read) / 1024
            write_speed = (new_write - old_write) / 1024
            print(Fore.YELLOW + f"Okuma: {read_speed:.2f} KB/sn | Yazma: {write_speed:.2f} KB/sn", end="\r")
            old_read, old_write = new_read, new_write
    except KeyboardInterrupt:
        print(Fore.RED + "\nDisk Performansı İzleme Durduruldu.")

def get_cpu_core_usage():
    print(Fore.CYAN + "CPU Çekirdek Kullanımları:")
    core_usages = psutil.cpu_percent(percpu=True, interval=1)
    for i, usage in enumerate(core_usages):
        print(Fore.YELLOW + f"Çekirdek {i + 1}: %{usage}")

def search_registry_key(key_name):
    try:
        result = subprocess.check_output(f'reg query HKLM /f "{key_name}" /t REG_SZ /s', shell=True, text=True)
        return f"Kayıt Defteri Arama Sonucu:\n{result}"
    except subprocess.CalledProcessError:
        return f"{key_name} kayıt defterinde bulunamadı."

def list_power_plans():
    try:
        result = subprocess.check_output("powercfg /list", shell=True, text=True)
        return f"Mevcut Güç Planları:\n{result}"
    except Exception as e:
        return f"Güç planı bilgisi alınamadı: {str(e)}"

def schedule_shutdown(minutes):
    try:
        seconds = minutes * 60
        subprocess.run(f"shutdown /s /t {seconds}", shell=True)
        return f"{minutes} dakika sonra bilgisayar kapatılacak."
    except Exception as e:
        return f"Kapatma zamanlayıcısı ayarlanamadı: {str(e)}"

def get_temperature_info():
    try:
        temperatures = psutil.sensors_temperatures()
        output = []
        for name, entries in temperatures.items():
            for entry in entries:
                output.append(f"{name} - {entry.label or 'N/A'}: {entry.current}°C")
        return "\n".join(output)
    except Exception as e:
        return f"Sıcaklık bilgisi alınamadı: {str(e)}"

def set_screen_brightness(level):
    try:
        level = max(0, min(level, 100))
        subprocess.run(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})", shell=True)
        return f"Ekran parlaklığı %{level} olarak ayarlandı."
    except Exception as e:
        return f"Ekran parlaklığı ayarlanamadı: {str(e)}"

def capture_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(filename, "PNG")
        return f"Ekran görüntüsü kaydedildi: {filename}"
    except Exception as e:
        return f"Ekran görüntüsü alınamadı: {str(e)}"

def list_bluetooth_devices():
    try:
        result = subprocess.check_output("powershell Get-PnpDevice -Class Bluetooth", shell=True, text=True)
        return f"Bluetooth Cihazları:\n{result}"
    except Exception as e:
        return f"Bluetooth cihazları listelenemedi: {str(e)}"

def find_large_files(directory, size_limit_mb):
    try:
        size_limit = size_limit_mb * 1024 * 1024
        large_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > size_limit:
                    large_files.append((file_path, os.path.getsize(file_path) // (1024**2)))
        if not large_files:
            return "Belirtilen boyuttan büyük dosya bulunamadı."
        return "\n".join([f"{file}: {size} MB" for file, size in large_files])
    except Exception as e:
        return f"Büyük dosyalar aranırken bir hata oluştu: {str(e)}"

def kill_background_process(process_name):
    try:
        for process in psutil.process_iter(['name']):
            if process.info['name'] == process_name:
                process.kill()
                return f"{process_name} başarıyla sonlandırıldı."
        return f"{process_name} çalışmıyor."
    except Exception as e:
        return f"Uygulama kapatılırken hata oluştu: {str(e)}"

def get_saved_wifi_passwords():
    try:
        result = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
        profiles = [line.split(":")[1].strip() for line in result.split("\n") if "All User Profile" in line]
        passwords = []
        for profile in profiles:
            try:
                result = subprocess.check_output(f"netsh wlan show profile {profile} key=clear", shell=True, text=True)
                password = [line.split(":")[1].strip() for line in result.split("\n") if "Key Content" in line][0]
                passwords.append(f"{profile}: {password}")
            except IndexError:
                passwords.append(f"{profile}: Şifre yok")
        return "\n".join(passwords)
    except Exception as e:
        return f"Wi-Fi şifreleri alınamadı: {str(e)}"

def check_for_updates():
    try:
        current_version = "1.0.0"
        response = requests.get("https://api.github.com/repos/kullanici/uygulama/releases/latest")
        latest_version = response.json()["tag_name"]
        if latest_version > current_version:
            return f"Yeni sürüm mevcut: {latest_version}. Lütfen güncelleyin."
        else:
            return "Uygulamanız güncel."
    except Exception as e:
        return f"Güncelleme kontrolü başarısız: {str(e)}"

def send_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Sistem İzleme Aracı",
            timeout=5
        )
        return "Bildirim gönderildi."
    except Exception as e:
        return f"Bildirim gönderilemedi: {str(e)}"

def backup_directory(source, destination):
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
        for file_name in os.listdir(source):
            full_file_name = os.path.join(source, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, destination)
        return f"{source} başarıyla {destination} dizinine yedeklendi."
    except Exception as e:
        return f"Yedekleme sırasında hata oluştu: {str(e)}"

def put_system_to_sleep():
    try:
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
        return "Bilgisayar uyku moduna alındı."
    except Exception as e:
        return f"Uyku moduna geçiş başarısız: {str(e)}"

def clean_temp_files():
    try:
        temp_path = os.getenv("TEMP")
        file_count = len(os.listdir(temp_path))
        for file in os.listdir(temp_path):
            try:
                file_path = os.path.join(temp_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                continue
        return f"{file_count} geçici dosya temizlendi."
    except Exception as e:
        return f"Disk temizleme sırasında hata oluştu: {str(e)}"

def optimize_for_gaming():
    try:
        services_to_stop = ["Windows Update", "SysMain", "Spooler"]
        for service in services_to_stop:
            subprocess.run(f"net stop {service}", shell=True)
        return "Oyun modu optimizasyonu tamamlandı."
    except Exception as e:
        return f"Oyun modu sırasında hata oluştu: {str(e)}"

def sentiment_analysis(text):
    try:
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return "Pozitif duygu algılandı."
        elif analysis.sentiment.polarity < 0:
            return "Negatif duygu algılandı."
        else:
            return "Nötr duygu algılandı."
    except Exception as e:
        return f"Duygu analizi yapılamadı: {str(e)}"

def start_key_logger(log_file):
    try:
        def on_press(key):
            with open(log_file, "a") as file:
                file.write(f"{key}\n")

        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        return f"Klavye dinleyici başlatılamadı: {str(e)}"

def schedule_backup(source, destination, interval_hours):
    try:
        while True:
            backup_directory(source, destination)
            time.sleep(interval_hours * 3600)
    except KeyboardInterrupt:
        return "Yedekleme işlemi durduruldu."

def main_menu():
    print(Fore.CYAN + "======== SİSTEM İZLEME VE PERFORMANS ARACI ========")
    print(Fore.CYAN + "=                -made by simsek66-              =")
    print(Fore.CYAN + "===================================================\n")
    print(Fore.CYAN + "1. Sistem Bilgileri")
    print(Fore.CYAN + "2. CPU Kullanımı")
    print(Fore.CYAN + "3. Bellek (RAM) Kullanımı")
    print(Fore.CYAN + "4. Disk Kullanımı")
    print(Fore.CYAN + "5. Ağ (Network) Bilgileri")
    print(Fore.CYAN + "6. Gerçek Zamanlı CPU İzleme")
    print(Fore.CYAN + "7. Log Oluştur")
    print(Fore.CYAN + "8. Çalışma Süresi (Uptime)")
    print(Fore.CYAN + "9. Batarya Durumu")
    print(Fore.CYAN + "10. Çalışan İşlemler")
    print(Fore.CYAN + "11. CPU ve RAM Sıcaklıkları")
    print(Fore.CYAN + "12. GPU Bilgileri")
    print(Fore.CYAN + "13. Toplam İşlem Sayısı")
    print(Fore.CYAN + "14. En Çok Kaynak Tüketen İşlemler")
    print(Fore.CYAN + "15. Güncel Tarih ve Saat")
    print(Fore.CYAN + "16. Ağ Durumu")
    print(Fore.CYAN + "17. GPU Kullanımı")
    print(Fore.CYAN + "18. Ağ Bağlantısı Durumu")
    print(Fore.CYAN + "19. Sistem Performans Grafiği (1 dakikalık)")
    print(Fore.CYAN + "20. Sistem Güncellemeleri")
    print(Fore.CYAN + "21. Depolama Aygıtları Bilgisi")
    print(Fore.CYAN + "22. Uygulama Performans Monitörü")
    print(Fore.CYAN + "23. Kritik Durum İzleme")
    print(Fore.CYAN + "24. Dosya Sistemi Sağlık Kontrolü")
    print(Fore.CYAN + "25. Wi-Fi Bağlantı Bilgileri")
    print(Fore.CYAN + "26. Ağ Trafiği İzleme")
    print(Fore.CYAN + "27. Disk Performansı İzleme")
    print(Fore.CYAN + "28. CPU Çekirdek Kullanımı")
    print(Fore.CYAN + "29. Kayıt Defteri Anahtarı Arama")
    print(Fore.CYAN + "30. Güç Planlarını Listele")
    print(Fore.CYAN + "31. Bilgisayar Kapatma Zamanlayıcı")
    print(Fore.CYAN + "32. Donanım Sıcaklıkları (Linux ve sensör gerektirir)")
    print(Fore.CYAN + "33. Ekran Parlaklığını Değiştir")
    print(Fore.CYAN + "34. Anlık Ekran Görüntüsü Al")
    print(Fore.CYAN + "35. Bluetooth Cihazlarını Listele")
    print(Fore.CYAN + "36. Büyük Dosyaları Bul")
    print(Fore.CYAN + "37. Wi-Fi Şifrelerini Göster")
    print(Fore.CYAN + "38. Sistem Bildirimi Gönder")
    print(Fore.CYAN + "39. Bilgisayarı Uyku Moduna Al")
    print(Fore.CYAN + "40. Yedekleme Yap")
    print(Fore.CYAN + "41. Geçici Dosyaları Temizle")
    print(Fore.CYAN + "42. Oyun Modu Optimizasyonu")
    print(Fore.CYAN + "43. Yapay Zeka Metin Duygu Analizi")
    print(Fore.CYAN + "44. Klavye Dinleyicisi (Keylogger)")
    print(Fore.CYAN + "45. Zamanlı Dosya Yedekleme")
    print(Fore.CYAN + "46. Çıkış")

    choice = input(Fore.CYAN + "\nBir seçenek girin (1-41): ")
    if choice == '1':
        print("\n" + get_system_info())
    elif choice == '2':
        print("\n" + get_cpu_usage())
    elif choice == '3':
        print("\n" + get_memory_info())
    elif choice == '4':
        print("\n" + get_disk_usage())
    elif choice == '5':
        print("\n" + get_network_info())
    elif choice == '6':
        get_cpu_usage_live()
    elif choice == '7':
        log_system_info()
    elif choice == '8':
        print("\n" + get_uptime())
    elif choice == '9':
        print("\n" + get_battery_status())
    elif choice == '10':
        show_processes()
    elif choice == '11':
        print("\n" + get_temperatures())
    elif choice == '12':
        print("\n" + get_gpu_info())
    elif choice == '13':
        print("\n" + get_process_count())
    elif choice == '14':
        print("\n" + get_top_processes())
    elif choice == '15':
        print("\n" + get_current_time())
    elif choice == '16':
        print("\n" + get_network_status())
    elif choice == '17':
        print("\n" + get_gpu_usage())
    elif choice == '18':
        print("\n" + get_ping_status())
    elif choice == '19':
        print(Fore.YELLOW + "\nGrafiğin oluşması için 60 saniye beklemelisiniz.")
        print("\n" + plot_system_usage())
    elif choice == "20":
        print(get_update_status())
    elif choice == "21":
        print(get_storage_devices())
    elif choice == "22":
        app_name = input("Uygulama adını girin: ")
        monitor_application_performance(app_name)
    elif choice == "23":
        critical_alerts()
    elif choice == "24":
        print(check_file_system_health())
    elif choice == "25":
        print(get_wifi_info())
    elif choice == "26":
        monitor_network_traffic()
    elif choice == "27":
        monitor_disk_performance()
    elif choice == "28":
        get_cpu_core_usage()
    elif choice == "29":
        key = input("Aranacak anahtar adını girin: ")
        print(search_registry_key(key))
    elif choice == "30":
        print(list_power_plans())
    elif choice == "31":
        minutes = int(input("Kaç dakika sonra kapatılsın?: "))
        print(schedule_shutdown(minutes))
    elif choice == "32":
        print(get_temperature_info())
    elif choice == "33":
        brightness = int(input("Parlaklık seviyesi (0-100): "))
        print(set_screen_brightness(brightness))
    elif choice == "34":
        print(capture_screenshot())
    elif choice == "35":
        print(list_bluetooth_devices())
    elif choice == "36":
        directory = input("Dizin yolu girin: ")
        size_limit = int(input("Boyut limiti (MB): "))
        print(find_large_files(directory, size_limit))
    elif choice == "37":
        print(get_saved_wifi_passwords())
    elif choice == "38":
        title = input("Bildirim Başlığı: ")
        message = input("Bildirim Mesajı: ")
        print(send_notification(title, message))
    elif choice == "39":
        print(put_system_to_sleep())
    elif choice == "40":
        source = input("Kaynak Dizin: ")
        destination = input("Hedef Dizin: ")
        print(backup_directory(source, destination))
    elif choice == "41":
        print(clean_temp_files())
    elif choice == "42":
        print(optimize_for_gaming())
    elif choice == "43":
        text = input("Analiz için bir metin girin: ")
        print(sentiment_analysis(text))
    elif choice == "44":
        log_file = "key_log.txt"
        print(f"Klavye dinleyici başlatılıyor... ({log_file})")
        start_key_logger(log_file)
    elif choice == "45":
        source = input("Yedeklenecek klasör: ")
        destination = input("Hedef klasör: ")
        interval = int(input("Yedekleme aralığı (saat): "))
        print(schedule_backup(source, destination, interval))
    elif choice == "46":
        print(Fore.RED + "Program sonlandırılıyor.")
        sys.exit()
    else:
        print(Fore.RED + "Geçersiz seçim. Lütfen tekrar deneyin.")
    
    restart_program()

def restart_program():
    choice = input(Fore.YELLOW + "\nMenüye dönmek ister misiniz? (E/H): ").lower()
    if choice == 'e':
        clear_screen()
        main_menu()
    elif choice == 'h':
        print(Fore.RED + "Program sonlandırılıyor.")
        sys.exit()

def bytebeat1(t):
    return ((t*440)>>(t&3))&255 & 0xFF

duration1 = 1
sample_rate1 = 8000

t_values1 = np.arange(0, duration1 * sample_rate1)
audio_data1 = np.array([bytebeat1(t) for t in t_values1], dtype=np.int8)

sd.play(audio_data1, sample_rate1)

time.sleep(1)

clear_screen()
main_menu()
