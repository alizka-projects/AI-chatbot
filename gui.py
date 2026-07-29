import customtkinter as ctk
from main import chat_with_AI
from tkinter import messagebox
import database as db
import speech_recognition as sr
import threading


BG_COLOR = "#FFF9F5"        # soft off-white background
FRAME_COLOR = "#F8AFC4"     # very light matcha green
CARD_COLOR = "#FFFDFB"      # clean card

BUTTON_COLOR = "#F8AFC4"    # strawberry pink
BUTTON_HOVER = "#CFECC8"    # deeper strawberry

ENTRY_COLOR = "#FFF2F6"     # soft pink input
TEXT_COLOR = "#2F2F2F"      # dark readable text
LABEL_COLOR = "#7CBF7C"     # pastel green accent

SCROLL_FRAME_COLOR = "#FFFDFB"  # pastel pink (your chat area)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

db.createTables() 
is_recording = False
current_chat = None


app = ctk.CTk()
app.title("MY CHAT-BOT")
app.geometry("1300x750")
app.resizable(True, True)
app.configure(fg_color="#F2D0DA"  )

# ---------------- Main Frame ----------------
main_frame = ctk.CTkFrame(app, corner_radius=15,fg_color=FRAME_COLOR)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=4)

main_frame.grid_rowconfigure(1, weight=1)

# ---------------- Title ----------------
title = ctk.CTkLabel(
    main_frame,
    text="HI, I AM YOUR AI ASSISTANT",
    font=("Segoe UI", 28, "bold"),
    text_color="#2F2F2F",
)
title.grid(row=0, column=0, columnspan=2 ,pady=15)


def new_chat():
    global current_chat
    current_chat = db.create_chat()
    for widget in chat_frame.winfo_children():
        widget.destroy()
    add_message(
        "Hi 👋 I am your AI assistant.",
        "assistant"
    )
    entry.delete(0, "end")
    load_sidebar()



def open_chat(chat_id):
    global current_chat
    current_chat = chat_id
    for widget in chat_frame.winfo_children():
        widget.destroy()
    messages = db.get_messages(chat_id)
    for role, content in messages:
        if role == "user":
            add_message(content, "user")
        else:
            add_message(content, "assistant")



def delete_chat_gui(chat_id):
    global current_chat
    answer = messagebox.askyesno(
        "Delete Chat",
        "Are you sure you want to delete this chat?"
    )
    if not answer:
        return
    db.delete_chat(chat_id)
    if current_chat == chat_id:
        current_chat = None
        for widget in chat_frame.winfo_children():
            widget.destroy()
        add_message(
                "Start a new conversation 😊",
                "assistant"
        )
    load_sidebar()



def load_sidebar():
    for widget in chat_list_frame.winfo_children():
        widget.destroy()
    chats = db.get_all()
    for chat in chats:
        row = ctk.CTkFrame(
        chat_list_frame,
        fg_color="transparent"
       )
        row.pack(fill="x", padx=5, pady=5)
        btn = ctk.CTkButton(
            row,
            text=chat[1],       # title
            width=170,
            fg_color="#79DE5D",
            hover_color="#8FB784",
            text_color="#2F312F",
            command=lambda cid=chat[0]: open_chat(cid)
        )
        btn.pack(side="left" ,fill="x", expand=True)
        delete_btn = ctk.CTkButton(
        row,
        text="🗑",
        width=35,
        fg_color="#2C8912",
        hover_color="#80BD78",
        command=lambda cid=chat[0]: delete_chat_gui(cid)
    )
        delete_btn.pack(side="right", padx=3)




sidebar_frame = ctk.CTkFrame(
   main_frame,
   width=220,
   height=650,
   fg_color="#F2D0DA"
)
sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=10)

history = ctk.CTkLabel(
    sidebar_frame,
    text="History",
    text_color="#2F2F2F",
    font=("Arial",20,"bold"),
    corner_radius=20,
    fg_color="transparent"
)
history.pack(fill="x",padx=10,pady=10)

new_chat_btn = ctk.CTkButton(
    sidebar_frame,
    text="+ New Chat",
    command=new_chat,
    fg_color="#79DE5D",
    hover_color="#8FB784",
    text_color="#2F312F"
)
new_chat_btn.pack(fill="x", padx=10, pady=10)


chat_list_frame = ctk.CTkScrollableFrame(
    sidebar_frame,
    fg_color="transparent"
)
chat_list_frame.pack(fill="both", expand=True, padx=5, pady=5)



