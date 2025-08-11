import json
import os
from datetime import datetime, timedelta

CORES = {
    "reset": "\033[0m",
    "vermelho": "\033[91m",
    "verde": "\033[92m",
    "amarelo": "\033[93m",
    "ciano": "\033[96m",
    "negrito": "\033[1m"
}

ARQUIVO_TAREFAS = "tarefas.json"

def carregar_tarefas():
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=4)

def adicionar_tarefa(tarefas, descricao, prazo=None):
    id_tarefa = 1 if not tarefas else max(t["id"] for t in tarefas) + 1
    data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    nova_tarefa = {
        "id": id_tarefa,
        "descricao": descricao,
        "concluida": False,
        "data_criacao": data_criacao,
        "prazo": prazo if prazo else "Sem prazo"
    }
    tarefas.append(nova_tarefa)
    print(CORES["verde"] + "Tarefa adicionada com sucesso!" + CORES["reset"])

def listar_tarefas(tarefas):
    if not tarefas:
        print(CORES["amarelo"] + "Nenhuma tarefa encontrada." + CORES["reset"])
        return

    print(CORES["ciano"] + "\n--- Lista de Tarefas ---" + CORES["reset"])

    def chave_ordenacao(tarefa):
        concluida = tarefa["concluida"]
        prazo_str = tarefa.get("prazo", "Sem prazo")
        if prazo_str == "Sem prazo":
            prazo_dt = datetime.max
        else:
            try:
                prazo_dt = datetime.strptime(prazo_str, "%d/%m/%Y")
            except ValueError:
                prazo_dt = datetime.max
        return (concluida, prazo_dt)

    tarefas_ordenadas = sorted(tarefas, key=chave_ordenacao)

    hoje = datetime.now()
    alerta_dias = timedelta(days=3)  # prazo para alerta

    for tarefa in tarefas_ordenadas:
        cor = CORES["verde"] if tarefa["concluida"] else CORES["amarelo"]
        status = "✔" if tarefa["concluida"] else "✗"
        prazo_str = tarefa.get("prazo", "Sem prazo")

        # Verifica se o prazo está próximo
        alerta = ""
        if prazo_str != "Sem prazo" and not tarefa["concluida"]:
            try:
                prazo_dt = datetime.strptime(prazo_str, "%d/%m/%Y")
                if hoje <= prazo_dt <= hoje + alerta_dias:
                    alerta = CORES["vermelho"] + " [!! PRAZO PRÓXIMO !!]" + CORES["reset"]
            except ValueError:
                pass

        print(f"{cor}{tarefa['id']}. [{status}] {tarefa['descricao']}{alerta}{CORES['reset']}")
        print(f"   Criada em: {tarefa['data_criacao']}")
        print(f"   Prazo: {prazo_str}")

def concluir_tarefa(tarefas, id_tarefa):
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["concluida"] = True
            print(CORES["verde"] + "Tarefa marcada como concluída!" + CORES["reset"])
            return
    print(CORES["vermelho"] + "Tarefa não encontrada." + CORES["reset"])

def remover_tarefa(tarefas, id_tarefa):
    for t in tarefas:
        if t["id"] == id_tarefa:
            tarefas.remove(t)
            print(CORES["verde"] + "Tarefa removida com sucesso!" + CORES["reset"])
            return
    print(CORES["vermelho"] + "Tarefa não encontrada." + CORES["reset"])

def editar_tarefa(tarefas, id_tarefa, nova_descricao):
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["descricao"] = nova_descricao
            print(CORES["verde"] + "Tarefa editada com sucesso!" + CORES["reset"])
            return
    print(CORES["vermelho"] + "Tarefa não encontrada." + CORES["reset"])

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("Pressione Enter para continuar...")
