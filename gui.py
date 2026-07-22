import customtkinter as ctk
from main import chat_with_AI

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

app = ctk.CTk()
app.title("MY CHAT-BOT")
app.geometry("900x600")
app.resizable(False, False)
app.configure(fg_color=BG_COLOR)

# ---------------- Main Frame ----------------
main_frame = ctk.CTkFrame(app, corner_radius=15,fg_color=FRAME_COLOR)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)


# ---------------- Title ----------------
title = ctk.CTkLabel(
    main_frame,
    text="HI, I AM YOUR AI ASSISTANT",
    font=("Segoe UI", 28, "bold"),
    text_color="#2F2F2F",
)
title.pack(pady=15)

details_frame = ctk.CTkScrollableFrame(
    main_frame,
    width=700,
    height=400,
    fg_color=SCROLL_FRAME_COLOR
)
details_frame.pack(padx=10, pady=10, fill="both", expand=True)

bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
bottom_frame.pack(fill="x", pady=10)
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
            details_frame,
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
    response = chat_with_AI(user_message)
    add_message(response, sender="assistant")    
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
app.mainloop()
