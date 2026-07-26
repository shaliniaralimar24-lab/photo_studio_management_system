import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from reportlab.pdfgen import canvas
import os
import webbrowser
from PIL import Image, ImageTk
import sys
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file


def resource_path(relative_path):
    """Get absolute path for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------- DATABASE CONFIG ----------------
# Credentials now come from environment variables (see .env file)
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "testdb")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# ---------------- SERVICES LIST (used for dropdown) ----------------
SERVICES_LIST = [
    "Passport Photo",
    "Studio Photoshoot",
    "Wedding Photography",
    "Wedding Videography",
    "Photo Printing",
    "Photo Framing",
    "ID Card Printing",
    "Video Editing",
    "Album Design"
]


# ---------------- BACKGROUND FUNCTION ----------------
def set_background(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    bg_image = Image.open(resource_path("background2.jpeg"))
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )


# ---------------- LOGIN SCREEN ----------------
def login_screen(root):
    card = tk.Frame(root, bg="#ffffff", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card,
             text="Photo Studio Login",
             font=("Arial", 20, "bold"),
             bg="#ffffff",
             fg="#222").pack(pady=15)

    tk.Label(card,
             text="Username",
             font=("Arial", 12),
             bg="#ffffff").pack(pady=(10, 0))
    user = tk.Entry(card, font=("Arial", 12), width=25, bd=1, relief="solid")
    user.pack(pady=5)

    tk.Label(card,
             text="Password",
             font=("Arial", 12),
             bg="#ffffff").pack(pady=(10, 0))
    pwd = tk.Entry(card, show="*", font=("Arial", 12), width=25, bd=1, relief="solid")
    pwd.pack(pady=5)

    def login():
        if user.get() == ADMIN_USERNAME and pwd.get() == ADMIN_PASSWORD:
            card.destroy()
            main_menu(root)
        else:
            messagebox.showerror("Error", "Invalid login")

    login_btn = tk.Button(card,
                           text="Login",
                           font=("Arial", 12, "bold"),
                           bg="#2c2c2c",
                           fg="white", width=15,
                           command=login)
    login_btn.pack(pady=20)


# ---------------- MAIN MENU ----------------
def main_menu(root):
    # ---- LOAD LOGO ----
    logo_img = Image.open(resource_path("logo.png"))
    logo_img = logo_img.resize((250, 250))  # adjust size if needed
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.place(relx=0.5, rely=0.15, anchor="center")

    frame = tk.Frame(root, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame,
             text="Atharva Digital & Photo Studio",
             font=("Arial", 18, "bold"),
             bg="white").pack(pady=20)

    tk.Button(frame, text="Dashboard", width=25,
              command=lambda: dashboard(root)).pack(pady=5)
    tk.Button(frame, text="Add Customer", width=25,
              command=lambda: add_customer(root)).pack(pady=5)
    tk.Button(frame, text="Add Order", width=25,
              command=lambda: add_order(root)).pack(pady=5)
    tk.Button(frame, text="Order History", width=25,
              command=lambda: order_history(root)).pack(pady=5)
    tk.Button(frame, text="Generate Bill", width=25,
              command=lambda: billing(root)).pack(pady=5)
    tk.Button(frame, text="Sample Gallery", width=25,
              command=lambda: sample_gallery(root)).pack(pady=5)


# ---------------- DASHBOARD ----------------
def dashboard(parent):
    win = tk.Toplevel(parent)
    win.title("Dashboard")
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")
    set_background(win)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM orders")
    revenue = cur.fetchone()[0]
    if revenue is None:
        revenue = 0

    frame = tk.Frame(win, bg="white", padx=100, pady=70)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Studio Dashboard",
             font=("Arial", 16, "bold"), bg="white").pack(pady=10)
    tk.Label(frame, text=f"Total Customers : {customers}", bg="white").pack(pady=5)
    tk.Label(frame, text=f"Total Orders : {orders}", bg="white").pack(pady=5)
    tk.Label(frame, text=f"Total Revenue : ₹{revenue}", bg="white").pack(pady=5)


# ---------------- ADD CUSTOMER ----------------
def add_customer(parent):
    win = tk.Toplevel(parent)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")
    set_background(win)

    frame = tk.Frame(win, bg="white", padx=100, pady=70)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Customer Name", bg="white").pack()
    name = tk.Entry(frame)
    name.pack()

    tk.Label(frame, text="Phone", bg="white").pack()
    phone = tk.Entry(frame)
    phone.pack()

    tk.Label(frame, text="Address", bg="white").pack()
    addr = tk.Entry(frame)
    addr.pack()

    def save():
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO customers(name,phone,address) VALUES(%s,%s,%s)",
                (name.get(), phone.get(), addr.get())
            )
            conn.commit()
            messagebox.showinfo("Success", "Customer Added")
            win.destroy()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror(
                "Invalid Phone Number",
                "Phone number must be exactly 10 digits (numbers only)."
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn is not None and conn.is_connected():
                conn.close()

    tk.Button(frame, text="Save", command=save).pack(pady=10)


# ---------------- ADD ORDER ----------------
def add_order(parent):
    win = tk.Toplevel(parent)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")
    set_background(win)

    frame = tk.Frame(win, bg="white", padx=100, pady=70)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Customer ID", bg="white").pack()
    cid = tk.Entry(frame)
    cid.pack()

    tk.Label(frame, text="Service", bg="white").pack()

    service = ttk.Combobox(frame, values=SERVICES_LIST, state="readonly", width=27)
    service.pack()
    service.current(0)  # default selection

    tk.Label(frame, text="Amount", bg="white").pack()
    amount = tk.Entry(frame)
    amount.pack()

    def save():
        if not service.get():
            messagebox.showerror("Error", "Please select a service")
            return
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders(customer_id,service,amount) VALUES(%s,%s,%s)",
            (cid.get(), service.get(), amount.get())
        )
        conn.commit()
        messagebox.showinfo("Success", "Order Saved")
        win.destroy()

    tk.Button(frame, text="Save Order", command=save).pack(pady=10)


# ---------------- ORDER HISTORY ----------------
def order_history(parent):
    win = tk.Toplevel(parent)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")
    set_background(win)

    listbox = tk.Listbox(win, width=80, height=10)
    listbox.pack(pady=30)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id,customer_id,service,amount FROM orders")
    for row in cur.fetchall():
        text = f"OrderID:{row[0]} | Customer:{row[1]} | {row[2]} | ₹{row[3]}"
        listbox.insert(tk.END, text)


# ---------------- SAMPLE GALLERY ----------------
def sample_gallery(parent):
    win = tk.Toplevel(parent)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")
    set_background(win)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    photo_folder = os.path.join(base_dir, "samples", "photos")
    video_folder = os.path.join(base_dir, "samples", "videos")

    def open_photo():
        if os.path.exists(photo_folder):
            webbrowser.open(photo_folder)
        else:
            messagebox.showerror("Error", "Photo folder not found")

    def open_video():
        if os.path.exists(video_folder):
            webbrowser.open(video_folder)
        else:
            messagebox.showerror("Error", "Video folder not found")

    def open_reel():
        webbrowser.open("https://www.instagram.com/atharva_studio2412")

    tk.Button(win, text="View Photo Samples", width=25, command=open_photo).pack(pady=10)
    tk.Button(win, text="Watch Video Samples", width=25, command=open_video).pack(pady=10)
    tk.Button(win, text="Watch Reels", width=25, command=open_reel).pack(pady=10)


# ---------------- BILLING ----------------
def billing(parent):
    win = tk.Toplevel(parent)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    win.geometry(f"{screen_width}x{screen_height}")
    set_background(win)

    frame = tk.Frame(win, bg="white", padx=100, pady=70)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Customer ID", bg="white").pack()
    cid = tk.Entry(frame)
    cid.pack()

    def generate():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.name,o.service,o.amount
            FROM customers c
            JOIN orders o
            ON c.customer_id=o.customer_id
            WHERE c.customer_id=%s
        """, (cid.get(),))
        rows = cur.fetchall()

        if not rows:
            messagebox.showerror("Error", "No orders")
            return

        name = rows[0][0]
        total = 0
        services = []
        for r in rows:
            services.append((r[1], r[2]))
            total += r[2]

        create_pdf(cid.get(), name, services, total)

    tk.Button(frame, text="Generate PDF Bill", command=generate).pack(pady=10)


# ---------------- PDF BILL ----------------
def create_pdf(cid, name, services, total):
    filename = f"bill_{cid}.pdf"
    c = canvas.Canvas(filename)

    # ---- LOGO ----
    if os.path.exists(resource_path("logo.png")):
        c.drawImage("logo.png", 40, 770, width=60, height=60)

    # ---- STUDIO NAME ----
    c.setFont("Helvetica-Bold", 18)
    c.drawString(120, 800, "Atharva Digital & Photo Studio")

    # ---- CUSTOMER INFO ----
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Customer : {name}")
    # c.drawString(50,730,f"Customer ID : {cid}")

    # ---- TABLE HEADER ----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 690, "Service")
    c.drawString(220, 690, "Amount")

    y = 660
    c.setFont("Helvetica", 12)
    for s, p in services:
        c.drawString(50, y, s)
        c.drawString(220, y, f"Rs. {p}")
        y -= 20

    # ---- TOTAL ----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 20, f"Total : Rs. {total}")

    c.save()
    messagebox.showinfo("Bill Generated", filename)


# ---------------- MAIN ----------------
root = tk.Tk()
root.title("Photo Studio Management")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
set_background(root)
login_screen(root)
root.mainloop()
