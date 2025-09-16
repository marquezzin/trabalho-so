def carregar_processos(nome_arquivo):
    processos = []

    #Abrindo arquivo no modo read e padrão de caracteres utf-8
    with open(nome_arquivo, 'r', encoding="utf-8") as arquivo:
        for linha in arquivo:
            #Removendo espaços em branco e quebras de linha
            linha = linha.strip()
            if not linha: #Pula linhas vazias
                continue

            partes = linha.split(';')
            #Mapeando os valores
            id_processo = int(partes[0])
            tempo_entrada = int(partes[1])
            tempo_io = int(partes[2])
            tempo_processamento = int(partes[3])
            prioridade = int(partes[4])

            #Monta o objeto processo e adiciona na lista de processos
            processo = {
                'idProcesso': id_processo,
                'tempoEntrada': tempo_entrada,
                'tempoIo': tempo_io,
                'tempoProcessamento': tempo_processamento,
                'prioridade': prioridade
            }

            processos.append(processo)
    return processos

if __name__ == "__main__":
    #OBS: O arquivo de texto deve estar no mesmo diretório que este.
    nome_arquivo = input("Digite o nome do arquivo (ex: dados.txt): ")
    try:
        lista_processos = carregar_processos(nome_arquivo)
        print("\nProcessos carregados com sucesso:\n")
        for p in lista_processos:
            print(p)
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado. Certifique-se de que o nome está correto e que o arquivo está no mesmo diretório.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")