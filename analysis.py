#!/usr/bin/env python3
"""
Script para análise e visualização dos resultados do QuickSort.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from typing import List, Tuple, Dict

def extract_data_from_log(log_file: str) -> Tuple[Dict[str, float], Dict[str, float], List[float]]:
    """
    Extrai dados do arquivo de log.
    
    Args:
        log_file: Caminho do arquivo de log
        
    Returns:
        Tuple com dicionários de tempos Python e C (por arquivo) e lista de speedups
    """
    python_times = {}
    c_times = {}
    speedups = []
    current_file = None
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        if "Arquivo:" in line:
            current_file = line.split(":")[1].strip()
        elif current_file and "Python:" in line and "ms" in line:
            time = float(line.split(":")[1].strip().replace(" ms", ""))
            python_times[current_file] = time
        elif current_file and "C:" in line and "ms" in line:
            time = float(line.split(":")[1].strip().replace(" ms", ""))
            c_times[current_file] = time
        elif "Speedup (Python/C):" in line and "N/A" not in line:
            speedup = float(line.split(":")[1].strip().replace("x", ""))
            speedups.append(speedup)
            
    return python_times, c_times, speedups

def categorize_size(size: int) -> str:
    """
    Categoriza o tamanho da entrada em pequeno, médio ou grande.
    
    Args:
        size: Tamanho da entrada
        
    Returns:
        str: Categoria do tamanho ('Pequeno', 'Médio' ou 'Grande')
    """
    if size < 1000:
        return 'Pequeno'
    elif size < 10000:
        return 'Médio'
    else:
        return 'Grande'

def plot_execution_times_by_file(size: str, python_times: Dict[str, float], c_times: Dict[str, float]):
    """
    Gera gráfico de tempo de execução por arquivo para um tamanho específico.
    
    Args:
        size: Tamanho da entrada
        python_times: Dicionário com tempos Python por arquivo
        c_times: Dicionário com tempos C por arquivo
    """
    # Cria diretório para este tamanho se não existir
    output_dir = os.path.join('analysis', f'analysis_{size}')
    os.makedirs(output_dir, exist_ok=True)
    
    files = sorted(python_times.keys())
    x = np.arange(len(files))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, [python_times[f] for f in files], width, label='Python', color='blue')
    rects2 = ax.bar(x + width/2, [c_times[f] for f in files], width, label='C', color='red')
    
    ax.set_ylabel('Tempo de Execução (ms)')
    ax.set_xlabel('Arquivo de Entrada')
    ax.set_title(f'Tempo de Execução por Arquivo (Tamanho {size})')
    ax.set_xticks(x)
    ax.set_xticklabels(files, rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'execution_times.png'))
    plt.close()

def plot_metric_comparison(data: Dict[str, Tuple[Dict[str, float], Dict[str, float], List[float]]], 
                         metric: str, calc_func: callable):
    """
    Gera gráfico comparativo de uma métrica específica por tamanho de entrada.
    
    Args:
        data: Dicionário com dados por tamanho
        metric: Nome da métrica
        calc_func: Função para calcular a métrica
    """
    sizes = sorted([int(size) for size in data.keys()])
    python_values = []
    c_values = []
    
    for size in sizes:
        python_times = list(data[str(size)][0].values())
        c_times = list(data[str(size)][1].values())
        
        python_values.append(calc_func(python_times))
        c_values.append(calc_func(c_times))
    
    x = np.arange(len(sizes))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, python_values, width, label='Python', color='blue')
    rects2 = ax.bar(x + width/2, c_values, width, label='C', color='red')
    
    ax.set_ylabel(f'{metric} (ms)')
    ax.set_xlabel('Tamanho da Entrada')
    ax.set_title(f'{metric} por Tamanho de Entrada')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.legend()
    
    # Adiciona valores nas barras
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(rect.get_x() + rect.get_width()/2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig(os.path.join('analysis', f'{metric.lower().replace(" ", "_")}.png'))
    plt.close()

def plot_speedup_comparison(data: Dict[str, Tuple[Dict[str, float], Dict[str, float], List[float]]]):
    """
    Gera gráfico de speedup médio por tamanho de entrada.
    """
    sizes = sorted([int(size) for size in data.keys()])
    speedups = [np.mean(data[str(size)][2]) for size in sizes]
    
    plt.figure(figsize=(10, 6))
    
    # Plota linha com marcadores
    plt.plot(sizes, speedups, 'g-o', linewidth=2, markersize=8)
    
    # Adiciona pontos de dados
    for i, v in enumerate(speedups):
        plt.text(sizes[i], v + 0.2, f'{v:.2f}x', ha='center', va='bottom')
    
    plt.xlabel('Tamanho da Entrada')
    plt.ylabel('Speedup (Python/C)')
    plt.title('Speedup Médio por Tamanho de Entrada')
    
    # Ajusta os limites do eixo y para melhor visualização
    plt.ylim(0, max(speedups) * 1.2)
    
    # Formata o eixo x para mostrar os tamanhos de forma mais legível
    plt.xticks(sizes, [f'{size:,}'.replace(',', '.') for size in sizes])
    
    # Adiciona grade
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join('analysis', 'speedup.png'))
    plt.close()

def main():
    """Função principal."""
    try:
        # Cria diretório de análise se não existir
        os.makedirs("analysis", exist_ok=True)
        
        # Coleta dados de todos os logs
        data = {}
        log_files = [f for f in os.listdir("log") if f.startswith("log_") and f.endswith(".txt")]
        
        if not log_files:
            print("Nenhum arquivo de log encontrado no diretório 'log'!")
            return
        
        for log_file in log_files:
            size = log_file.split("_")[1].split(".")[0]
            data[size] = extract_data_from_log(os.path.join("log", log_file))
            
            # Gera gráfico de tempo de execução por arquivo para este tamanho
            plot_execution_times_by_file(size, data[size][0], data[size][1])
        
        # Gera gráficos comparativos
        plot_metric_comparison(data, "Tempo Médio", np.mean)
        plot_metric_comparison(data, "Desvio Padrão", np.std)
        plot_metric_comparison(data, "Mediana", np.median)
        plot_metric_comparison(data, "Mínimo", np.min)
        plot_metric_comparison(data, "Máximo", np.max)
        plot_metric_comparison(data, "Amplitude", lambda x: np.max(x) - np.min(x))
        plot_speedup_comparison(data)
        
        print("Análise concluída! Arquivos gerados:")
        print("\nDiretórios de análise por tamanho:")
        for size in data.keys():
            print(f"- analysis_{size}/")
            print("  - execution_times.png (Gráfico de tempos por arquivo)")
        
        print("\nGráficos comparativos em /analysis:")
        print("- tempo_medio.png")
        print("- desvio_padrao.png")
        print("- mediana.png")
        print("- minimo.png")
        print("- maximo.png")
        print("- amplitude.png")
        print("- speedup.png")
        
    except Exception as e:
        print(f"Erro durante a análise: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 