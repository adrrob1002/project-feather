import math

b = 150  # dim in mm
a = 2500  # dim
t = 0.8  # sheet thickness
t1 = 1.5  # stringer thickness
Area_stringer = 20 * 1.5 + 18.5 * 1.5  # in mm^2
Area_sheetX = 148.4 * 0.8
Area_sheetY = 40 * 0.8
mass = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
holes = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
bolt = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

webs = [[[]] * 8] * 8

# alu-maximum properties
E = 71.7 * 10 ** 9
yield_stress = 345 * 10 ** 6  # Pa
ult_stress = 483 * 10 ** 6  # Pa
density = 2780  # kg/m^3
rows = 2400
cols = 5

# neutral axis position, second area moment of inertia, no of stringers,
# first area moment of inertia,
# cross-secton mass per meter,stringer positioning
properties = [[75, 1671501.97, 4, 13114, 1.150, "ALL stringers"],
              [63.8635, 1353612.75, 3, 22733, 0.9888, "Top right missing"],
              [86.1635, 1353612.75, 3, 22733, 0.9888, "Bottom left missing"],
              [75, 1125021, 2, 22733, 0.83, "Top right and bottom left missing"]]

spacing_bolts = rows * [cols * [0.0]]  # column-section type row-position across the beam
spacing_webs = rows * [cols * [0.0]]  # in mm
spacing_webs_with_hole = rows * [cols * [0.0]]  # in mm

moment_stress = rows * [cols * [0.0]]
moment_stress_comp = rows * [cols * [0.0]]
shear_stress = [0, 0, 0, 0, 0]
Ks = [0, 0, 0, 0, 0]  # shear buckling coefficient
# for the first part of the beam from 0 to 0.72m
V = 1595  # shear force in Newtons
M = 1675  # moment in Newtons
k = 4  # buckling coefficient
Kt = 4.1
weight_per_hole = 0.0027947

for j in range(0, 4):
    shear_stress[j] = V * properties[j][3] / (properties[j][1] * 0.8) * 1000 * 2
    Ks[j] = (shear_stress[j] / E) / ((0.8 / 150) ** 2)

for i in range(72):
    M = 1675 - (V * i) / 100
    for j in range(4):
        moment_stress[i][j] = (M * abs(properties[j][0] - 150) / 1000) / properties[j][1] * 1000 * 4
        moment_stress_comp[i][j] = M * (150 - properties[j][0]) / properties[j][1] * 1000 * 3
        spacing_webs[i][j] = math.sqrt(k * 3.145 * 2 * E / (12 * (1 - 0.33 ** 2) * moment_stress_comp[i][j]))
        spacing_webs_with_hole[i][j] = spacing_webs[i][j] / math.sqrt(Kt)
        spacing_bolts[i][j] = math.sqrt((0.9 * 3.5 * E * ((t + t1) / 1000) ** 2) / moment_stress_comp[i][j]) * 1000
# for j in range (0,4):
# print(properties[j][5],Ks[j])
# for i in range (0,73):
# print(i,"cm",moment_stress[i][j],moment_stresscomp[i][j],shear_stress[j],spacing_bolts[i][j],spacing_webs[i][j],spacing_webs_with_hole[i][j])
for j in range(0, 4):
    length = 0
    poz = 0
    weight = 0
    no_holes_total = 0
    ok = 0
    no_bolts_total = 0
    nr = 0
    for i in range(0, 72, 10):
        print(i)
        if i > poz / 10 or poz == 0:
            ok = 0

            mom = max(moment_stress[i][j], moment_stress_comp[i][j])
            if mom > yield_stress:
                ok = 1
            if 7.66 < Ks[j] < 8:
                ratio = 1.4
            elif Ks[j] > 11:
                ratio = 1
                length = 150 * ratio
            if poz + length > 720:
                length = 720 - poz
                poz = 720
            else:
                poz += length
            weight += (length * properties[j][4]) / 1000
            nr += 1
            webs[j][1].append(length)
            bolts = int(length / (spacing_bolts[i][j] - 10))
            if spacing_bolts[i][j] > length:
                bolts = 1
            no_bolts_total += bolts * 3
            no_holes_possible = int((length - 15) / 55)
            if mom * Kt < yield_stress and spacing_webs_with_hole[i][j] > 40:
                no_holes_total += no_holes_possible
    webs[j][1][0] = nr
    weight += no_bolts_total * (2.33 / 1000)
    weight -= no_holes_total * weight_per_hole
    mass[j][1] = weight
    holes[j][1] = no_holes_total
    bolt[j][1] = no_bolts_total
    # print(weight,no_holes_total,no_bolts_total,j)
