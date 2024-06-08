import os
import sys
import tkinter

from   tkinter   import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, OptionMenu
from   pathlib   import Path
from   pytube    import YouTube as YT
from   threading import Thread
from   time      import sleep

if getattr(sys, 'frozen', False):
    import pyi_splash

OUTPUT_PATH   = Path(__file__).parent
ASSETS_PATH   = OUTPUT_PATH / Path(r"assets")
DOWNLOAD_PATH = './YouTube_Downloads'
RESOLUTIONS   = ["Resolution",
                 "144p", 
                 "240p",
                 "360p",
                 "480p",
                 "720p",
                 "1080p",
                 "1440p",
                 "2160p",
                 ]
                 

window       = Tk()
entryContent = tkinter.StringVar()
titleVar     = tkinter.StringVar()
resVar       = tkinter.StringVar()
feedbackVar  = tkinter.StringVar()
resVar.set(RESOLUTIONS[0])


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def grab_title():
    global title
    try:
        link  = entryContent.get()
        title = YT(link).title

        if title is not None:

            titleVar.set("Video:  " + title)
    
    except Exception:
        pass
        titleVar.set("")


def title_thread():
    Thread(target = grab_title, daemon = True).start()


def on_enter(widget):
    global link
    link = entryContent.get()
    title_thread()


def set_res(resolution: str):
    global user_res
    user_res = resolution
    link     = entryContent.get()
    try:

        if link != None:

            if RESOLUTIONS.index(user_res) > 5:
                feedbackVar.set(
                    "WARNING!\nSelecting resolutions higher than 720p may result in a video without sound."
                    )

            else:
                feedbackVar.set("")

    except Exception as e:
        feedbackVar.set(e)


def in_progress(stream, chunk, bytes_remaining):
    feedbackVar.set("Downloading.")
    sleep(0.5)
    feedbackVar.set("Downloading..")
    sleep(0.5)
    feedbackVar.set("Downloading...")
    sleep(0.5)
    feedbackVar.set("Downloading ..")
    sleep(0.5)
    feedbackVar.set("Downloading  .")
    sleep(0.5)
    feedbackVar.set("Downloading")
    sleep(0.5)


def on_complete(stream, file_path):
    feedbackVar.set("Done!")
    sleep(3)
    feedbackVar.set("")

def download_func():
    try:

        title_thread()
        link = entryContent.get()
        yt = YT(link, on_progress_callback = in_progress, 
                     on_complete_callback = on_complete
                     )

        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)

        try:
            stream = yt.streams.filter(res = user_res, 
                                    file_extension = 'mp4', 
                                    progressive = True
                                    ).first()
                
        except NameError:
            stream = yt.streams.get_highest_resolution()
            feedbackVar.set("Resolution not set. Defaulting to highest available.")

        stream.download(DOWNLOAD_PATH)

    except Exception as e:

        if str(e) == "regex_search: could not find match for (?:v=|\\/)([0-9A-Za-z_-]{11}).*":
            feedbackVar.set("No link provided!")
            sleep(3)
            feedbackVar.set("")
        
        elif str(e) == "'NoneType' object has no attribute 'download'":
            feedbackVar.set("Video unavailable! Select a lower resolution then try again.")
            sleep(3)
            feedbackVar.set("")

        else:
            feedbackVar.set("[!] Unexpected error occured:  [ " + str(e) + " ]")
            sleep(5)
            feedbackVar.set("")
            pass


def download_thread():
    Thread(target = download_func, daemon = True).start()


window.geometry("480x315")
window.configure(bg = "#FFFFFF")
window.title("YouTube Downloader")
window.iconbitmap(relative_to_assets('ytd_icon.ico'))


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 300,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

banner = PhotoImage(
    file = relative_to_assets("banner.png"))
image_2 = canvas.create_image(
    240.0,
    43.0,
    image = banner
)

yt_logo = PhotoImage(
    file = relative_to_assets("yt_logo.png"))
image_3 = canvas.create_image(
    41.0,
    35.0,
    image = yt_logo
)

canvas.create_text(
    67.0,
    21.0,
    anchor = "nw",
    text = "YouTube Downloader",
    fill = "#FFFFFF",
    font = ("Roboto", 25 * -1)
)

searchBar = Entry(
    bd = 0,
    bg = "#DBD8D8",
    fg = "#000716",
    highlightthickness = 0,
    textvariable = entryContent
)

searchBar.place(
    x = 22.0,
    y = 110.0,
    width = 410.0,
    height = 35.0
)
searchBar.bind('<Return>', on_enter)

searchBar_img = PhotoImage(
    file=relative_to_assets("searchBar.png"))
entry_bg_1 = canvas.create_image(
    228.0,
    126.0,
    image = searchBar_img
)

vid_title = Label(master = window,
                  textvariable = titleVar,
                  bg = 'white'
                  ).place(
                x = 20.0,
                y = 160.0)

link_icon = PhotoImage(
    file=relative_to_assets("link_icon.png"))
image_1 = canvas.create_image(
    459.0,
    126.0,
    image = link_icon
)

button_image_1 = PhotoImage(
    file=relative_to_assets("download_btn_test.png"))

download_btn = Button(
    image=button_image_1,
    borderwidth = 0,
    highlightthickness = 0,
    command = download_thread,
    relief = "flat"
)
download_btn.place(
    x = 100.0,
    y = 202.0,
    width = 139.0,
    height = 56.0
)

resMenu = OptionMenu(window,
                     resVar,
                     *RESOLUTIONS,
                     command = set_res
                     ).place(x = 270.0,
                             y = 210.0
                             )

feedback_text = Label(master = window,
                  textvariable = feedbackVar,
                  bg = 'white'
                  ).place(
                x = 15.0,
                y = 275.0)

window.resizable(False, False)

if getattr(sys, 'frozen', False):
    pyi_splash.close()

window.mainloop()