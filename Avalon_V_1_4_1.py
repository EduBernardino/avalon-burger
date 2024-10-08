import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk

# Arquivos para salvar os insumos e pedidos
arquivo_alimentos = 'insumos_alimentos.json'
arquivo_diversos = 'insumos_diversos.json'
arquivo_pedidos = 'pedidos.json'
arquivo_menu = 'itens_menu.json'


# ---------------------------------------------------------------------------------------------------------------------
# Funções para carregar e salvar os dados de insumos
def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# ---------------------------------------------------------------------------------------------------------------------
def salvar_dados(insumos, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(insumos, f)

# ---------------------------------------------------------------------------------------------------------------------
# Carregar os insumos do arquivo JSON
insumos_alimentos = carregar_dados(arquivo_alimentos) or {
    "Pão": {"preco": 0, "quantidade": 0},
    "Margarina": {"preco": 0, "quantidade": 0},
    "Maionese": {"preco": 0, "quantidade": 0},
    "Ketchup": {"preco": 0, "quantidade": 0},
    "Mostarda": {"preco": 0, "quantidade": 0},
    "Carne": {"preco": 0, "quantidade": 0},
    "Bacon": {"preco": 0, "quantidade": 0},
    "Alface": {"preco": 0, "quantidade": 0},
    "Tomate": {"preco": 0, "quantidade": 0},
    "Queijo": {"preco": 0, "quantidade": 0},
    "Picles": {"preco": 0, "quantidade": 0},
}

insumos_diversos = carregar_dados(arquivo_diversos) or {
    "Saches": {"preco": 0, "quantidade": 0},
    "Sacos": {"preco": 0, "quantidade": 0},
    "Papel": {"preco": 0, "quantidade": 0},
    "Gás": {"preco": 0, "quantidade": 0},
}
itens_menu = carregar_dados(arquivo_menu) or {
    "X-Burguer": {"preco": 15.99},
    "X-Salada": {"preco": 19.90},
    "X-Bacon": {"preco": 19.99},
    "Duplo Burguer": {"preco": 29.00},
}

pedidos = carregar_dados(arquivo_pedidos) or []

# Carregar pedidos do arquivo JSON
arquivo_numero_pedido = 'numero_pedido.json'

def carregar_numero_pedido():
    if os.path.exists(arquivo_numero_pedido):
        with open(arquivo_numero_pedido, 'r') as f:
            try:
                data = json.load(f)
                numero = data.get('numero_pedido', 1)  # Pega o número do pedido, padrão para 1
            except json.JSONDecodeError:
                numero = 1  # Se o JSON estiver corrompido ou não for válido
    else:
        numero = 1  # Começa em 1 se o arquivo não existir
    return numero
 #--------------------------------------------------------------------------------------------------------------------

def salvar_numero_pedido(numero):
    data = {'numero_pedido': numero}
    with open(arquivo_numero_pedido, 'w') as f:
        json.dump(data, f, indent=4)  # Escreve o número do pedido no arquivo JSON

# ---------------------------------------------------------------------------------------------------------------------

# Função para calcular o preço médio
def calcular_preco_medio(preco_atual, quantidade_atual, preco_novo, quantidade_nova):
    total_preco = (preco_atual * quantidade_atual) + (preco_novo * quantidade_nova)
    total_quantidade = quantidade_atual + quantidade_nova
    if total_quantidade == 0:
        return 0
    return total_preco / total_quantidade

# ------------------------------------------------------------------------------------------------------------------------

# Função para salvar insumos com cálculo do preço médio
def salvar_insumos(insumos, arquivo):
    for item, campos in campos_entrada.items():
        preco_novo = float(campos["preco"].get())
        quantidade_nova = float(campos["quantidade"].get())

        preco_atual = insumos[item]["preco"]
        quantidade_atual = insumos[item]["quantidade"]

        # Calcula o preço médio
        preco_medio = calcular_preco_medio(preco_atual, quantidade_atual, preco_novo, quantidade_nova)

        # Atualiza o preço e a quantidade
        insumos[item]["preco"] = preco_novo
        insumos[item]["quantidade"] += quantidade_nova
        insumos[item]["preco_medio"] = preco_medio

    salvar_dados(insumos, arquivo)
    print(f"Valores atualizados e salvos em {arquivo}")

# ---------------------------------------------------------------------------------------------------------------------
# Função para adicionar um novo item
def adicionar_item(insumos, arquivo):
    def salvar_novo_item():
        nome = entrada_nome.get()
        preco = float(entrada_preco.get())
        quantidade = float(entrada_quantidade.get())
        if nome in insumos:
            insumos[nome]["preco"] = preco
            insumos[nome]["quantidade"] += quantidade
        else:
            insumos[nome] = {"preco": preco, "quantidade": quantidade}
        salvar_dados(insumos, arquivo)
        janela_novo_item.destroy()
        criar_interface_insumos(insumos, categoria_atual, arquivo)

    janela_novo_item = tk.Toplevel()
    janela_novo_item.title("Adicionar Novo Item")
    
    tk.Label(janela_novo_item, text="Nome do Item:").grid(row=0, column=0)
    entrada_nome = tk.Entry(janela_novo_item)
    entrada_nome.grid(row=0, column=1)

    tk.Label(janela_novo_item, text="Preço de Compra:").grid(row=1, column=0)
    entrada_preco = tk.Entry(janela_novo_item)
    entrada_preco.grid(row=1, column=1)

    tk.Label(janela_novo_item, text="Quantidade Comprada:").grid(row=2, column=0)
    entrada_quantidade = tk.Entry(janela_novo_item)
    entrada_quantidade.grid(row=2, column=1)

    tk.Button(janela_novo_item, text="Salvar", command=salvar_novo_item).grid(row=3, column=0, columnspan=2)

# ---------------------------------------------------------------------------------------------------------------------
# Função para criar a interface de insumos com a nova coluna de Preço Médio
def criar_interface_insumos(insumos, categoria, arquivo):
    global categoria_atual
    categoria_atual = categoria

    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text=f"Insumos - {categoria}", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    tk.Label(janela, text="Preço de Compra").grid(row=1, column=1)
    tk.Label(janela, text="Quantidade Comprada").grid(row=1, column=2)
    tk.Label(janela, text="Preço Médio").grid(row=1, column=3)

    global campos_entrada
    campos_entrada = {}
    row = 2
    for item in insumos:
        tk.Label(janela, text=item).grid(row=row, column=0, padx=10, pady=5)

        entrada_preco = tk.Entry(janela, width=10)
        entrada_preco.grid(row=row, column=1)
        entrada_preco.insert(0, insumos[item]["preco"])

        entrada_quantidade = tk.Entry(janela, width=10)
        entrada_quantidade.grid(row=row, column=2)
        entrada_quantidade.insert(0, insumos[item]["quantidade"])

        # Exibe o preço médio calculado
        preco_medio_label = tk.Label(janela, text=f"{insumos[item].get('preco_medio', 0):.2f}")
        preco_medio_label.grid(row=row, column=3)

        campos_entrada[item] = {"preco": entrada_preco, "quantidade": entrada_quantidade}
        row += 1

    ttk.Button(janela, text="Salvar Valores", command=lambda: salvar_insumos(insumos, arquivo)).grid(row=row, column=0, columnspan=4, pady=10)
    ttk.Button(janela, text="Adicionar Item", command=lambda: adicionar_item(insumos, arquivo)).grid(row=row + 1, column=0, columnspan=4, pady=10)

    # Alternar entre insumos
    if categoria == "Alimentos":
        ttk.Button(janela, text="Trocar para Insumos Diversos", command=lambda: criar_interface_insumos(insumos_diversos, "Diversos", arquivo_diversos)).grid(row=row + 2, column=0, columnspan=4, pady=10)
    else:
        ttk.Button(janela, text="Trocar para Insumos Alimentos", command=lambda: criar_interface_insumos(insumos_alimentos, "Alimentos", arquivo_alimentos)).grid(row=row + 2, column=0, columnspan=4, pady=10)

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=row + 3, column=0, columnspan=4, pady=10)
# ---------------------------------------------------------------------------------------------------------------------
# Função para mostrar o estoque
def mostrar_estoque(insumos):
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Estoque - Quantidade e Último Preço", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(janela, text="Item").grid(row=1, column=0)
    tk.Label(janela, text="Quantidade").grid(row=1, column=1)
    tk.Label(janela, text="Último Preço").grid(row=1, column=2)

    row = 2
    for item, dados in insumos.items():
        tk.Label(janela, text=item).grid(row=row, column=0, padx=10, pady=5)
        tk.Label(janela, text=dados["quantidade"]).grid(row=row, column=1, padx=10, pady=5)
        tk.Label(janela, text=dados["preco"]).grid(row=row, column=2, padx=10, pady=5)
        row += 1

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=row, column=0, columnspan=3, pady=20)

