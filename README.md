# Algoritmos de Ordenação - QuickSort

Este projeto contém implementações do algoritmo QuickSort em Python e C, permitindo análises comparativas de desempenho entre as duas linguagens.

## Estrutura do Projeto

```
.
├── input/              # Diretório para arquivos de entrada
├── output/             # Diretório para arquivos de saída
├── quicksort.py        # Implementação do QuickSort em Python
├── quicksort.c         # Implementação do QuickSort em C
├── gerador_numeros.py  # Gerador de números aleatórios
├── Makefile            # Script de compilação para o código C
└── README.md           
```

## Como Usar

### 1. Gerando Números Aleatórios

Para gerar um arquivo com números aleatórios:

```bash
python/python3 gerador_numeros.py <tamanho_da_lista> [nome_arquivo]
```

Exemplo:
```bash
python/python3 gerador_numeros.py 1000 entrada
```

Observações:
- Se não especificar o nome do arquivo, será usado "entrada.txt"
- A extensão .txt será adicionada automaticamente se não for fornecida
- Os números gerados estão no intervalo de 1 a 1.000.000
- O arquivo será salvo no diretório `input/`

### 2. Executando o QuickSort em Python

```bash
python/python3 quicksort.py <arquivo_entrada>
```

Exemplo:
```bash
python/python3 quicksort.py entrada.txt
```

O resultado será salvo em `output/entrada_out.txt`

### 3. Executando o QuickSort em C

Primeiro, compile o programa:
```bash
make clean && make
```

Depois execute:
```bash
./quicksort <arquivo_entrada>
```

Exemplo:
```bash
./quicksort entrada.txt
```

O resultado será salvo em `output/entrada_out.txt`

## Formato dos Arquivos

- **Arquivo de Entrada**: Números inteiros separados por vírgula (ex: "1,5,2,8,3")
- **Arquivo de Saída**: Mesmos números ordenados, separados por vírgula (ex: "1,2,3,5,8")

## Medição de Tempo

Ambas as implementações mostram:
- Tempo de leitura do arquivo
- Tempo do algoritmo QuickSort
- Tempo de escrita do arquivo
- Tempo total de execução

## Exemplo de Uso Completo

```bash
# Gera um arquivo com 1000 números
python/python3 gerador_numeros.py 1000 teste

# Ordena usando Python
python/python3 quicksort.py teste.txt
# Resultado em output/teste_out.txt

# Compila e ordena usando C
make clean && make
./quicksort teste.txt
# Resultado em output/teste_out.txt
