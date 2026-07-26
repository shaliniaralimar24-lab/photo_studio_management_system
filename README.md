# Atharva Digital & Photo Studio — Management System

A desktop application built with Python and Tkinter to manage customers, orders, billing, and sample galleries for a photo studio business. Uses MySQL for data storage and ReportLab to generate PDF bills.

## Features

- **Admin Login** — simple username/password gate before accessing the system
- **Dashboard** — quick overview of total customers, total orders, and total revenue
- **Add Customer** — store customer name, phone number, and address (phone validated to exactly 10 digits via a database CHECK constraint)
- **Add Order** — log a new order for a customer with a service selected from a dropdown list and an amount
- **Order History** — view all orders placed
- **Generate Bill** — auto-generate a PDF invoice for a customer, listing all their services and total amount due
- **Sample Gallery** — quick links to view sample photos, videos, and the studio's Instagram reels

## Tech Stack

- **Python 3** — core application logic
- **Tkinter** — GUI
- **MySQL** — database (via `mysql-connector-python`)
- **ReportLab** — PDF bill generation
- **Pillow (PIL)** — image handling for logo/background

## Project Structure

```
├── photo_studio_management.py   # Main application
├── schema.sql                    # Database schema (tables + constraints)
├── requirements.txt               # Python dependencies
├── .env.example                   # Template for environment variables (safe to commit)
├── .gitignore                     # Excludes .env, cache files, generated PDFs
├── logo.png                       # Studio logo (used in app + PDF bills)
├── background2.jpeg               # App background image
├── samples/
│   ├── photos/                    # Sample photo gallery folder
│   └── videos/                    # Sample video gallery folder
└── README.md
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up the database
Make sure MySQL Server is running, then run:
```bash
mysql -u your_mysql_username -p < schema.sql
```
This creates the `testdb` database along with the `customers` and `orders` tables.

> **Note:** MySQL CHECK constraints require **MySQL 8.0.16 or newer**. Run `SELECT VERSION();` in MySQL to confirm.

### 4. Configure environment variables
Copy `.env.example` to a new file named `.env`, then fill in your real values:
```bash
cp .env.example .env
```
```
DB_HOST=127.0.0.1
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_NAME=testdb
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password
```
The `.env` file is listed in `.gitignore` and will never be pushed to GitHub — this keeps your credentials private.

### 5. Run the application
```bash
python photo_studio_management.py
```

### Default Admin Login
Set in your `.env` file. Unless changed, the example values are:
```
Username: admin
Password: 123
```
*(Set your own values in `.env` before deploying anywhere beyond local/personal use.)*

## Roadmap / Possible Improvements

- Move database credentials to environment variables instead of hardcoding
- Add client-side input validation before hitting the database
- Replace the Order History listbox with a sortable table view
- Auto-fill order amount based on selected service
- Hash the admin password instead of storing it in plaintext

## Author

Built by Shalini as part of BCA coursework project.
