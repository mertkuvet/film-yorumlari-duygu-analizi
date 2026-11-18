# Türkçe Film Yorumlarında Duygu Analizi

Bu projede Türkçe film yorumları, metin işleme ve makine öğrenmesi yöntemleri kullanılarak **olumlu** veya **olumsuz** olarak sınıflandırılır. Yorumlar **Counting Vectors** ve **TF-IDF** ile sayısallaştırılır; **Decision Tree (Karar Ağacı)** modeliyle tahmin yapılır. İki metin temsilinin sonuçları karşılaştırılır.

Proje **Jupyter Notebook** üzerinde çalışır. Ayrı bir web arayüzü yoktur.

## 1. Kurulum ve Çalıştırma

Python 3.10 veya üzeri bir sürüm gereklidir.

1. Proje klasörünü indirin ve açın.
2. Terminali proje klasöründe açıp kütüphaneleri yükleyin:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. `duygu_analizi.ipynb` dosyasını VS Code veya Jupyter Notebook ile açın.
4. Kullanılacak Python ortamını (kernel) seçin ve **Run All** ile hücreleri sırayla çalıştırın.
5. Çalışma tamamlandığında sonuçları hücrelerin altında, kayıtlı grafik ve raporları da `sonuclar/` klasöründe inceleyin.

**Not:** `film_yorumlari.csv` ve `zor_ornekler.csv`, Notebook ile aynı klasörde bulunmalıdır. İstenirse veri setleri `python veri_seti_olustur.py` komutuyla yeniden oluşturulabilir.

## 2. Kendi Film Yorumunu Test Etme

Notebook'ta **12. Rastgele yeni yorumlarda kullanım** başlığına gidin. Bu bölümde `kullanici_ornekleri` listesindeki metinleri değiştirin:

```python
kullanici_ornekleri = [
    "Film gerçekten çok güzeldi, oyunculuklar harikaydı.",
    "Senaryo sıkıcıydı, filmi hiç beğenmedim."
]

for yorum in kullanici_ornekleri:
    print(f"{tahmin_et(yorum):8} | {yorum}")
```

Bu hücreyi tekrar çalıştırdığınızda her yorum için **Olumlu** veya **Olumsuz** tahmini görüntülenir. `tahmin_et` fonksiyonu aynı bölümde tanımlandığından, önceki hücrelerin en az bir kez çalıştırılmış olması gerekir.

## 3. Kullanılan Yöntemler

- **Ön işleme:** Küçük harfe dönüştürme, tokenization ve bazı stop word'lerin çıkarılması.
- **Metin temsili:** Counting Vectors (`CountVectorizer`) ve TF-IDF (`TfidfVectorizer`).
- **Sınıflandırma:** Decision Tree (`DecisionTreeClassifier`).
- **Değerlendirme:** Accuracy, precision, recall, F1, macro-F1 ve confusion matrix.
- **Model seçimi:** 5-katlı çapraz doğrulama (`GroupKFold`) ve Grid Search (`GridSearchCV`).

## 4. Veri Seti

`film_yorumlari.csv` dosyasında **500 olumlu ve 500 olumsuz**, toplam **1.000 Türkçe film yorumu** bulunmaktadır. `zor_ornekler.csv` dosyasında ise ayrıca hazırlanmış **40 zor yorum** yer alır.

Yorumlar **yapay zekâ desteğiyle oluşturulmuş sentetik verilerdir**; gerçek izleyici değerlendirmeleri değildir. Benzer temel yorumlardan türetilen örneklerin eğitim ve test kümelerine dağılmasını önlemek için `temel_id` ile gruplama yapılır. Bu kimlik, sınıflandırma modeline girdi olarak verilmez.

## 5. Model Sonuçları

Proje paketindeki kaydedilmiş çalıştırmanın sonuçları:

| Ölçüt | Sonuç |
|---|---:|
| Eğitim verisi | 802 yorum |
| Test verisi | 198 yorum |
| Test accuracy | **%86,9** |
| Test precision (olumlu sınıf) | %81,2 |
| Test recall (olumlu sınıf) | %94,8 |
| Test F1 (olumlu sınıf) | 0,875 |
| Test macro-F1 | **0,868** |
| Zor yorumlarda accuracy | **%42,5** |

Bu çalıştırmada seçilen model **Counting Vectors + Decision Tree** olmuştur (`criterion=gini`, `max_depth=10`, `min_samples_leaf=1`). Son seçilen modeli ve güncel ölçümleri görmek için Notebook'un **10. Model seçimi ve son test** bölümüne bakılmalıdır. Model parametreleri veya ortam değişirse sonuçlar farklılaşabilir.

## 6. Sonuçlar Nerede?

- **7. Başarı ölçütleri:** İlk model karşılaştırmaları.
- **8. N-Fold Cross Validation:** Çapraz doğrulama sonuçları.
- **9. Grid Search:** Denenen parametreler.
- **10. Model seçimi ve son test:** Seçilen model, başarı metrikleri ve confusion matrix.
- **11. Bağımsız ve zor yorumlar üzerinde kontrol:** Daha zor örneklerin sonuçları.
- **12. Rastgele yeni yorumlarda kullanım:** Kendi yorumlarınızla tahmin yapma.

## 7. Proje Dosyaları

```text
film_yorumlari_duygu_analizi/
├── duygu_analizi.ipynb       # Ana Jupyter Notebook
├── film_yorumlari.csv        # 1.000 etiketli yorum
├── zor_ornekler.csv          # 40 zor yorum
├── veri_seti_olustur.py      # Sentetik veri oluşturma kodu
├── requirements.txt          # Gerekli Python kütüphaneleri
├── README.md                 # Proje açıklaması
└── sonuclar/                 # Grafikler, tablolar ve raporlar
```

## 8. Sonuç ve Sınırlamalar

Model, sentetik test kümesinde **%86,9** doğruluk elde etmiştir. Ancak ayrı hazırlanan zor yorumlardaki **%42,5** doğruluk, özellikle olumsuzluk ve karışık duygu içeren cümlelerde zorlandığını göstermektedir. Bu nedenle sonuçlar, gerçek kullanıcı yorumlarında aynı başarıya ulaşılacağı anlamına gelmez.

Çalışmanın amacı, farklı metin temsillerinin sınıflandırma üzerindeki etkisini karşılaştırmak ve model performansını ölçmektir.
