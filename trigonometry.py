import math
R = 6371000
S = 36.92
F = 44.77
N = 7
instrument_vysota =[
    (1.35), (1.56), (1.56), (1.50), (1.50), (1.55), (1.55), (1.51), (1.51), (1.33), (1.33), (1.43)
]
navedeniya_vysota = [
    (1.37), (2.51), (1.73), (2.68), (1.54), (1.92), (2.18), (2.84), (2.93), (2.14), (2.89), (2.05)
]
horizont_prolozhenie = [
    (141.69), (141.69), (103.63), (103.63), (114.13), (114.13), (116.41), (116.41), (63.95), (63.95), (118.30), (118.30)
]
circle_right = [
    (-99), (75), (-107), (62), (280), (-292), (-274), (216), (62), (-181), (-162), (97)
]
circle_left = [
    (98), (-77), (105), (-62), (-279), (290), (274), (-216), (-61), (182), (161), (-98)
]

MO = []

for minutes in range(len(circle_right)):
    MO.append(circle_left[minutes] + circle_right[minutes])

MO = [minutes / 2 for minutes in MO]
MO = [minutes / 60 for minutes in MO ]

NU = []

for minutes in range(len(circle_left)):
    NU.append(circle_left[minutes] - circle_right[minutes])

NU = [minutes / 2 for minutes in NU ]
NU = [minutes / 60 for minutes in NU ]

tgNU= []

tgNU = [math.tan(math.radians(degrees)) for degrees in NU]

h_with_apostrofe = []

for i in range(len(tgNU)):
    h_with_apostrofe.append(tgNU[i] * horizont_prolozhenie[i])

h = []

for i in range(len(h_with_apostrofe)):
    h.append(h_with_apostrofe[i] + instrument_vysota[i] - navedeniya_vysota[i])
# блок вывода 1
print('n:', N)
print("Высота инструмента", instrument_vysota)
print('Высота наведения:', navedeniya_vysota)
print("Место нуля:", MO)
print("Угол наклона оси визирования:", NU)
print("Горизонтальные проложения:",horizont_prolozhenie)
print("h':", h_with_apostrofe)
print('Превышения:', h)

#======================Вторая часть===========================
odd_elements = []
even_elements = []

for i in range(len(h)):
    if (i + 1) % 2 == 1:
        odd_elements.append(h[i])
    else:
        even_elements.append(h[i])

sredina = []

for i in range(len(odd_elements)):
    pot = ((odd_elements[i] - even_elements[i]) / 2)
    sredina.append(pot)

prolozhenia = horizont_prolozhenie[::2]

nevyazka_dop = sum(prolozhenia) / (2500 * math.sqrt(7))

nevyazka_fact = sum(sredina) - (F - S)

def popravki_proportional(lengths, nevyazka):

    total_length = sum(lengths)
    if total_length == 0:
        return [0] * len(lengths)

    corrections = []
    for length in lengths:
        correction = -nevyazka * (length / total_length)
        corrections.append(correction)

    return corrections
popravki = popravki_proportional(prolozhenia, nevyazka_fact)

ispravlennye_sredina = []

for i in range(len(sredina)):
    corrected = sredina[i] + popravki[i]

    ispravlennye_sredina.append(round(corrected, 2))

vysoty_punktov = []
vysoty_tekuschie = S

for i in range(len(ispravlennye_sredina)):
    vysoty_tekuschie += ispravlennye_sredina[i]
    vysoty_punktov.append(round(vysoty_tekuschie, 2))
# блок вывода 2
print("Прямые превышения:", odd_elements)
print("Обратные превышения:", even_elements)
print("Средние превышения:", (sredina))
print("Допустимая невязка:", (nevyazka_dop))
print("Фактическая невязка:", (nevyazka_fact))
if abs(nevyazka_fact) <= nevyazka_dop:
    print("  Невязка удовлетворяет условию: |fh| ≤ fhдоп ")
else:
    print("  Невязка не удовлетворяет условию: |fh| ≤ fhдоп ")
print('Поправки:', popravki)
print('Исправленные превышения:', ispravlennye_sredina)
print('Высоты точек: начальная - 36.92', vysoty_punktov)