# ---------------------------------------------------------------------------------------------------------------------
def criar_interface_menu():
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Itens do Menu", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    tk.Label(janela, text="Nome do Item").grid(row=1, column=0)
    tk.Label(janela, text="Preço (R$)").grid(row=1, column=1)

    row = 2
    for item, dados in itens_menu.items():
        tk.Label(janela, text=item).grid(row=row, column=0, padx=10, pady=5)
        tk.Label(janela, text=f"R$ {dados['preco']:.2f}").grid(row=row, column=1, padx=10, pady=5)
        row += 1

    ttk.Button(janela, text="Adicionar Item ao Menu", command=adicionar_item_menu).grid(row=row, column=0, columnspan=2, pady=10)
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=row + 1, column=0, columnspan=2, pady=10)

# ---------------------------------------------------------------------------------------------------------------------
# Função para adicionar um novo item ao menu
def adicionar_item_menu():
    def salvar_novo_item_menu():
        nome = entrada_nome.get()
        preco = float(entrada_preco.get())
        if nome in itens_menu:
            messagebox.showwarning("Atenção", "Este item já está no menu.")
        else:
            itens_menu[nome] = {"preco": preco}
            salvar_dados(itens_menu, arquivo_menu)
            janela_novo_item_menu.destroy()
            criar_interface_menu()

    janela_novo_item_menu = tk.Toplevel()
    janela_novo_item_menu.title("Adicionar Novo Item ao Menu")

    tk.Label(janela_novo_item_menu, text="Nome do Item:").grid(row=0, column=0)
    entrada_nome = tk.Entry(janela_novo_item_menu)
    entrada_nome.grid(row=0, column=1)

    tk.Label(janela_novo_item_menu, text="Preço (R$):").grid(row=1, column=0)
    entrada_preco = tk.Entry(janela_novo_item_menu)
    entrada_preco.grid(row=1, column=1)

    tk.Button(janela_novo_item_menu, text="Salvar", command=salvar_novo_item_menu).grid(row=2, column=0, columnspan=2)

