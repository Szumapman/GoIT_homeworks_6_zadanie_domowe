# GoIT_homeworks_6_zadanie_domowe


## Zadanie[​](https://textbook.edu.goit.global/lms-python-homework/pl/docs/python-core/hw-06/#zadanie "Bezpośredni link do nagłówka")

Wielu z nas na pulpicie ma folder o nazwie “Do przejrzenia”, do którego wrzucamy na bieżąco randomowe rzeczy, ale nigdy nie mamy czasu, aby w końcu ten folder “przejrzeć” i zrobić porządek.

Napiszemy skrypt, który wreszcie zrobi porządek w tym folderze. Ostatecznie będziesz mógł dostosować ten program do swoich potrzeb tak, aby realizował indywidualny scenariusz odpowiadający Twoim wymaganiom. W tym celu nasza aplikacja będzie sprawdzać rozszerzenie pliku (ostatnie znaki w nazwie pliku, zwykle po kropce) i na podstawie rozszerzenia podejmować decyzję, do jakiej kategorii należy ten plik.

Przy uruchomieniu skrypt przyjmuje jeden argument - jest to nazwa folderu, w którym będzie przeprowadzał sortowanie. Przyjmując, że plik z programem nazywa się  `sort.py`, aby posortować folder  `/user/Desktop/Bałagan`, należy uruchomić skrypt za pomocą polecenia  `python sort.py /user/Desktop/Bałagan`.

-   Stworzenie osobnej funkcji do przetwarzania folderu na pewno ułatwi Ci pomyślne wykonanie tego zadania.
-   Funkcja przetwarzania folderów powinna rekurencyjnie wywoływać samą siebie, gdy napotyka zagnieżdżone foldery, aby program obejmował wszystkie poziomy katalogów.

Skrypt powinien przejść do podanego podczas uruchomienia folderu i posortować wszystkie pliki według rodzajów:

-   obrazy ('JPEG', 'PNG', 'JPG', 'SVG');
-   pliki wideo ('AVI', 'MP4', 'MOV', 'MKV');
-   dokumenty ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
-   muzyka ('MP3', 'OGG', 'WAV', 'AMR');
-   archiwa ('ZIP', 'GZ', 'TAR');
-   nieznane rozszerzenia.

Możesz powiększyć i uzupełnić tę listę według własnego uznania.

W wynikach pracy powinny się znaleźć:

-   Lista plików w każdej kategorii (muzyka, wideo, zdjęcia itp.)
-   Wykaz wszystkich znanych rozszerzeń plików, które występują w folderze docelowym.
-   Wykaz wszystkich rozszerzeń plików, które pozostały nierozpoznane przez skrypt.

Następnie należy dodać funkcje odpowiedzialne za przetwarzanie każdego rodzaju plików.

Dodatkowo należy zmienić nazwy wszystkich plików i folderów, usuwając wszystkie znaki, które mogą powodować problemy. W tym celu do nazw plików możesz zastosować funkcję  `normalize`. Pamiętaj jednak, że zmienianie nazw plików nie powinno mieć wpływu na rozszerzenia.

Funkcja `normalize`:

1.  Zmienia polskie litery na zwyczajne znaki (na przykład, ą, ę, ż i td.)
2.  Zamienia wszystkie litery, oprócz zwyczajnych znaków i cyfr, na znak '_'.

Wymagania dotyczące funkcji `normalize`:

-   przyjmuje ciąg znaków jako argument wejściowy i zwraca ciąg znaków;
-   wykonuje transliterację polskich liter zwyczajnymi znakami.
-   zamienia wszystkie litery, oprócz zwyczajnych znaków i cyfr, na znak '_'.
-   transliteracja może nie być zgodna ze standardem, ale powinna być czytelna;
-   pozostaje zachowana wielkość liter (wielkie litery pozostają wielkimi i podobnie w przypadku małych liter) po transliteracji.

## Instrukcje dotyczące sortowania plików:[​](https://textbook.edu.goit.global/lms-python-homework/pl/docs/python-core/hw-06/#instrukcje-dotycz%C4%85ce-sortowania-plik%C3%B3w "Bezpośredni link do nagłówka")

-   obrazy → folder `images`
-   dokumenty → folder `documents`
-   pliki audio → folder `audio`
-   pliki wideo → folder `video`
-   zawartość archiwów po rozpakowaniu → folder `archives`

## Kryteria akceptacji pracy domowej[​](https://textbook.edu.goit.global/lms-python-homework/pl/docs/python-core/hw-06/#kryteria-akceptacji-pracy-domowej "Bezpośredni link do nagłówka")

-   nazwy wszystkich plików i folderów są zmieniane przy użyciu funkcji `normalize`;
-   po zmianie nazw plików rozszerzenia pozostają bez zmiany;
-   puste foldery są usuwane;
-   skrypt “ignoruje” foldery `archives, video, audio, documents, images`;
-   zawartość rozpakowanego archiwum jest przenoszona do podfolderu o takiej samej nazwie (ale bez rozszerzenia na końcu) w folderze  `archives`;
-   pliki o nieznanych rozszerzeniach pozostają bez zmiany.