# print("RUNDA 2")

# for part 2
rows = 2400
cols = 5
properties = [[75, 1671501.97, 4, 13114, 1.150, "ALL stringers"],
              # neutral axis position, second area moment of inertia, no of stringers, first area moment of inertia,cross-secton mass per meter,stringer positioning
              [63.8635, 1353612.75, 3, 22733, 0.9888, "Top right missing"],
              [86.1635, 1353612.75, 3, 22733, 0.9888, "Bottom left missing"],
              [75, 1125021, 2, 22733, 0.83, "Top right and bottom left missing"]]

spacing_bolts = rows * [cols * [0.0]]  # column-section type row-position across the beam
spacing_webs = rows * [cols * [0.0]]  # in mm
spacing_webs_with_hole = rows * [cols * [0.0]]  # in mm

moment_stress = rows * [cols * [0.0]]
moment_stress_comp = rows * [cols * [0.0]]
shear_stress = [0, 0, 0, 0, 0]

Ks = [0, 0, 0, 0, 0]  # shear buckling coefficient
V = 454  # shear force in Newtons
M = 526.44  # moment in Newtons
k = 4  # buckling coefficient
Kt = 4.1
weight_per_hole = 0.0027947
for j in range(0, 4):
    shear_stress[j] = V * properties[j][3] / (properties[j][1] * 0.8) * 1000 * 2
    Ks[j] = (shear_stress[j] / E) / ((0.8 / 150) ** (2))
for i in range(72, 192):
    M = 526.44 - (V * (i - 72)) / 100
    for j in range(0, 4):
        moment_stress[i][j] = abs(M * (abs(properties[j][0] - 150) / 1000) / properties[j][1] * 1000 * 4)
        moment_stress_comp[i][j] = abs(M * (150 - properties[j][0]) / properties[j][1] * 1000 * 3)
        spacing_webs[i][j] = math.sqrt(k * 3.145 * 2 * E / (12 * (1 - 0.33 ** 2) * abs(moment_stress_comp[i][j])))
        spacing_webs_with_hole[i][j] = spacing_webs[i][j] / math.sqrt(Kt)
        spacing_bolts[i][j] = math.sqrt((0.9 * 3.5 * E * ((t + t1) / 1000) ** 2) / moment_stress_comp[i][j]) * 1000
# for j in range (0,4):
# print(properties[j][5],Ks[j])
# for i in range (72,192):
# print(i,"cm",moment_stress[i][j],moment_stresscomp[i][j],shear_stress[j],spacing_bolts[i][j],spacing_webs[i][j],spacing_webs_with_hole[i][j])
for j in range(0, 4):
    length = 0
    poz = 720
    weight = 0
    no_holes_total = 0
    ok = 0
    no_bolts_total = 0
    nr = 0
    for i in range(72, 192, 10):
        if i > poz / 10 or poz == 0:
            ok = 0

            mom = max(moment_stress[i][j], moment_stress_comp[i][j])
            if mom > yield_stress:
                ok = 1
            if Ks[j] < 5.1:
                ratio = 3
            elif Ks[j] > 11:
                ratio = 1
            elif Ks[j] > 5.5:
                ratio = 3.5
                length = 150 * ratio
            if poz + length > 1920:
                length = 1920 - poz
                poz = 1920
            else:
                poz += length
            nr += 1
            webs[j][2].append(length)
            weight += (length * properties[j][4]) / 1000
            bolts = int(length / (spacing_bolts[i][j] - 10))
            if spacing_bolts[i][j] > length:
                bolts = 1
            no_bolts_total += bolts * 3
            no_holes_possible = int((length - 15) / 55)
            if mom * Kt < yield_stress and spacing_webs_with_hole[i][j] > 40:
                no_holes_total += no_holes_possible
    webs[j][2][0] = nr
    weight += no_bolts_total * (2.33 / 1000)
    weight -= no_holes_total * weight_per_hole
    mass[j][2] = weight
    holes[j][2] = no_holes_total
    bolt[j][2] = no_bolts_total
    # print(weight,no_holes_total,no_bolts_total,j)
# for part 3
# print("Runda 3")
rows = 2400
cols = 5
properties = [[75, 1671501.97, 4, 13114, 1.150, "ALL stringers"],
              # neutral axis position, second area moment of inertia, no of stringers, first area moment of inertia,cross-secton mass per meter,stringer positioning
              [63.8635, 1353612.75, 3, 22733, 0.9888, "Top right missing"],
              [86.1635, 1353612.75, 3, 22733, 0.9888, "Bottom left missing"],
              [75, 1125021, 2, 22733, 0.83, "Top right and bottom left missing"]]