# ---------------------------------------------------------------------------------------------------------------------
# Função para a tela principal

def tela_principal():
    # Limpar widgets anteriores
    for widget in janela.winfo_children():
        widget.destroy()

    # Carregar a imagem usando PIL
    imagem = Image.open(r"C:\Users\User\Desktop\Logo\logo.jpeg")  # Use o caminho corrigido
    imagem = imagem.resize((300, 300))  # Redimensionar a imagem para se ajustar ao layout
    imagem_tk = ImageTk.PhotoImage(imagem)

    # Exibir a imagem no canto superior direito
    label_imagem = tk.Label(janela, image=imagem_tk)
    label_imagem.image = imagem_tk  # Manter a referência da imagem
    label_imagem.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="ne")

    # Botões principais
    ttk.Button(janela, text="Compras", command=lambda: criar_interface_insumos(insumos_alimentos, "Alimentos", arquivo_alimentos)).grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(janela, text="Estoque", command=lambda: mostrar_estoque(insumos_alimentos)).grid(row=1, column=0, padx=10, pady=10)
    ttk.Button(janela, text="Vendas", command=tela_vendas).grid(row=2, column=0, padx=10, pady=10)

    # Botão para visualizar pedidos
    ttk.Button(janela, text="Lista de Pedidos", command=visualizar_pedidos).grid(row=3, column=0, padx=10, pady=10)

    # Novo botão "Itens do Menu"
    ttk.Button(janela, text="Itens do Menu", command=criar_interface_menu).grid(row=4, column=0, padx=10, pady=10)

# ---------------------------------------------------------------------------------------------------------------------
# Função para a tela de vendas
numero_pedido = 1

