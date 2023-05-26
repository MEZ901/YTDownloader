import tkinter
import customtkinter
from pytube import YouTube

def download():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        video = ytObject.streams.get_highest_resolution()
        video.download("./videos")
    except Exception as e:
        print(e)
    
    finish_label.configure(text="Finished Downloading")

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Add UI Elements
title = customtkinter.CTkLabel(app, text="Insert YouTube URL")
title.pack(padx=10, pady=10)

# Link Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finish_label = customtkinter.CTkLabel(app, text="")
finish_label.pack()

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=download) 
download.pack(pady=10)

# Run App
app.mainloop()