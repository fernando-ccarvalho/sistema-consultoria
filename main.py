from mysql.connector import Error
from tkinter import  *
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
import customtkinter as ctk
from view import (
    inserir_info,
    mostrar_info,
    atualizar_info,
    deletar_info,
    buscar_info_id
)

#===============================
# FUNÇÕES
#===============================


def limpar_campo():
    e_nome.delete(0, 'end')
    e_email.delete(0, 'end')
    e_tel.delete(0, 'end')
    e_cal.delete(0, 'end')
    e_estado.set("")
    e_assunto.delete(0, 'end')

def preencher_tabela(dados):
    for linha in tree.get_children():
        tree.delete(linha)

    for indice, item in enumerate(dados):
        tag_cor = 'par' if indice % 2 == 0 else 'impar'
        tree.insert('', 'end', values=item, tags=(tag_cor,))

def mostrar():
    try:
        lista_atualizada = mostrar_info()
    except Error as erro:
        messagebox.showerror('Erro de Banco', f'Não foi possível conectar ao banco de dados:\n{erro}')
        return
    
    preencher_tabela(lista_atualizada)



def inserir():
    nome = e_nome.get().strip()
    email = e_email.get().strip()
    tel = e_tel.get().strip()
    dia = e_cal.get().strip()
    estado = e_estado.get().strip()
    assunto = e_assunto.get().strip()

    lista = [nome, email, tel, dia, estado, assunto]

   
    if '' in lista:
        messagebox.showerror('Erro', 'Preencha todos os campos')
        return

    try:
        inserir_info(lista)
    except Error as erro:
        messagebox.showerror('Erro de Banco', f'Não foi possível salvar os dados:\n{erro}')
        return
    
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    limpar_campo()

    mostrar()

def atualizar():
    if not tree.selection():
        messagebox.showerror('Erro', 'Selecione um registro na tabela para atualizar')
        return
    
    chave_selecionada = tree.selection()[0]
        
    valores = tree.item(chave_selecionada, 'values')

    id_real = valores [0]

    nome = e_nome.get().strip()
    email = e_email.get().strip()
    tel = e_tel.get().strip()
    dia = e_cal.get().strip()
    estado = e_estado.get().strip()
    assunto = e_assunto.get().strip()
    
    lista = [nome, email, tel, dia, estado, assunto, id_real]
    if '' in lista:
        messagebox.showerror('Erro', 'Preencha todos os campos antes de atualizar')
        return
    
    try:
        atualizar_info(lista)
    except Error as erro:
        messagebox.showerror('Erro de Banco', f'Não foi possível atualizar os dados:\n{erro}')
        return
    limpar_campo()

    mostrar()

def deletar():
    
    selecionados = tree.selection()

    if not selecionados:
        messagebox.showerror('Erro', 'Selecione quem deseja deletar')
        return
    
    certeza = messagebox.askyesno('Confirmação', f'Deseja deletar {len(selecionados)} usuários?')
    if not certeza:
        return
    
    for chave in selecionados:
        valores_linha = tree.item(chave, 'values')
        id_real = [valores_linha[0]]

        try:
            deletar_info(id_real)
        except Error as erro:
            messagebox.showerror('Erro de Banco', f'Não foi possível deletar os dados:\n{erro}')
            return
    limpar_campo()
    mostrar()

def buscar():
    termo = e_busca.get().strip()
    
    if termo == '':
        messagebox.showwarning('Aviso', 'Digite algo para a busca')
        return
    
    try:
        lista_buscada = buscar_info_id(termo)
    except Error as erro:
        messagebox.showerror('Erro de Banco', f'Não foi possível buscar os dados:\n{erro}')
        return

    if not lista_buscada:
        messagebox.showinfo('Busca', f'Nenhum registro encontrado para "{termo}"')
        return
    
    preencher_tabela(lista_buscada)


def refresh():
    limpar_campo()

    e_busca.delete(0, 'end')

    if tree.selection():
        tree.selection_remove(tree.selection())

    mostrar()

def preencher_form(event):
    if not tree.selection():
            return 
    limpar_campo()
    
    selecionado = tree.selection()[0]

    valores = tree.item(selecionado, 'values')

    e_nome.insert(0, valores[1])
    e_email.insert(0, valores[2])
    e_tel.insert(0, valores[3])
    e_cal.insert(0, valores[4])
    e_estado.set(valores[5])
    e_assunto.insert(0, valores[6])

#===============================

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


janela = ctk.CTk()
janela.title('Sistema de Consultoria')
janela.geometry('1043x453')
janela.resizable(width=FALSE, height=FALSE)

frame_cima = ctk.CTkFrame(janela, width=310, height=50, corner_radius=0, fg_color="#2b3e50")
frame_cima.grid(row=0, column=0, sticky='nsew')

frame_baixo = ctk.CTkFrame(janela, width=310, height=403, corner_radius=0)
frame_baixo.grid(row=1, column=0, sticky=NSEW, pady=1)

frame_direito = ctk.CTkFrame(janela, width=733, height=453, corner_radius=0)
frame_direito.grid(row=0, column=1, rowspan=2, sticky=NSEW) 
frame_direito.grid_propagate(False)


####### Label cima

app_nome = ctk.CTkLabel(frame_cima, text='Formulário de Consultoria', font=('Segoe UI', 16, 'bold'), text_color='white')
app_nome.place(x=15, y=20)


#######     Frame baixo

### NOME

