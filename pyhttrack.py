import os
import json
import subprocess
import shutil
import sys
import platform
from datetime import datetime
from colorama import Fore, Style, init as colorama_init

colorama_init()

def format_size(bytes_num):
    try:
        bytes_num = int(bytes_num)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_num < 1024:
                return f"{bytes_num:.2f} {unit}"
            bytes_num /= 1024
        return f"{bytes_num:.2f} PB"
    except:
        return "-"

arch = platform.machine().lower()
system = platform.system().lower()

arch_map = {
    "x86_64": "x64",
    "amd64": "x64",
    "i386": "x86",
    "i686": "x86",
    "arm64": "arm64",
    "aarch64": "arm64"
}

folder_arch = arch_map.get(arch)
wget_filename = "wget.exe" if system == "windows" else "wget"
wget_path = os.path.join("wget", folder_arch, wget_filename) if folder_arch else None

def install_wget():
    if system == "linux":
        print("Wget not found. Trying to install wget...")
        try:
            subprocess.run(["apt", "update"], check=True)
            subprocess.run(["apt", "install", "-y", "wget"], check=True)
            print("Wget installed successfully.")
            return shutil.which("wget")
        except subprocess.CalledProcessError:
            print("Failed to install wget. Make sure you have sudo access.")
    else:
        print("Automatic installation only supported on Linux.")
    return None

if wget_path and os.path.isfile(wget_path):
    wget_exec = wget_path
elif shutil.which("wget"):
    wget_exec = "wget"
else:
    wget_exec = install_wget()
    if not wget_exec:
        print("Cannot find or install wget.")
        sys.exit(1)

# Bersihkan terminal
os.system('cls' if os.name == 'nt' else 'clear')

results = []
os.makedirs("web", exist_ok=True)

try:
    with open('web.json', 'r') as file:
        urls = json.load(file)
except FileNotFoundError:
    print("File 'web.json' not found.")
    sys.exit(1)

print(f"\nTotal URL : {len(urls)}")
print("==================\n")

for url in urls:
    print(f"Downloading: {url}")
    try:
        print("\n")
        process = subprocess.Popen([
            wget_exec,
            "-r", "-m", "-c",
            "--no-parent",
            "--convert-links",
            "--adjust-extension",
            "--page-requisites",
            "--limit-rate=100k",
            "--random-wait",
            "--wait=1",
            "--timeout=15",
            "--tries=3",
            "--no-clobber",
            "--no-check-certificate",
            "--retry-connrefused",
            "-e", "robots=off",
            "--user-agent=Mozilla/5.0",
            "--directory-prefix=web",
            url
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = line.strip()

            if "saved [" in line and "'" in line:
                path = line.split("'")[1]
                raw_size = line.split("saved [")[-1].split("]")[0]
                byte_size = raw_size.split("/")[-1]
                size = format_size(byte_size)

                results.append({
                    "timestamp": now,
                    "url": url,
                    "file": path,
                    "status": "success",
                    "size": size
                })
                print(f"{Fore.GREEN}[{now}] Downloaded:{Style.RESET_ALL} {path} | {size}")

            elif "not modified" in line and "'" in line:
                path = line.split("'")[1]
                results.append({
                    "timestamp": now,
                    "url": url,
                    "file": path,
                    "status": "not modified",
                    "size": "-"
                })
                print(f"{Fore.YELLOW}[{now}] Skipped:{Style.RESET_ALL} {path}")
            else:
                path = line.split("'")[1]
                results.append({
                    "timestamp": now,
                    "url": url,
                    "file": path,
                    "status": "failed",
                    "size": "-"
                })
                print(f"{Fore.RED}[{now}] Failed:{Style.RESET_ALL} {path}")
        process.wait()
    except Exception as e:
        print(f"{Fore.RED}Failed to Download:{Style.RESET_ALL} {url}\n")

if results:
    with open("log.txt", "a", encoding="utf-8") as log_file:
        for result in results:
            log_file.write(f"[{result['timestamp']}] {result['url']} | {result['file']} | {result['status']} | {result['size']}\n")
else:
    print("No URLs to process.")
    sys.exit(0)

success = sum(r['status'] == 'success' for r in results)
skipped = sum(r['status'] == 'not modified' for r in results)
failed = sum(r['status'] == 'failed' for r in results)

print(f"\n{Fore.GREEN}Success : {success}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Skipped : {skipped}{Style.RESET_ALL}")
print(f"{Fore.RED}Failed  : {failed}{Style.RESET_ALL}")
