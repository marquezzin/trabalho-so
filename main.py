# Função para carregar os processos a partir de um arquivo de texto
def carregar_processos(nome_arquivo):
    processos = []

    # Abrindo arquivo no modo read e padrão de caracteres utf-8
    with open(nome_arquivo, 'r', encoding="utf-8") as arquivo:
        for linha in arquivo:
            # Removendo espaços em branco e quebras de linha
            linha = linha.strip()
            if not linha: # Pula linhas vazias
                continue

            partes = linha.split(';')
            # Mapeando os valores
            id_processo = int(partes[0])
            tempo_entrada = int(partes[1])
            tempo_io = int(partes[2])
            tempo_processamento = int(partes[3])
            prioridade = int(partes[4])

            # Monta o objeto processo e adiciona na lista de processos
            processo = {
                'idProcesso': id_processo,
                'tempoEntrada': tempo_entrada,
                'tempoIo': tempo_io,
                'tempoProcessamento': tempo_processamento,
                'prioridade': prioridade
            }

            processos.append(processo)
    return processos

# Tempos de clock
FATIA_CPU = 3
FATIA_IO = FATIA_CPU * 2

# Função para executar os processos e retorna a lista de processos finalizados com seus tempos de finalização
def executar_processos(processos):
    tempo_atual = 0
    fila_cpu = []
    fila_io = [] 
    finalizados = []

    # Ordena os processos pelo tempo de entrada
    processos = sorted(processos, key=lambda p: p['tempoEntrada'])

    while processos or fila_cpu or fila_io:

        while processos and processos[0]['tempoEntrada'] <= tempo_atual:
            # Tira o processo da lista de processos e adiciona na fila de CPU
            proc = processos.pop(0)
            fila_cpu.append(proc)

        if fila_cpu:
            # Ordena a fila de CPU pela prioridade e tempo de entrada
            fila_cpu = sorted(fila_cpu, key=lambda p: (p['prioridade'], p['tempoEntrada']))
            proc = fila_cpu.pop(0)
            uso_cpu = min(proc['tempoProcessamento'], FATIA_CPU)
            proc['tempoProcessamento'] -= uso_cpu
            tempo_atual += uso_cpu

            if proc['tempoProcessamento'] == 0 and proc['tempoIo'] == 0:
                # Encerramento (1 ciclo extra)
                tempo_atual += 1
                finalizados.append((tempo_atual, proc['idProcesso']))
            elif proc['tempoIo'] > 0:
                fila_io.append(proc)
            else:
                # Ainda precisa de CPU
                fila_cpu.append(proc)

        elif fila_io:
            proc = fila_io.pop(0)
            uso_io = min(FATIA_IO, proc['tempoIo'])
            proc['tempoIo'] -= uso_io
            tempo_atual += uso_io

            if proc['tempoProcessamento'] > 0:
                fila_cpu.append(proc)
            elif proc['tempoIo'] > 0:
                fila_io.append(proc)
            else:
                # Encerramento (1 ciclo extra)
                tempo_atual += 1
                finalizados.append((tempo_atual, proc['idProcesso']))

        else:
            # Se não houver nenhum processo na fila de cpu e io, adianta o relógio
            tempo_atual += 1



    return finalizados 


if __name__ == "__main__":

    nome_arquivo = input("Digite o nome do arquivo (ex: dados.txt): ")
    nome_saida = "saida.txt"
    try:
        lista_processos = carregar_processos(nome_arquivo)
        resultado = executar_processos(lista_processos)

        # Escreve no arquivo de saída
        with open(nome_saida, "w") as f:
            for tempo_finalizacao, id_processo in resultado:
                f.write(f"{tempo_finalizacao};{id_processo}\n")

        print(f"Execução concluída! Resultado gravado em '{nome_saida}'.")

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado. Certifique-se de que o nome está correto e que o arquivo está no mesmo diretório.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")