def tela_vendas():
    global numero_pedido  # Acessa a variável global para manter o número do pedido

    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Vendas", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Criação da lista de pedidos
    global lista_pedidos
    lista_pedidos = []

    # Rótulo para exibir o número do pedido
    label_numero_pedido = tk.Label(janela, text=f"Número do Pedido: {numero_pedido}", font=("Arial", 12))
    label_numero_pedido.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Criação da interface de pedidos
    def adicionar_pedido():
        item = combo_itens.get()  # Pega o item selecionado
        dados_item = itens_menu.get(item)  # Obtém os dados do item (incluindo o preço)

        if dados_item is None:  # Caso o item não esteja no dicionário, exibir um aviso
            messagebox.showwarning("Erro", "Item não encontrado no menu.")
            return
        
        preco = dados_item.get("preco")  # Acessa o preço do item
        
        if preco is None:  # Verifica se o preço foi corretamente obtido
            messagebox.showwarning("Erro", "Preço não encontrado para o item selecionado.")
            return

        lista_pedidos.append((item, preco))  # Adiciona o item e o preço à lista de pedidos
        lista_pedidos_display.insert(tk.END, f"{item} R$ {preco:.2f}")  # Exibe no listbox
        
    def finalizar_pedido():
        global numero_pedido  # Atualiza o número do pedido para o próximo
        if not lista_pedidos:
            messagebox.showwarning("Atenção", "Não há itens no pedido.")
            return

        data = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M")  # Correção aqui
        id_pedido = numero_pedido  # Usa o número do pedido atual
        total = sum(preco for _, preco in lista_pedidos)

        pedidos.append({
            "data": data,
            "hora": hora,
            "numero_pedido": id_pedido,  # Corrigido para manter consistência
            "itens": lista_pedidos,
            "total": total,
            "id": id_pedido  # Adicionando o ID ao pedido
        })
        salvar_dados(pedidos, arquivo_pedidos)

        # Salvar o número do pedido atualizado
        salvar_numero_pedido(numero_pedido)

        messagebox.showinfo("Pedido Finalizado", f"Pedido #{id_pedido} finalizado com sucesso!")
        lista_pedidos.clear()
        lista_pedidos_display.delete(0, tk.END)

        numero_pedido += 1
        label_numero_pedido.config(text=f"Número do Pedido: {numero_pedido}")  # Atualiza o rótulo com o novo número

    tk.Label(janela, text="Selecione um item:").grid(row=2, column=0, padx=10, pady=10)

    combo_itens = ttk.Combobox(janela, values=list(itens_menu.keys()))
    combo_itens.grid(row=2, column=1)

    ttk.Button(janela, text="Adicionar ao Pedido", command=adicionar_pedido).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(janela, text="Finalizar Pedido", command=finalizar_pedido).grid(row=4, column=0, columnspan=2, pady=10)

    tk.Label(janela, text="Itens no Pedido:").grid(row=5, column=0, columnspan=2)
    lista_pedidos_display = tk.Listbox(janela, width=40, height=10)
    lista_pedidos_display.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=7, column=0, columnspan=2, pady=20)

# ---------------------------------------------------------------------------------------------------------------------
# Função para visualizar a lista de pedidos
def visualizar_pedidos():
    global pedidos  # Acesso à lista global de pedidos
    
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Lista de Pedidos", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(janela, text="Data").grid(row=1, column=0)
    tk.Label(janela, text="Hora").grid(row=1, column=1)
    tk.Label(janela, text="Nº Pedido").grid(row=1, column=2)
    tk.Label(janela, text="Detalhes do Pedido").grid(row=1, column=3)

    # Verificar se a lista de pedidos está vazia
    if not pedidos:  # Se não houver pedidos
        tk.Label(janela, text="Nenhum pedido registrado.").grid(row=2, column=0, columnspan=4)  # Exibir mensagem
    else:
        for index, pedido in enumerate(pedidos, start=1):
            tk.Label(janela, text=pedido["data"]).grid(row=index + 1, column=0)  # Data na coluna 0
            tk.Label(janela, text=pedido["hora"]).grid(row=index + 1, column=1)  # Hora na coluna 1
            tk.Label(janela, text=pedido["numero_pedido"]).grid(row=index + 1, column=2)  # Nº Pedido na coluna 2
            ttk.Button(janela, text="Detalhes", command=lambda p=pedido: mostrar_detalhes_pedido(p)).grid(row=index + 1, column=3)  # Botão na coluna 3

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=len(pedidos) + 2, column=0, columnspan=4, pady=20)
# ---------------------------------------------------------------------------------------------------------------------
# Função para mostrar detalhes de um pedido
def mostrar_detalhes_pedido(pedido):
    detalhes = "\n".join(f"{item[0]} R$ {item[1]:.2f}" for item in pedido["itens"])
    mensagem = f"Pedido ID: {pedido['id']}\nData e Hora: {pedido['data']} {pedido['hora']}\nItens:\n{detalhes}\nTotal: R$ {pedido['total']:.2f}"
    messagebox.showinfo("Detalhes do Pedido", mensagem)

# ---------------------------------------------------------------------------------------------------------------------
# Criando a janela principal
janela = tk.Tk()
janela.title("Avalon Burger")

# Iniciar na tela principal
tela_principal()

# Iniciar o loop da interface gráfica
janela.mainloop()

