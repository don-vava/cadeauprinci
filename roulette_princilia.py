import tkinter as tk
from tkinter import font as tkfont
import random
import math
import time
import os
from PIL import Image, ImageTk

# ─────────────────────────────────────────────
#  CONFIGURATION DES CADEAUX
#  Tu peux changer les emojis et les noms !
# ─────────────────────────────────────────────
GIFTS = [
    {"num": 1,  "emoji": "🎀", "label": "Cadeau 1"},
    {"num": 2,  "emoji": "🌸", "label": "Cadeau 2"},
    {"num": 3,  "emoji": "💜", "label": "Cadeau 3"},
    {"num": 4,  "emoji": "✨", "label": "Cadeau 4"},
    {"num": 5,  "emoji": "🌟", "label": "Cadeau 5"},
    {"num": 6,  "emoji": "🦋", "label": "Cadeau 6"},
    {"num": 7,  "emoji": "👑", "label": "Cadeau 7"},
    {"num": 8,  "emoji": "🌈", "label": "Cadeau 8"},
    {"num": 9,  "emoji": "💫", "label": "Cadeau 9"},
    {"num": 10, "emoji": "🎠", "label": "Cadeau 10"},
    {"num": 11, "emoji": "🌺", "label": "Cadeau 11"},
    {"num": 12, "emoji": "🎊", "label": "Cadeau 12"},
]

# ─────────────────────────────────────────────
#  IMAGE DE FIN
#  Mets ton image dans le même dossier que ce fichier
#  et renomme-la : photo_fin.jpg (ou .png)
# ─────────────────────────────────────────────
FINAL_IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMG_1779-removebg-preview.png")

WHEEL_COLORS = [
    "#c460f5", "#f5609a", "#f5a360", "#60c4f5",
    "#f560c4", "#a360f5", "#f5e060", "#60f5a3",
    "#f56060", "#60f5f5", "#f5b060", "#b0f560",
]

BG_COLOR   = "#fdf0ff"
PINK       = "#f5609a"
PURPLE     = "#c460f5"
GOLD       = "#f5c842"
WHITE      = "#ffffff"
DARK_TEXT  = "#4a004a"