spacing_bolts = rows * [cols * [0.0]]  # column-section type row-position across the beam
spacing_webs = rows * [cols * [0.0]]  # in mm
spacing_webs_with_hole = rows * [cols * [0.0]]  # in mm

moment_stress = rows * [cols * [0.0]]
moment_stress_comp = rows * [cols * [0.0]]
shear_stress = [0, 0, 0, 0, 0]

Ks = [0, 0, 0, 0, 0]  # shear buckling coefficient
V = 55  # shear force in Newtons
M = -18.29  # moment in Newtons
k = 4  # buckling coefficient
Kt = 4.1
weight_per_hole = 0.0027947
for j in range(0, 4):
    shear_stress[j] = V * properties[j][3] / (properties[j][1] * 0.8) * 1000 * 2
    Ks[j] = (shear_stress[j] / E) / ((0.8 / 150) ** (2))
for i in range(192, 226):
    M = (V * (i - 192)) / 100 - 18.29
    for j in range(0, 4):
        moment_stress[i][j] = abs(M * (abs(properties[j][0] - 150) / 1000) / properties[j][1] * 1000 * 4)
        moment_stress_comp[i][j] = abs(M * (150 - properties[j][0]) / properties[j][1] * 1000 * 3)
        spacing_webs[i][j] = math.sqrt(k * 3.145 * 2 * E / (12 * (1 - 0.33 ** 2) * moment_stress_comp[i][j]))
        spacing_webs_with_hole[i][j] = spacing_webs[i][j] / math.sqrt(Kt)
        spacing_bolts[i][j] = math.sqrt((0.9 * 3.5 * E * ((t + t1) / 1000) ** 2) / moment_stress_comp[i][j]) * 1000
# for j in range (0,4):
# print(properties[j][5],Ks[j])
# for i in range (192,226):
# print(i,"cm",moment_stress[i][j],moment_stresscomp[i][j],shear_stress[j],spacing_bolts[i][j],spacing_webs[i][j],spacing_webs_with_hole[i][j])
for j in range(0, 4):
    length = 0
    poz = 1920
    weight = 0
    no_holes_total = 0
    ok = 0
    no_bolts_total = 0
    nr = 0
    for i in range(192, 226, 10):
        if i > poz / 10 or poz == 0:
            ok = 0
            mom = max(moment_stress[i][j], moment_stress_comp[i][j])
            if mom > yield_stress:
                ok = 1
            if Ks[j] < 5.1:
                ratio = 3
            elif Ks[j] > 11:
                ratio = 1
            elif Ks[j] > 5.5:
                ratio = 3.5
                length = 150 * ratio
            if poz + length > 2260:
                length = 2260 - poz
                poz = 2260
            else:
                poz += length
            nr += 1
            webs[j][3][nr] = length
            weight += (length * properties[j][4]) / 1000
            bolts = int(length / (spacing_bolts[i][j] - 10))
            if spacing_bolts[i][j] > length:
                bolts = 1
            no_bolts_total += bolts * 3
            no_holes_possible = int((length - 15) / 55)
            if mom * Kt < yield_stress and spacing_webs_with_hole[i][j] > 40:
                no_holes_total += no_holes_possible
    webs[j][3][0] = nr
    weight += no_bolts_total * (2.33 / 1000)
    weight -= no_holes_total * weight_per_hole
    mass[j][3] = weight
    holes[j][3] = no_holes_total
    bolt[j][3] = no_bolts_total
    # print(weight,no_holes_total,no_bolts_total,j)
print("Final analysis")
for j in range(0, 4):
    mass_t = 0
    bolt_left = 60  # I only calculated the required number of bolts on the compressed side of the beam
    print()
    print()
    print()
    print(j, properties[j][5])
    for i in range(1, 4):
        print("Web partitions", end=' ')
        for k in range(1, webs[j][i][0] + 1):
            print(webs[j][i][k], "mm", end=' ')
        print("Stage", i)
        print("mass  (without the added mass from the leftout bolts)", mass[j][i], "kg", "no of holes", holes[j][i],
              "no of bolts(compresion side)", bolt[j][i])
        bolt_left -= bolt[j][i]
        mass_t += mass[j][i]
    print("total mass (without the added mass from the leftout bolts)", mass_t)
    print("bolts left for the side in tension", bolt_left)
