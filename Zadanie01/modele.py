class Produkt:
    def __init__(self, sku, nazwa, kategoria, cena_brutto, stawka_vat, ilosc):
        if cena_brutto <= 0:
            raise ValueError("Cena musi być większa od 0")
        if ilosc <= 0:
            raise ValueError("Ilość musi być większa od 0")
        if stawka_vat < 0:
            raise ValueError("VAT nie może być ujemny")

        self.sku = sku
        self.nazwa = nazwa
        self.kategoria = kategoria
        self.cena_brutto = cena_brutto
        self.stawka_vat = stawka_vat
        self.ilosc = ilosc
        self.rabat_suma = 0.0

    def wartosc_brutto(self):
        return self.cena_brutto * self.ilosc

    def wartosc_netto(self):
        return self.wartosc_brutto() / (1 + self.stawka_vat)


class Klient:
    def __init__(self, id_klienta, poziom_lojalnosci):
        self.id_klienta = id_klienta
        self.poziom_lojalnosci = poziom_lojalnosci