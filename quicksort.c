/**
 * Implementação do algoritmo QuickSort em C.
 * Este código é equivalente à implementação em Python.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Protótipos das funções */
void quicksort(int arr[], int low, int high);
int partition(int arr[], int low, int high);
void trocar(int* a, int* b);
int contar_numeros(const char* filename);
double obter_tempo_ms(void);
char* gerar_nome_saida(const char* nome_entrada);
char* gerar_caminho(const char* diretorio, const char* arquivo);

/**
 * Troca dois elementos de posição em um array.
 */
void trocar(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

/**
 * @brief Particiona o array usando o último elemento como pivô
 *
 * Esta função reorganiza o array de forma que:
 * - Elementos menores ou iguais ao pivô ficam à esquerda
 * - Elementos maiores que o pivô ficam à direita
 *
 * @param arr Array a ser particionado
 * @param low Índice inicial da partição
 * @param high Índice final da partição
 * @return Posição final do pivô
 */
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            trocar(&arr[i], &arr[j]);
        }
    }
    trocar(&arr[i + 1], &arr[high]);
    return (i + 1);
}

/**
 * @brief Implementação do algoritmo QuickSort
 *
 * Ordena o array in-place usando a estratégia de dividir e conquistar:
 * 1. Escolhe um pivô (último elemento)
 * 2. Particiona o array em torno do pivô
 * 3. Recursivamente ordena as duas partições
 *
 * @param arr Array a ser ordenado
 * @param low Índice inicial da partição
 * @param high Índice final da partição
 */
void quicksort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

/**
 * @brief Gera um caminho completo para o arquivo
 *
 * @param diretorio Nome do diretório
 * @param arquivo Nome do arquivo
 * @return Caminho completo do arquivo (deve ser liberado com free)
 */
char* gerar_caminho(const char* diretorio, const char* arquivo) {
    size_t tamanho = strlen(diretorio) + strlen(arquivo) + 2; // +2 para '/' e '\0'
    char* caminho = (char*)malloc(tamanho);
    if (caminho == NULL) {
        printf("Erro: falha na alocação de memória\n");
        exit(1);
    }
    snprintf(caminho, tamanho, "%s/%s", diretorio, arquivo);
    return caminho;
}

/**
 * @brief Conta o número de elementos no arquivo
 *
 * @param filename Nome do arquivo (deve estar no diretório input/)
 * @return Número de elementos no arquivo
 */
int contar_numeros(const char* filename) {
    char* caminho = gerar_caminho("input", filename);
    FILE* file = fopen(caminho, "r");
    if (file == NULL) {
        printf("Erro: não foi possível abrir o arquivo '%s'\n", caminho);
        free(caminho);
        exit(1);
    }

    int count = 1;  // Começa com 1 para o primeiro número
    char c;
    while ((c = fgetc(file)) != EOF) {
        if (c == ',') count++;
    }

    fclose(file);
    free(caminho);
    return count;
}

/**
 * @brief Retorna o tempo atual em milissegundos
 *
 * @return Tempo em milissegundos
 */
double obter_tempo_ms(void) {
    return (double)clock() * 1000.0 / CLOCKS_PER_SEC;
}

/**
 * @brief Gera o nome do arquivo de saída baseado no arquivo de entrada
 *
 * @param nome_entrada Nome do arquivo de entrada
 * @return Nome do arquivo de saída (deve ser liberado com free)
 */
char* gerar_nome_saida(const char* nome_entrada) {
    char* nome_base = strdup(nome_entrada);
    char* ext = strstr(nome_base, ".txt");
    if (ext != NULL) {
        *ext = '\0';
    }
    
    size_t tamanho = strlen(nome_base) + 9; // +9 para "_out.txt\0"
    char* nome_saida = (char*)malloc(tamanho);
    if (nome_saida == NULL) {
        printf("Erro: falha na alocação de memória\n");
        free(nome_base);
        exit(1);
    }
    
    snprintf(nome_saida, tamanho, "%s_out.txt", nome_base);
    free(nome_base);
    return nome_saida;
}

