# YouTube-Downloader
Simple python script that downloads YouTube videos.
The UI is very ugly. This script was an exercise for me to learn about Tkinter.

![image](https://github.com/user-attachments/assets/7bd0232f-f88f-4d4e-9aa9-54f4475d3f77)


> [!NOTE]
> If you provide a playlist link, the script will only download the first video. Maybe I will add an option to download the whole playlist idk at the moment this was simply an exercise.

### For Users:

If you know how to setup requirements and stuff, feel free to use the script as it is. If not, a portable executable can be found under [Releases](https://github.com/xesdoog/YouTube-Downloader/releases).


> [!NOTE]
> The portable executable from the releases tab will be flagged by Windows Security as a virus. The code is open source and the executable was built by Github Actions. This behavior is caused by 2 main things:
> 1. The program doesn't have a certificate. Those cost money and it's not worth it to sign a simple Python script.
> 2. Windows Security specifically hates PyInstaller-packed executables for some odd reason.
