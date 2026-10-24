import psutil


def hardware_status():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }


if __name__ == "__main__":
    print(hardware_status())