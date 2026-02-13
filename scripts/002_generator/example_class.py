# Creating a simple iterable class

class Bag:
    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        # burada iterator olarak liste iteratörünü döndürüyoruz
        return iter(self._items)

# b = Bag(["comb", "napkin", "water"])
# for item in b:
#     print(item)


# What is next() ?
# It's a built-in function and it utilizes/calls the __next__() metthod of the iterator
# value = next(iterator)
# yukarıdaki çağrı iterator'ün __next__() metodunu çağırır ve şuna dönüşür:
# next(iterator) -> iterator.__next__()
# Iterator biterse StopIteration hatası fırlatır. Hata fırlatmaması için default değer verirsin:
# it = iter([10, 20])
# next(it)        # 10
# next(it)        # 20
# next(it, -1)    # -1  (bittiği için default döndü)


# Iterable olmak = iter(object) çalışması
# Iterator olmak = next(iterator) çalışması


# Iterable ayrı, Iterator ayrı class

class Countdown:
    def __init__(self, start):
        self.start = start
    def __iter__(self):
        return CountdownIterator(self.start)


class CountdownIterator:
    def __init__(self, current):
        self.current = current

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        # the value that is gonna be produced
        value = self.current
        # current has to be minus 1
        self.current -= 1
        return value

# Countdown is the lectern and the CountdownIterator is a tool in order to toggle the page
# Countdown is iterable class and CountdownIterator is an iterator class. But they both have __iter_-
# dunder method as python expects it.
# Iterable olan sınıfta __iter__ olmalı çünkü for x in Countdown(4): yazınca Python önce şunu yapar
# iterable = iter(countdown_object)
# bu da countdown_object'e ait __iter__() metodunu çağırır yani şuna dönüşür:
# countdown_object.__iter__(4)
# Yani Countdown.__iter__()'in görevi iterator objesini döndürmek.
# Iterator olan class'ta da __iter__() olmalı çünkü iterator next() ile ilerler (__next__()) ama aynı zamanda
# iter(it) çağrıldığında kendisini döndürmelidir.

# MEALEN:
# Countdown.__iter__ = iterator üret der
# CountdownIterator.__iter__() = ben zaten iteratorum kendimi ver der