import customtkinter as ctk
from main import chat_with_AI
from database import create_chat,save_messages,get_all,get_messages,createTables

BG_COLOR = "#FFF9F5"        # soft off-white background
FRAME_COLOR = "#F5FAF3"     # very light matcha green
CARD_COLOR = "#FFFDFB"      # clean card

BUTTON_COLOR = "#F8AFC4"    # strawberry pink
BUTTON_HOVER = "#CFECC8"    # deeper strawberry

ENTRY_COLOR = "#FFF2F6"     # soft pink input
TEXT_COLOR = "#2F2F2F"      # dark readable text
LABEL_COLOR = "#7CBF7C"     # pastel green accent

SCROLL_FRAME_COLOR = "#FFFDFB"  # pastel pink (your chat area)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

createTables() 
current_chat =create_chat()

app = ctk.CTk()
app.title("MY CHAT-BOT")
app.geometry("1300x750")
app.resizable(True, True)
app.configure(fg_color=BG_COLOR)

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
title.grid(row=0, column=0, columnspan=2,pady=15)


def open_chat(chat_id):

    global current_chat

    current_chat = chat_id

    # purani chat bubbles hatao
    for widget in chat_frame.winfo_children():
        widget.destroy()

    messages = get_messages(chat_id)

    for role, content in messages:

        if role == "user":
            add_message(content, "user")
        else:
            add_message(content, "assistant")


        
def load_sidebar():
    for widget in sidebar_frame.winfo_children():
        widget.destroy()

    chats = get_all()

    for chat in chats:

        btn = ctk.CTkButton(
            sidebar_frame,
            text=chat[1],       # title
            width=220,
            command=lambda cid=chat[0]: open_chat(cid)
        )

        btn.pack(fill="x", padx=10, pady=5)

    
sidebar_frame = ctk.CTkScrollableFrame(
   main_frame,
   width=220,
   height=650,
   fg_color=SCROLL_FRAME_COLOR
)
sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=10)


details_frame = ctk.CTkScrollableFrame(
    main_frame,
    height=650,
    fg_color=SCROLL_FRAME_COLOR
)
details_frame.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=10)

chat_frame = ctk.CTkScrollableFrame(
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
      bubble_color = "#F8AFC4"
      anchor="e"
    else:
      bubble_color = "#CFECC8"
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

    # alignment
    if sender == "user":
        bubble.pack(anchor="e", padx=12, pady=6)
    else:
        bubble.pack(anchor="w", padx=12, pady=6)

def send_message():

    user_message = entry.get()
    if user_message.strip() == "":
       return
    add_message(user_message, sender="user")
    entry.delete(0, "end")
    save_messages(current_chat, "user", user_message)

    response = chat_with_AI(user_message)
    add_message(response, sender="assistant")   
    save_messages(current_chat, "assistant", response)

     
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
send_button.pack(pady=10)

add_message("Hi 👋 I am your AI assistant. How can I help you?", "assistant")   
load_sidebar()  
app.mainloop()
