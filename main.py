from bs4 import BeautifulSoup
import requests
import csv
import pickle


class Item(object):

    def __init__(self):
        self.smallImageSrc = None
        self.link = None
        self.price = None
        self.category = None
        self.subcategory = None
        self.title = None
        self.descriptionHtml = []
        self.description = []
        self.fullImage = None


class PictureLinks:

    def __init__(self):
        self.smallImageSrc = None
        self.fullImage = None


# INICJALIZUJ ZMIENNE
p_value = 0
source = "https://www.rebel.pl/e4u.php/1,ModProducts/AdvancedSearch/?advanced%5Bsubmit%5D=Szukaj+%26%23187%3B&advanced%5Bphrase%5D=&advanced%5BID_CATEGORY%5D%5B0%5D=0&advanced%5BID_CATEGORY%5D%5B1%5D=0&advanced%5Bwydawca%5D=&advanced%5Bautor%5D=&advanced%5Bprice%5D=0&advanced%5Blanguage%5D=0&advanced%5Bgracze_1%5D=&advanced%5Bgracze_2%5D=&advanced%5Bczas_do%5D=0&advanced%5Bwiek%5D=&advanced%5Bavailable%5D=0&advanced%5Bdodatek%5D=&back=&p=20&p="
all_items = list()
all_pictures = list()
rebelString = 'https://www.rebel.pl'  # do getRequestow konkretnych produktow


# UTWORZ PLIK CSV Z ODPOWIEDNIMI KOLUMNAMI
csv_file = open('produkty_4.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file, delimiter='`')
csv_writer.writerow(['tytul', 'cena', 'link','smImgSrc', 'fullImgSrc', 'kategoria', 'podkategoria', 'opisHTML', 'opisSTRING'])


# GLOWNA PETLA (PRZECHODZI PRZEZ WSZYSTKIE STRONY)
while p_value < 1000:  # tak dlugo dopoki nie dojdziesz do 1000 produktu, p_value zwieksza sie o 20 w kazdej petli

    all_links = list()  # lista wszystkich linkow do produktow
    counter = 0 # licznik produktow, po odfiltrowaniu zbednych htmlowych tagow

    # Get request dla rebel.pl , wyszukiwanie zaawansowane --> wyswietla wszystkie produkty na stronie
    response = requests.get(source + str(p_value))  # p = 0 -->1 strona p = 20 -->2 strona itd
    soup = BeautifulSoup(response.content, 'lxml')
    products = soup.find_all('td', class_='small') #produkty,ktore zawieraja htmlowe elementy ktore trzeba jeszcze odfiltrowac

    #PETLA DLA KAZDEGO PRODUKTU NA JEDNEJ STRONIE
    for product in products:
        image = product.a.img
        try:  # sprobuj znalezc src img, jesli nie ma to rzuc exception
            imgSrc = image['src']

        except Exception as e:
            pass

        #LINKI
        link = product.a['href']
        if link not in all_links and link.startswith('/product'):  # usun duplikaty i zostaw tylko to co jest produktem
            all_links.append(link)  # tworz liste wszystkich linkow ktore sie nie powtarzaja
            item = Item()  # stworz obiekt tylko gdy znaleziono link
            item.link = rebelString + link

        if imgSrc.startswith("http"):  # jesli jest to miniaturka produktu (tylko te maja src http), zakladamy ze jak przejdzie tego ifa to jest produktem
            counter += 1  # ktory produkt z kolei
            print(str(counter))

            #LINKI DO MINIATUREK
            picture = PictureLinks() # tworzymy instancje pictureLinks do pickle dumpa
            picture.smallImageSrc = imgSrc
            item.smallImageSrc = imgSrc

            #GET REQUEST STRONY NA KTOREJ JEST JUZ KONKRETNY PRODUKT
            product_page = item.link
            product_response = requests.get(product_page) #strona gdzie opisany jest konkretny produkt
            product_soup = BeautifulSoup(product_response.content, 'lxml')

            # CENA
            price = product_soup.find('span', class_='price').string
            item.price = price

            # SZUKANIE TAGA Z KATEGORIAMI
            categories_junk = product_soup.find_all('div', class_='boxHeader')  # kategorie + nieodfiltrowane tagi html (smieci)

            # KOLUMNA NA STRONIE GDZIE OPISANE SA WSZYSTKIE PRODUKTY
            middleColumn = product_soup.find('td', class_='middleColumn')

            # TYTUL
            title = middleColumn.find('h1', class_='').string
            item.title = title

            # SZUKANIE KATEGORII i PODKATEGORII
            for c in categories_junk:

                c = c.h2.string
                if '::' in c:  # ze znakiem '::' wlasciwe kategorie, juz nie smieci
                    categories = c

            category_list = categories.split('::')

            # KATEGORIE I PODKATEGORIE
            item.category = category_list[0][:-1]  # pierwsza czesc to kategoria, usuwamy ostatni element stringa bo to spacja
            item.subcategory = category_list[1][1:]  # druga czesc to podkategoria, string zaczynamy od 1 znaku bo wdarla sie nam tam spacja

            # OPIS PRODUKTU
            descriptionHtml = middleColumn.find('div', id='mainDescription')  # szukaj opisu

            #OPIS Z TAGAMI HTML
            item.descriptionHtml = str(descriptionHtml) # zamien na stringa

            #OPIS BEZ TAGOW HTML
            item.description.append(''.join(descriptionHtml.strings)) #  usuwamy tutaj tagi, zostawiamy sam tekst , powstaje LISTA STRINGOW (1 elementowa)
            item.description = ''.join(item.description)  # zamien liste stringow na jednego stringa

            #LINK DO PELNEGO ZDJECIA
            picture_source = middleColumn.a['href']  # link do podstrony ze zdjeciem
            picture_source = rebelString+picture_source # pelny link
            picture_response = requests.get(picture_source) # wchodzimy na podstrone ze zdjeciem
            picture_soup = BeautifulSoup(picture_response.content, 'lxml')
            fullImage = picture_soup.table.td.img['src']
            fullImage = rebelString+fullImage

            item.fullImage = fullImage
            picture.fullImage = fullImage

            all_items.append(item)
            all_pictures.append(picture)
            csv_writer.writerow([item.title, item.price, item.link, item.smallImageSrc,item.fullImage, item.category, item.subcategory, item.descriptionHtml, item.description])

    print(p_value)
    p_value += 20 # przejdz do nastepnej strony
    all_links.clear() # wyczysc listy za kazdym razem zeby nie marnowac pamieci
    print(len(all_items), 'ILOSC PRODUKTOW W LISCIE') #
    print()
print(len(all_items),'FINISHED SCRAPPING')
with open("produkty.txt", "wb") as fp:   #Pickling
    pickle.dump(all_pictures, fp) # ZAPISUJE DO PLIKU TABLICE Z LINKAMI DO PELNYCH ZDJEC
print('Finished pickle dump')

csv_file.close()
