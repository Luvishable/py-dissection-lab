"""
- Her generator bir iterator'dür ama her iterator bir generator değildir
- Çünkü generator dediğimiz şey iterator protokolünü (__iter__ + __next__ ) Python'un yield
  mekanizmasıyla otomatik olarak implement eden özel bir iterator'dür.

- Iterator sıradaki elemanı ver mantığıyla çalışan bir nesnedir.
- Iterator olma şartı:
    - __next__() metodu olacak -> sıradaki elemen döndürülür. StopIteration fırlatır bittiğinde
    - __iter__() metodu olacak → genelde return self (iterator’lar iterable gibi de davranır)
"""

# class ile manuel iterator
class CountdownIterator:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# aynı countdown'un generator versiyonu
def countdown(start: int):
    current = start
    while current > 0:
        yield current
        current -= 1

# Kullanımda ikisi de aynı görünür
# it1 = CountdownIterator(3)
# it2 = countdown(3)
#
# next(it1)  # 3
# next(it2)  # 3


"""
STATE MACHINE

- pratikte generator fonksiyonu bir state machine gibi çalışır
- yield noktaları duraklama noktalarıdır ve generator çalışırken python şunları saklar:
    - hangi satırdaydı / instruction pointer (nereden devam edeceğini)
    - local değişkenler 
    - bazı iç çalışma verileri
- Bu yüzden generator kaldığı yerden çalışmaya devam edebilir. Yani state yönetimi elle değil python tarafından yapılmış olur
- NOT: state machine illa finite olmak zorunda değil sonsuz bir akış da olabilir.
- state machine bir işlemi durumlar ve bu durumlar arasındaki geçişler olarak modelleme tekniğidir
Basit örnek: bir parser düşün.
START durumundasın, harf gelirse IN_WORD’e geç,
boşluk gelrse START’ta kal, newline gelirse END gibi…

Bu modelin faydası: “akış kontrolü + nerede kaldığını bilmek” sistematik hale gelir.
"""

"""
send throw ve close generator'ü sadece üretici değil de iki yönlü çalışan yapı olarak (coroutine) kullanınca devreye girer.
"""

# Normalde generator dışarı verir (yield x); send() ile içeriye veri sokarsın

# x = yield something => burada x dışarıdan send edilen değerdir.
# ÖRNEK: running_average() coroutine
def running_average():
    total = 0.0
    n = 0
    avg = None
    while True:
        x = yield avg   # dışarı avg ver sonra dışarıdan x al
        total += x
        n += 1
        avg = total / n

coro = running_average()
print(next(coro))   # coroutine'i prime eder: ilk yield'e kadar çalıştırır -> None
print(coro.send(10))    # 10 gönder, avg döner -> 10
print(coro.send(20))    # 15
print(coro.send(30))    # 20

# NOTE: neden next(coro) ile prime ediyoruz? Çünkü send ilk olarak yield noktasına gelmiş bir generator ister.
# Başlamamışsa önce next() ile yield'e getirirsin.


# .throw(exc) -> generator'ün içinden exception fırlatmak
# Generator duraklamışken içine bir exception enjekte edersin. Generator içinde bunu yakalayabilir.
# ÖRNEK: reset komutu


class Reset(Exception):
    pass

def counter():
    i = 0
    while True:
        try:
            cmd = yield i
            if cmd == "inc":
                i += 1
        except Reset:
            i = 0

c = counter()
print(next(c))              # 0
print(c.send("inc"))        # 1
print(c.send("inc"))        # 2
print(c.throw(Reset))       # 0
print(c.send("inc"))        # 1



# .close() ile generator'ü kapatmak
# generator'e GeneratorExit exception'unu forlattırır. Genator kapanır ve finally blokları çalıştırılır
def reader(path):
    f = open(path, "r", encoding="utf-8")
    try:
        for line in f:
            yield line
    finally:
        f.close()
        print("file closed")


g = reader("logs/app.log")
print(next(g))
g.close()  # "file closed" basar, dosya kapanır

# Çoğu zaman .close()’u sen elle çağırmazsın; with, garbage collection veya framework çağırır.
# Ama generator “resource” tutuyorsa finally ile cleanup çok değerlidir.