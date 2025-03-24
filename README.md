Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
Bu proje, bir metro ağı üzerindeki en kısa ve en hızlı rotaları bulmayı amaçlayan bir rota optimizasyon simülasyonudur.

En az aktarmalı rota için BFS (Breadth-First Search) algoritması,

En hızlı rota için A (A-Star) algoritması* kullanılmıştır.

Simülasyon, istasyonlar arasındaki bağlantıları ve süreleri dikkate alarak en optimal yolu hesaplar.

📌 Kullanılan Teknolojiler ve Kütüphaneler
Kütüphane	Açıklama
collections.deque	BFS algoritması için kuyruk (queue) veri yapısını sağlar.
heapq	A* algoritması için öncelik kuyruğu (priority queue) uygular.
defaultdict	Metro hatlarını gruplamak için kullanılır.
typing	Tip açıklamaları ekleyerek kodun okunabilirliğini artırır.
📌 Algoritmaların Çalışma Mantığı
1️⃣ BFS (En Az Aktarmalı Rota)
Nasıl Çalışır?
📌 BFS (Breadth-First Search), katmanlı arama (level-wise search) yaparak, en kısa adımlı yolu bulur.

Başlangıç istasyonu kuyruğa eklenir.

Ziyaret edilen istasyonlar listesi tutulur.

Her iterasyonda bir sonraki istasyonlar kuyruğa eklenir.

Hedef istasyona ulaşıldığında durur ve yolu döndürür.

Neden BFS?
✔ En kısa aktarmalı rotayı garantiler çünkü tüm yolları eşit adımlarla genişletir.
✔ Optimal çözüm üretir, çünkü önce en kısa yollar keşfedilir.

2️⃣ A (En Hızlı Rota)*
Nasıl Çalışır?
📌 *A (A-Star)**, en düşük süreli rotayı bulur.

Öncelik kuyruğu (heapq) kullanarak en düşük süreye sahip olan yolu seçer.

Her iterasyonda komşu istasyonlar keşfedilir ve süre hesaplanır.

Toplam süre en az olan yol her adımda öncelikli olarak genişletilir.

Hedef istasyona ulaşıldığında durur ve en hızlı rota döndürülür.

Neden A?*
✔ Dijkstra'dan daha hızlıdır, çünkü doğrudan hedefe yönlenir.
✔ En düşük süreli rotayı bulur, çünkü maliyeti en düşük olan yolları seçer.

📌 Projeyi Geliştirme Fikirleri
+ Daha Gerçekçi Simülasyonlar

Gerçek metro verisi (örneğin İstanbul veya Ankara metrosu) ile genişletme.

İstasyonların GPS koordinatları ile harita entegrasyonu.

+ Yapay Zeka Destekli Optimizasyon

Dinamik trafik yoğunluğu faktörünü ekleyerek gerçek zamanlı tahmin yapılabilir.

Makine öğrenmesi ile zaman bazlı tahmini ulaşım süreleri hesaplanabilir.

+ Kullanıcı Dostu Arayüz

Web veya mobil uygulama üzerinden arayüz eklenebilir.

Grafiksel harita ve istasyon bilgileri görselleştirilebilir.
