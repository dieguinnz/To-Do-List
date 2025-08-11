import tkinter as tk
from tkinter import ttk, messagebox
from funcoes import carregar_tarefas, salvar_tarefas
from datetime import datetime, timedelta

 
ALERTA_DIAS = 3  # Prazo para alerta próximo

class TarefaForm(tk.Toplevel):
    def __init__(self, master, tarefa=None, callback=None):
        super().__init__(master)
        self.title("Tarefa")
        self.callback = callback
        self.tarefa = tarefa

        tk.Label(self, text="Descrição:").grid(row=0, column=0, sticky="e")
        self.desc_entry = tk.Entry(self, width=40)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Prazo (dd/mm/aaaa):").grid(row=1, column=0, sticky="e")
        self.prazo_entry = tk.Entry(self, width=20)
        self.prazo_entry.grid(row=1, column=1, padx=5, pady=5)

        if tarefa:
            self.desc_entry.insert(0, tarefa["descricao"])
            if tarefa["prazo"] != "Sem prazo":
                self.prazo_entry.insert(0, tarefa["prazo"])

        self.btn_salvar = tk.Button(self, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

    def salvar(self):
        descricao = self.desc_entry.get().strip()
        prazo = self.prazo_entry.get().strip()

        if not descricao:
            messagebox.showwarning("Erro", "Descrição não pode estar vazia.")
            return

        if prazo:
            try:
                datetime.strptime(prazo, "%d/%m/%Y")
            except ValueError:
                messagebox.showwarning("Erro", "Prazo deve estar no formato dd/mm/aaaa.")
                return
        else:
            prazo = "Sem prazo"

        if self.callback:
            self.callback(descricao, prazo)
        self.destroy()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List - GUI")

        self.tarefas = carregar_tarefas()

        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set,
                                 columns=("Descricao", "Status", "Criada", "Prazo"), show="headings", height=15)
        self.tree.pack()

        self.scrollbar.config(command=self.tree.yview)

        self.tree.heading("Descricao", text="Descrição")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Criada", text="Data Criação")
        self.tree.heading("Prazo", text="Prazo")

        self.tree.column("Descricao", width=250)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        self.tree.column("Criada", width=120, anchor=tk.CENTER)
        self.tree.column("Prazo", width=100, anchor=tk.CENTER)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=5)

        self.add_btn = tk.Button(self.btn_frame, text="Adicionar", command=self.abrir_form_adicionar)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.edit_btn = tk.Button(self.btn_frame, text="Editar", command=self.abrir_form_editar)
        self.edit_btn.grid(row=0, column=1, padx=5)

        self.done_btn = tk.Button(self.btn_frame, text="Concluir", command=self.concluir)
        self.done_btn.grid(row=0, column=2, padx=5)

        self.remove_btn = tk.Button(self.btn_frame, text="Remover", command=self.remover)
        self.remove_btn.grid(row=0, column=3, padx=5)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

        self.atualizar_lista()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        hoje = datetime.now()
        alerta_periodo = timedelta(days=ALERTA_DIAS)

        for t in self.tarefas:
            status = "Concluída" if t["concluida"] else "Pendente"
            prazo_str = t.get("prazo", "Sem prazo")
            if prazo_str != "Sem prazo" and not t["concluida"]:
                try:
                    prazo_dt = datetime.strptime(prazo_str, "%d/%m/%Y")
                    if hoje <= prazo_dt <= hoje + alerta_periodo:
                        status += " ⚠️ Prazo Próximo"
                except ValueError:
                    pass
            self.tree.insert("", "end", iid=t["id"],
                             values=(t["descricao"], status, t.get("data_criacao", ""), prazo_str))

    def get_tarefa_selecionada(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma tarefa.")
            return None
        for t in self.tarefas:
            if t["id"] == int(selecionado):
                return t
        return None

    def abrir_form_adicionar(self):
        TarefaForm(self.root, callback=self.adicionar_tarefa)

    def adicionar_tarefa(self, descricao, prazo):
        nova_tarefa = {
            "id": max([t["id"] for t in self.tarefas], default=0) + 1,
            "descricao": descricao,
            "concluida": False,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "prazo": prazo
        }
        self.tarefas.append(nova_tarefa)
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()
        self.status_label.config(text="Tarefa adicionada!")

    def abrir_form_editar(self):
        tarefa = self.get_tarefa_selecionada()
        if tarefa:
            TarefaForm(self.root, tarefa=tarefa, callback=self.editar_tarefa)

    def editar_tarefa(self, descricao, prazo):
        tarefa = self.get_tarefa_selecionada()
        if tarefa:
            tarefa["descricao"] = descricao
            tarefa["prazo"] = prazo
            salvar_tarefas(self.tarefas)
            self.atualizar_lista()
            self.status_label.config(text="Tarefa editada!")

    def concluir(self):
        tarefa = self.get_tarefa_selecionada()
        if tarefa:
            tarefa["concluida"] = True
            salvar_tarefas(self.tarefas)
            self.atualizar_lista()
            self.status_label.config(text="Tarefa concluída!")

    def remover(self):
        tarefa = self.get_tarefa_selecionada()
        if tarefa:
            confirmar = messagebox.askyesno("Confirmar", f"Remover tarefa '{tarefa['descricao']}'?")
            if confirmar:
                self.tarefas.remove(tarefa)
                salvar_tarefas(self.tarefas)
                self.atualizar_lista()
                self.status_label.config(text="Tarefa removida!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
