"""
- Python'da generator "bütün sonuçları tek seferde üretmek yerine, ihtiyaç oldukça adım adım üreten"
(lazy evaluation) bir akıştır.
- Bellek dostu
- akış tabanlı (stream)
- pipeline kurmaya uygun

- Normal fonksiyon return ile biter ve tek bir değer döndürür
- Generator fonksiyon yield ile duraklar, değer üretir, sonra bir sonraki next() çağrısında kaldığı yerden devam eder.
- Generator arka planda bir iterator 'dür. __iter__ ve ??next__ davranışı vardır
- Kısaca: “liste üretme” değil, “değer akıtma” (streaming).
"""

def count_up_to(n):
    i = 1
    while i <= n:
        yield i   # değer üret, durakla
        i += 1    # next() ile buradan devam eder


# Generator expression: list comprehension but lazy
# nums = [x*x for x in range(10)]
# print(nums)

# nums = (x*x for x in range(10))
# for i in range(5):
#     print(next(nums))

"""
Büyük veri varsa ve bellek durumu kritikse 
DB sonuçları chunklarla işlenecekse
Kural: Hepsini RAM'e almak gereksizse -> generator kullan

Stream / pipeline tasarlarken
Bir işi parçalara bölüp zincirlemek:

oku → filtrele → dönüştür → yaz
Her aşama generator olursa backpressure gibi davranır: tüketildikçe üretir.


Sonsuz/uzun akışlar

log stream
event stream
sensör/telemetri
“bitmesi gerekmeyen” üretimler
"""


# Generator tek kullanımlıktır. Yani sonuçlar birden fazla defa kullanılacaksa generator kullanma
g = (x for x in range(3))
print(list(g))  #[1, 2, 3]
print(list(g))  # []


# Bir generator başka bir iterable'ı akıtabilir
def chain(a, b):
    yield from a
    yield from b