class RoulettePrincilia:
    def __init__(self, root):
        self.root = root
        self.root.title("🎀 La Roulette de Princilia 🎀")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.remaining = list(GIFTS)
        self.found = []
        self.spinning = False
        self.angle = 0.0
        self.spin_speed = 0.0
        self.anim_id = None
        self.winner = None

        self._build_ui()
        self._draw_wheel()
        self._update_gifts_grid()

    # ──────────────────────────────────────────
    #  UI CONSTRUCTION
    # ──────────────────────────────────────────
    def _build_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=BG_COLOR)
        title_frame.pack(pady=(16, 4))

        stars = tk.Label(title_frame, text="⭐🌸✨🎀✨🌸⭐",
                         bg=BG_COLOR, font=("Arial", 16))
        stars.pack()

        title = tk.Label(title_frame,
                         text="La Roulette de Princilia",
                         bg=BG_COLOR, fg=PURPLE,
                         font=("Arial", 26, "bold"))
        title.pack()

        sub = tk.Label(title_frame,
                       text="Tourne la roue pour déballer tes cadeaux ! 🎁",
                       bg=BG_COLOR, fg=PINK, font=("Arial", 12))
        sub.pack()

        # Main layout
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(padx=20, pady=8)

        left = tk.Frame(main, bg=BG_COLOR)
        left.pack(side="left", padx=16)

        right = tk.Frame(main, bg=BG_COLOR)
        right.pack(side="left", padx=16)

        # Wheel canvas
        self.canvas = tk.Canvas(left, width=380, height=380,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        # Spin button
        self.spin_btn = tk.Button(
            left, text="🌟  Tourner !  🌟",
            command=self._spin,
            bg=PURPLE, fg=WHITE,
            font=("Arial", 16, "bold"),
            relief="flat", padx=24, pady=10,
            activebackground=PINK, activeforeground=WHITE,
            cursor="hand2"
        )
        self.spin_btn.pack(pady=(12, 4))

        # Counter label
        self.counter_label = tk.Label(
            left, text="12 cadeaux restants 🎁",
            bg=BG_COLOR, fg=PURPLE, font=("Arial", 12)
        )
        self.counter_label.pack()

        # Message label
        self.msg_label = tk.Label(
            left, text="",
            bg=BG_COLOR, fg=PINK,
            font=("Arial", 13, "italic"),
            wraplength=360, justify="center"
        )
        self.msg_label.pack(pady=6)

        # Gifts grid (right side)
        grid_title = tk.Label(right,
                              text="🎁 Les cadeaux de Princilia 🎁",
                              bg=BG_COLOR, fg=PURPLE, font=("Arial", 13, "bold"))
        grid_title.pack(pady=(0, 8))

        self.grid_frame = tk.Frame(right, bg=BG_COLOR)
        self.grid_frame.pack()

        self.gift_labels = {}

    def _update_gifts_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        cols = 3
        for i, g in enumerate(GIFTS):
            row = i // cols
            col = i % cols
            is_found = g["num"] in self.found

            bg = "#e8e8e8" if is_found else WHITE
            fg_num = "#aaaaaa" if is_found else PURPLE
            alpha = 0.4 if is_found else 1.0

            card = tk.Frame(self.grid_frame, bg=bg,
                            highlightbackground="#e8c0f8" if not is_found else "#dddddd",
                            highlightthickness=2,
                            relief="flat", padx=8, pady=6)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            emoji_text = "✅" if is_found else g["emoji"]
            emoji_lbl = tk.Label(card, text=emoji_text, bg=bg, font=("Arial", 20))
            emoji_lbl.pack()

            num_lbl = tk.Label(card, text=f"N°{g['num']}",
                               bg=bg, fg=fg_num, font=("Arial", 12, "bold"))
            num_lbl.pack()

            if is_found:
                cross = tk.Label(card, text="déballé", bg=bg,
                                 fg="#aaaaaa", font=("Arial", 8))
                cross.pack()

    # ──────────────────────────────────────────
    #  WHEEL DRAWING
    # ──────────────────────────────────────────
    def _draw_wheel(self):
        self.canvas.delete("all")
        cx, cy, r = 190, 190, 170
        items = self.remaining if self.remaining else GIFTS
        n = len(items)

        for i, g in enumerate(items):
            start_deg = self.angle + i * (360 / n)
            extent = 360 / n
            color = WHEEL_COLORS[i % len(WHEEL_COLORS)]

            # Slice
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start_deg, extent=extent,
                fill=color, outline=WHITE, width=2
            )

            # Number label on slice
            mid_deg = math.radians(start_deg + extent / 2)
            tx = cx + (r * 0.65) * math.cos(mid_deg)
            ty = cy - (r * 0.65) * math.sin(mid_deg)
            self.canvas.create_text(
                tx, ty, text=str(g["num"]),
                fill=WHITE, font=("Arial", 14, "bold")
            )

        # Outer ring
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline=PURPLE, width=5, fill=""
        )
        self.canvas.create_oval(
            cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5,
            outline=PINK, width=2, fill=""
        )

        # Center circle
        self.canvas.create_oval(cx - 28, cy - 28, cx + 28, cy + 28,
                                fill=WHITE, outline=PURPLE, width=3)
        self.canvas.create_text(cx, cy, text="🎀", font=("Arial", 18))

        # Pointer triangle (top)
        self.canvas.create_polygon(
            cx - 14, cy - r - 12,
            cx + 14, cy - r - 12,
            cx,      cy - r + 8,
            fill=PURPLE, outline=WHITE, width=2
        )

    # ──────────────────────────────────────────
    #  SPIN LOGIC
    # ──────────────────────────────────────────
    def _spin(self):
        if self.spinning or not self.remaining:
            return
        self.spinning = True
        self.spin_btn.config(state="disabled")
        self.msg_label.config(text="")

        # Pick winner
        self.winner = random.choice(self.remaining)

        # Target: winner slice should end under pointer (top = 90° in standard math)
        n = len(self.remaining)
        arc = 360 / n
        win_idx = self.remaining.index(self.winner)

        # Pointer is at angle=90° (top). We want the middle of winner slice there.
        extra_spins = random.randint(6, 10) * 360
        # Current angle offset of winner slice center
        current_center = self.angle + win_idx * arc + arc / 2
        # We want it to land at 90° (pointing up); rotation is CCW in canvas
        needed = (90 - current_center) % 360
        self.spin_target = self.angle + extra_spins + needed

        self.spin_speed = random.uniform(18, 22)
        self._animate_spin()

    def _animate_spin(self):
        remaining_dist = self.spin_target - self.angle
        if remaining_dist <= 0 or self.spin_speed < 0.3:
            self.angle = self.spin_target % 360
            self._draw_wheel()
            self.spinning = False
            self._reveal_winner()
            return

        # Ease out
        self.spin_speed = max(0.25, self.spin_speed * 0.985)
        self.angle += self.spin_speed
        self._draw_wheel()
        self.anim_id = self.root.after(16, self._animate_spin)

    # ──────────────────────────────────────────
    #  REVEAL WINNER
    # ──────────────────────────────────────────
    def _reveal_winner(self):
        g = self.winner
        self.found.append(g["num"])
        self.remaining = [x for x in self.remaining if x["num"] != g["num"]]

        self._update_gifts_grid()
        self._draw_wheel()

        rem = len(self.remaining)

        # Show popup
        self._show_popup(g, rem)

    def _show_popup(self, g, rem):
        popup = tk.Toplevel(self.root)
        popup.title("🎁 Cadeau trouvé !")
        popup.configure(bg=BG_COLOR)
        popup.resizable(False, False)
        popup.grab_set()

        # Center popup
        popup.geometry("360x320+%d+%d" % (
            self.root.winfo_x() + 180,
            self.root.winfo_y() + 160
        ))

        tk.Label(popup, text="🎉", bg=BG_COLOR, font=("Arial", 48)).pack(pady=(20, 4))

        tk.Label(popup, text=f"Cadeau numéro",
                 bg=BG_COLOR, fg=PURPLE, font=("Arial", 14)).pack()

        tk.Label(popup, text=str(g["num"]),
                 bg=BG_COLOR, fg=PINK, font=("Arial", 52, "bold")).pack()

        msgs = [
            "C'est l'heure de déballer ! 🎀",
            "Quelle surprise t'attend ? 🌟",
            "Un cadeau rien que pour toi ! 👑",
            "La magie opère ! ✨",
            "Oh ! Regarde ce beau cadeau ! 🌸",
        ]
        tk.Label(popup, text=random.choice(msgs),
                 bg=BG_COLOR, fg=DARK_TEXT, font=("Arial", 12, "italic")).pack(pady=4)

        # Remaining message
        if rem == 0:
            counter_msg = "🎊 C'était le dernier cadeau !"
        elif rem == 1:
            counter_msg = "Il reste 1 cadeau à déballer ! 🎁"
        else:
            counter_msg = f"Il reste {rem} cadeaux à déballer ! 🎁"

        tk.Label(popup, text=counter_msg,
                 bg=BG_COLOR, fg=PURPLE, font=("Arial", 12, "bold")).pack(pady=4)

        def close_popup():
            popup.destroy()
            if rem == 0:
                self._show_final()
            else:
                self.spin_btn.config(state="normal")
                self._update_counter(rem)

        tk.Button(popup, text="Déballer ! 🎊",
                  command=close_popup,
                  bg=PINK, fg=WHITE,
                  font=("Arial", 14, "bold"),
                  relief="flat", padx=20, pady=8,
                  activebackground=PURPLE,
                  cursor="hand2").pack(pady=8)

    def _update_counter(self, rem):
        if rem == 1:
            self.counter_label.config(text="1 cadeau restant 🎁")
        else:
            self.counter_label.config(text=f"{rem} cadeaux restants 🎁")

    # ──────────────────────────────────────────
    #  FINAL SCREEN
    # ──────────────────────────────────────────
    def _show_final(self):
        # Destroy main content and show final screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#1a001a")

        container = tk.Frame(self.root, bg="#1a001a")
        container.pack(expand=True, fill="both", pady=20)

        # Fireworks title
        tk.Label(container,
                 text="🎊🎉🎀🌟🎊🎉🎀🌟🎊",
                 bg="#1a001a", font=("Arial", 22)).pack(pady=(16, 4))

        tk.Label(container,
                 text="Tous les cadeaux sont déballés !",
                 bg="#1a001a", fg=GOLD,
                 font=("Arial", 24, "bold")).pack(pady=4)

        # Final message
        tk.Label(container,
                 text="Bon à l'année prochaine ! 🎀",
                 bg="#1a001a", fg=PINK,
                 font=("Arial", 30, "bold")).pack(pady=(8, 16))

        tk.Label(container,
                 text="Avec tout notre amour 💜✨",
                 bg="#1a001a", fg=WHITE,
                 font=("Arial", 14, "italic")).pack()

        # Final image
        self._load_final_image(container)

        tk.Label(container,
                 text="🌸✨🎀👑🌟💜🌸✨🎀👑🌟💜",
                 bg="#1a001a", font=("Arial", 18)).pack(pady=(16, 8))

    def _load_final_image(self, container):
        try:
            img_path = FINAL_IMAGE_PATH
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # Resize to fit nicely
                img.thumbnail((500, 400), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(container, image=photo,
                               bg="#1a001a",
                               relief="ridge", bd=4,
                               highlightbackground=PURPLE,
                               highlightthickness=4)
                lbl.image = photo  # keep reference
                lbl.pack(pady=12)
            else:
                tk.Label(container,
                         text="📷 Ajoute 'photo_fin.jpg' dans le dossier du jeu !",
                         bg="#1a001a", fg="#aaaaaa",
                         font=("Arial", 11, "italic")).pack(pady=12)
        except Exception as e:
            tk.Label(container,
                     text=f"📷 Image non trouvée : {e}",
                     bg="#1a001a", fg="#aaaaaa",
                     font=("Arial", 10)).pack(pady=8)


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageTk

    root = tk.Tk()
    app = RoulettePrincilia(root)
    root.mainloop()
