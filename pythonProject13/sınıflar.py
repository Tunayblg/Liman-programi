
#Gemiler diye ana bir sınıf oluşturup diğer gemi çeşitlerini bu main sınıfı baz alarak ekstra özelliklerini ekleyerek oluşturdk

class Gemiler:
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili):
        self.seri_no = seri_no
        self.gemi_ismi = gemi_ismi
        self.agirlik = agirlik
        self.model_yili = model_yili

class YolcuGemisi(Gemiler):
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili, max_yolcu_sayisi):
        super().__init__(seri_no, gemi_ismi, agirlik, model_yili)
#super(), Python da kalıtım  kullanırken bir üst sınıfın özelliklerine ve metodlarına erişmek için kullanılır
        self.max_yolcu_sayisi = max_yolcu_sayisi

class PetrolTankeri(Gemiler):
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili, max_petrol_kapasitesi):
        super().__init__(seri_no, gemi_ismi, agirlik, model_yili)
#self ile de sınıfın kendi özelliğini belirledik.
        self.max_petrol_kapasitesi = max_petrol_kapasitesi

class KonteynerGemisi(Gemiler):
    def __init__(self, seri_no, gemi_ismi, agirlik, model_yili, konteyner_sayisi, max_tonaj):
        super().__init__(seri_no, gemi_ismi, agirlik, model_yili)
        self.konteyner_sayisi = konteyner_sayisi
        self.max_tonaj = max_tonaj

#Aynı metodu (kalıtım) kullanarak bu sefer Kaptan ve mürettebat sınıflarını içeren Görevliler sınıfı oluşturuyoruz.
#hem kaptana hem mürettabata özgü özellikler oldugundan ortak ozellikleri GÖREVLİLER sınıfında toplayıp kaptan ve murettebatı ayırdık.

class Gorevliler:
    def __init__(self, ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi):
        self.ID = ID
        self.ad_soyad = ad_soyad
        self.adres = adres
        self.uyruk = uyruk
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi

class Kaptan(Gorevliler):
    def __init__(self, ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi, lisans):
        super().__init__(ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi)
        self.lisans = lisans

class MUrettebat(Gorevliler):
    def __init__(self, ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi, gorev):
        super().__init__(ID, ad_soyad, adres, uyruk, dogum_tarihi, ise_giris_tarihi)
        self.gorev = gorev

class Sefer:
    def __init__(self, gemi_id, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, diger_limanlar):
        self.gemi_id = gemi_id
        self.yola_cikis_tarihi = yola_cikis_tarihi
        self.donus_tarihi = donus_tarihi
        self.yola_cikis_limani = yola_cikis_limani
        self.diger_limanlar = diger_limanlar  # Birden fazla liman olabileceginden liste olarak tutucaz

class SeferlerYonetimi:
    def __init__(self):
        self.gecmis_seferler = []  # Geçmiş seferler listesi
        self.gelecek_seferler = []  # Gelecek seferler listesi
        self.olasi_seferler = []  # Olası seferler listesi

    def sefer_ekle(self, sefer_tipi, sefer):
        if sefer_tipi == "gecmis":
            self.gecmis_seferler.append(sefer)
        elif sefer_tipi == "gelecek":
            self.gelecek_seferler.append(sefer)
        elif sefer_tipi == "olasi":
            self.olasi_seferler.append(sefer)

class Limanlar:
    def __init__(self, liman_ad, ulke, nufus, pasaport_gerekli_mi, demirleme_ucreti):
        self.liman_ad = liman_ad
        self.ulke = ulke
        self.nufus = nufus
        self.pasaport_gerekli_mi = pasaport_gerekli_mi
        self.demirleme_ucreti = demirleme_ucreti
#Limanın adı ve ülkesi liman için ayırt edici olacaktır koşulunu saglamak için:
        self.tanimlayici = f"{liman_ad}-{ulke}"
