#!/usr/bin/env python3
"""
Script de teste comparativo para as implementações do QuickSort.

Este script executa e compara o desempenho das implementações do QuickSort
em Python e C, coletando métricas de tempo e gerando relatórios estatísticos.
"""

import os
import subprocess
import time
import statistics
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

class PerformanceTest:
    def __init__(self):
        """Inicializa o teste de performance."""
        self.python_results: Dict[str, Dict[str, float]] = {}
        self.c_results: Dict[str, Dict[str, float]] = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verifica se os arquivos necessários existem
        if not os.path.exists("quicksort.c"):
            print("Erro: arquivo 'quicksort.c' não encontrado!")
            exit(1)
        if not os.path.exists("quicksort.py"):
            print("Erro: arquivo 'quicksort.py' não encontrado!")
            exit(1)
            
        # Cria diretório de logs se não existir
        os.makedirs("log", exist_ok=True)
            
        # Determina o comando Python correto
        self.python_cmd = self._get_python_command()
        
        # Compila o código C
        try:
            subprocess.run(["gcc", "quicksort.c", "-o", "quicksort"], check=True)
            print("Código C compilado com sucesso!")
        except subprocess.CalledProcessError:
            print("Erro ao compilar o código C!")
            exit(1)
        except FileNotFoundError:
            print("Erro: GCC não encontrado! Certifique-se de que o compilador C está instalado.")
            exit(1)

    def _get_python_command(self) -> str:
        """
        Determina o comando Python correto para o sistema.
        
        Returns:
            str: Comando Python ('python3' ou 'python')
        """
        try:
            # Tenta python3 primeiro
            subprocess.run(["python3", "--version"], capture_output=True, check=True)
            return "python3"
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Tenta python
                subprocess.run(["python", "--version"], capture_output=True, check=True)
                return "python"
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Erro: Python não encontrado no sistema!")
                exit(1)

    def get_input_files(self) -> List[str]:
        """Retorna a lista de arquivos de entrada ordenados numericamente."""
        if not os.path.exists("input"):
            print("Erro: diretório 'input' não encontrado!")
            exit(1)
            
        files = [f for f in os.listdir("input") if f.startswith("entrada_") and f.endswith(".txt")]
        return sorted(files, key=lambda x: int(x.split("_")[1].split(".")[0]))

    def get_input_size(self, input_file: str) -> int:
        """
        Obtém o tamanho da entrada contando o número de elementos no arquivo.
        
        Args:
            input_file: Nome do arquivo de entrada
            
        Returns:
            int: Número de elementos no arquivo
        """
        with open(os.path.join("input", input_file), 'r') as f:
            content = f.read().strip()
            return len(content.split(','))

    def extract_times_from_output(self, output: str, language: str) -> Dict[str, float]:
        """
        Extrai todos os tempos de execução da saída do programa.
        
        Args:
            output: Saída do programa
            language: 'Python' ou 'C'
            
        Returns:
            Dict[str, float]: Dicionário com os tempos de leitura, algoritmo, escrita e total
        """
        times = {
            "leitura": 0.0,
            "algoritmo": 0.0,
            "escrita": 0.0,
            "total": 0.0
        }
        
        lines = output.split('\n')
        for line in lines:
            try:
                if "Leitura do arquivo:" in line:
                    times["leitura"] = float(line.split(":")[1].strip().split()[0])
                elif "Algoritmo QuickSort:" in line:
                    times["algoritmo"] = float(line.split(":")[1].strip().split()[0])
                elif "Escrita do arquivo:" in line:
                    times["escrita"] = float(line.split(":")[1].strip().split()[0])
                elif "Tempo total:" in line:
                    times["total"] = float(line.split(":")[1].strip().split()[0])
            except (IndexError, ValueError) as e:
                print(f"Erro ao extrair tempo da linha '{line}': {e}")
                
        return times

    def run_python_quicksort(self, input_file: str) -> Dict[str, float]:
        """
        Executa o QuickSort em Python para um arquivo de entrada.
        
        Args:
            input_file: Nome do arquivo de entrada
            
        Returns:
            Dict[str, float]: Dicionário com os tempos de execução
        """
        try:
            result = subprocess.run(
                [self.python_cmd, "quicksort.py", input_file],
                capture_output=True,
                text=True,
                check=True
            )
            return self.extract_times_from_output(result.stdout, "Python")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar QuickSort Python: {e}")
            print(f"Saída de erro: {e.stderr}")
            return {"leitura": 0.0, "algoritmo": 0.0, "escrita": 0.0, "total": 0.0}

    def run_c_quicksort(self, input_file: str) -> Dict[str, float]:
        """
        Executa o QuickSort em C para um arquivo de entrada.
        
        Args:
            input_file: Nome do arquivo de entrada
            
        Returns:
            Dict[str, float]: Dicionário com os tempos de execução
        """
        try:
            result = subprocess.run(
                ["./quicksort", input_file],
                capture_output=True,
                text=True,
                check=True
            )
            return self.extract_times_from_output(result.stdout, "C")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar QuickSort C: {e}")
            print(f"Saída de erro: {e.stderr}")
            return {"leitura": 0.0, "algoritmo": 0.0, "escrita": 0.0, "total": 0.0}

    def calculate_statistics(self, times: List[float]) -> Dict[str, float]:
        """
        Calcula estatísticas para uma lista de tempos.
        
        Args:
            times: Lista de tempos de execução
            
        Returns:
            Dict[str, float]: Dicionário com as estatísticas calculadas
        """
        if not times:
            return {
                "média": 0.0,
                "desvio_padrão": 0.0,
                "mediana": 0.0,
                "mínimo": 0.0,
                "máximo": 0.0,
                "amplitude": 0.0
            }
            
        return {
            "média": statistics.mean(times),
            "desvio_padrão": statistics.stdev(times) if len(times) > 1 else 0,
            "mediana": statistics.median(times),
            "mínimo": min(times),
            "máximo": max(times),
            "amplitude": max(times) - min(times)
        }

    def generate_report(self) -> str:
        """
        Gera o relatório de comparação.
        
        Returns:
            str: Relatório formatado
        """
        report = []
        report.append("=" * 80)
        report.append(f"RELATÓRIO DE PERFORMANCE - QUICKSORT")
        report.append(f"Data e hora do teste: {self.timestamp}")
        report.append("=" * 80)
        
        # Informações do sistema
        report.append("\nINFORMAÇÕES DO SISTEMA:")
        report.append("-" * 80)
        report.append(f"Sistema Operacional: {sys.platform}")
        report.append(f"Comando Python: {self.python_cmd}")
        
        report.append("\nRESULTADOS POR ARQUIVO:")
        report.append("-" * 80)
        
        # Resultados detalhados por arquivo
        for input_file in sorted(self.python_results.keys()):
            report.append(f"\nArquivo: {input_file}")
            python_ms = self.python_results[input_file]['total']
            c_ms = self.c_results[input_file]['total']
            report.append(f"Python: {python_ms:.6f} ms")
            report.append(f"C: {c_ms:.6f} ms")
            if c_ms > 0:
                speedup = python_ms / c_ms
                report.append(f"Speedup (Python/C): {speedup:.6f}x")
            else:
                report.append("Speedup (Python/C): N/A (erro na execução)")
        
        # Estatísticas gerais
        report.append("\nESTATÍSTICAS GERAIS:")
        report.append("-" * 80)
        
        python_times = [result['total'] for result in self.python_results.values()]
        c_times = [result['total'] for result in self.c_results.values()]
        
        python_stats = self.calculate_statistics(python_times)
        c_stats = self.calculate_statistics(c_times)
        
        report.append("\nPython:")
        for metric, value in python_stats.items():
            report.append(f"  {metric}: {value:.6f} ms")
            
        report.append("\nC:")
        for metric, value in c_stats.items():
            report.append(f"  {metric}: {value:.6f} ms")
            
        # Speedup médio
        if c_stats['média'] > 0:
            avg_speedup = python_stats['média'] / c_stats['média']
            report.append(f"\nSpeedup médio (Python/C): {avg_speedup:.6f}x")
            report.append(f"Isso significa que, em média, a implementação em Python é {avg_speedup:.6f} vezes mais lenta que a implementação em C.")
        else:
            report.append("\nSpeedup médio (Python/C): N/A (erro na execução)")
        
        return "\n".join(report)

    def run_tests(self):
        """Executa os testes de performance."""
        input_files = self.get_input_files()
        
        if not input_files:
            print("Nenhum arquivo de entrada encontrado no diretório 'input'!")
            return
        
        print(f"Iniciando testes com {len(input_files)} arquivos de entrada...")
        
        # Cria diretório de logs se não existir
        os.makedirs("log", exist_ok=True)
        
        # Agrupa arquivos por tamanho
        files_by_size = {}
        for input_file in input_files:
            size = self.get_input_size(input_file)
            if size not in files_by_size:
                files_by_size[size] = []
            files_by_size[size].append(input_file)
        
        # Executa testes para cada tamanho
        for size, files in sorted(files_by_size.items()):
            print(f"\nTestando arquivos de tamanho {size}...")
            
            # Reseta resultados para este tamanho
            self.python_results = {}
            self.c_results = {}
            
            # Executa testes para todos os arquivos deste tamanho
            for input_file in files:
                print(f"\nTestando arquivo: {input_file}")
                
                # Teste Python
                print("Executando QuickSort em Python...")
                self.python_results[input_file] = self.run_python_quicksort(input_file)
                
                # Teste C
                print("Executando QuickSort em C...")
                self.c_results[input_file] = self.run_c_quicksort(input_file)
            
            # Gera e salva o relatório para este tamanho
            report = self.generate_report()
            log_file = os.path.join("log", f"log_{size}.txt")
            
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"\nRelatório salvo em '{log_file}'")
        
        print("\nTodos os testes foram concluídos!")

def main():
    """Função principal do programa."""
    try:
        tester = PerformanceTest()
        tester.run_tests()
    except Exception as e:
        print(f"Erro durante a execução dos testes: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 