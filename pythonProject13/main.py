import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#liman,sefer, kaptan ve mürettebat için  ulkeler tanımadık. kutu içersinde bu kıta/ulkelerden biri secilecek.
kita_ulke = {
    "Asya": ["Çin", "Hindistan", "Japonya", "Güney Kore"],
    "Avrupa": ["Türkiye", "Almanya", "Fransa", "İngiltere", "İtalya", "İspanya"],
    "Afrika": ["Nijerya", "Mısır", "Demokratik Kongo Cumhuriyeti", "Güney Afrika", "Etiyopya"],
    "Kuzey Amerika": ["ABD", "Kanada", "Meksika", "Küba", "Jamaika"],
    "Güney Amerika": ["Brezilya", "Arjantin", "Kolombiya", "Şili", "Peru"],
    "Avustralya": ["Avustralya", "Yeni Zelanda", "Papua Yeni Gine", "Fiji", "Samoa"]
}

# Konteyner gemileri için veritabanı dosyası
conn_container = sqlite3.connect('container_ships.db')
c_container = conn_container.cursor()

# Yolcu gemileri için veritabanı dosyası
conn_passenger = sqlite3.connect('passenger_ships.db')
c_passenger = conn_passenger.cursor()

# Petrol tankerleri için veritabanı dosyası
conn_tanker = sqlite3.connect('tanker_ships.db')
c_tanker = conn_tanker.cursor()

# Konteyner gemisi için tablo oluşturma ve bilgileri ekleme
c_container.execute('''CREATE TABLE IF NOT EXISTS container_ships
                     (ship_type TEXT, serial_number TEXT, ship_name TEXT, weight REAL, model TEXT, max_container_count INTEGER, max_weight_capacity REAL)''')

# Yolcu gemisi için tablo oluşturma ve bilgileri ekleme
c_passenger.execute('''CREATE TABLE IF NOT EXISTS passenger_ships
                     (ship_type TEXT, serial_number TEXT, ship_name TEXT, weight REAL, model TEXT, max_passenger_count INTEGER)''')

# Petrol tankeri için tablo oluşturma ve bilgileri ekleme
c_tanker.execute('''CREATE TABLE IF NOT EXISTS tanker_ships
                     (ship_type TEXT, serial_number TEXT, ship_name TEXT, weight REAL, model TEXT, max_petrol_capacity INTEGER)''')


def kitalar_kombo_guncelle(combo):
    # Combobxı güncelle, kıtaları ekle
    combo["values"] = tuple(kita_ulke.keys())

def ulkeler_kombo_guncelle(combo, kita):
    # Seçilen kıtaya göreulkleri güncelle
    secili_kita_ulkeler = kita_ulke.get(kita, [])
    combo["values"] = tuple(secili_kita_ulkeler)

#primary key yani ayırt edici olarak gemi id si kullandık

