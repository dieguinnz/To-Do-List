import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class TarefaForm(tk.Toplevel):
    def __init__(self, master, tarefa=None, callback=None):
        super().__init__(master)
        self.title("Tarefa")
        self.callback = callback
        self.tarefa = tarefa

        tk.Label(self, text="Descrição:").grid(row=0, column=0, sticky="e")
        self.desc_entry = tk.Entry(self, width=40)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Prazo:").grid(row=1, column=0, sticky="e")
        self.prazo_entry = DateEntry(self, date_pattern='dd/mm/yyyy')
        self.prazo_entry.grid(row=1, column=1, padx=5, pady=5)

        # Se estiver editando, preenche os dados
        if tarefa:
            self.desc_entry.insert(0, tarefa["descricao"])
            try:
                data_prazo = datetime.strptime(tarefa["prazo"], "%d/%m/%Y")
                self.prazo_entry.set_date(data_prazo)
            except Exception:
                # Se prazo inválido ou "Sem prazo", não seta nada
                pass

        self.btn_salvar = tk.Button(self, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

    def salvar(self):
        descricao = self.desc_entry.get().strip()
        prazo = self.prazo_entry.get()

        if not descricao:
            messagebox.showwarning("Erro", "Descrição não pode estar vazia.")
            return

        # Aqui já sai no formato dd/mm/yyyy do DateEntry, só precisa validar que não é futuro impossível (opcional)
        try:
            data_prazo = datetime.strptime(prazo, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Erro", "Prazo inválido.")
            return

        if self.callback:
            self.callback(descricao, prazo)
        self.destroy()