/**
 * @brief Função principal do programa
 *
 * Fluxo de execução:
 * 1. Lê argumentos da linha de comando
 * 2. Lê números do arquivo de entrada
 * 3. Ordena os números usando QuickSort
 * 4. Salva o resultado em arquivo
 * 5. Mostra estatísticas de tempo
 *
 * @param argc Número de argumentos
 * @param argv Array de argumentos
 * @return 0 em caso de sucesso, 1 em caso de erro
 */
int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Uso: %s <arquivo_entrada>\n", argv[0]);
        printf("Exemplo: %s numeros.txt\n", argv[0]);
        printf("O arquivo deve estar no diretório 'input'\n");
        printf("O resultado será salvo no diretório 'output'\n");
        return 1;
    }

    const char* arquivo_entrada = argv[1];
    char* arquivo_saida = gerar_nome_saida(arquivo_entrada);
    char* caminho_entrada = gerar_caminho("input", arquivo_entrada);
    char* caminho_saida = gerar_caminho("output", arquivo_saida);
    
    double tempo_inicio, tempo_leitura = 0, tempo_algoritmo = 0, tempo_escrita = 0;
    
    // Mede tempo de leitura
    tempo_inicio = obter_tempo_ms();
    
    int n = contar_numeros(arquivo_entrada);
    int* numeros = (int*)malloc(n * sizeof(int));
    if (numeros == NULL) {
        printf("Erro: falha na alocação de memória\n");
        free(arquivo_saida);
        free(caminho_entrada);
        free(caminho_saida);
        return 1;
    }

    FILE* file = fopen(caminho_entrada, "r");
    if (file == NULL) {
        printf("Erro: arquivo '%s' não encontrado no diretório 'input'\n", arquivo_entrada);
        free(numeros);
        free(arquivo_saida);
        free(caminho_entrada);
        free(caminho_saida);
        return 1;
    }

    for (int i = 0; i < n; i++) {
        if (fscanf(file, "%d", &numeros[i]) != 1) {
            printf("Erro: formato inválido no arquivo de entrada\n");
            fclose(file);
            free(numeros);
            free(arquivo_saida);
            free(caminho_entrada);
            free(caminho_saida);
            return 1;
        }
        if (i < n-1) {
            fgetc(file); // Pula a vírgula
        }
    }
    fclose(file);
    
    tempo_leitura = obter_tempo_ms() - tempo_inicio;

    // Mede tempo do algoritmo
    tempo_inicio = obter_tempo_ms();
    quicksort(numeros, 0, n - 1);
    tempo_algoritmo = obter_tempo_ms() - tempo_inicio;

    // Mede tempo de escrita
    tempo_inicio = obter_tempo_ms();
    
    file = fopen(caminho_saida, "w");
    if (file == NULL) {
        printf("Erro: não foi possível criar o arquivo em 'output/%s'\n", arquivo_saida);
        free(numeros);
        free(arquivo_saida);
        free(caminho_entrada);
        free(caminho_saida);
        return 1;
    }

    for (int i = 0; i < n; i++) {
        fprintf(file, "%d", numeros[i]);
        if (i < n-1) {
            fprintf(file, ",");
        }
    }
    fclose(file);
    
    tempo_escrita = obter_tempo_ms() - tempo_inicio;
    double tempo_total = tempo_leitura + tempo_algoritmo + tempo_escrita;

    // Imprime os resultados
    printf("\nTempos de execução (C):\n");
    printf("Leitura do arquivo: %.3f ms\n", tempo_leitura);
    printf("Algoritmo QuickSort: %.3f ms\n", tempo_algoritmo);
    printf("Escrita do arquivo: %.3f ms\n", tempo_escrita);
    printf("Tempo total: %.3f ms\n", tempo_total);
    printf("\nOrdenação concluída. Resultado salvo em 'output/%s'\n", arquivo_saida);

    free(numeros);
    free(arquivo_saida);
    free(caminho_entrada);
    free(caminho_saida);
    return 0;
} 