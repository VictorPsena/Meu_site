import matplotlib.pyplot as plt
import numpy as np

## Curva 1
x1 = [1,2,5,6,7,8,10,13,17]
y1 = [3,3.7,3.9,4.2,5.7,6.6,7.1,6.7,4.5]
df1= [1,-0.67]
## Curva 2
x2 = [17,20,23,24,25,27,27.7]
y2 = [4.5,7,6.1,5.6,5.8,5.2,4.1]
df2= [3,-4]

## Curva 3
x3 = [27.7,28,29,30]
y3 = [4.1,4.3,4.1,3]
df3 = [0.33,-1.5]


A = []
B = []
xs = []
h = []
x = [x1,x2,x3]
y = [y1,y2,y3]
df = [df1,df2,df3]
for i in range(len(x)):
  ni = len(x[i])
  A.append(np.eye(ni))
  B.append(np.zeros(ni))
  xs.append(np.zeros(ni))
  h.append(np.zeros(ni-1))
for val in range(len(x)):
  for i in range(len(x[val])-1):
    h[val][i] = x[val][i+1]-x[val][i]

for val in range(len(x)):
  ############### Para o Spline Fixado.
  A[val][0,0] = 2*h[val][0]
  A[val][0,1] = h[val][0]
  A[val][-1][-1] = 2*h[val][-1]
  A[val][-1][-2] = h[val][-1]
  B[val][0] = (3/h[val][0])*(y[val][1] - y[val][0]) - 3*df[val][0]
  B[val][-1] = 3*df[val][1] - 3/(h[val][-1])*(y[val][-1] - y[val][-2])
  ###############
  for i in range(1,len(x[val])-1):
    A[val][i,i] = 2*(h[val][i-1]+h[val][i])
    A[val][i,i-1] = h[val][i-1]
    A[val][i,i+1] = h[val][i]
    B[val][i] = (3/h[val][i])*(y[val][i+1]-y[val][i]) - (3/h[val][i-1])*(y[val][i]-y[val][i-1])


c = []

bs = []
ds = []
divs =[]
for i in range(len(x)):
  c.append(np.linalg.inv(A[i])@B[i])
for val in range(len(x)):
  b = []
  d = []
  for i in range(len(x[val])-1):
    b.append((1/h[val][i])*(y[val][i+1]-y[val][i])-(h[val][i]/3)*(2*c[val][i] + c[val][i+1]))
    d.append((c[val][i+1]- c[val][i])/(3*h[val][i]))
    div = np.linspace(x[val][i],x[val][i+1],10)
  divs.append(div)
  bs.append(b)
  ds.append(d)

zs = []
for val in range(len(x)):
    curve_z = []
    for i in range(len(x[val])-1):
        # Cria 10 pontos entre cada par x[i] e x[i+1]
        curve_z.extend(np.linspace(x[val][i], x[val][i+1], 10))
    zs.append(np.array(curve_z).reshape(-1, 1))


Ss = []
for val in range(len(x)):
    n = len(x[val])
    S = []
    for j in range(len(zs[val])):
      val_z = zs[val][j][0]
      intervalo_encontrado = False
      for i in range(n-1):
          if (i == n-2 and val_z >= x[val][i] and val_z <= x[val][i+1]) or (i < n-2 and val_z >= x[val][i] and val_z < x[val][i+1]):
              S.append(y[val][i] + bs[val][i]*(val_z-x[val][i]) + c[val][i]*(val_z-x[val][i])**2 + ds[val][i]*(val_z-x[val][i])**3)
              intervalo_encontrado = True
              break

      if not intervalo_encontrado:
        if val_z < x[val][0]:
            S.append(y[val][0] + bs[val][0]*(val_z-x[val][0]) + c[val][0]*(val_z-x[val][0])**2 + ds[val][0]*(val_z-x[val][0])**3)
        else:
            S.append(y[val][n-2] + bs[val][n-2]*(val_z-x[val][n-2]) + c[val][n-2]*(val_z-x[val][n-2])**2 + ds[val][n-2]*(val_z-x[val][n-2])**3)
    Ss.append(S)


for i in range(len(x)):
  plt.plot(x[i], y[i], 'o', label=f'Pontos Originais {i+1}')
  plt.plot(zs[i], Ss[i], '-', label=f'Spline Cúbico Natural {i+1}')
plt.legend(fontsize = '6')
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, linestyle ='--')
plt.show()