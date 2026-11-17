# funções para a aplicação do método
import numpy as np

## Funções secundárias
def maior_pivo(matriz: np.array, linha: int) -> tuple[np.array, float]:
    indice = np.argmax(np.abs(matriz[linha:, linha])) # pega todas as linhas na coluna e ve o indice do maior valor;
    #para matriz tridiagonal aqui muda para np.argmax(matriz[linha:linha+2, linha])
    indice_pivo = linha + indice

    matriz[[linha, indice_pivo]] = matriz[[indice_pivo, linha]] # Troca de linhas
    pivo = matriz[linha, linha]

    return matriz, pivo


## Funções primárias
def gauss_decrescente(matriz: np.array) -> np.array:

    # verificando se é matriz quadrada
    arr = np.delete(matriz, -1, axis=1)
    if arr.shape[0] != arr.shape[1]:
        return print('Matriz incompatível')
    
    for i in range(len(matriz)): # fixa a linha de 0 até n-1
        # Selecionando o pivô
        matriz, pivo = maior_pivo(matriz, i)
        if np.isclose(pivo, 0):
            raise ValueError("Matriz singular")
        # matriz = np.column_stack((matriz_pivo, b))

        for j in range(i+1,len(matriz)): # Faz as contas em cada linha de 1 até n-1
            # para matriz tridiagonal aqui muda para i+1 sem o for.
            # Calculando as linhas
            matriz[j] = matriz[j] - (matriz[j,i]/pivo)*matriz[i]

    return matriz

def gauss_crescente(matriz: np.array) -> tuple[np.array, np.array]:
    n = len(matriz)
    x = np.zeros(n)
    b = matriz[:,-1]
    matriz = np.delete(matriz, -1, axis=1)

    for i in range(n-1, -1, -1):
        soma = 0
        for j in range(i+1, n):
            soma += matriz[i,j]*x[j]
        x[i] = (1/matriz[i, i])*(b[i] - soma)
         



    return x


# matrix = np.array([[4,2,6],[5,5,3]])
# arr, pivo = maior_pivo(matriz=matrix, linha=0)
# print(arr)
# print(pivo)

# matrix = np.array([[1,2,6,3],[5,5,3,5],[1,2,3,5]])
# matrix = np.array([[4,5,0,0,2],[5,6,7,0,5],[0,4,8,9,8],[0,0,7,9,10]])
# arr = gauss_decrescente(matrix)
# print(arr)

# x = gauss_crescente(arr)
# print(x)