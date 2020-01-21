# ScrapperRebel
Znajduje sie tutaj skrypt, który pobiera kluczowe elementy np. cena, tytuł produktów znajdujących się na stronie rebel.pl i zapisuje je do pliku csv (separator ` , string delimiter "). Dodatkowo zawarty jest także skrypt który pobiera zdjęcia tych produktów.

Zawarty jest też poglądowy plik csv ( ma inne seperatory ( , ) niż w skrypcie z racji na utworzenie go w poprzedniej wersji skryptu)

INSTRUKCJA OBSŁUGI:
1. Uruchomić plik main
2. Po zakończeniu działania skryptu main (trwa to długo ze względu na dużą ilość danych, można je zmniejszyć zmieniając wartość p_value na początku skryptu na np 20 lub 40 {musi być wielokrotność 20}.
3. Uruchomić skrypt ImageDownloader, powinien utworzyć się nowy folder ze zdjęciami produktów. ( pobiera on informacje z pliku produkty.txt , który jest już zapełniony { został stworzony po uruchomieniu skryptu main, zatem krok 1 nie jest wymagany do sprawdzenia jego działania}
