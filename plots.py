import matplotlib.pyplot as plt

plt.plot([0,0.5,1,1.5,2,2.5,3,3.5,4], [18,17,16,13,19,18,16,14,18], '-bo')
plt.axis([0, 4, 0, 20])
plt.ylabel('Equilibrium time')
plt.xlabel('Centralization')
plt.show()