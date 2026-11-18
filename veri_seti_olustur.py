"""Özgün, açıkça SENTETİK Türkçe film yorumu veri seti üretimi.
Gerçek kullanıcı yorumu / dış kaynak / web kazıma içermez.
Aynı temel yorumun varyasyonları `temel_id` altında izlenir.
"""
import csv
import random
from pathlib import Path

SEED = 20261118

OLUMLU = [
"Film beni başından sonuna kadar etkiledi.",
"Hikâyenin anlatımı çok güçlü ve akıcıydı.",
"Oyuncular rollerine gerçekten hayat vermiş.",
"Final sahnesi beklentilerimi fazlasıyla karşıladı.",
"Görsel dünyası ve atmosferi çok başarılıydı.",
"Müzikler sahnelere mükemmel uyum sağlamış.",
"Karakterlerin gelişimini izlemek keyifliydi.",
"Diyaloglar doğal ve inandırıcı yazılmış.",
"Uzun zamandır böyle iyi bir film izlememiştim.",
"Beklediğimden çok daha iyi çıktı.",
"Senaryo yaratıcı fikirlerle doluydu.",
"Filmde gereksiz uzatılmış bir sahne hissetmedim.",
"Yönetmenin anlatım tarzını çok beğendim.",
"Kamera açıları hikâyeyi harika destekliyordu.",
"Sürükleyici olay örgüsü hiç sıkılmama izin vermedi.",
"İzlerken karakterlerle bağ kurabildim.",
"Hem eğlendiren hem düşündüren bir yapım olmuş.",
"Sonu tatmin edici ve anlamlıydı.",
"Gerilim dozu çok iyi ayarlanmıştı.",
"Komedi sahneleri gerçekten güldürdü.",
"Duygusal anlar yapay durmuyordu.",
"Oyuncu kadrosu uyum içinde çalışmış.",
"Her sahnenin özenle çekildiği belliydi.",
"Kurgusu hikâyeyi anlaşılır ve canlı tutuyor.",
"Tekrar izlemek isteyeceğim filmlerden biri.",
"Bu filmi arkadaşlarıma gönül rahatlığıyla öneririm.",
"Konunun işlenişi sıradanlıktan uzaktı.",
"Film çok iyi bir tempo yakalamış.",
"Görsel efektler abartısız ve etkileyiciydi.",
"Mekân seçimi anlatılan dünyaya çok yakışmış.",
"Yan karakterler bile özenle yazılmış.",
"Sürpriz gelişmeler mantıklı biçimde kurulmuş.",
"İlk sahneden itibaren ilgimi çekti.",
"Kötü olacağını düşünmüştüm ama çok beğendim.",
"Beklentimi aşan sıcak bir hikâye anlatıyor.",
"Zamanın nasıl geçtiğini fark etmedim.",
"Yönetmen seyirciyi hikâyenin içine çekiyor.",
"Kapanış sahnesi akılda kalıcıydı.",
"Filmin mesajı etkileyici biçimde verilmiş.",
"Başroldeki oyuncunun performansı kusursuza yakındı.",
"Renk kullanımı ve ışıklandırma çok hoşuma gitti.",
"Karmaşık konuyu anlaşılır biçimde sunmuşlar.",
"Duygu geçişleri son derece başarılıydı.",
"Yavaş sahneler bile anlamlıydı.",
"Mizahı zorlama değil kendiliğinden gelişiyor.",
"Her ayrıntının bir amacı vardı.",
"Film izledikten sonra güzel bir tat bıraktı.",
"Müzik seçimlerine bayıldım.",
"Karakterlerin kararları beni düşündürdü ve etkiledi.",
"Sahne geçişleri çok pürüzsüzdü.",
"Özgün dünyasıyla kendini hemen sevdiriyor.",
"Konu ilerledikçe film daha da güzelleşiyor.",
"Bu kadar dengeli bir senaryo beklemiyordum.",
"Oyuncuların kimyası hikâyeyi güçlendirmiş.",
"Filmin ritmi hemen hiç düşmüyor.",
"Anlatım dili son derece zarifti.",
"Yapım tasarımı etkileyici ayrıntılar içeriyor.",
"Üzücü bir konu olmasına rağmen çok iyi işlenmiş.",
"Daha uzun sürse bile izlemek isterdim.",
"Küçük ayrıntıları ustaca kullanmışlar.",
"Çocuk oyuncular bile oldukça inandırıcıydı.",
"Dönemin atmosferi başarılı şekilde yansıtılmış.",
"Dram ve mizah arasında güzel bir denge kurulmuş.",
"Bu yapım verdiğim zamana değdi.",
"Filmin sonunda iyi ki izlemişim dedim.",
"Müzik olmadan bile sahneler güçlüydü.",
"Hikâyedeki dönüşüm çok inandırıcıydı.",
"Kısa sürede favorilerim arasına girdi.",
"Detaylı fakat anlaşılır bir senaryo kurulmuş.",
"İlk bölümdeki merak duygusu sonuna kadar sürdü.",
"Kamera hareketleri çok yerinde kullanılmış.",
"Oyunculukların doğallığı beni şaşırttı.",
"Eğlenceli ve sıcak bir seyir deneyimiydi.",
"Büyük bir keyifle izledim.",
"Zor konuyu incelikle ele almışlar.",
"Finali şaşırtıcı ama tutarlıydı.",
"Film bittiğinde yüzümde gülümseme vardı.",
"Hikâyedeki dostluk teması etkileyiciydi.",
"Diyalogların kalitesi filmi yukarı taşıyor.",
"Kısacası çok başarılı bir sinema deneyimiydi."
]

