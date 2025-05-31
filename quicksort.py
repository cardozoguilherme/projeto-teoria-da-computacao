#!/usr/bin/env python3
"""
Implementação do algoritmo QuickSort em Python.

Este módulo implementa o algoritmo de ordenação QuickSort de forma equivalente
à implementação em C.
"""

import sys
import time
import os

def trocar(arr: list, i: int, j: int) -> None:
    """
    Troca dois elementos de posição em um array.
    
    Args:
        arr: Lista onde será feita a troca
        i: Índice do primeiro elemento
        j: Índice do segundo elemento
    """
    arr[i], arr[j] = arr[j], arr[i]

def partition(arr: list, low: int, high: int) -> int:
    """
    Particiona o array usando o último elemento como pivô.
    
    Esta função reorganiza o array de forma que:
    - Elementos menores ou iguais ao pivô ficam à esquerda
    - Elementos maiores que o pivô ficam à direita
    
    Args:
        arr: Lista a ser particionada
        low: Índice inicial da partição
        high: Índice final da partição
    
    Returns:
        int: A posição final do pivô
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            trocar(arr, i, j)
    
    trocar(arr, i + 1, high)
    return i + 1

def quicksort(arr: list, low: int, high: int) -> None:
    """
    Implementação do algoritmo QuickSort.
    
    Ordena o array in-place usando a estratégia de dividir e conquistar:
    1. Escolhe um pivô (último elemento)
    2. Particiona o array em torno do pivô
    3. Recursivamente ordena as duas partições
    
    Args:
        arr: Lista a ser ordenada
        low: Índice inicial da partição
        high: Índice final da partição
    """
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def ler_arquivo(nome_arquivo: str) -> list:
    """
    Lê números de um arquivo, separados por vírgula.
    
    Args:
        nome_arquivo: Nome do arquivo a ser lido (deve estar no diretório input/)
    
    Returns:
        list: Lista de números lidos do arquivo
    
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se o arquivo contiver dados em formato inválido
    """
    caminho = os.path.join('input', nome_arquivo)
    with open(caminho, 'r') as f:
        numeros_str = f.read().strip()
        return [int(x) for x in numeros_str.split(',')]

def salvar_arquivo(arr: list, nome_arquivo: str) -> None:
    """
    Salva números em um arquivo, separados por vírgula.
    
    Args:
        arr: Lista de números a ser salva
        nome_arquivo: Nome do arquivo de saída (será salvo no diretório output/)
    """
    caminho = os.path.join('output', nome_arquivo)
    with open(caminho, 'w') as f:
        f.write(','.join(map(str, arr)))

def gerar_nome_saida(nome_entrada: str) -> str:
    """
    Gera o nome do arquivo de saída baseado no arquivo de entrada.
    
    Args:
        nome_entrada: Nome do arquivo de entrada
    
    Returns:
        str: Nome do arquivo de saída (original + "_out.txt")
    """
    nome_base = os.path.splitext(nome_entrada)[0]
    return f"{nome_base}_out.txt"

def main() -> None:
    """
    Função principal do programa.
    
    Fluxo de execução:
    1. Verifica argumentos da linha de comando
    2. Lê números do arquivo de entrada
    3. Ordena os números usando QuickSort
    4. Salva o resultado em arquivo
    5. Mostra estatísticas de tempo
    """
    if len(sys.argv) < 2:
        print("Uso: python quicksort.py <arquivo_entrada>")
        print("Exemplo: python quicksort.py numeros.txt")
        print("O arquivo deve estar no diretório 'input'")
        print("O resultado será salvo no diretório 'output'")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    arquivo_saida = gerar_nome_saida(arquivo_entrada)
    
    try:
        # Mede tempo de leitura
        tempo_inicio = time.time()
        numeros = ler_arquivo(arquivo_entrada)
        tempo_leitura = (time.time() - tempo_inicio) * 1000  # Converte para ms
        
        # Mede tempo do algoritmo
        tempo_inicio = time.time()
        quicksort(numeros, 0, len(numeros) - 1)
        tempo_algoritmo = (time.time() - tempo_inicio) * 1000  # Converte para ms
        
        # Mede tempo de escrita
        tempo_inicio = time.time()
        salvar_arquivo(numeros, arquivo_saida)
        tempo_escrita = (time.time() - tempo_inicio) * 1000  # Converte para ms
        
        # Calcula e mostra os tempos
        tempo_total = tempo_leitura + tempo_algoritmo + tempo_escrita
        print(f"\nTempos de execução (Python):")
        print(f"Leitura do arquivo: {tempo_leitura:.3f} ms")
        print(f"Algoritmo QuickSort: {tempo_algoritmo:.3f} ms")
        print(f"Escrita do arquivo: {tempo_escrita:.3f} ms")
        print(f"Tempo total: {tempo_total:.3f} ms")
        print(f"\nOrdenação concluída. Resultado salvo em 'output/{arquivo_saida}'")
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado no diretório 'input'")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 