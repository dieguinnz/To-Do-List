from funcoes import (
    carregar_tarefas,
    salvar_tarefas,
    adicionar_tarefa,
    listar_tarefas,
    concluir_tarefa,
    remover_tarefa,
    editar_tarefa,  # nova função
    limpar_tela,
    pausar
)

from formulario import TarefaForm

CORES = {
    "reset": "\033[0m",
    "vermelho": "\033[91m",
    "verde": "\033[92m",
    "amarelo": "\033[93m",
    "ciano": "\033[96m",
    "negrito": "\033[1m"
}

def mostrar_menu(tarefas):
    total = len(tarefas)
    print(CORES["ciano"] + "--- To Do List ---" + CORES["reset"])
    print(f"Você tem {CORES['amarelo']}{total}{CORES['reset']} tarefa(s).")
    print("1 - Adicionar tarefa")
    print("2 - Listar tarefas")
    print("3 - Marcar tarefa como concluída")
    print("4 - Remover tarefa")
    print("5 - Sair")
    print("6 - Editar tarefa")  

def main(tarefas=None):
    if tarefas is None:
        tarefas = carregar_tarefas()
    while True:
        limpar_tela()
        mostrar_menu(tarefas)
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            descricao = input("Digite a descrição da tarefa: ")
            prazo = input("Digite o prazo (dd/mm/aaaa) ou deixe em branco: ")
            prazo = prazo if prazo.strip() else None
            adicionar_tarefa(tarefas, descricao, prazo)
            salvar_tarefas(tarefas)
            pausar()

        elif escolha == "2":
            listar_tarefas(tarefas)
            pausar()

        elif escolha == "3":
            try:
                id_tarefa = int(input("Digite o ID da tarefa que deseja concluir: "))
                concluir_tarefa(tarefas, id_tarefa)
                salvar_tarefas(tarefas)
            except ValueError:
                print("Por favor, digite um número válido.")
            pausar()

        elif escolha == "4":
            try:
                id_tarefa = int(input("Digite o ID da tarefa que deseja remover: "))
                remover_tarefa(tarefas, id_tarefa)
                salvar_tarefas(tarefas)
            except ValueError:
                print("Por favor, digite um número válido.")
            pausar()

        elif escolha == "5":
            print("Saindo do programa...")
            break

        elif escolha == "6":
            try:
                id_tarefa = int(input("Digite o ID da tarefa que deseja editar: "))
                nova_descricao = input("Digite a nova descrição: ")
                editar_tarefa(tarefas, id_tarefa, nova_descricao)
                salvar_tarefas(tarefas)
            except ValueError:
                print(CORES["vermelho"] + "Por favor, digite um número válido." + CORES["reset"])
            pausar()

if __name__ == "__main__":
    main()
