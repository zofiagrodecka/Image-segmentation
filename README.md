# Segmentacja obrazu na zadane obszary tonalne i stosowanie do nich osobnych wartości progowania automatycznego z manualną korektą.

Autorzy: Zofia Grodecka, Jan Prokop
OS: WINDOWS

Program ma być aplikacją okienkową pozwalającą na:
- Import plików (wybranie plików ze skanami, które mają zostać obrobione)
- Wykrywanie i wyznaczanie obszarów tonalnych o różnych średnich poziomach szarości/jasności.
- Możliwość korekty wybranych obszarów tonalnych przez użytkownika
- Obliczanie progu dla każdego z wyznaczonych obszarów
- Manualną opcję zmiany wartości tej bramki/progu.
- Zastosowanie wyliczonego progowania odpowiednio dla wszystkich obszarów tonalnych.
- Pokazanie efektu końcowego przy obecnych ustawieniach
- Eksport plików (do wybranego katalogu)

Do tego przydałby się właściwy interfejs do przechodzenia przez kolejne kroki działania
programu.

Wstępny podział pracy:

Tydzień 1-4: (3, 4 laby)
- Wykrywanie obszarów tonalnych | Jasiek 
- Implementacja algorytmu Otsu, jeśli nie będzie dawał odpowiednio dobrych efektów, to implementacja innego wyznaczania progu. | Zofia
- Możliwość manualnego dodawania obszarów | Jasiek
- Możliwość manualnej zmiany progowania | Zofia

Tydzień 5-7: (5 laby)
- Wyświetlanie kroków w aplikacji okienkowej | Zofia
- Dodanie interfejsu pokazującego wybrane obszary i np. suwak z wyboremwartości progowania. | Zofia / Jasiek
- Dodanie wygodnego sposobu wybierania plików i miejsca na eksport. | Jasiek

Tydzień 8+:
- Pewnie czegoś nie zrobimy na czas, więc to jest bufor
- Poprawa programu zależnie od feedbacku
