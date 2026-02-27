from modele import Produkt, Klient

class SilnikWyceny:
    def __init__(self, koszyk, klient, promocje):
        self.koszyk = koszyk
        self.klient = klient
        self.promocje = promocje
        self.koszt_dostawy = 15.0

    def nalicz_wszystko(self):
        print(f"Log: Start wyceny dla klienta {self.klient.id_klienta}")

        # 1. 2+1
        self._promocja_2_plus_1()

        # 2. procent na kategorię (np. ksiazka)
        self._promocja_procentowa_kategoria("ksiazka", 0.15)

        # 3. najtańszy -50% w kategorii
        self._promocja_najtanszy_50("elektronika")

        # 4. kupon z progiem
        self._promocja_kupon_z_progiem(200)

        # 5. darmowa dostawa
        self._darmowa_dostawa_prog(200)

        # 6. blokada ceny minimalnej
        self._pilnuj_minimalnej_ceny()

    # PROMOCJE 

    def _promocja_2_plus_1(self):
        if "2+1" in self.promocje:
            for p in self.koszyk:
                if p.ilosc >= 3:
                    ile_gratis = p.ilosc // 3
                    p.rabat_suma += ile_gratis * p.cena_brutto

    def _promocja_procentowa_kategoria(self, kategoria, procent):
        if "15_procent" in self.promocje:
            for p in self.koszyk:
                if p.kategoria == kategoria and p.kategoria != "outlet":
                    rabat = (p.wartosc_brutto() - p.rabat_suma) * procent
                    p.rabat_suma += rabat

    def _promocja_najtanszy_50(self, kategoria):
        if "NAJTANSZY50" in self.promocje:
            produkty = [p for p in self.koszyk if p.kategoria == kategoria]
            if len(produkty) > 0:
                najtanszy = min(produkty, key=lambda x: x.cena_brutto)
                rabat = (najtanszy.cena_brutto * 0.5)
                najtanszy.rabat_suma += rabat

    def _promocja_kupon_z_progiem(self, prog):
        byla_2_plus_1 = any("2+1" in self.promocje for _ in self.koszyk)

        suma = sum(p.wartosc_brutto() - p.rabat_suma for p in self.koszyk)

        if "KUPON20" in self.promocje and not byla_2_plus_1:
            if suma >= prog and len(self.koszyk) > 0:
                self.koszyk[0].rabat_suma += 20.0

    def _darmowa_dostawa_prog(self, prog):
        suma = sum(p.wartosc_brutto() - p.rabat_suma for p in self.koszyk)
        if suma >= prog:
            self.koszt_dostawy = 0.0

    def _pilnuj_minimalnej_ceny(self):
        for p in self.koszyk:
            cena_po = p.wartosc_brutto() - p.rabat_suma
            minimalna = 1.0 * p.ilosc
            if cena_po < minimalna:
                p.rabat_suma = p.wartosc_brutto() - minimalna

    # PARAGON 

    def zapisz_paragon_do_pliku(self):
        suma_brutto = 0
        suma_netto = 0
        suma_rabat = 0

        with open("ostatni_paragon.txt", "w", encoding="utf-8") as f:
            f.write("=== PARAGON GENERATOR ===\n\n")

            for p in self.koszyk:
                przed = p.wartosc_brutto()
                po = przed - p.rabat_suma
                netto = po / (1 + p.stawka_vat)

                suma_brutto += po
                suma_netto += netto
                suma_rabat += p.rabat_suma

                f.write(f"{p.nazwa}\n")
                f.write(f"  Cena przed: {przed:.2f} PLN\n")
                f.write(f"  Rabat: {p.rabat_suma:.2f} PLN\n")
                f.write(f"  Cena po: {po:.2f} PLN\n\n")

            vat = suma_brutto - suma_netto

            f.write("----- PODSUMOWANIE -----\n")
            f.write(f"Suma brutto: {suma_brutto:.2f} PLN\n")
            f.write(f"Suma netto: {suma_netto:.2f} PLN\n")
            f.write(f"VAT: {vat:.2f} PLN\n")
            f.write(f"Dostawa: {self.koszt_dostawy:.2f} PLN\n")
            f.write(f"Oszczędność klienta: {suma_rabat:.2f} PLN\n")