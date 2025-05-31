#!/usr/bin/env python3
"""
Gerador de números aleatórios para teste do QuickSort.

Este módulo gera múltiplos arquivos de teste contendo números inteiros aleatórios
para serem usados como entrada nos programas de ordenação QuickSort.

Características:
- Gera números inteiros no intervalo [1, 1.000.000]
- Salva os números em arquivo texto, separados por vírgula
- Permite especificar a quantidade de números e quantidade de arquivos
- Limpa os diretórios input/ e output/ antes de gerar novos arquivos
- Salva os arquivos no diretório input/ com nomes padronizados (entrada_1.txt, entrada_2.txt, etc.)
- Permite limpar os diretórios usando o comando 'clean'
"""

import sys
import random
import os
import shutil

def limpar_diretorios() -> None:
    """
    Limpa os diretórios input/ e output/, recriando-os se necessário.
    """
    for diretorio in ['input', 'output']:
        if os.path.exists(diretorio):
            shutil.rmtree(diretorio)
        os.makedirs(diretorio)
    print("Diretórios input/ e output/ foram limpos e recriados.")

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

def salvar_arquivo(numeros: list, numero_arquivo: int) -> None:
    """
    Salva os números em um arquivo no diretório input.
    
    Args:
        numeros: Lista de números a ser salva
        numero_arquivo: Número do arquivo para gerar o nome padronizado
    
    Note:
        - O arquivo será salvo no diretório input/
        - O nome do arquivo será entrada_N.txt, onde N é o número do arquivo
        - Os números são salvos separados por vírgula
    """
    nome_arquivo = f"entrada_{numero_arquivo}.txt"
    caminho = os.path.join('input', nome_arquivo)
    with open(caminho, 'w') as f:
        f.write(','.join(map(str, numeros)))
    print(f"Arquivo gerado: input/{nome_arquivo}")

def mostrar_ajuda() -> None:
    """
    Mostra as instruções de uso do programa.
    """
    print("Uso:")
    print("  1. Para gerar arquivos:")
    print("     python input_generator.py <quantidade_numeros> <quantidade_arquivos>")
    print("     Exemplo: python input_generator.py 1000 5")
    print("     (Gera 5 arquivos com 1000 números cada)")
    print("\n  2. Para limpar os diretórios:")
    print("     python input_generator.py clean")
    print("     (Remove todos os arquivos dos diretórios input/ e output/)")

def main() -> None:
    """
    Função principal do programa.
    
    Fluxo de execução:
    1. Verifica argumentos da linha de comando
    2. Se o comando for 'clean':
       - Limpa os diretórios input/ e output/
    3. Caso contrário:
       - Limpa os diretórios input/ e output/
       - Para cada arquivo solicitado:
         - Gera a quantidade especificada de números
         - Salva os números em um arquivo com nome padronizado
    """
    if len(sys.argv) < 2:
        mostrar_ajuda()
        sys.exit(1)

    # Verifica se é o comando de limpeza
    if sys.argv[1].lower() == 'clean':
        try:
            limpar_diretorios()
            print("Operação de limpeza concluída com sucesso!")
            sys.exit(0)
        except Exception as e:
            print(f"Erro durante a limpeza: {str(e)}")
            sys.exit(1)

    # Se não for limpeza, verifica se tem argumentos suficientes para geração
    if len(sys.argv) < 3:
        mostrar_ajuda()
        sys.exit(1)

    try:
        quantidade_numeros = int(sys.argv[1])
        quantidade_arquivos = int(sys.argv[2])
        
        if quantidade_numeros <= 0:
            raise ValueError("A quantidade de números deve ser positiva")
        if quantidade_arquivos <= 0:
            raise ValueError("A quantidade de arquivos deve ser positiva")
            
    except ValueError as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

    try:
        # Limpa os diretórios antes de começar
        limpar_diretorios()
        
        # Gera os arquivos
        for i in range(1, quantidade_arquivos + 1):
            numeros = gerar_numeros(quantidade_numeros)
            salvar_arquivo(numeros, i)
            
        print(f"\nGeração concluída! {quantidade_arquivos} arquivos foram criados com {quantidade_numeros} números cada.")
        
    except Exception as e:
        print(f"Erro ao gerar arquivos: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 