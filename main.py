import cv2
import random, time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import functions as f

# BEYZA NUR OKATAN 20011034
# ABDULKADİR TÜRE  20011042

# YAPAY ZEKA DERSİ 1. ODEV - GENETIK ALGORITMA ILE GORSEL TAKLIT

# Ilgili kütüphaneleri yuklemek icin; pip install -r requirements.txt

def main():

    boyut = 64 # 48x48 , 60x60 ideal, girdi ve cikti gorsellerini resize etmek icin kullanilir.
    
    girdi_yolu = "girdi7.png" #Girdi görselinin yolu
    nokta_sayisi = 500 #Odevin genel yonergesine uygun olarak cember icinde rastgele nokta secilmez. Yalnızca cember etrafındaki 360 nokta kullanılır.
    #Ek islev olarak nokta_sayisi 0'dan buyuk verilirse algoritma cember icinden de rastgele nokta_sayisi kadar nokta secer. Boylece gorsel taklit yetenegi artar.

    girdi = f.resim_oku(girdi_yolu,boyut) #girdi görseli alınır ve boyutlandırılır.
    cember_k = f.cember_dizi(boyut,nokta_sayisi) #cember noktalarının koordinatları alınır.

    #Genetik algoritma parametreleri kullanıcıdan alınır.
    k = int(input("K deger giriniz: ")) #bireydeki nokta sayısı (cember noktaları)
    populasyon_s = int(input("Baslangic populasyon buyuklugunu giriniz:")) #populasyon sayısı
    nesil_s = int(input("Nesil sayisini giriniz:")) #nesil sayısı
    mutasyon_orani = float(input("Mutasyon oranini giriniz:")) #mutasyon oranı
    en_iyi_s = int(input("Baslangic populasyonunudan en iyi kac bireyin secilecegini giriniz:"))#her iterasyonda secilecek olan en iyi birey sayısı
    if en_iyi_s % 2 != 0:
        en_iyi_s = en_iyi_s - 1

    baslangic_zamani = time.time() #Algoritmanın başlangıç zamanı alınır.

    #Baslangıc populasyonu olusturulur.
    populasyon = []
    for i in range(populasyon_s):
        birey = random.sample(cember_k, k)
        populasyon.append(birey)

    #Başlangıç populasyonu ve girdi görseli karşılaştırılır ve benzerlik oranı hesaplanır.
    oranlar = []
    for birey in populasyon:
        cikti = f.gorsel_ciz(boyut, birey)
        oran = f.benzerlik_hesapla(girdi, cikti)
        oranlar.append((birey, oran))
    #Baslangıc populasyonundaki en iyi bireyler seçilir.
    en_iyiler = f.en_iyi_bireyler(oranlar, en_iyi_s)
    gorsel_array = []
    #Nesil sayısı boyunca iterasyon yapılır.
    for i in range(nesil_s):
        #Caprazlama asaması cocuklar olusturulur.
        cocuklar = []
        for j in range(0,en_iyi_s,2):
            eb1 = en_iyiler[j][0]
            eb2 = en_iyiler[j+1][0]
            cocuk = f.cocuk_olustur(eb1, eb2)
            cocuklar.append(cocuk)
        #Mutasyon asaması
        for cocuk in cocuklar:
            cocuk = f.mutasyon(cocuk, mutasyon_orani, cember_k)
            en_iyiler.append((cocuk, f.benzerlik_hesapla(girdi, f.gorsel_ciz(boyut, cocuk))))
        
        #En iyi bireyler seçilir.
        en_iyiler = f.en_iyi_bireyler(en_iyiler, en_iyi_s)
        print(f"{i+1}. Nesil en iyi bireyin benzerlik orani: {en_iyiler[0][1]}")
        gorsel_array.append(en_iyiler[0][1])
        
        #Anlık görsellestirme islemi yapılır.
        cikti = f.gorsel_ciz(boyut, en_iyiler[0][0])
        plt.imshow(cikti, cmap='gray')
        plt.axis('off')
        plt.title(f"{i+1}. Nesil en iyi bireyin benzerlik orani: {en_iyiler[0][1]:.4f}")
        plt.show(block=False)
        plt.pause(0.05)
        plt.clf()

        en_iyiler = random.sample(en_iyiler, len(en_iyiler)) # Gen havuzunda karıştırma yapılır. Boylece ebeveyn seciminde rastgelelik artar.
        
    bitis_zamani = time.time() #Algoritmanın bitiş zamanı alınır.

    print(f"Algoritma toplam {nesil_s} nesilde tamamlandı. Toplam süre: {bitis_zamani - baslangic_zamani:.2f} saniye")

    #Genetik algoritma sonucunda en iyi bireyin cikti görseli kaydedilir.
    cikti = f.gorsel_ciz(boyut, en_iyiler[0][0])
    image = Image.fromarray((cikti).astype(np.uint8), mode='L')
    image.save("cikti4.png")
    print("En iyi bireyin cikti görseli kaydedildi.")
    #grafik çizdirme
    plt.plot(gorsel_array)
    plt.xlabel("Nesil")
    plt.ylabel("Benzerlik Orani")
    plt.title("Benzerlik Orani Grafigi")
    plt.savefig("benzerlik_orani_grafik.png")
    plt.show()

if __name__ == "__main__":
    main()