import platform

def detect_os():
    system = platform.system()

    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "Mac"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"

if __name__ == "__main__":
    os_name = detect_os()
    print(f"The current operating system is: {os_name}")
