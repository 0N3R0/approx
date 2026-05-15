import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

dane_x = []
dane_y = []


def formatuj_wynik(wartosc, niepewnosc, cyfry_znaczace=2):
    if niepewnosc == 0 or math.isnan(niepewnosc):
        return f"{wartosc:.2f}".replace('.', ','), "0,00"
    
    # Obliczenie rzędu wielkości niepewności
    rzad = math.floor(math.log10(abs(niepewnosc)))

    miejsca_po_przecinku = -rzad + (cyfry_znaczace - 1)

    if miejsca_po_przecinku < 0:
        miejsca_po_przecinku = 0
        
    wartosc_zaokraglona = round(wartosc, miejsca_po_przecinku)
    niepewnosc_zaokraglona = round(niepewnosc, miejsca_po_przecinku)
    
    # Budujemy stringa do ilosci miejsc po przecinku
    format_str = f"{{:.{miejsca_po_przecinku}f}}"
    
    w_str = format_str.format(wartosc_zaokraglona).replace('.', ',')
    n_str = format_str.format(niepewnosc_zaokraglona).replace('.', ',')
    
    return w_str, n_str

def dodaj_punkt():
    try:
        tekst_x = pole_x.get().replace(',', '.')
        tekst_y = pole_y.get().replace(',', '.')
        
        wartosc_x = float(tekst_x)
        wartosc_y = float(tekst_y)
        
        dane_x.append(wartosc_x)
        dane_y.append(wartosc_y)

        pole_x.delete(0, tk.END)
        pole_y.delete(0, tk.END)
        
        aktualizuj_wykres()
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadzono niepoprawne dane. Użyj cyfr (np. 2,5).")

def wyczysc_dane():
    dane_x.clear()
    dane_y.clear()
    aktualizuj_wykres()

def aktualizuj_wykres():
    wykres.clear()
    wykres.grid(True, linestyle='--', alpha=0.6)
    
    wykres.set_title('Aproksymacja danych pomiarowych')
    wykres.set_xlabel('Oś X (np. Czas t [s])')
    wykres.set_ylabel('Oś Y (np. Napięcie U [V])')

    if dane_x:
        wykres.scatter(dane_x, dane_y, color='red', zorder=5, label='Punkty pomiarowe')

    # Do aproksymacji liniowej używamy metody najmniejszych kwadratów
    n = len(dane_x)
    if n >= 2:
        suma_x = sum(dane_x)
        suma_y = sum(dane_y)
        suma_xx = sum(x**2 for x in dane_x)
        suma_xy = sum(dane_x[i] * dane_y[i] for i in range(n))

        mianownik = n * suma_xx - suma_x**2
        
        if mianownik != 0:
            a = (n * suma_xy - suma_x * suma_y) / mianownik
            b = (suma_xx * suma_y - suma_x * suma_xy) / mianownik

            # Obliczamy niepewności u(a) oraz u(b) i od razu poprawnie je formatujemy
            if n > 2:
                suma_resztek = sum((dane_y[i] - (a * dane_x[i] + b))**2 for i in range(n))
                s_e = (suma_resztek / (n - 2)) ** 0.5
                
                niepewnosc_a = s_e * (n / mianownik) ** 0.5
                niepewnosc_b = s_e * (suma_xx / mianownik) ** 0.5

                a_str, niepewnosc_a_str = formatuj_wynik(a, niepewnosc_a)
                b_str, niepewnosc_b_str = formatuj_wynik(b, niepewnosc_b)
            else:
                a_str = f"{a:.4g}".replace('.', ',')
                b_str = f"{b:.4g}".replace('.', ',')
                niepewnosc_a_str = "brak (min. 3 pkt)"
                niepewnosc_b_str = "brak (min. 3 pkt)"

            # Rysujemy prostą z marginesem
            x_min = min(dane_x)
            x_max = max(dane_x)
            margines_x = (x_max - x_min) * 0.05 if x_max != x_min else 1.0
            
            x_linia = [x_min - margines_x, x_max + margines_x]
            y_linia = [a * (x_min - margines_x) + b, a * (x_max + margines_x) + b]
            
            opis_legendy = (f'Prosta: y = Ax + B\n'
                            f'A = {a_str} ± {niepewnosc_a_str}\n'
                            f'B = {b_str} ± {niepewnosc_b_str}')
            
            wykres.plot(x_linia, y_linia, color='forestgreen', linewidth=2, label=opis_legendy)
            wykres.legend(loc='upper left')
        else:
            messagebox.showwarning("Błąd matematyczny", "Punkty ułożone idealnie w pionie. Brak możliwości wyliczenia.")

    plotno.draw()

# Konfiguracja dla interfejsu graficznego
okno = tk.Tk()
okno.title("Aproksymacja Liniowa")

panel = tk.Frame(okno, padx=15, pady=15)
panel.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(panel, text="Wartość X:").pack()
pole_x = tk.Entry(panel)
pole_x.pack(pady=5)

tk.Label(panel, text="Wartość Y:").pack()
pole_y = tk.Entry(panel)
pole_y.pack(pady=5)

tk.Button(panel, text="Dodaj punkt", command=dodaj_punkt).pack(fill=tk.X, pady=5)
tk.Button(panel, text="Wyczyść dane", command=wyczysc_dane).pack(fill=tk.X, pady=15)

figura = Figure(figsize=(8, 6), dpi=100)
wykres = figura.add_subplot(111)
plotno = FigureCanvasTkAgg(figura, master=okno)
plotno.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

aktualizuj_wykres()

okno.mainloop()