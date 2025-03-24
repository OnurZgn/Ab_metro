from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (komşu istasyon, süre)

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        if sure <= 0:
            raise ValueError(f"Hatalı süre: {sure}. Süre pozitif olmalıdır.")
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """ Yeni bir istasyon ekler. Aynı ID'ye sahip istasyon zaten varsa ekleme yapmaz. """
        if idx in self.istasyonlar:
            print(f"Uyarı: {idx} ID'li istasyon zaten mevcut.")
            return

        self.istasyonlar[idx] = Istasyon(idx, ad, hat)
        self.hatlar[hat].append(self.istasyonlar[idx])

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """ İki istasyon arasında bağlantı ekler. Hatalı ID girilirse hata mesajı döndürür. """
        if istasyon1_id not in self.istasyonlar or istasyon2_id not in self.istasyonlar:
            raise ValueError(f"Bağlantı hatası: '{istasyon1_id}' veya '{istasyon2_id}' istasyon ID'si bulunamadı.")
        
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]

        try:
            istasyon1.komsu_ekle(istasyon2, sure)
            istasyon2.komsu_ekle(istasyon1, sure)
        except ValueError as e:
            print(f"Hata: {e}")

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """ BFS kullanarak en az aktarmalı rotayı bulur. """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print(f"Hata: '{baslangic_id}' veya '{hedef_id}' istasyonu bulunamadı.")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic], 0)])  # (şu anki istasyon, yol, aktarma sayısı)
        ziyaret_edildi = {}

        while kuyruk:
            mevcut, yol, aktarma_sayisi = kuyruk.popleft()

            if mevcut == hedef:
                return yol  # Hedefe ulaştık

            for komsu, _ in mevcut.komsular:
                yeni_aktarma = aktarma_sayisi + (1 if komsu.hat != mevcut.hat else 0)

                if komsu not in ziyaret_edildi or ziyaret_edildi[komsu] > yeni_aktarma:
                    ziyaret_edildi[komsu] = yeni_aktarma
                    kuyruk.append((komsu, yol + [komsu], yeni_aktarma))

        return None  # Hedefe ulaşılamadıysa

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """ Dijkstra algoritması ile en kısa sürede ulaşılabilecek rotayı bulur. """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print(f"Hata: '{baslangic_id}' veya '{hedef_id}' istasyonu bulunamadı.")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        pq = [(0, id(baslangic), baslangic, [baslangic])]  # (toplam_süre, id, şu_an_istasyon, yol)
        ziyaret_edildi = {}

        while pq:
            toplam_sure, _, mevcut, yol = heapq.heappop(pq)

            if mevcut in ziyaret_edildi and ziyaret_edildi[mevcut] <= toplam_sure:
                continue
            ziyaret_edildi[mevcut] = toplam_sure

            if mevcut == hedef:
                return (yol, toplam_sure)  # Hedefe ulaştık, yolu ve süreyi döndür

            for komsu, sure in mevcut.komsular:
                yeni_toplam_sure = toplam_sure + sure
                yeni_yol = yol + [komsu]
                heapq.heappush(pq, (yeni_toplam_sure, id(komsu), komsu, yeni_yol))

        return None  # Hedefe ulaşılamadıysa


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 
    try:
        metro_yeni = MetroAgi()

        # İstasyonlar ve bağlantılar ekleniyor
        metro_yeni.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
        metro_yeni.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
        metro_yeni.istasyon_ekle("K3", "Mecidiyeköy", "Mavi Hat")
        metro_yeni.istasyon_ekle("K4", "Levent", "Mavi Hat")
        metro_yeni.istasyon_ekle("K5", "Bostancı", "Yeşil Hat")
        metro_yeni.istasyon_ekle("K6", "Kadıköy", "Yeşil Hat")
        
        # Bağlantılar
        metro_yeni.baglanti_ekle("K1", "K2", 4)  # Kızılay - Ulus
        metro_yeni.baglanti_ekle("K2", "K3", 6)  # Ulus - Mecidiyeköy
        metro_yeni.baglanti_ekle("K3", "K4", 7)  # Mecidiyeköy - Levent
        metro_yeni.baglanti_ekle("K4", "K5", 8)  # Levent - Bostancı
        metro_yeni.baglanti_ekle("K5", "K6", 9)  # Bostancı - Kadıköy

        # 1. Test: Doğrudan bağlı iki istasyon
        print("\nTest 1: Kızılay - Ulus (Doğrudan Bağlantı)")
        rota = metro_yeni.en_az_aktarma_bul("K1", "K2")
        if rota:
            print("En az aktarmalı rota: ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")
        
        sonuc = metro_yeni.en_hizli_rota_bul("K1", "K2")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika): ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        # 2. Test: Aktarma gerektiren rota
        print("\nTest 2: Kızılay - Levent (Aktarma Gerektiriyor)")
        rota = metro_yeni.en_az_aktarma_bul("K1", "K4")
        if rota:
            print("En az aktarmalı rota: ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")
        
        sonuc = metro_yeni.en_hizli_rota_bul("K1", "K4")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika): ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        # 3. Test: Uzak mesafede iki istasyon
        print("\nTest 3: Kızılay - Kadıköy (Uzak mesafe, birden fazla aktarma)")
        rota = metro_yeni.en_az_aktarma_bul("K1", "K6")
        if rota:
            print("En az aktarmalı rota: ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")
        
        sonuc = metro_yeni.en_hizli_rota_bul("K1", "K6")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika): ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        # 4. Test: Hedef bulunmayan senaryo
        print("\nTest 4: Kızılay - Kadıköy (Bağlantı yok)")
        rota = metro_yeni.en_az_aktarma_bul("K1", "Kadıköy")  # Hatalı ID
        if rota:
            print("En az aktarmalı rota: ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")
        
        sonuc = metro_yeni.en_hizli_rota_bul("K1", "Kadıköy")  # Hatalı ID
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika): ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        # 5. Test: Farklı hatlardaki istasyonlar
        print("\nTest 5: Kızılay - Kadıköy (Farklı hatlar)")
        rota = metro_yeni.en_az_aktarma_bul("K1", "K6")
        if rota:
            print("En az aktarmalı rota: ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")
        
        sonuc = metro_yeni.en_hizli_rota_bul("K1", "K6")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika): ", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")