# Análise Comparativa: QuickSort em Python e C

Este projeto realiza uma análise comparativa do algoritmo QuickSort implementado em Python e C, medindo e comparando o desempenho das duas implementações com diferentes tamanhos de entrada.

## Estrutura do Projeto

```
.
├── input/                  # Diretório com arquivos de entrada
│   ├── entrada_1.txt      # Arquivos com números para ordenação
│   └── ...
├── output/                # Diretório com resultados da ordenação
│   ├── entrada_1_out.txt  # Arquivos com números ordenados
│   └── ...
├── log/                   # Diretório com logs de execução
│   ├── log_10000.txt     # Log para entradas de tamanho 10000
│   ├── log_100000.txt    # Log para entradas de tamanho 100000
│   └── log_1000000.txt   # Log para entradas de tamanho 1000000
├── analysis/             # Diretório com gráficos e análises
│   ├── analysis_10000/   # Análises para entradas de tamanho 10000
│   ├── analysis_100000/  # Análises para entradas de tamanho 100000
│   ├── analysis_1000000/ # Análises para entradas de tamanho 1000000
│   ├── tempo_medio.png   # Gráfico de tempo médio por tamanho
│   ├── desvio_padrao.png # Gráfico de desvio padrão por tamanho
│   ├── mediana.png      # Gráfico de mediana por tamanho
│   ├── minimo.png       # Gráfico de mínimo por tamanho
│   ├── maximo.png       # Gráfico de máximo por tamanho
│   ├── amplitude.png    # Gráfico de amplitude por tamanho
│   └── speedup.png      # Gráfico de speedup por tamanho
├── quicksort.py         # Implementação do QuickSort em Python
├── quicksort.c          # Implementação do QuickSort em C
├── performance_test.py  # Script de teste de performance
└── analysis.py         # Script de análise e geração de gráficos
```

## Requisitos

- Python 3.x
- GCC (Compilador C)
- Bibliotecas Python:
  - matplotlib
  - numpy
  - pandas

## Como Usar

1. **Compilar o código C**:
   ```bash
   make clean && make
   ```

2. **Gerar arquivos de entrada**:
   ```bash
   python input_generator.py
   ```

3. **Executar os testes de performance**:
   ```bash
   python performance_test.py
   ```
   Este comando irá:
   - Executar o QuickSort em Python e C para cada arquivo de entrada
   - Gerar logs com os tempos de execução no diretório `log/`
   - Criar um arquivo de log separado para cada tamanho de entrada

4. **Gerar análises e gráficos**:
   ```bash
   python analysis.py
   ```
   Este comando irá:
   - Processar os logs gerados
   - Criar gráficos comparativos no diretório `analysis/`
   - Gerar análises específicas para cada tamanho de entrada

## Gráficos Gerados

1. **Por tamanho de entrada** (em `analysis/analysis_<tamanho>/`):
   - `execution_times.png`: Comparação dos tempos de execução Python vs C para cada arquivo

2. **Comparativos gerais** (em `analysis/`):
   - `tempo_medio.png`: Tempo médio de execução por tamanho
   - `desvio_padrao.png`: Desvio padrão dos tempos por tamanho
   - `mediana.png`: Mediana dos tempos por tamanho
   - `minimo.png`: Tempo mínimo por tamanho
   - `maximo.png`: Tempo máximo por tamanho
   - `amplitude.png`: Amplitude dos tempos por tamanho
   - `speedup.png`: Speedup (Python/C) por tamanho

## Formato dos Arquivos

1. **Arquivos de entrada** (`input/entrada_*.txt`):
   - Números inteiros separados por vírgula
   - Sem espaços entre os números

2. **Arquivos de saída** (`output/entrada_*_out.txt`):
   - Números ordenados separados por vírgula
   - Mesmo formato dos arquivos de entrada

3. **Arquivos de log** (`log/log_<tamanho>.txt`):
   - Tempos de execução para cada arquivo
   - Estatísticas por linguagem (Python e C)
   - Speedup calculado para cada caso

## Implementações

Ambas as implementações (Python e C) usam a mesma estratégia do QuickSort:
- Pivô: último elemento
- Particionamento: elementos menores à esquerda, maiores à direita
- Recursão: ordenação das duas partições

## Análise de Performance

O script gera análises detalhadas comparando:
- Tempo de execução por arquivo
- Métricas estatísticas (média, desvio padrão, mediana, etc.)
- Speedup entre as implementações

Os gráficos permitem visualizar:
- Diferenças de performance entre Python e C
- Comportamento com diferentes tamanhos de entrada
- Variabilidade dos tempos de execução
