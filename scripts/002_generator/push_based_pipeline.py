# pull-based -> akışta kontrol tüketicidedir.
# Tüketici next() ister -> upstream bir değer üretir -> değer aşağı iner
# yani böylece veri çekilmiş olur (pull) for x in stream: ...

# push-based akışta kontrol üreticide/producer'dadır. Producer yeni veri geldi der ve:
# - aşağıdaki aşamalara push ile send eder
# - aşamalar bir şey gelince çalış mantığıyla davranır, her aşama bir coroutine-style generator gibi input bekler

# PUSH PIPELINE NASIL KURULUR?
# Aşağıdaki örnekte:
# sink_print() son aşamadır: geleni yazdırır
# filter_error() ara aşamadır: sadece ERROR içeren satırları geçirir
# source_push(lines, target): kaynak; satırları target'a push eder.

def sink_print():
    """Consumes items pushed via .send(item)"""
    try:
        while True:
            item = yield    # bu satırda beklenir; dışarıdan send ile item gelecek
            print("OUT:", item)
    except GeneratorExit:
        return      # Kapatılınca temiz çık


def filter_error(target):
    """Passes through only lines containing 'ERROR'"""
    try:
        while True:
            line = yield            # input bekle
            if "ERROR" in line:
                target.send(line)   # aşağıya push et
    except GeneratorExit:
        target.close()              # zinciri kapat
        return

def source_push(lines, target):
    """Producer pushes items downstream"""
    for line in lines:
        target.send(line)
    target.close()


# Wiring ve çalıştırma
out = sink_print()
next(out)       # prime: ilk yield'e kadar getirir

flt = filter_error(out)
next(flt)       # prime

lines = ["INFO ok", "ERROR boom", "INFO ok2", "ERROR AGAIN"]
source_push(lines, flt)