OLUMSUZ = [
"Film beni başından sonuna kadar sıktı.",
"Hikâyenin anlatımı dağınık ve yorucuydu.",
"Oyuncular rollerine hiç inandıramadı.",
"Final sahnesi beklentilerimi karşılamadı.",
"Görsel dünyası ve atmosferi oldukça zayıftı.",
"Müzikler sahnelerle hiç uyum sağlamamış.",
"Karakterlerin gelişimi ikna edici değildi.",
"Diyaloglar yapay ve zorlama yazılmış.",
"Uzun zamandır bu kadar kötü film izlememiştim.",
"Beklediğimden çok daha kötü çıktı.",
"Senaryo klişe fikirlerle doluydu.",
"Filmde gereksiz uzatılmış çok fazla sahne vardı.",
"Yönetmenin anlatım tarzını hiç beğenmedim.",
"Kamera açıları hikâyeyi anlatmakta yetersizdi.",
"Yavaş olay örgüsü yüzünden sıkıldım.",
"İzlerken karakterlerle bağ kuramadım.",
"Ne eğlendiren ne düşündüren bir yapım olmuş.",
"Sonu tatmin edici değildi.",
"Gerilim dozu çok kötü ayarlanmıştı.",
"Komedi sahneleri bir kez bile güldürmedi.",
"Duygusal anlar çok yapay duruyordu.",
"Oyuncu kadrosu arasında hiç uyum yoktu.",
"Sahneler gelişigüzel çekilmiş gibiydi.",
"Kurgusu hikâyeyi takip etmeyi zorlaştırıyor.",
"Tekrar izlemeyi asla düşünmem.",
"Bu filmi arkadaşlarıma kesinlikle önermem.",
"Konunun işlenişi fazlasıyla sıradandı.",
"Film hiçbir zaman iyi bir tempo yakalayamamış.",
"Görsel efektler özensiz ve rahatsız ediciydi.",
"Mekân seçimi anlatılan dünyaya hiç yakışmamış.",
"Yan karakterler bile yüzeysel yazılmış.",
"Sürpriz gelişmeler mantıksız biçimde yerleştirilmiş.",
"İlk sahneden itibaren ilgimi kaybetti.",
"İyi olacağını düşünmüştüm ama hiç beğenmedim.",
"Beklentimin altında kalan sıradan bir hikâye.",
"Dakikaların geçmesini bekledim.",
"Yönetmen seyirciyi hikâyenin dışında bırakıyor.",
"Kapanış sahnesi anlamsızdı.",
"Filmin mesajı karmaşık ve belirsiz verilmiş.",
"Başroldeki oyuncunun performansı çok zayıftı.",
"Renk kullanımı ve ışıklandırma göz yoruyordu.",
"Basit konuyu gereksiz yere karmaşıklaştırmışlar.",
"Duygu geçişleri oldukça başarısızdı.",
"Yavaş sahneler boşuna uzatılmıştı.",
"Mizahı son derece zorlama duruyor.",
"Ayrıntıların çoğunun bir amacı yoktu.",
"Film izledikten sonra kötü bir tat bıraktı.",
"Müzik seçimlerinden hiç hoşlanmadım.",
"Karakterlerin kararları mantıksız ve sinir bozucuydu.",
"Sahne geçişleri çok kopuktu.",
"Özgün bir şey sunmuyor ve kendini tekrar ediyor.",
"Konu ilerledikçe film daha da kötüleşiyor.",
"Bu kadar tutarsız bir senaryo beklemiyordum.",
"Oyuncuların uyumsuzluğu hikâyeyi zayıflatmış.",
"Filmin ritmi sürekli düşüyor.",
"Anlatım dili özensizdi.",
"Yapım tasarımı ucuz ve zayıf görünüyordu.",
"İlginç konuyu bile kötü işlemişler.",
"Daha kısa sürse bile izlemek istemezdim.",
"Küçük ayrıntılar gereksiz yere uzatılmış.",
"Çocuk oyuncuların performansları inandırıcı değildi.",
"Dönemin atmosferi yeterince yansıtılmamış.",
"Dram ve mizah arasındaki denge bozulmuş.",
"Bu yapım verdiğim zamana değmedi.",
"Filmin sonunda keşke izlemeseydim dedim.",
"Müzikler olmadan sahneler tamamen etkisiz kalırdı.",
"Hikâyedeki dönüşüm hiç inandırıcı değildi.",
"Kısa sürede unutmak istediğim filmler arasına girdi.",
"Gereksiz ayrıntılarla dolu karışık bir senaryo.",
"İlk bölümdeki merak duygusu hızla kayboldu.",
"Kamera hareketleri yersiz kullanılmış.",
"Oyunculukların yapaylığı beni rahatsız etti.",
"Sıkıcı ve soğuk bir seyir deneyimiydi.",
"Büyük bir hayal kırıklığıyla izledim.",
"Zor konuyu yüzeysel biçimde ele almışlar.",
"Finali şaşırtıcı değil sadece tutarsızdı.",
"Film bittiğinde zaman kaybettiğimi düşündüm.",
"Hikâyedeki dostluk teması oldukça sığ kaldı.",
"Diyalogların kalitesizliği filmi aşağı çekiyor.",
"Kısacası başarısız bir sinema deneyimiydi."
]

