# Analise Harmonica: exercicio 3.4 da lista 3

Este arquivo e uma referencia textual local para o exercicio 3.4 de `lista3.pdf`, usando a notacao de `Notas_Harmonica_2026_2.pdf`. Assim, a solucao pode ser consultada sem reabrir os PDFs.

## Enunciado

Sejam `p0 < p < p1`, `1 <= q <= infinito` e `f in L^{p,q}`.

1. Provar que `f = f_L + f_H`, com
   `||f_L||_{L^{p0,infinito}} + ||f_H||_{L^{p1,infinito}} <= C ||f||_{L^{p,q}}`.
2. Usar o item anterior e o lema de Fatou para mostrar que, se `T` e do tipo fraco `(p0,q0)` e `(p1,q1)`, entao T e enumeravelmente subaditivo na classe de Lorentz intermediaria. Completar a passagem de funcoes simples para uma funcao geral na prova do teorema de Hunt, sem supor linearidade.
3. Provar que a estimativa restrita
   `||T chi_E||_{L^{q,infinito}} <= C mu(E)^{1/p}`
   para conjuntos `E` de medida finita, nos pares extremos, e equivalente a
   `||Tf||_{L^{p,infinito}} <= C ||f||_{L^{p,1}}`.

As constantes abaixo dependem apenas dos expoentes; escrevemos `lesssim` para ocultar tais constantes.

## Notacao das notas

Para `p < infinito`,

`||f||*_{p,q} = p^{1/q} || lambda mu({|f| >= lambda})^{1/p} ||_{L^q((0,infinito),d lambda/lambda)}`,

e

`||f||*_{p,infinito} = sup_{lambda>0} lambda mu({|f| >= lambda})^{1/p}`.

As quase-normas com e sem estrela sao equivalentes. O Lema 3.12 das notas fornece uma decomposicao diadica: existem `H_n` decrescentes e conjuntos disjuntos `E_n`, com `mu(E_n) <= 2^n`, tais que, a menos de modificar os valores nos conjuntos de nivel,

`f = sum_n f_n`, `|f_n| <= H_n chi_{E_n}`,

e

`a_n = H_n 2^{n/p}`, `||a||_{ell^q} lesssim ||f||*_{p,q}`.

O caso `q=infinito` significa `sup_n |a_n| lesssim ||f||*_{p,infinito}`.

## 1. Decomposicao em dois extremos fracos

Defina

`f_L = sum_{n<=0} f_n`, `f_H = sum_{n>0} f_n`.

Primeiro normalize `||f||*_{p,q}=1`; o caso geral segue multiplicando a decomposicao por essa norma. Como `|a_n| <= ||a||_{ell^q} <= 1`, temos

`H_n <= 2^{-n/p}`.

### Estimativa de `f_L`

Se `0 < lambda <= H_0`, entao

`mu({|f_L| > lambda}) <= sum_{n<=0} mu(E_n) <= sum_{n<=0}2^n <= 2`,

logo `lambda mu({|f_L| > lambda})^{1/p0} lesssim 1`.

Se `lambda > H_0`, seja `m <= 0` o ultimo indice com `H_m > lambda`. Entao

`mu({|f_L| > lambda}) <= sum_{n<=m}2^n <= 2^{m+1}`

e, como `lambda < H_m <= 2^{-m/p}`, temos `2^m <= lambda^{-p}`. Portanto,

`lambda mu({|f_L| > lambda})^{1/p0} lesssim lambda^{1-p/p0} <= 1`,

pois `p0 < p` e `lambda > H_0`, com `H_0 <= 1`.

Assim, `||f_L||*_{p0,infinito} lesssim 1`.

### Estimativa de `f_H`

Se `lambda > H_1`, o conjunto de nivel e vazio. Se `0 < lambda <= H_1`, seja `m >= 1` o ultimo indice com `H_m > lambda`. Como antes,

`mu({|f_H| > lambda}) <= sum_{1<=n<=m}2^n <= 2^{m+1}`

e `2^m <= lambda^{-p}`. Logo

`lambda mu({|f_H| > lambda})^{1/p1} lesssim lambda^{1-p/p1} <= 1`,

porque `p < p1` e `lambda <= H_1 <= 1`.

Concluimos que `||f_H||*_{p1,infinito} lesssim 1`. Desfazendo a normalizacao,

`||f_L||_{p0,infinito} + ||f_H||_{p1,infinito} lesssim ||f||_{p,q}`.

O ponto essencial e separar os blocos diadicos pelo indice `n=0`, e nao por um corte fixo nos valores de `|f|`. Um corte fixo nao controla a cauda de baixa amplitude em um espaco de medida infinito.

## 2. Subaditividade enumeravel e passagem para funcoes gerais

Suponha que `T` seja sublinear:

`|T(u+v)| <= |T(u)| + |T(v)|`, `|T(cu)| = |c| |T(u)|`.

Para uma soma finita `F_N = sum_{k=1}^N f_k`, aplique o item 1 a cada parcela:

`f_k = f_{k,L} + f_{k,H}`.

Entao

`|T(F_N)| <= sum_{k=1}^N |T(f_{k,L})| + sum_{k=1}^N |T(f_{k,H})|`.

As hipoteses de tipo fraco nos extremos dao

`||T(f_{k,L})||_{L^{q0,infinito}} lesssim ||f_{k,L}||_{L^{p0,infinito}}`,

