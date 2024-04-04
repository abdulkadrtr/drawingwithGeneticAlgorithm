import cv2
import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#girdi görseli alır, resize islemi yapar ve array olarak döndürür.
def resim_oku(image_path,boyut):
    img = Image.open(image_path)
    img = img.resize((boyut, boyut))
    img = img.convert('L')
    img_array = np.array(img)
    img_array[img_array < 255] = 0
    return img_array

#cember noktalarının x,y koordinatlarını array olarak döndürür.
def cember_dizi(boyut, nokta_sayisi):
    array = []
    # Kare içinden rastgele nokta_sayisi noktayı array dizisine ekle
    for i in range(nokta_sayisi):
        random_x = np.random.uniform(0, boyut)
        random_y = np.random.uniform(0, boyut)
        array.append((int(random_x), int(random_y)))
    # Noktaları görselleştirmek için plt ekranı
    plt.figure(figsize=(5, 5))
    plt.scatter(*zip(*array), color='red')
    plt.xlim(0, boyut)
    plt.ylim(0, boyut)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    return array

#Birey dizisini görsel olarak cizer ve matrisi döndürür.
def gorsel_ciz(boyut, birey):
    matris = np.full((boyut, boyut), 255)
    for i in range(len(birey) - 1):
        # İki nokta arasında çizgi çizin
        cv2.line(matris, (birey[i][0], birey[i][1]), (birey[i+1][0], birey[i+1][1]), 0, 1)
    for x, y in birey:
        matris[y, x] = 0
    return matris

#Girdi ve cikti görsellerini karsilastirir ve benzerlik oranini yüzde cinsinden döndürür.
def benzerlik_hesapla(girdi,cikti):
    benzerlik = 0
    for i in range(len(girdi)):
        for j in range(len(girdi[i])):
            if girdi[i][j] == cikti[i][j]:
                benzerlik += 1
    benzerlik = (benzerlik / (len(girdi)**2)) * 100
    return benzerlik

#en iyi skora sahip t bireyi döndürür.
def en_iyi_bireyler(oranlar, t):
    oranlar.sort(key=lambda x: x[1], reverse=True)  # Benzerlik oranına göre sırala
    en_iyiler = oranlar[:t]  # En iyi t bireyi sec
    return en_iyiler

#cocuk birey icin tek noktalı caprazlama yapar. Nokta rastgele secilir.
def cocuk_olustur(birey1, birey2):
    nokta = random.randint(0, len(birey1) - 1)
    cocuk = birey1[:nokta] + birey2[nokta:]
    return cocuk

#0 - 1 arasında rastgele bir sayı seçilir ve bu sayı mutasyon oranından küçükse bireyde rastgele bir nokta değiştirilir.
def mutasyon(birey, oran, cember_k):
    if random.random() < oran:
        nokta = random.randint(0, len(birey) - 1)
        birey[nokta] = random.choice(cember_k)
    return birey