# Bunlar sınıf bilgisi taşımayan, her iki etikette de kullanılan bağlam parçalarıdır.
BASLANGIC = [
"Dün akşam izlediğim yapımda", "Hafta sonu sinemada", "Evde tek başıma izlediğim filmde",
"Bir arkadaşımın tavsiyesiyle izlediğim yapımda", "Uzun bir aradan sonra izlediğim filmde",
"Gece açtığım bu filmde", "İlk defa izlediğim yapımda", "Sinemadan çıktıktan sonra düşündüm ki",
"Bugün izlediğim filmde", "Bir süredir merak ettiğim filmde", "Birlikte izlediğimiz yapımda",
"Rastgele seçtiğim filmde", "Uzun yolculukta açtığım yapımda", "Yeni keşfettiğim bu filmde",
"Tekrar değerlendirdiğim filmde", "İzleme listemden seçtiğim yapımda"
]
BITIS = [
"Genel değerlendirmem bu yönde.", "Özellikle hikâye aklımda kaldı.",
"Bunu filmin bütününü düşünerek söylüyorum.", "Birçok sahneye dikkat ettim.",
"İzleme deneyimim böyle geçti.", "Bana göre filmin belirgin tarafı buydu.",
"Yapım hakkında ilk izlenimim buydu.", "Seyir sonrasında düşündüğüm şey buydu.",
"Filmi değerlendirirken bunu esas aldım.", "Bu konuda düşüncem değişmedi.",
"Bütün sahneleri göz önünde bulundurdum.", "İzledikten sonra aynı kanaatte kaldım."
]

