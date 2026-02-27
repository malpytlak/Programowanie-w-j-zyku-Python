import pytest
from modele import Produkt, Klient
from silnik import SilnikWyceny



# 2+1


def test_2_plus_1_dla_3_sztuk():
    p = Produkt("SKU1", "Myszka", "elektronika", 100.0, 0.23, 3)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["2+1"])
    s.nalicz_wszystko()
    assert p.rabat_suma == 100.0


def test_2_plus_1_dla_2_sztuk():
    p = Produkt("SKU1", "Myszka", "elektronika", 100.0, 0.23, 2)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["2+1"])
    s.nalicz_wszystko()
    assert p.rabat_suma == 0.0


def test_2_plus_1_dla_4_sztuk():
    p = Produkt("SKU1", "Myszka", "elektronika", 100.0, 0.23, 4)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["2+1"])
    s.nalicz_wszystko()
    assert p.rabat_suma == 100.0



# Procent na kategorię


def test_rabat_procentowy_na_ksiazki():
    p = Produkt("SKU-K", "Książka", "ksiazka", 100.0, 0.05, 1)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["15_procent"])
    s.nalicz_wszystko()
    assert p.rabat_suma == 15.0


def test_outlet_bez_procentu():
    p = Produkt("SKU-O", "Buty", "outlet", 100.0, 0.23, 1)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["15_procent"])
    s.nalicz_wszystko()
    assert p.rabat_suma == 0.0



# Najtańszy -50%


def test_najtanszy_50_procent():
    p1 = Produkt("S1", "Drogi", "elektronika", 200.0, 0.23, 1)
    p2 = Produkt("S2", "Tani", "elektronika", 100.0, 0.23, 1)

    k = Klient("1", "BASIC")
    s = SilnikWyceny([p1, p2], k, ["NAJTANSZY50"])
    s.nalicz_wszystko()

    # 50% z 100 = 50 rabatu
    assert p2.rabat_suma == 50.0
    assert p1.rabat_suma == 0.0



# Kupon z progiem


def test_kupon_dziala_przy_progu():
    p = Produkt("S1", "Monitor", "elektronika", 250.0, 0.23, 1)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["KUPON20"])
    s.nalicz_wszystko()

    assert p.rabat_suma == 20.0


def test_kupon_nie_dziala_ponizej_progu():
    p = Produkt("S1", "Kabel", "elektronika", 100.0, 0.23, 1)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, ["KUPON20"])
    s.nalicz_wszystko()

    assert p.rabat_suma == 0.0


def test_kupon_nie_laczy_sie_z_2plus1():
    p = Produkt("SKU1", "Myszka", "elektronika", 100.0, 0.23, 3)
    k = Klient("1", "BASIC")

    s = SilnikWyceny([p], k, ["2+1", "KUPON20"])
    s.nalicz_wszystko()

    assert p.rabat_suma == 100.0  # tylko 2+1



# Darmowa dostawa


def test_darmowa_dostawa_tak():
    p = Produkt("SKU-E", "Monitor", "elektronika", 300.0, 0.23, 1)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, [])
    s.nalicz_wszystko()
    assert s.koszt_dostawy == 0.0


def test_darmowa_dostawa_nie():
    p = Produkt("SKU-E", "Kabel", "elektronika", 50.0, 0.23, 1)
    k = Klient("1", "BASIC")
    s = SilnikWyceny([p], k, [])
    s.nalicz_wszystko()
    assert s.koszt_dostawy == 15.0



# Minimalna cena 1 zł


def test_minimalna_cena_1zl():
    p = Produkt("SKU-T", "Zapałki", "ksiazka", 1.10, 0.23, 1)
    k = Klient("1", "BASIC")

    # duży rabat ręcznie
    p.rabat_suma = 1.0

    s = SilnikWyceny([p], k, [])
    s.nalicz_wszystko()

    cena_koncowa = p.wartosc_brutto() - p.rabat_suma
    assert cena_koncowa >= 1.0



# Walidacja


def test_bledna_cena():
    with pytest.raises(ValueError):
        Produkt("S1", "Test", "inne", -10.0, 0.23, 1)


def test_bledna_ilosc():
    with pytest.raises(ValueError):
        Produkt("S1", "Test", "inne", 10.0, 0.23, 0)