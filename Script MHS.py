import matplotlib.pyplot as plt          # Importando a biblioteca matplotlib.pyplot e dando o apelido de plt para a plotagem do gráfico.
from scipy.optimize import curve_fit     # Importando a biblioteca scipy.optimize para o ajuste de curva e cálculo dos parâmetros fixos da curva.
import numpy as np                       # Importando a biblioteca numpy e dando o apelido de np, que possui várias funcionalidades matemáticas.
from sklearn.metrics import r2_score     # Importando a biblioteca sklearn.metrics para calcular o R².
import sys                               # Importando a biblioteca sys, que permite o uso da funcionalidade sys.exit(0).

m = []           # Declarando o vetor que armazenará os dados de massa.
t = []           # Declarando o vetor que armazenará os dados de tempo para x ciclos.
T = []           # Declarando o vetor que armazenará os dados de periodo médio ao quadrado.
T_ajustado = []  # Declarando o vetor que armazenará os dados de periodo médio ao quadrado obtidos a partir dos dados de parâmetros fixos na equação y.

N = int(input('Quantas molas foram utilizadas? '))  # Pedindo para o usuário informar quantas molas foram usadas.

if N != 1:
    associação_de_molas = int(input('Qual foi a associação das molas (1 para série ou 2 para paralelo)? '))  # Pedindo para o usuário informar qual a associação das molas usadas.
    if associação_de_molas !=1 and associação_de_molas !=2: # Se o número de molas for diferente de 1 e 2, então:
        print('Valor inválido! Reinicie o código e digite um valor válido')   # Avisa o usuário que o valor informado não é válido e pede para reiniciar o código.
        sys.exit(0) # Se essa linha for compilada, finaliza-se a execução do código aqui.

n = int(input('Quantas massas diferentes foram utilizados? '))  # Pedindo para o usuário informar quantos valores de massas foram usados.
  
num_de_ciclos = int(input('Quantos ciclos foram realizados em um periodo de tempo? '))   # Pedindo para o usuário informar quantos ciclos foram contabilizados para medição do tempo.
 
for i in range(0, n):  # Loop até coletar a quantidade de dados informado pelo usuário.
    m.append(float(input('Informe a ' +str(i+1)+ 'ª massa utilizada (em quilogramas)? ')))  # Pedindo para o usuário informar as massas utilizadas.
    t.append(float(input('Qual foi o tempo de ' +str(num_de_ciclos)+ ' ciclos com a '  +str(i+1)+ 'ª massa? ')))   # Pedindo para o usuário informar o tempo medido em x ciclos com a massa informada anteriormente.
    T.append((t[i]/num_de_ciclos)**2)  # Calculando a força peso que será igual à força elástica, no caso da massa estar pendurada na perpendicular.

def y(m,K,a):   # Criando a função com a equação de MHS "linearizada" adicionado o termo 'a' para uma linha de tendência mais precisa.
    return 4*(np.pi**2)*m/K + a    

fig, ax = plt.subplots(figsize = (9,6)) # Definindo o tamanho do gráfico para melhor visualização.
xData = np.array(m)  # Colocando as variáveis de massa nos dados do eixo x.
yData = np.array(T)  # Colocando as variáveis de período médio ao quadrado nos dados do eixo y.
plt.axis(ymin=0, ymax=(T[(n-1)])*1.1, xmin=0, xmax=(m[(n-1)])*1.1)   # Definindo os valores limites dos eixos do gráfico.

if N == 1:  # Se há apenas uma mola, o título do gráfico será o texto entre aspas simples a seguir:
    plt.title('Movimento Harmônico Simples (Com uma mola)')
elif associação_de_molas == 1:  # Se há associação em série de molas, o título do gráfico será o texto entre aspas simples a seguir:
    plt.title('Movimento Harmônico Simples (Associação em série)')
else: # Se há associação em paralelo de molas, o título do gráfico será o texto entre aspas simples a seguir:
    plt.title('Movimento Harmônico Simples (Associação em paralelo)')
    
plt.plot(xData, yData, 'bo', label='Dados') # Plotando valores informados pelo usuário.

popt, pcov = curve_fit(y, xData, yData)  # Calculando parâmetros fixos por meio da função da linha 29 e 30.
xFit = np.arange(0.0, ((m[(n-1)])*2), 0.1) # Definindo o tamanho e o intervalo da curva de tendência.
b = 4*(np.pi**2)*(1/popt[0])  # Calculando o coeficiente linear.
    
for i in range(0, n):  # As linhas 49 e 50 serão responsáveis pelo cálculo do período médio ao quadrado com os dados dos parâmetros fixos calculados e inseridos na equação y.
    T_ajustado.append(4*(np.pi**2)*m[i]/popt[0] + popt[1])
    
r2 = r2_score(T_ajustado, T) # A partir dos dados de período médio ao quadrado informados pelo usuário, compara-se estatisticamente com o período médio ao quadrado obtido pelos parâmetros fixos estimados pelo script, obtendo-se o R², onde 1 representa uma compatibilidade perfeita entre dados experimentais e os estimados, já 0 representa uma incompatibilidade total entre eles.

if N == 1: # Se só se utilizou uma mola, há apenas uma constante elástica, portanto, se utiliza K.
    plt.plot(xFit, y(xFit, *popt), 'r', label=f'Parâmetro de ajuste: m/K={b:.5f} kg*m/N, a={popt[1]:.5f} s²\nEquação: T² = 4*π²*m/K + a\nR² = {r2:.5f} \nConstante da mola K={popt[0]:.5f} N/m') # Plotando valores calculados no ajuste de curva e R².
else: # Se utilizou uma associação de molas, há uma constante elástica equivalente, portanto, se utiliza K_eq.
    plt.plot(xFit, y(xFit, *popt), 'r', label=f'Parâmetro de ajuste: m/K={b:.5f} kg*m/N, a={popt[1]:.5f} s²\nEquação: T² = 4*π²*m/K_eq. + a\nR² = {r2:.5f} \nConstante equivalente da mola K={popt[0]:.5f} N/m') # Plotando valores calculados no ajuste de curva e R².
    
plt.xlabel('m (kg)') # Título da eixo x.
plt.ylabel('T² (s²)') # Título da eixo y.
plt.legend() # Exibição da legenda.
plt.show() # Exibição do gráfico.