# Farklı temel yorumlara ortaklaşa eklenebilen duygu özetleri.
# Bunlar da özgün olarak yazılmıştır; gerçek kullanıcı değerlendirmesi değildir.
OLUMLU_OZET = [
    "Genel olarak filmi beğendim.", "Sonuçta iyi bir filmdi.",
    "Bence oldukça başarılı bir yapım.", "İzlemekten keyif aldım.",
    "Benim için güzel bir seyir deneyimiydi.", "Bu filmi sevdim.",
    "İzlediğime memnun oldum.", "Kesinlikle tavsiye ederim.",
    "Bence vakit ayırmaya değer.", "Oyuncuları ve hikâyeyi beğendim."
]
OLUMSUZ_OZET = [
    "Genel olarak filmi beğenmedim.", "Sonuçta kötü bir filmdi.",
    "Bence oldukça başarısız bir yapım.", "İzlerken hiç keyif almadım.",
    "Benim için sıkıcı bir seyir deneyimiydi.", "Bu filmi sevmedim.",
    "İzlediğime pişman oldum.", "Kesinlikle tavsiye etmem.",
    "Bence vakit ayırmaya değmez.", "Oyuncuları ve hikâyeyi beğenmedim."
]

ZOR_ORNEKLER = [
("Kötü bir film bekliyordum, hiç de kötü değildi.",1),
("Beni şaşırtan tarafı, hiç sıkılmamış olmam.",1),
("Başta sıkıcı görünse de hikâye giderek güzelleşti.",1),
("Bazı sahneleri beğenmedim ama genel olarak iyi bir filmdi.",1),
("Zayıf bir başlangıcı vardı fakat finali çok başarılıydı.",1),
("Film üzücüydü ama anlatımı mükemmeldi.",1),
("Olumsuz yorumlara rağmen filmi sevdim.",1),
("Hataları olsa da keyifle izledim.",1),
("Sade bir yapım ama etkileyici bir hikâyesi var.",1),
("Tahmin ettiğim kadar sıradan çıkmadı, gayet iyiydi.",1),
("Sonu hüzünlüydü, buna rağmen filmi çok beğendim.",1),
("Yavaş ilerledi ama hiç kopmadım.",1),
("Müzikleri sevmedim, oyunculuklar ise şahane.",1),
("Eksikliklerini gördüm fakat yeniden izlerim.",1),
("Önce tereddüt ettim, sonra hayran kaldım.",1),
("Başlangıcı kusurlu olmasına rağmen çok tatmin ediciydi.",1),
("Beklentim düşüktü ama sinemadan mutlu ayrıldım.",1),
("İlk on dakikası iyi değildi, sonrası harikaydı.",1),
("Karanlık atmosferi rahatsız edici değil, büyüleyiciydi.",1),
("Kimse önermemişti ama bana oldukça iyi geldi.",1),
("İyi olacağını umdum ama tam bir hayal kırıklığıydı.",0),
("Görüntüleri hoştu fakat hikâyesi berbat.",0),
("Yüksek puanına rağmen filmi hiç sevemedim.",0),
("Bazı şakaları komikti ama toplamda kötüydü.",0),
("Başlangıcı harikaydı, devamı tam bir fiyasko.",0),
("Müzikleri güzeldi ama film bir türlü açılmadı.",0),
("Oyuncuları beğenmeme rağmen senaryo rezaletti.",0),
("Çok övüldü ancak izlediğime pişmanım.",0),
("Fragman ilgimi çekmişti fakat film sıkıcı çıktı.",0),
("Bir iki iyi sahne kurtarmaya yetmemiş.",0),
("Hikâyenin fikri güzel, işlenişi çok zayıf.",0),
("Üzücü olması sorun değildi, asıl sorun anlatımın kötülüğüydü.",0),
("İlk yarıyı sevdim ama ikinci yarı dağıldı.",0),
("Güçlü oyunculara rağmen film işlemiyor.",0),
("Yönetmeni sevsem de bu filmini beğenmedim.",0),
("Büyük beklentilerle gittim, mutsuz ayrıldım.",0),
("Birkaç iyi diyalog dışında hatırlanacak şey yok.",0),
("Etkileyici görünmeye çalışmış ama yapay kalmış.",0),
("Final sürprizliydi fakat hiçbir anlam ifade etmedi.",0),
("Çekimleri kaliteli olsa da izlemesi yorucuydu.",0),
]

