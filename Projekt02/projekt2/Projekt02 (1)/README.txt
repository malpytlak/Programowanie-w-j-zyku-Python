==============================================================
                       Enchanted Library
==============================================================

Mini-Goodreads dla miłośniczek książek, zbudowany na Flasku.
Tytuły pobierane są na żywo z Open Library API (darmowe, bez
klucza), a konta, półki i recenzje są trzymane lokalnie
w bazie SQLite.

Autorki:  Małgorzata Pytlak, Julia Radosz
Przedmiot: Programowanie w języku Python - Projekt II (2025/26)
Framework: Flask (Python 3.10+)


--------------------------------------------------------------
Instalacja i uruchomienie
--------------------------------------------------------------

Wymagany Python 3.10+ i pip.

1) Instalacja zależności:

       pip install -r requirements.txt

2) Jednorazowa inicjalizacja bazy (tworzy tabele i dwa konta
   testowe z zahashowanymi hasłami). Wklej do terminala:

   python -c "from app import create_app, db; from app.models import User; from werkzeug.security import generate_password_hash; app = create_app(); ctx = app.app_context(); ctx.push(); db.drop_all(); db.create_all(); db.session.add(User(username='admin', email='admin@lib.pl', password_hash=generate_password_hash('puchatek123'), is_admin=True)); db.session.add(User(username='kopciuszek', email='k@lib.pl', password_hash=generate_password_hash('pantofelek'), is_admin=False)); db.session.commit(); print('Gotowe!')"

3) Start serwera deweloperskiego:

       python run.py

   Aplikacja działa pod adresem http://127.0.0.1:5000


--------------------------------------------------------------
Konta testowe
--------------------------------------------------------------

    Admin       login: admin        haslo: puchatek123
    Uzytkownik  login: kopciuszek   haslo: pantofelek


--------------------------------------------------------------
Funkcje aplikacji
--------------------------------------------------------------

  * Katalog - 12 bestsellerów na stronie głównej, zakładki
    gatunków (Fantasy, Thriller, Romance, Horror, History,
    Science), wyszukiwarka po tytule/autorze.

  * Szczegóły książki - opis, biogram autora, rok wydania,
    wydawca, liczba stron, recenzje innych czytelników.

  * Półka (My Shelf) - użytkownik przypisuje książce status
    Want to read / Currently reading / Finished.

  * Recenzje - ocena 1-5 gwiazdek + tekst; wymaga wcześniejszego
    dodania książki do półki.

  * Panel admina - usuwanie recenzji i użytkowników wraz
    z ich danymi.


--------------------------------------------------------------
Testy
--------------------------------------------------------------

       pytest tests/ -v

Testy używają bazy SQLite w pamięci, a wywołania do Open
Library są mockowane (testy nie chodzą do sieci).


--------------------------------------------------------------
Dalsza dokumentacja
--------------------------------------------------------------

Szczegółowa dokumentacja architektury, modułów i podziału
pracy znajduje się w pliku dokumentacja.pdf.

Przyjazny przewodnik uzupełniający: ../przewodnik.pdf
