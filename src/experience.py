import matplotlib.pyplot as plt

# dendrite fixée nseg =  5 L =  50 diam =  2 insert pas
# variation de la longueur LA axone
L_d = [800, 900, 1000, 1100, 1200, 1300]
Corr1 = [[0.97, 0.97, 0.97, 0.96, 0.95, 0.94],
         [0.87, 0.97, 0.8, 0.7, 0.63, 0.69],
         [0.99, 0.99, 0.99, 0.99, 0.99, 0.99]]

# variation du diamètre DA axone
D_d = [1, 2, 3, 4, 5, 6]
Corr2 = [[0.33, 0.97, 0.72, 0.51, 0.31, 0.29],
         [0, 0.8, 0.15, 0, 0, 0],
         [0.87, 0.99, 0.97, 0.92, 0.61, 0.56]]

# axone fixé nseg = 100 L = 1000 diam =  2 insert hh
# variation de la longueur LD dendrite
L_a = [30, 50, 70, 80, 100, 130]
Corr3 = [[0.97, 0.97, 0.96, 0.96, 0.93, 0.89],
         [0.79, 0.8, 0.82, 0.51, 0, 0],
         [0.99, 0.99, 0.99, 0.99, 0.99, 0.99]]

# axone fixé nseg = 100 L = 1000 diam =  2 insert hh
# variation du diamètre DD dendrite
D_a = [1, 2, 3.01, 4, 5, 6, 7]
Corr4 = [[0.97, 0.97, 0.97, 0.96, 0.95, 0.94, 0.92],
         [0.78, 0.8, 0.82, 0.8, 0.56, 0.32, 0.14],
         [0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99]]

plt.figure(1)
plt.subplot(211)
plt.plot(L_d, Corr1[0], 'o', label = 'Moyenne')
plt.plot(L_d, Corr1[1], 'o', label = 'Minimum')
plt.plot(L_d, Corr1[2], 'o', label = 'Maximum')
plt.grid()
plt.xlabel("Longueur d'axone µm")
plt.ylabel("Corrélation")
plt.legend()

plt.subplot(212)
plt.plot(L_d, Corr2[0], 'o', label = 'Moyenne')
plt.plot(L_d, Corr2[1], 'o', label = 'Minimum')
plt.plot(L_d, Corr2[2], 'o', label = 'Maximum')
plt.grid()
plt.xlabel("Diamètre d'axone µm")
plt.ylabel("Corrélation")
plt.legend()
plt.show()

plt.figure(2)
plt.subplot(211)
plt.plot(L_a, Corr3[0], 'o', label = 'Moyenne')
plt.plot(L_a, Corr3[1], 'o', label = 'Minimum')
plt.plot(L_a, Corr3[2], 'o', label = 'Maximum')
plt.grid()
plt.xlabel("Longueur de dendrite µm")
plt.ylabel("Corrélation")
plt.legend()

plt.subplot(212)
plt.plot(D_a, Corr4[0], 'o', label = 'Moyenne')
plt.plot(D_a, Corr4[1], 'o', label = 'Minimum')
plt.plot(D_a, Corr4[2], 'o', label = 'Maximum')
plt.grid()
plt.xlabel("Diamètre de dendrite µm")
plt.ylabel("Corrélation")
plt.legend()
plt.show()
