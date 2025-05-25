#!/usr/bin/env python3
"""
Gerador de números aleatórios para teste do QuickSort.

Este módulo gera arquivos de teste contendo números inteiros aleatórios
para serem usados como entrada nos programas de ordenação QuickSort.

Características:
- Gera números inteiros no intervalo [1, 1.000.000]
- Salva os números em arquivo texto, separados por vírgula
- Permite especificar a quantidade de números e nome do arquivo
- Salva os arquivos no diretório input/
"""

import sys
import random
import os

def gerar_numeros(quantidade: int) -> list:
    """
    Gera uma lista de números aleatórios.
    
    Args:
        quantidade: Quantidade de números a serem gerados
    
    Returns:
        list: Lista com os números aleatórios gerados
    
    Note:
        Os números gerados estão no intervalo de 1 a 1.000.000
    """
    return [random.randint(1, 1_000_000) for _ in range(quantidade)]

def salvar_arquivo(numeros: list, nome_arquivo: str) -> None:
    """
    Salva os números em um arquivo no diretório input.
    
    Args:
        numeros: Lista de números a ser salva
        nome_arquivo: Nome do arquivo de saída
    
    Note:
        - O arquivo será salvo no diretório input/
        - A extensão .txt será adicionada se não fornecida
        - Os números são salvos separados por vírgula
    """
    if not nome_arquivo.endswith('.txt'):
        nome_arquivo += '.txt'
    
    caminho = os.path.join('input', nome_arquivo)
    with open(caminho, 'w') as f:
        f.write(','.join(map(str, numeros)))
    print(f"Arquivo gerado: input/{nome_arquivo}")

def main() -> None:
    """
    Função principal do programa.
    
    Fluxo de execução:
    1. Verifica argumentos da linha de comando
    2. Gera a quantidade solicitada de números
    3. Salva os números em arquivo no diretório input/
    
    Uso:
        python gerador_numeros.py <quantidade> [nome_arquivo]
    
    Exemplo:
        python gerador_numeros.py 1000 entrada.txt
    """
    if len(sys.argv) < 2:
        print("Uso: python gerador_numeros.py <quantidade> [nome_arquivo]")
        print("Exemplo: python gerador_numeros.py 1000 entrada.txt")
        print("O arquivo será salvo no diretório 'input'")
        sys.exit(1)

    try:
        quantidade = int(sys.argv[1])
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser um número positivo")
    except ValueError as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

    nome_arquivo = sys.argv[2] if len(sys.argv) > 2 else "entrada.txt"
    
    try:
        numeros = gerar_numeros(quantidade)
        salvar_arquivo(numeros, nome_arquivo)
    except Exception as e:
        print(f"Erro ao gerar arquivo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 