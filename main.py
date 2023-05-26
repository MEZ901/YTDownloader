import tkinter
from tkinter import ttk
import customtkinter
from pytube import YouTube
from PIL import ImageTk, Image
import urllib.request

def preview():
    try:
        ytLink = link.get()
        global ytObject
        ytObject = YouTube(ytLink, on_progress_callback=progress_function)

        helper_text.configure(text="")
        title_label.configure(text=ytObject.title)

        update_thumbnail()
        update_qualities()
    except Exception as e:
        print(e)
        helper_text.configure(text="Invalid URL", text_color="red")
        title_label.configure(text="")
        thumbnail_label.configure(image="")
        return
    

def update_thumbnail():
    try:
        filename = "thumbnail/thumbnail.jpg"
        urllib.request.urlretrieve(ytObject.thumbnail_url, filename)

        img = Image.open(filename)
        img = img.resize((640, 360))

        img = ImageTk.PhotoImage(img)
        thumbnail_label.configure(image=img)
        thumbnail_label.image = img

    except Exception as e:
        print(e)


def update_qualities():
    qualities = ytObject.streams.filter(progressive=True)
    quality_options = [quality.resolution for quality in qualities]
    quality_combobox['values'] = quality_options
    if quality_options:
        quality_combobox.current(0)


def get_selected_quality():
    selected_quality = quality_combobox.get()
    return selected_quality


def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress_percentage = bytes_downloaded / total_size * 100
    percentage = str(int(progress_percentage))

    p_percentage.configure(text=percentage + "%")
    p_percentage.update()

    progress_bar.set(float(progress_percentage) / 100)


def download():
    try:
        selected_quality = get_selected_quality()
        video = ytObject.streams.filter(resolution=selected_quality, progressive=True).first()
        video.download("./videos")
    except Exception as e:
        print(e)
    
    helper_text.configure(text="Finished Downloading", text_color="green")


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

# Frame for Input and Preview Button
top_frame = tkinter.Frame(app, background="SystemButtonFace", bg=app.cget("bg"))
top_frame.pack()

# Link Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(top_frame, width=350, height=40, textvariable=url_var)
link.pack(side=tkinter.LEFT, padx=5,)

# preview Button
preview = customtkinter.CTkButton(top_frame, text="preview", command=preview, height=40) 
preview.pack(side=tkinter.LEFT, padx=5,)

# Helper Text
helper_text = customtkinter.CTkLabel(app, text="")
helper_text.pack()

# Title Label
title_label = customtkinter.CTkLabel(app, text="")
title_label.pack()

# Thumbnail Label
thumbnail_label = tkinter.Label(app, width=640, height=360, bg=app.cget("bg"))
thumbnail_label.pack()

# Frame for Combobox and Download Button
bottom_frame = tkinter.Frame(app, background="SystemButtonFace", bg=app.cget("bg"))
bottom_frame.pack()

# Quality Combobox
quality_combobox = ttk.Combobox(bottom_frame, width=30, height=30, state="readonly")
quality_combobox.pack(side=tkinter.LEFT, padx=5, pady=5)

# Download Button
download = customtkinter.CTkButton(bottom_frame, text="Download", command=download)
download.pack(side=tkinter.LEFT, padx=5, pady=5)

# Progress Bar
p_percentage = customtkinter.CTkLabel(app, text="0%")
p_percentage.pack()

progress_bar = customtkinter.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

# Run App
app.mainloop()