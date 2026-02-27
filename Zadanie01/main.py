from modele import Produkt, Klient
from silnik import SilnikWyceny

def menu():
    print("1. Dodaj produkt do koszyka")
    print("2. Podlicz i generuj paragon")
    print("3. Wyjście")

koszyk = []

while True:
    menu()
    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        try:
            nazwa = input("Nazwa produktu: ")
            cena = float(input("Cena: "))
            kat = input("Kategoria (np. outlet, ksiazka, elektronika): ")
            ile = int(input("Ilość: "))

            p = Produkt("SKU-TEST", nazwa, kat, cena, 0.23, ile)
            koszyk.append(p)

        except ValueError as e:
            print("Błąd danych:", e)

    elif wybor == "2":
        klient = Klient("Janusz-01", "GOLD")

        promocje = ["2+1", "15_procent", "NAJTANSZY50", "KUPON20"]

        silnik = SilnikWyceny(koszyk, klient, promocje)
        silnik.nalicz_wszystko()
        silnik.zapisz_paragon_do_pliku()
        print("Paragon zapisany do pliku ostatni_paragon.txt!")
        break

    elif wybor == "3":
        break