l_nome = ctk.CTkLabel(frame_baixo, text='Nome *', anchor=NW, font=('Segoe UI', 12, 'bold'))
l_nome.place(x=15, y=10)
e_nome = ctk.CTkEntry (frame_baixo, width=280, placeholder_text='Digite o nome completo')
e_nome.place(x=15, y=35)

### EMAIL

l_email = ctk.CTkLabel(frame_baixo, text='Email *', font=('Segoe UI', 12, 'bold'))
l_email.place(x=15, y=70)
e_email = ctk.CTkEntry(frame_baixo, width=280, placeholder_text='exemplo@gmail.com')
e_email.place(x=15, y=95)

### TELEFONE

l_tel = ctk.CTkLabel(frame_baixo, text='Telefone *', font=('Segoe UI', 12, 'bold'))
l_tel.place(x=15, y=130)
e_tel = ctk.CTkEntry (frame_baixo, width=280, placeholder_text='(00) 00000-0000')
e_tel.place(x=15, y=155)

### DATA DE CONSULTA

l_cal = ctk.CTkLabel(frame_baixo, text='Data da consulta *', font=('Segoe UI', 12, 'bold'))
l_cal.place(x=15, y=190)
e_cal = DateEntry(frame_baixo, width=12, bg='darkblue', fg='white', borderwidth=0, date_pattern='dd/mm/yyyy')
e_cal.place(x=15, y=215)

### ESTADO DA CONSULTA

l_estado = ctk.CTkLabel(frame_baixo, text='Estado da consulta *', font=('Segoe UI', 12, 'bold'))
l_estado.place(x=140, y=190)
e_estado = ttk.Combobox(frame_baixo, width=20, values=['Agendado', 'Confirmado', 'Cancelado', 'Concluído'], state='readonly')
e_estado.place(x=140, y=215)

### INFORMAÇÃO EXTRA

l_assunto = ctk.CTkLabel(frame_baixo, text='Informação extra *', font=('Segoe UI', 12, 'bold'))
l_assunto.place(x=15, y=250)
e_assunto = ctk.CTkEntry(frame_baixo, width=280)
e_assunto.place(x=15, y=275)

### BOTÃO INSERIR

b_inserir = ctk.CTkButton(frame_baixo, command=inserir, text='Inserir', width=80, fg_color='#2ecc71', hover_color="#27ae60", text_color='white',font=('Segoe UI', 12, 'bold'), cursor='hand2')
b_inserir.place(x=10, y=320)

### BOTÃO ATUALIZAR 

b_atualizar = ctk.CTkButton(frame_baixo, command=atualizar, text='Atualizar', width=80, font=('Segoe UI', 12, 'bold'), fg_color="#3498db", hover_color="#2980b9", text_color="white", cursor='hand2')
b_atualizar.place(x=105, y=320)

### DELETAR 

b_deletar = ctk.CTkButton(frame_baixo, command=deletar, text='Deletar', width=80, font=('Segoe UI', 12, 'bold'), fg_color="#e74c3c", hover_color="#c0392b", text_color="white", cursor='hand2')
b_deletar.place(x=195, y=320)


### MECANISMO DE BUSCA

e_busca = ctk.CTkEntry(frame_baixo, width=170, placeholder_text='Buscar usuário')
e_busca.place(x=15, y=365)

b_buscar = ctk.CTkButton(frame_baixo, command=buscar, text='\U0001F50D', width=40, cursor='hand2')
b_buscar.place(x=195, y= 365)

b_refresh = ctk.CTkButton(frame_baixo, command=refresh, text='↻', width=40, fg_color="#95a5a6", hover_color="#7f8c8d", cursor='hand2')
b_refresh.place(x=245, y=365)

################# FRAME DIREITO



tabela_head = ['ID', 'Nome', 'email', 'tel', 'Data', 'Estado', 'Sobre']


tree = ttk.Treeview(frame_direito, selectmode='extended', columns=tabela_head, show='headings')

estilo = ttk.Style()
estilo.theme_use('clam')
estilo.configure('Treeview', 
                 rowheight=28, 
                 font=('Segoe UI', 9), 
                 background='#2b3e50',
                 fieldbackground='#2b3e50',
                 foreground='white',
                 borderwidth=0)
estilo.configure('Treeview.Heading', 
                 font=('Segoe UI', 10, 'bold'), 
                 background='#38576b',
                 foreground='white',
                 relief='flat')

estilo.map('Treeview', background=[('selected', '#3498db')])

tree.tag_configure('par', background='#2c3e50')
tree.tag_configure('impar', background='#34495e')

###scroller vertical

vsb = ctk.CTkScrollbar(frame_direito, orientation='vertical', command=tree.yview)

hsb = ctk.CTkScrollbar(frame_direito, orientation='horizontal', command=tree.xview)

tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.grid(column=0, row=0, sticky=NSEW)
vsb.grid(column=1, row=0, sticky=NS)
hsb.grid(column=0, row=1, sticky=EW)

frame_direito.grid_rowconfigure(0, weight=1)
frame_direito.grid_columnconfigure(0, weight=1)
frame_direito.grid_columnconfigure(1, weight=0)

hd = ["nw", "nw", "nw", "nw", "nw", "center", "center"]
h = [35, 160, 150, 95, 90, 80, 350]

n = 0

for col in tabela_head:
    tree.heading(col, text=col.title(), anchor=CENTER)
    tree.column(col, width=h[n], anchor=hd[n], stretch=False)
   
    n += 1



tree.bind('<ButtonRelease-1>', preencher_form)



mostrar()

janela.mainloop()   