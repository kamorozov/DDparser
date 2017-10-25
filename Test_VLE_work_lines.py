import matplotlib.pyplot as plt
x = []
y =[]
for i in range(0, 101):
    x.append(i / 100)
    # benzene - toluene
    y_i = - 0.4191 * (i/ 100) ** 4 + 1.5087 * (i/ 100) ** 3 - 2.3858 * (i/ 100) ** 2 + 2.2951 * (i/ 100) + 0.0005
    y.append(y_i)
plt.plot([0, 1], [0, 1])
plt.plot(x, y)
F = 1
x_f = 0.555
y_f = - 0.4191 * x_f ** 4 + 1.5087 * x_f ** 3 - 2.3858 * x_f ** 2 + 2.2951 * x_f + 0.0005
x_1d = 0.999
x_1w = 1 - x_1d
D = F * (x_f - x_1w)/(x_1d - x_1w)
f = F / D
Rmin = (x_1d - y_f) / (y_f - x_f)
R = Rmin * 1.3
x_work = []
y_work = []
for j in range(1, 999):
    x_work.append(j / 1000)
    if j / 1000 <= x_f:
        y_work_down = (R + f) / (R + 1) * j / 1000 - (1 - f) / (R + 1) * x_1w
        y_work.append(y_work_down)
    elif j / 1000 >= x_f:
        y_work_up = R / (R + 1) * j / 1000 + x_1d / (R + 1)
        y_work.append(y_work_up)
plt.plot(x_work, y_work)
plt.axis([0, 1, 0, 1])
plt.show()