#Seri numarasına göre yolcu gemisini silecek fonksiyon
def delete_passenger_ship():
    serial_number = serial_number_entry.get()
    conn = sqlite3.connect('passenger_ships.db')
    c = conn.cursor()
    c.execute("DELETE FROM ships WHERE serial_number=?", (serial_number,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Yolcu gemisi bilgileri başarıyla silindi.")


#Seri numarasına göre tanker gemisini silecek fonksiyon
def delete_tanker_ship():
    serial_number = serial_number_entry.get()
    conn = sqlite3.connect('tanker_ships.db')
    c = conn.cursor()
    c.execute("DELETE FROM ships WHERE serial_number=?", (serial_number,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Petrol tankeri bilgileri başarıyla silindi.")

def submit_ship():
    ship_type = notebook.tab(notebook.select(), "text")

    if ship_type == "Konteyner Gemisi":
        db_file = 'container_ships.db'
        serial_number = serial_number_entry.get()
        ship_name = ship_name_entry.get()
        weight = weight_entry.get()
        model = model_entry.get()
        max_container_count = max_container_count_entry.get()
        max_weight_capacity = max_weight_capacity_entry.get()

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS ships
                     (ship_type TEXT, serial_number TEXT, ship_name TEXT, weight REAL, model TEXT, max_container_count INTEGER, max_weight_capacity REAL)''')

        c.execute("INSERT INTO ships VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (ship_type, serial_number, ship_name, weight, model, max_container_count, max_weight_capacity))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Konteyner gemisi bilgileri başarıyla kaydedildi.")
    elif ship_type == "Yolcu Gemisi":
        db_file = 'yolcu.db'
        serial_number = serial_number_entry.get()
        ship_name = ship_name_entry.get()
        weight = weight_entry.get()
        model = model_entry.get()
        max_passenger_count = max_passenger_count_entry.get()

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS ships
                     (ship_type TEXT, serial_number TEXT, ship_name TEXT, weight REAL, model TEXT, max_passenger_count INTEGER)''')

        c.execute("INSERT INTO ships VALUES (?, ?, ?, ?, ?, ?)",
                  (ship_type, serial_number, ship_name, weight, model, max_passenger_count))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Yolcu gemisi bilgileri başarıyla kaydedildi.")
    elif ship_type == "Petrol Tankeri":
        db_file = 'tanker_ships.db'
        serial_number = serial_number_entry.get()
        ship_name = ship_name_entry.get()
        weight = weight_entry.get()
        model = model_entry.get()
        max_petrol_capacity = max_petrol_capacity_entry.get()

        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS ships
                     (ship_type TEXT, serial_number TEXT, ship_name TEXT, weight REAL, model TEXT, max_petrol_capacity INTEGER)''')

        c.execute("INSERT INTO ships VALUES (?, ?, ?, ?, ?, ?)",
                  (ship_type, serial_number, ship_name, weight, model, max_petrol_capacity))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Petrol tankeri bilgileri başarıyla kaydedildi.")


def submit_port():
    db_file = 'liman.db'

    # Liman adını kontrol etmek için
    port_name = port_name_entry.get()
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM ports WHERE port_name=?", (port_name,))
    existing_port = c.fetchone()
    conn.close()

    # Daha önce uğranmış mı kontrolü
    if existing_port:
        response = messagebox.askyesno("Uyarı", "Bu limana daha önce uğrulmuş. Yine de devam etmek istiyor musunuz?")
        if not response:
            return

    country = ulkeler_combo.get()
    population = population_entry.get()
    passport_required = passport_var.get()  # Radyo düğmesinin değeri
    docking_fee = docking_fee_entry.get()

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS ports
                 (port_name TEXT, country TEXT, population INTEGER, passport_required TEXT, docking_fee REAL)''')

    c.execute("INSERT INTO ports VALUES (?, ?, ?, ?, ?)",
              (port_name, country, population, passport_required, docking_fee))

    conn.commit()
    conn.close()

    messagebox.showinfo("Başarılı", "Liman bilgileri başarıyla kaydedildi.")

def submit_captain():
    db_file = 'kaptan.db'

    captain_id = captain_id_entry.get()
    name_surname = name_surname_entry.get()
    address = address_entry.get()
    country = ulkeler_combo.get()
    birth_date = birth_date_entry.get()
    employment_date = employment_date_entry.get()
    license = license_entry.get()

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS captains
                 (captain_id INTEGER, name_surname TEXT, address TEXT, country TEXT, birth_date TEXT, employment_date TEXT, license TEXT)''')

    c.execute("INSERT INTO captains VALUES (?, ?, ?, ?, ?, ?, ?)",
              (captain_id, name_surname, address, country, birth_date, employment_date, license))

    conn.commit()
    conn.close()

    messagebox.showinfo("Başarılı", "Kaptan bilgileri başarıyla kaydedildi.")

def submit_crew():
    db_file = 'mürettebat.db'

    crew_id = crew_id_entry.get()
    name_surname = name_surname_entry.get()
    address = address_entry.get()
    country = ulkeler_combo_crew.get()
    birth_date = birth_date_entry.get()
    employment_date = employment_date_entry.get()
    task = task_combo.get()

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS crew
                 (crew_id INTEGER, name_surname TEXT, address TEXT, country TEXT, birth_date TEXT, employment_date TEXT, task TEXT)''')

    c.execute("INSERT INTO crew VALUES (?, ?, ?, ?, ?, ?, ?)",
              (crew_id, name_surname, address, country, birth_date, employment_date, task))

    conn.commit()
    conn.close()

    messagebox.showinfo("Başarılı", "Mürettebat bilgileri başarıyla kaydedildi.")

def submit_voyage():
    voyage_id = voyage_id_entry.get()
    departure_date = departure_date_entry.get()
    return_date = return_date_entry.get()
    departure_port = departure_port_entry.get()

    conn = sqlite3.connect('voyages.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS voyages
                 (voyage_id INTEGER, departure_date TEXT, return_date TEXT, departure_port TEXT)''')

    c.execute("INSERT INTO voyages VALUES (?, ?, ?, ?)",
              (voyage_id, departure_date, return_date, departure_port))

    conn.commit()
    conn.close()

    messagebox.showinfo("Başarılı", "Sefer kaydı başarıyla kaydedildi.")
def delete_ship():
    serial_number = serial_number_entry.get()
    conn = sqlite3.connect('ships.db')
    c = conn.cursor()
    c.execute("DELETE FROM ships WHERE serial_number=?", (serial_number,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Gemi bilgileri başarıyla silindi.")

db_file = 'veritabani.db'

def delete_captain():
    captain_id = captain_id_entry.get()
    conn = sqlite3.connect('kaptan.db')
    c = conn.cursor()
    c.execute("DELETE FROM captains WHERE captain_id=?", (captain_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Kaptan bilgileri başarıyla silindi.")
#HATA ALIYORUM SEFER VE GEMİ KOTROLU
"""""
def sefere_gemi_cikar(gemi_id):
    # Eğer belirtilen gemi zaten bir seferdeyse, çıkış yapma
    cursor.execute("SELECT seferde_mi FROM Gemi WHERE ID = ?", (gemi_id,))
    seferde_mi = cursor.fetchone()[0]
    if seferde_mi:
        print("Bu gemi zaten bir seferde!")
        return False
    else:
        # Diğer gemilerin seferde olup olmadığını kontrol et
        cursor.execute("SELECT ID FROM Gemi WHERE seferde_mi = 1")
        seferdeki_gemiler = cursor.fetchall()
        if seferdeki_gemiler:
            print("Başka bir gemi zaten seferde!")
            return False
        else:
            # Gemiyi sefere çıkar
            cursor.execute("UPDATE Gemi SET seferde_mi = 1 WHERE ID = ?", (gemi_id,))
            conn.commit()
            print("Gemi başarıyla sefere çıkarıldı!")
            return True
"""""
"""""
def gemi_kontrol(gemi_id):
    cursor.execute("SELECT kaptan_sayisi, murettebat_sayisi FROM Gemi WHERE ID = ?", (gemi_id,))
    kaptan_sayisi, murettebat_sayisi = cursor.fetchone()
    if kaptan_sayisi >= 2 and murettebat_sayisi >= 1:
        print("Gemi hazır!")
        return True
    else:
        print("Gemi yeterli kaptan ve mürettebatı içermiyor!")
        return False
"""

def show_port_ships():
    def get_port_ships():
        port_id = port_id_entry.get()
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT ship_name FROM ships WHERE port_id=?", (port_id,))
        ships = c.fetchall()
        conn.close()
        return ships

    port_ships_window = tk.Toplevel(root)
    port_ships_window.title("Liman Gemileri")

    port_id_label = tk.Label(port_ships_window, text="Liman ID:")
    port_id_label.grid(row=0, column=0, padx=10, pady=5)

    port_id_entry = tk.Entry(port_ships_window)
    port_id_entry.grid(row=0, column=1, padx=10, pady=5)

    show_button = tk.Button(port_ships_window, text="Göster", command=lambda: show_ships(get_port_ships()))
    show_button.grid(row=0, column=2, padx=10, pady=5)

    ships_listbox = tk.Listbox(port_ships_window)
    ships_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

    def show_ships(ships):
        ships_listbox.delete(0, tk.END)
        if ships:
            for ship in ships:
                ships_listbox.insert(tk.END, ship[0])
        else:
            ships_listbox.insert(tk.END, "Bu limanda gemi bulunmamaktadır.")
def delete_crew():
    crew_id = crew_id_entry.get()
    conn = sqlite3.connect('ships.db')
    c = conn.cursor()
    c.execute("DELETE FROM crew WHERE crew_id=?", (crew_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Mürettebat bilgileri başarıyla silindi.")
root = tk.Tk()
root.title("Gemi ve Liman Bilgileri Formu")
root.geometry("400x400")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

# Konteyner Gemisi Sekmesi
container_frame = ttk.Frame(notebook)
notebook.add(container_frame, text="Konteyner Gemisi")

#query_tab = ttk.Frame(root)
#query_tab.grid(row=0, column=1, padx=10, pady=10)

#query_button = tk.Button(query_tab, text="Liman Gemilerini Göster", command=show_port_ships)
#query_button.grid(row=0, column=0, padx=10, pady=5)

# Konteyner gemisi için giriş alanları
serial_number_label = ttk.Label(container_frame, text="Seri Numarası:")
serial_number_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
serial_number_entry = ttk.Entry(container_frame)
serial_number_entry.grid(row=0, column=1, padx=5, pady=5)

ship_name_label = ttk.Label(container_frame, text="Gemi Adı:")
ship_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
ship_name_entry = ttk.Entry(container_frame)
ship_name_entry.grid(row=1, column=1, padx=5, pady=5)

weight_label = ttk.Label(container_frame, text="Ağırlık:")
weight_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
weight_entry = ttk.Entry(container_frame)
weight_entry.grid(row=2, column=1, padx=5, pady=5)

model_label = ttk.Label(container_frame, text="Model:")
model_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
model_entry = ttk.Entry(container_frame)
model_entry.grid(row=3, column=1, padx=5, pady=5)

max_container_count_label = ttk.Label(container_frame, text="Maks. Konteyner Sayısı:")
max_container_count_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
max_container_count_entry = ttk.Entry(container_frame)
max_container_count_entry.grid(row=4, column=1, padx=5, pady=5)

max_weight_capacity_label = ttk.Label(container_frame, text="Maks. Ağırlık Kapasitesi:")
max_weight_capacity_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
max_weight_capacity_entry = ttk.Entry(container_frame)
max_weight_capacity_entry.grid(row=5, column=1, padx=5, pady=5)

container_submit_button = ttk.Button(container_frame, text="Gemi Bilgilerini Kaydet", command=submit_ship)
container_submit_button.grid(row=6, columnspan=2, pady=5)
delete_ship_button = ttk.Button(container_frame, text="Gemiyi sil", command=delete_ship)
delete_ship_button.grid(row=7, columnspan=2, pady=5)

# Yolcu Gemisi Sekmesi
passenger_frame = ttk.Frame(notebook)
notebook.add(passenger_frame, text="Yolcu Gemisi")

# Yolcu gemisi için giriş alanları
serial_number_label = ttk.Label(passenger_frame, text="Seri Numarası:")
serial_number_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
serial_number_entry = ttk.Entry(passenger_frame)
serial_number_entry.grid(row=0, column=1, padx=5, pady=5)

ship_name_label = ttk.Label(passenger_frame, text="Gemi Adı:")
ship_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
ship_name_entry = ttk.Entry(passenger_frame)
ship_name_entry.grid(row=1, column=1, padx=5, pady=5)

weight_label = ttk.Label(passenger_frame, text="Ağırlık:")
weight_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
weight_entry = ttk.Entry(passenger_frame)
weight_entry.grid(row=2, column=1, padx=5, pady=5)

model_label = ttk.Label(passenger_frame, text="Model:")
model_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
model_entry = ttk.Entry(passenger_frame)
model_entry.grid(row=3, column=1, padx=5, pady=5)

max_passenger_count_label = ttk.Label(passenger_frame, text="Maks. Yolcu Sayısı:")
max_passenger_count_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
max_passenger_count_entry = ttk.Entry(passenger_frame)
max_passenger_count_entry.grid(row=4, column=1, padx=5, pady=5)

passenger_submit_button = ttk.Button(passenger_frame, text="Gemi Bilgilerini Kaydet", command=submit_ship)
passenger_submit_button.grid(row=5, columnspan=2, pady=5)
delete_passenger_ship_button = ttk.Button(passenger_frame, text="Veri Sil", command=delete_passenger_ship)
delete_passenger_ship_button.grid(row=7, columnspan=2, pady=5)

# Petrol Tankeri Sekmesini oluştur
tanker_frame = ttk.Frame(notebook)
notebook.add(tanker_frame, text="Petrol Tankeri")

# Petrol tankeri için giriş alanları
serial_number_label = ttk.Label(tanker_frame, text="Seri Numarası:")
serial_number_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
serial_number_entry = ttk.Entry(tanker_frame)
serial_number_entry.grid(row=0, column=1, padx=5, pady=5)

ship_name_label = ttk.Label(tanker_frame, text="Gemi Adı:")
ship_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
ship_name_entry = ttk.Entry(tanker_frame)
ship_name_entry.grid(row=1, column=1, padx=5, pady=5)

weight_label = ttk.Label(tanker_frame, text="Ağırlık:")
weight_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
weight_entry = ttk.Entry(tanker_frame)
weight_entry.grid(row=2, column=1, padx=5, pady=5)

model_label = ttk.Label(tanker_frame, text="Model:")
model_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
model_entry = ttk.Entry(tanker_frame)
model_entry.grid(row=3, column=1, padx=5, pady=5)

max_petrol_capacity_label = ttk.Label(tanker_frame, text="Maks. Petrol Kapasitesi:")
max_petrol_capacity_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
max_petrol_capacity_entry = ttk.Entry(tanker_frame)
max_petrol_capacity_entry.grid(row=4, column=1, padx=5, pady=5)

tanker_submit_button = ttk.Button(tanker_frame, text="Gemi Bilgilerini Kaydet", command=submit_ship)
tanker_submit_button.grid(row=5, columnspan=2, pady=5)
delete_tanker_ship_button = ttk.Button(tanker_frame, text="Gemiyi sil", command=delete_tanker_ship)
delete_tanker_ship_button.grid(row=7, columnspan=2, pady=5)

# Liman Bilgileri Sekmesi
port_frame = ttk.Frame(notebook)
notebook.add(port_frame, text="Liman Bilgileri")

# Liman bilgileri için giriş alanları
port_name_label = ttk.Label(port_frame, text="Liman Adı:")
port_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
port_name_entry = ttk.Entry(port_frame)
port_name_entry.grid(row=0, column=1, padx=5, pady=5)

kita_label = ttk.Label(port_frame, text="Kıta:")
kita_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
kita_combo = ttk.Combobox(port_frame, values=list(kita_ulke.keys()), state="readonly")
kita_combo.grid(row=1, column=1, padx=5, pady=5)
kita_combo.bind("<<ComboboxSelected>>", lambda event: ulkeler_kombo_guncelle(ulkeler_combo, kita_combo.get()))

ulkeler_label = ttk.Label(port_frame, text="Ülke:")
ulkeler_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
ulkeler_combo = ttk.Combobox(port_frame, state="readonly")
ulkeler_combo.grid(row=2, column=1, padx=5, pady=5)

population_label = ttk.Label(port_frame, text="Nüfus:")
population_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
population_entry = ttk.Entry(port_frame)
population_entry.grid(row=3, column=1, padx=5, pady=5)

passport_label = ttk.Label(port_frame, text="Pasaport Gerekli mi?")
passport_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
passport_var = tk.StringVar()
passport_yes_radio = ttk.Radiobutton(port_frame, text="Evet", variable=passport_var, value="Evet")
passport_yes_radio.grid(row=4, column=1, padx=5, pady=5)
passport_no_radio = ttk.Radiobutton(port_frame, text="Hayır", variable=passport_var, value="Hayır")
passport_no_radio.grid(row=4, column=2, padx=5, pady=5)

docking_fee_label = ttk.Label(port_frame, text="İskele Ücreti:")
docking_fee_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
docking_fee_entry = ttk.Entry(port_frame)
docking_fee_entry.grid(row=5, column=1, padx=5, pady=5)

port_submit_button = ttk.Button(port_frame, text="Liman Bilgilerini Kaydet", command=submit_port)
port_submit_button.grid(row=6, columnspan=2, pady=5)

""" " 
delete_tanker_ship_button = ttk.Button(tanker_frame, text="Limanı sil", command=delete_tanker_ship)
delete_tanker_ship_button.grid(row=7, columnspan=2, pady=5)
"""

#Liman silme sekmesini çalıştıramadım


# Kaptan Sekmesi
captain_frame = ttk.Frame(notebook)
notebook.add(captain_frame, text="Kaptan")

# Kaptan bilgileri için giriş alanları
captain_id_label = ttk.Label(captain_frame, text="Kaptan ID:")
captain_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
captain_id_entry = ttk.Entry(captain_frame)
captain_id_entry.grid(row=0, column=1, padx=5, pady=5)

name_surname_label = ttk.Label(captain_frame, text="Ad Soyad:")
name_surname_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
name_surname_entry = ttk.Entry(captain_frame)
name_surname_entry.grid(row=1, column=1, padx=5, pady=5)

address_label = ttk.Label(captain_frame, text="Adres:")
address_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
address_entry = ttk.Entry(captain_frame)
address_entry.grid(row=2, column=1, padx=5, pady=5)

kita_label_captain = ttk.Label(captain_frame, text="Kıta:")
kita_label_captain.grid(row=3, column=0, padx=5, pady=5, sticky="e")
kita_combo_captain = ttk.Combobox(captain_frame, values=list(kita_ulke.keys()), state="readonly")
kita_combo_captain.grid(row=3, column=1, padx=5, pady=5)
kita_combo_captain.bind("<<ComboboxSelected>>", lambda event: ulkeler_kombo_guncelle(ulkeler_combo_captain, kita_combo_captain.get()))

ulkeler_label_captain = ttk.Label(captain_frame, text="Uyruk:")
ulkeler_label_captain.grid(row=4, column=0, padx=5, pady=5, sticky="e")
ulkeler_combo_captain = ttk.Combobox(captain_frame, state="readonly")
ulkeler_combo_captain.grid(row=4, column=1, padx=5, pady=5)

birth_date_label = ttk.Label(captain_frame, text="Doğum Tarihi:")
birth_date_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
birth_date_entry = ttk.Entry(captain_frame)
birth_date_entry.grid(row=5, column=1, padx=5, pady=5)

employment_date_label = ttk.Label(captain_frame, text="İşe Giriş Tarihi:")
employment_date_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
employment_date_entry = ttk.Entry(captain_frame)
employment_date_entry.grid(row=6, column=1, padx=5, pady=5)

task_label = ttk.Label(captain_frame, text="Lisans")
task_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
task_combo = ttk.Combobox(captain_frame, values=["1.Kaptan", "2.Kaptan", "3.Kaptan"], state="readonly")
task_combo.grid(row=7, column=1, padx=5, pady=5)
license_entry = ttk.Entry(captain_frame)
#license_entry.grid(row=7, column=1, padx=5, pady=5)

captain_submit_button = ttk.Button(captain_frame, text="Kaptan Bilgilerini Kaydet", command=submit_captain)
captain_submit_button.grid(row=8, columnspan=2, pady=5)

delete_captain_button = ttk.Button(captain_frame, text="Kaptan'ı sil ", command=delete_captain)
delete_captain_button.grid(row=9, columnspan=2, pady=5)


# Mürettebat Sekmesi
crew_frame = ttk.Frame(notebook)
notebook.add(crew_frame, text="Mürettebat")

# Mürettebat bilgileri için giriş alanları
crew_id_label = ttk.Label(crew_frame, text="ID:")
crew_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
crew_id_entry = ttk.Entry(crew_frame)
crew_id_entry.grid(row=0, column=1, padx=5, pady=5)

name_surname_label = ttk.Label(crew_frame, text="Ad Soyad:")
name_surname_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
name_surname_entry = ttk.Entry(crew_frame)
name_surname_entry.grid(row=1, column=1, padx=5, pady=5)

address_label = ttk.Label(crew_frame, text="Adres:")
address_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
address_entry = ttk.Entry(crew_frame)
address_entry.grid(row=2, column=1, padx=5, pady=5)

kita_label_crew = ttk.Label(crew_frame, text="Kıta:")
kita_label_crew.grid(row=3, column=0, padx=5, pady=5, sticky="e")
kita_combo_crew = ttk.Combobox(crew_frame, values=list(kita_ulke.keys()), state="readonly")
kita_combo_crew.grid(row=3, column=1, padx=5, pady=5)
kita_combo_crew.bind("<<ComboboxSelected>>", lambda event: ulkeler_kombo_guncelle(ulkeler_combo_crew, kita_combo_crew.get()))

ulkeler_label_crew = ttk.Label(crew_frame, text="Uyruk:")
ulkeler_label_crew.grid(row=4, column=0, padx=5, pady=5, sticky="e")
ulkeler_combo_crew = ttk.Combobox(crew_frame, state="readonly")
ulkeler_combo_crew.grid(row=4, column=1, padx=5, pady=5)

birth_date_label = ttk.Label(crew_frame, text="Doğum Tarihi:")
birth_date_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
birth_date_entry = ttk.Entry(crew_frame)
birth_date_entry.grid(row=5, column=1, padx=5, pady=5)

employment_date_label = ttk.Label(crew_frame, text="İşe Giriş Tarihi:")
employment_date_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
employment_date_entry = ttk.Entry(crew_frame)
employment_date_entry.grid(row=6, column=1, padx=5, pady=5)

task_label = ttk.Label(crew_frame, text="Görev:")
task_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
task_combo = ttk.Combobox(crew_frame, values=["BAŞ MAKİNİST", "ELEKTRİKÇİ", "GÜVERTE REİSİ", "YAĞCI", "AŞÇI", "KAMAROT"], state="readonly")
task_combo.grid(row=7, column=1, padx=5, pady=5)

crew_submit_button = ttk.Button(crew_frame, text="Mürettebat Bilgilerini Kaydet", command=submit_crew)
crew_submit_button.grid(row=8, columnspan=2, pady=5)
delete_crew_button = ttk.Button(crew_frame, text="Mürettebar görevlisini sil", command=delete_crew)
delete_crew_button.grid(row=9, columnspan=2, pady=5)

# Sefer Kayıtları Sekmesi oluşturuyorz
voyage_frame = ttk.Frame(notebook)
notebook.add(voyage_frame, text="Sefer Kayıtları")

# Sefer kayıtları için giriş alanlarının kodları
voyage_id_label = ttk.Label(voyage_frame, text="ID:")
voyage_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
voyage_id_entry = ttk.Entry(voyage_frame)
voyage_id_entry.grid(row=0, column=1, padx=5, pady=5)

departure_date_label = ttk.Label(voyage_frame, text="Yola Çıkış Tarihi:")
departure_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
departure_date_entry = ttk.Entry(voyage_frame)
departure_date_entry.grid(row=1, column=1, padx=5, pady=5)

return_date_label = ttk.Label(voyage_frame, text="Dönüş Tarihi:")
return_date_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
return_date_entry = ttk.Entry(voyage_frame)
return_date_entry.grid(row=2, column=1, padx=5, pady=5)

departure_port_label = ttk.Label(voyage_frame, text="Yola Çıkış Limanı:")
departure_port_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
departure_port_entry = ttk.Entry(voyage_frame)
departure_port_entry.grid(row=3, column=1, padx=5, pady=5)

voyage_submit_button = ttk.Button(voyage_frame, text="Sefer Kaydını Kaydet", command=submit_voyage)
voyage_submit_button.grid(row=4, columnspan=2, pady=5)
root.mainloop()



#Gemiler diye ana bir sınıf oluşturup diğer gemi çeşitlerini bu main sınıfı baz alarak ekstra özelliklerini ekleyerek oluşturdk

class Gemiler:
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili):
        self.seri_no = seri_no
        self.gemi_ismi = gemi_ismi
        self.agirlik = agirlik
        self.model_yili = model_yili

class YolcuGemisi(Gemiler):
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili, max_yolcu_sayisi):
        super().__init__(seri_no, gemi_ismi, agirlik, model_yili)
#super(), Python da kalıtım  kullanırken bir üst sınıfın özelliklerine ve metodlarına erişmek için kullanılır
        self.max_yolcu_sayisi = max_yolcu_sayisi

class PetrolTankeri(Gemiler):
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili, max_petrol_kapasitesi):
        super().__init__(seri_no, gemi_ismi, agirlik, model_yili)
#self ile de sınıfın kendi özelliğini belirledik.
        self.max_petrol_kapasitesi = max_petrol_kapasitesi

class KonteynerGemisi(Gemiler):
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili, konteyner_sayisi, max_tonaj):
        super().__init__(seri_no, gemi_ismi, agirlik, model_yili)
        self.konteyner_sayisi = konteyner_sayisi
        self.max_tonaj = max_tonaj

#Aynı metodu (kalıtım) kullanarak bu sefer Kaptan ve mürettebat sınıflarını içeren Görevliler sınıfı oluşturuyoruz.
#hem kaptana hem mürettabata özgü özellikler oldugundan ortak ozellikleri GÖREVLİLER sınıfında toplayıp kaptan ve murettebatı ayırdık.

class Gorevliler:
    def __init__(self, ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi):
        self.ID = ID
        self.ad_soyad = ad_soyad
        self.adres = adres
        self.uyruk = uyruk
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi

class Kaptan(Gorevliler):
    def __init__(self, ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi, lisans):
        super().__init__(ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi)
        self.lisans = lisans

class MUrettebat(Gorevliler):
    def __init__(self, ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi, gorev):
        super().__init__(ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi)
        self.gorev = gorev

class Sefer:
    def __init__(self, gemi_id, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, diger_limanlar):
        self.gemi_id = gemi_id
        self.yola_cikis_tarihi = yola_cikis_tarihi
        self.donus_tarihi = donus_tarihi
        self.yola_cikis_limani = yola_cikis_limani
        self.diger_limanlar = diger_limanlar  # Birden fazla liman olabileceginden liste olarak tutucaz

class SeferlerYonetimi:
    def __init__(self):
        self.gecmis_seferler = []  # Geçmiş seferler listesi
        self.gelecek_seferler = []  # Gelecek seferler listesi
        self.olasi_seferler = []  # Olası seferler listesi

    def sefer_ekle(self, sefer_tipi, sefer):
        if sefer_tipi == "gecmis":
            self.gecmis_seferler.append(sefer)
        elif sefer_tipi == "gelecek":
            self.gelecek_seferler.append(sefer)
        elif sefer_tipi == "olasi":
            self.olasi_seferler.append(sefer)

class Limanlar:
    def __init__(self, liman_ad, ulke, nufus, pasaport_gerekli_mi, demirleme_ucreti):
        self.liman_ad = liman_ad
        self.ulke = ulke
        self.nufus = nufus
        self.pasaport_gerekli_mi = pasaport_gerekli_mi
        self.demirleme_ucreti = demirleme_ucreti
#Limanın adı ve ulkesi liman için ayırt edici olacaktır koşulunu saglamak için
        self.tanimlayici = f"{liman_ad}-{ulke}"