def olustur(klasor=None):
    klasor = Path(klasor) if klasor else Path(__file__).resolve().parent
    rng = random.Random(SEED)
    kayitlar=[]
    for etiket, temel_listesi, harf in [(1, OLUMLU, 'P'),(0, OLUMSUZ, 'N')]:
        for i, temel in enumerate(temel_listesi,1):
            for j in range(8):
                # Aynı kök cümleyi taşıyan grupları izliyoruz.
                pre = BASLANGIC[(i*3+j*5)%len(BASLANGIC)]
                son = BITIS[(i*5+j*7)%len(BITIS)]
                ifade = temel.rstrip('.')
                ifade = ifade[0].replace('İ','i').replace('I','ı').lower()+ifade[1:]
                ozetler = OLUMLU_OZET if etiket == 1 else OLUMSUZ_OZET
                ozet = ozetler[(i*7+j*3) % len(ozetler)]
                if j == 0: yorum=temel
                elif j == 1: yorum=f'{pre}, {ifade}.'
                elif j == 2: yorum=f'{temel} {ozet}'
                elif j == 3: yorum=f'{pre}, {ifade}. {ozet}'
                elif j == 4: yorum=f'{temel} {son} {ozet}'
                elif j == 5: yorum=f'{pre}, {ifade}. {son} {ozet}'
                elif j == 6: yorum=f'{ozet} {temel}'
                else: yorum=f'{ozet} {pre}, {ifade}.'
                kayitlar.append({'yorum':yorum,'etiket':etiket,'temel_id':f'{harf}{i:03d}'})
    rng.shuffle(kayitlar)
    # Sınıf başına tam 500 benzersiz yorum alıyoruz.
    result=[]
    seen=set()
    for etiket in (0,1):
        n=0
        for row in kayitlar:
            key=row['yorum'].casefold()
            if row['etiket']==etiket and key not in seen:
                result.append(row); seen.add(key); n+=1
                if n==500:break
        if n!=500: raise ValueError(f'{etiket} sınıfında 500 örnek oluşturulamadı: {n}')
    rng.shuffle(result)
    with (klasor/'film_yorumlari.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['yorum','etiket','temel_id']);w.writeheader();w.writerows(result)
    with (klasor/'zor_ornekler.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['yorum','etiket']);w.writerows(ZOR_ORNEKLER)
    print(f'{len(result)} sentetik eğitim/test havuzu ve {len(ZOR_ORNEKLER)} bağımsız zor örnek yazıldı.')
    return result

if __name__=='__main__':olustur()