details_frame = ctk.CTkScrollableFrame(
    main_frame,
    height=650,
    fg_color="#F2D0DA"
)
details_frame.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=10)


chat_frame = ctk.CTkFrame(
    details_frame,
    fg_color="transparent"
)
chat_frame.pack(fill="both", expand=True, padx=10, pady=10)


bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
bottom_frame.grid(row=2,column=1, pady=10,sticky="ew")


entry= ctk.CTkEntry(
    bottom_frame,
    placeholder_text="Ask me anything...",
    width=750,
    height=42,
    border_width=2,
    corner_radius=20,
    fg_color=ENTRY_COLOR,
    text_color="#2F2F2F",
    placeholder_text_color="#9CA3AF",
)
entry.pack(side="left",fill="x", padx=(5,5))



def add_message(text, sender="user"):
    if sender == "user":
      bubble_color = "#EC8EA9"
      anchor="e"
    else:
      bubble_color = "#B4E4A8"
      anchor="w"
    bubble = ctk.CTkFrame(
            chat_frame,
            fg_color=bubble_color,
            corner_radius=15,
            width=500,
            height=50
        )
    msg = ctk.CTkLabel(
        bubble,
        text=text,
        wraplength=420,
        justify="left",
        text_color="#2F2F2F", 
        font=("Segoe UI", 14)  
    )
    msg.pack(padx=10, pady=5)
    if sender == "user":
        bubble.pack(anchor="e", padx=12, pady=6)
    else:
        bubble.pack(anchor="w", padx=12, pady=6)




def send_message():
    global current_chat
    user_message = entry.get().strip()
    if user_message == "":
       return
    if current_chat is None:
            current_chat = db.create_chat()
            load_sidebar()

    add_message(user_message, sender="user")
    entry.delete(0, "end")
    db.save_messages(current_chat, "user", user_message)
    title=db.get_chat_title(current_chat)

    if (title=="New Chat"):
        db.update_chat_title(current_chat,user_message[:30])
        load_sidebar()
    response = chat_with_AI(user_message)
    add_message(response, sender="assistant")   
    db.save_messages(current_chat, "assistant", response)



     
send_button = ctk.CTkButton(
    bottom_frame,
    text="🍓 Send",
    width=110,
    height=42,
    corner_radius=20,
    fg_color="#FB7185",
    hover_color="#F43F5E",
    text_color="#FFFFFF",
    command=send_message,
  
)
send_button.pack(side= "left",padx=(5,5),pady=0)

def voice_input():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text

    except:
       return None

def recording_start():
    global is_recording
    is_recording = True

    mic_button.configure(
        text="🔴",
        fg_color="red",
        hover_color="#FF3B30"

    )
    send_button.configure(
        state="disabled"
    )

    entry.configure(
        state="disabled"
    )

def recording_stop():
    global is_recording
    is_recording = False
   

    mic_button.configure(
        text="🎤",
        fg_color="#FB7185",
        hover_color="#F43F5E"
    )
    send_button.configure(
        state="normal"
    )

    entry.configure(
        state="normal"
    )
def process_voice():
    global current_chat
    if current_chat is None:
        current_chat= db.create_chat()
        app.after(0, load_sidebar)
    try:
        user_message = voice_input()


        if user_message is None:
            return
        app.after(0, lambda: add_message(user_message, "user"))
        db.save_messages(current_chat,"user", user_message)
        title = db.get_chat_title(current_chat)
        if title == "New Chat":
            db.update_chat_title(current_chat, user_message[:30])
            app.after(0, load_sidebar)

        response= chat_with_AI(user_message)
        app.after(0, lambda: add_message(response,"assistant"))
        db.save_messages(current_chat,"assistant", response)
    finally:
        app.after(0, recording_stop)


def send_voice():
    recording_start()
    thread= threading.Thread(

        target=process_voice,
        daemon=True
    )
    thread.start()
    
mic_button = ctk.CTkButton(
    bottom_frame,
    text="🎤",
    width=60,
    corner_radius=100,
    fg_color="#FB7185",
    hover_color="#F43F5E",
    text_color="#FFFFFF",
    command=send_voice
)
mic_button.pack(side="left", padx=(10,5), pady=0)



add_message("Hi 👋 I am your AI assistant. How can I help you?", "assistant")   
load_sidebar()  
app.mainloop()

