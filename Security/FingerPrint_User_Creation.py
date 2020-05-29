import platform, pyautogui


# Get client OS.
operating_system = platform.system()
system_release = platform.release()
system_version = platform.version()
system_platform = platform.platform()

# Get Screen Size of User [Windows10]
width, height = pyautogui.size()


# To Be Continued.. Fingerprinting.
