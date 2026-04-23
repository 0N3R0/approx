import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dane_x = []
dane_y = []

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
    wykres.set_xlabel('Oś X')
    wykres.set_ylabel('Oś Y')

    if dane_x:
        wykres.scatter(dane_x, dane_y, color='red', zorder=5, label='Punkty pomiarowe')

    # Do aproksymacji liniowej wykorzystujemy metodę najmniejszych kwadratów
    # Wyliczanie współczynników 'a' i 'b' dla prostej y = ax + b

    n = len(dane_x)
    if n >= 2:
        # Wyliczanie wszystkich sum potrzebnych do wzoru
        suma_x = sum(dane_x)
        suma_y = sum(dane_y)
        suma_xx = sum(x**2 for x in dane_x)
        suma_xy = sum(dane_x[i] * dane_y[i] for i in range(n))

        # Mianownik ze wzoru
        mianownik = n * suma_xx - suma_x**2
        
        if mianownik != 0:
            # Wyliczenie docelowych parametrów aproksymacji
            a = (n * suma_xy - suma_x * suma_y) / mianownik
            b = (suma_xx * suma_y - suma_x * suma_xy) / mianownik

            x_min = min(dane_x)
            x_max = max(dane_x)
            
            x_linia = [x_min, x_max]
            y_linia = [a * x_min + b, a * x_max + b]
            
            a_str = f"{a:.2f}".replace('.', ',')
            b_str = f"{b:.2f}".replace('.', ',')
            rownanie = f'Aproksymacja: y = {a_str}x + {b_str}'
            
            wykres.plot(x_linia, y_linia, color='forestgreen', linewidth=2, label=rownanie)
            wykres.legend(loc='upper left')
        else:
            messagebox.showwarning("Błąd matematyczny", "Punkty ułożone w pionie. Brak możliwości wyliczenia.")

    plotno.draw()

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

figura = Figure(figsize=(7, 5), dpi=100)
wykres = figura.add_subplot(111)
plotno = FigureCanvasTkAgg(figura, master=okno)
plotno.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

aktualizuj_wykres()

okno.mainloop()
