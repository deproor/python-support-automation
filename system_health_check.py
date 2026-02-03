import os
import platform
import socket
import subprocess
import shutil
from datetime import datetime

def bytes_to_gb(b: int) -> float:
    return round(b / (1024**3), 2)

def ping_google() -> bool:
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", count_flag, "1", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3
        )
        return result.returncode == 0
    except Exception:
        return False

def generate_report():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    user = os.getenv("USERNAME") or os.getenv("USER") or "unknown"
    system = platform.system()
    release = platform.release()

    disk_path = "C:\\" if system.lower() == "windows" else "/"
    total, used, free = shutil.disk_usage(disk_path)

    online = ping_google()

    report = []
    report.append("=== SUPPORT HEALTH CHECK ===")
    report.append(f"Time: {now}")
    report.append(f"Host: {hostname}")
    report.append(f"User: {user}")
    report.append(f"OS: {system} {release}")
    report.append(
        f"Disk ({disk_path}) - Total: {bytes_to_gb(total)} GB | "
        f"Used: {bytes_to_gb(used)} GB | Free: {bytes_to_gb(free)} GB"
    )
    report.append(f"Internet: {'OK' if online else 'FAIL'}")
    report.append("============================")

    return "\n".join(report)

if __name__ == "__main__":
    report_content = generate_report()

    print(report_content)

    with open("health_report.txt", "w", encoding="utf-8") as f:
        f.write(report_content)