`||T(f_{k,H})||_{L^{q1,infinito}} lesssim ||f_{k,H}||_{L^{p1,infinito}}`.

Aplicando a quase-desigualdade triangular de Lorentz as somas finitas e depois o item 1, obtem-se a estimativa necessaria para `F_N`. Em particular, a constante nao depende de `N`.

Para a soma infinita, ponha `F_N = sum_{k=1}^N f_k`. A sublinearidade fornece, para cada soma finita,

`|T(F_N)| <= G_N`, `G_N = sum_{k=1}^N |T(f_k)|`.

As funcoes `G_N` crescem pontualmente para `G = sum_{k=1}^infinito |T(f_k)|`. O Lema de Fatou aplicado a

`lambda -> lambda mu({|T(F_N)| > lambda})^{1/q}`

permite passar ao limite, depois de usar a definicao de `T(sum f_k)` como o limite apropriado das somas finitas (ou a desigualdade sublinear diretamente com o resto). Assim,

`||T(sum_{k=1}^infinito f_k)|| <= sum_{k=1}^infinito ||T(f_k)||`,

com a interpretacao de quase-norma e a constante da quase-triangularidade de Lorentz. Este e o detalhe que evita aplicar diretamente a desigualdade triangular a uma soma infinita.

### Extensao de simples para `f in L^{p,q}`

Escolha funcoes simples `s_j` tais que `||f-s_j||_{L^{p,q}} -> 0` (por truncacao dos valores e do suporte). Escreva

`f = s_j + (f-s_j)`.

Sublinearidade fornece

`|Tf| <= |T(s_j)| + |T(f-s_j)|`.

O argumento ja provado para funcoes simples controla o primeiro termo, e a mesma estimativa aplicada ao resto controla o segundo por `C||f-s_j||_{L^{p,q}}`. Fatou, ou primeiro a passagem para somas finitas e depois Fatou, da

`||Tf|| <= C liminf_j ||s_j||_{L^{p,q}} = C||f||_{L^{p,q}}`.

Nenhuma identidade `T(s_j)-T(s_k)=T(s_j-s_k)` foi usada; isso seria ilegitimo sem linearidade. Usa-se somente a desigualdade sublinear para decompor `f` em aproximante mais resto.

## 3. Tipo fraco restrito equivale a `L^{p,1} -> L^{q,infinito}`

### Implicacao facil

Se

`||T chi_E||_{L^{q,infinito}} lesssim mu(E)^{1/p}`

para todo conjunto mensuravel `E` de medida finita, tome `f=chi_E`. Como

`||chi_E||_{L^{p,1}} = mu(E)^{1/p}`,

segue imediatamente que

`||Tf||_{L^{q,infinito}} lesssim ||f||_{L^{p,1}}`

na classe das funcoes caracteristicas.

### Implicacao geral

Comece com uma funcao simples nao-negativa, escrita com niveis diadicos:

`f = sum_k a_k chi_{E_k}`,

onde os `E_k` sao disjuntos, `mu(E_k)<infinito` e `a_k>0`. Pela sublinearidade e homogeneidade,

`|Tf| <= sum_k a_k |T chi_{E_k}|`.

Para uma soma finita, a quase-desigualdade triangular em `L^{q,infinito}` e a hipotese restrita fornecem

`||T(sum_{k=1}^N a_k chi_{E_k})||_{L^{q,infinito}}`
`lesssim sum_{k=1}^N a_k mu(E_k)^{1/p}`.

Agora aplique Fatou as somas parciais. Nao se deve escrever diretamente uma desigualdade triangular para a soma infinita: primeiro controla-se cada soma finita por uma constante independente de `N`, e somente entao passa-se ao limite. Pela caracterizacao atomica de Lorentz,

`||f||_{L^{p,1}} lesssim sum_k a_k mu(E_k)^{1/p}`,

e portanto

`||Tf||_{L^{q,infinito}} lesssim ||f||_{L^{p,1}}`.

Para uma funcao geral `f in L^{p,1}`, escolha simples nao-negativas `f_j` que convergem a `f` em `L^{p,1}` e repita o argumento com `f_j` e o resto `f-f_j`. Fatou conclui a estimativa para `f`. Para funcao complexa, aplique o argumento a `|f|` quando `|T f| <= T(|f|)` (a forma usual da sublinearidade); caso contrario, use a decomposicao em partes real e imaginaria prevista na hipotese sobre `T`.

A necessidade e a sufiencia estao provadas:

`T` e do tipo fraco restrito `(p,q)` em conjuntos de medida finita

se e somente se

`||Tf||_{L^{q,infinito}} lesssim ||f||_{L^{p,1}}`.

## Observacao sobre o teorema de Hunt

Na prova do teorema de Hunt, os pares extremos sao `(p0,q0)` e `(p1,q1)`, e os expoentes intermediarios satisfazem

`1/p = (1-theta)/p0 + theta/p1`,

`1/q = (1-theta)/q0 + theta/q1`.

O item 1 fornece a decomposicao nos dois extremos; o item 2 permite tratar somas e limites sem linearidade; e o item 3 transforma as estimativas em conjuntos caracteristicos na estimativa completa `L^{p,1} -> L^{q,infinito}`. Esses sao precisamente os detalhes omitidos que a lista pede completar.
