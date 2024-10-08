import json
import os
import csv
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
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
despesas = []

# Função para atualizar as despesas
def adicionar_despesa(item, valor):
    global despesas  # Declare que você está usando a variável global
    data_atual = datetime.now().strftime("%Y-%m-%d")  # Formato AAAA-MM-DD
    despesas.append({"item": item, "valor": valor, "data": data_atual})  # Inclui a data
    print(f"Despesa adicionada: {item} - R$ {valor:.2f} em {data_atual}")

# Função para salvar insumos com cálculo do preço médio
def salvar_insumos(insumos, arquivo):
    global despesas
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

        # Adiciona a despesa
        adicionar_despesa(item, preco_novo * quantidade_nova)

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
    label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(janela, text="Preço de Compra").grid(row=1, column=1)
    tk.Label(janela, text="Quantidade Comprada").grid(row=1, column=2)

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

        campos_entrada[item] = {"preco": entrada_preco, "quantidade": entrada_quantidade}
        row += 1

    ttk.Button(janela, text="Salvar Valores", command=lambda: salvar_insumos(insumos, arquivo)).grid(row=row, column=0, columnspan=3, pady=10)
    ttk.Button(janela, text="Adicionar Item", command=lambda: adicionar_item(insumos, arquivo)).grid(row=row + 1, column=0, columnspan=3, pady=10)

    # Alternar entre insumos
    if categoria == "Alimentos":
        ttk.Button(janela, text="Trocar para Insumos Diversos", command=lambda: criar_interface_insumos(insumos_diversos, "Diversos", arquivo_diversos)).grid(row=row + 2, column=0, columnspan=3, pady=10)
    else:
        ttk.Button(janela, text="Trocar para Insumos Alimentos", command=lambda: criar_interface_insumos(insumos_alimentos, "Alimentos", arquivo_alimentos)).grid(row=row + 2, column=0, columnspan=3, pady=10)

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=row + 3, column=0, columnspan=3, pady=10)
# ---------------------------------------------------------------------------------------------------------------------
# Função para mostrar o estoque
def mostrar_estoque(insumos):
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Estoque - Quantidade, Último Preço e Preço Médio", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    tk.Label(janela, text="Item").grid(row=1, column=0)
    tk.Label(janela, text="Quantidade").grid(row=1, column=1)
    tk.Label(janela, text="Último Preço").grid(row=1, column=2)
    tk.Label(janela, text="Preço Médio").grid(row=1, column=3)

    row = 2
    for item, dados in insumos.items():
        tk.Label(janela, text=item).grid(row=row, column=0, padx=10, pady=5)
        tk.Label(janela, text=dados["quantidade"]).grid(row=row, column=1, padx=10, pady=5)
        tk.Label(janela, text=f"{dados['preco']:.2f}").grid(row=row, column=2, padx=10, pady=5)

        # Calcular o preço médio
        quantidade_atual = dados["quantidade"]
        preco_atual = dados["preco"]

        # Aqui você precisa definir os valores para `preco_novo` e `quantidade_nova` conforme necessário
        preco_novo = 0  # Defina conforme seu contexto
        quantidade_nova = 0  # Defina conforme seu contexto

        preco_medio = calcular_preco_medio(preco_atual, quantidade_atual, preco_novo, quantidade_nova)
        tk.Label(janela, text=f"{preco_medio:.2f}").grid(row=row, column=3, padx=10, pady=5)

        row += 1

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=row, column=0, columnspan=4, pady=20)

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

imagens_caminhos = [
    r"C:\Users\User\Desktop\Logo\logo1.jpeg",
    r"C:\Users\User\Desktop\Logo\logo2.jpeg",
    r"C:\Users\User\Desktop\Logo\logo3.jpeg",
]  # Adicione quantas imagens quiser

# Variável para controlar o índice da imagem atual
indice_imagem_atual = 0

def trocar_imagem():
    global indice_imagem_atual, imagem_tk

    # Carregar a nova imagem
    imagem = Image.open(imagens_caminhos[indice_imagem_atual])
    imagem = imagem.resize((450, 600))  # Redimensionar a imagem
    imagem_tk = ImageTk.PhotoImage(imagem)

    # Atualizar a label com a nova imagem
    label_imagem.config(image=imagem_tk)
    label_imagem.image = imagem_tk  # Manter a referência da imagem

    # Atualizar o índice da imagem atual
    indice_imagem_atual = (indice_imagem_atual + 1) % len(imagens_caminhos)

    # Agendar a troca da imagem novamente após 2000 ms (2 segundos)
    janela.after(5000, trocar_imagem)

# ----------------------------------------------------------------------------------------------------------------------

def tela_principal():
    global label_imagem

    # Limpar widgets anteriores
    for widget in janela.winfo_children():
        widget.destroy()

    # Exibir a imagem inicial
    imagem = Image.open(imagens_caminhos[indice_imagem_atual])
    imagem = imagem.resize((300, 300))  # Redimensionar a imagem
    imagem_tk = ImageTk.PhotoImage(imagem)

    # Exibir a imagem no canto superior direito
    label_imagem = tk.Label(janela, image=imagem_tk)
    label_imagem.image = imagem_tk  # Manter a referência da imagem
    label_imagem.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="ne")

    # Criar um LabelFrame para o Menu sem título
    menu_frame = ttk.LabelFrame(janela, text="", padding=(10, 10), labelanchor="n")  # Título removido
    menu_frame.grid(row=0, column=0, padx=10, pady=10)

    # Botões principais dentro do Menu

    ttk.Button(menu_frame, text="Vendas", command=tela_vendas).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(menu_frame, text="Lista de Pedidos", command=visualizar_pedidos).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(menu_frame, text="Compras", command=lambda: criar_interface_insumos(insumos_alimentos, "Alimentos", arquivo_alimentos)).grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(menu_frame, text="Estoque", command=lambda: mostrar_estoque(insumos_alimentos)).grid(row=3, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(menu_frame, text="Financeiro", command=abrir_financeiro).grid(row=4, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(menu_frame, text="Calculadora", command=criar_calculadora).grid(row=5, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(menu_frame, text="Salvar .CSV", command=salvar_pedidos_csv).grid(row=6, column=0, padx=10, pady=10, sticky='ew')

    # Iniciar a troca de imagens
    trocar_imagem()

def abrir_financeiro():
    # Limpar a janela para o conteúdo do Financeiro
    for widget in janela.winfo_children():
        widget.destroy()

    # Título da janela de Financeiro
    label_titulo = tk.Label(janela, text="Financeiro", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Criação do frame de opções financeiras
    financeiro_frame = ttk.LabelFrame(janela, text="Gerenciamento Financeiro", padding=(20, 20))
    financeiro_frame.grid(row=1, column=0, padx=10, pady=10)

    # Botões dentro da janela de Financeiro seguindo o padrão do menu inicial
    ttk.Button(financeiro_frame, text="Faturamento", command=mostrar_faturamento).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(financeiro_frame, text="Despesas", command=mostrar_despesas).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(financeiro_frame, text="Fluxo de Caixa", command=mostrar_fluxo_caixa).grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    ttk.Button(financeiro_frame, text="Impostos", command=mostrar_impostos).grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    # Botão para voltar à tela principal
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=2, column=0, padx=10, pady=10, sticky='ew')


# Função para gerar o relatório de faturamento com filtro de datas
def gerar_relatorio_faturamento(data_inicio, data_fim):
    # Converter as datas selecionadas para o formato correto
    data_inicio = data_inicio.strftime("%Y-%m-%d")
    data_fim = data_fim.strftime("%Y-%m-%d")

    # Filtrar pedidos pelo intervalo de datas selecionado
    pedidos_filtrados = [pedido for pedido in pedidos if data_inicio <= pedido['data'] <= data_fim]

    if not pedidos_filtrados:
        messagebox.showinfo("Relatório de Faturamento", "Nenhum pedido encontrado no período selecionado.")
        return

    # Cálculos para o relatório
    faturamento_bruto = sum(pedido['total'] for pedido in pedidos_filtrados)
    numero_vendas = len(pedidos_filtrados)
    media_valor_pedido = faturamento_bruto / numero_vendas if numero_vendas > 0 else 0.0
    total_taxas_entrega = sum(pedido.get('taxa_entrega', 0.0) for pedido in pedidos_filtrados)

    # Contabilizar os itens mais vendidos no período filtrado
    contador_itens = {}
    for pedido in pedidos_filtrados:
        for item in pedido['itens']:
            nome_item = item[0]
            if nome_item in contador_itens:
                contador_itens[nome_item] += 1
            else:
                contador_itens[nome_item] = 1

    # Ordenar itens mais vendidos por quantidade
    itens_mais_vendidos = sorted(contador_itens.items(), key=lambda x: x[1], reverse=True)

    # Montar a mensagem do relatório
    relatorio = (
        f"Relatório de Faturamento\n"
        f"Período: {data_inicio} a {data_fim}\n"
        f"Faturamento Bruto: R$ {faturamento_bruto:.2f}\n"
        f"Número de Vendas: {numero_vendas}\n"
        f"Média de Valor por Pedido: R$ {media_valor_pedido:.2f}\n"
        f"Total de Taxas de Entrega: R$ {total_taxas_entrega:.2f}\n\n"
        f"Itens Mais Vendidos:\n"
    )

    # Adicionar os itens mais vendidos ao relatório
    for item, quantidade in itens_mais_vendidos:
        relatorio += f"{item}: {quantidade} vendidos\n"

    # Exibir o relatório em uma caixa de diálogo
    messagebox.showinfo("Relatório de Faturamento", relatorio)


# Função para mostrar a janela de seleção de data e exibir o relatório de faturamento
def mostrar_faturamento():
    # Limpar a janela
    for widget in janela.winfo_children():
        widget.destroy()

    # Título da janela de Faturamento
    label_titulo = tk.Label(janela, text="Relatório de Faturamento", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Labels e campos para selecionar o intervalo de datas
    label_data_inicio = tk.Label(janela, text="Data Início:")
    label_data_inicio.grid(row=1, column=0, padx=10, pady=10)
    data_inicio = DateEntry(janela, date_pattern='y-mm-dd')
    data_inicio.grid(row=1, column=1, padx=10, pady=10)

    label_data_fim = tk.Label(janela, text="Data Fim:")
    label_data_fim.grid(row=2, column=0, padx=10, pady=10)
    data_fim = DateEntry(janela, date_pattern='y-mm-dd')
    data_fim.grid(row=2, column=1, padx=10, pady=10)

    # Botão para gerar o relatório de faturamento
    ttk.Button(janela, text="Gerar Relatório", command=lambda: gerar_relatorio_faturamento(data_inicio.get_date(), data_fim.get_date())).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Botão para voltar à tela de financeiro
    ttk.Button(janela, text="Voltar", command=abrir_financeiro).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# --------------------------------------------------------------------------------------------------------------------

# Função para mostrar o módulo de Despesas
def mostrar_despesas():
    # Limpar a janela para o conteúdo de Despesas
    for widget in janela.winfo_children():
        widget.destroy()

    # Título da janela de Despesas
    label_titulo = tk.Label(janela, text="Despesas", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Campos para o filtro de data
    tk.Label(janela, text="Data Inicial:").grid(row=1, column=0)
    entrada_data_inicial = DateEntry(janela, width=12, background='darkblue', foreground='white', borderwidth=2)
    entrada_data_inicial.grid(row=1, column=1)

    tk.Label(janela, text="Data Final:").grid(row=2, column=0)
    entrada_data_final = DateEntry(janela, width=12, background='darkblue', foreground='white', borderwidth=2)
    entrada_data_final.grid(row=2, column=1)

    # Botão para aplicar o filtro de data
    ttk.Button(janela, text="Filtrar", command=lambda: aplicar_filtro(entrada_data_inicial.get_date(), entrada_data_final.get_date())).grid(row=3, column=0, columnspan=2, pady=10)

    # Total gasto em insumos
    total_insumos = calcular_total_insumos(insumos_alimentos) + calcular_total_insumos(insumos_diversos)
    label_total_insumos = tk.Label(janela, text=f"Total Gasto em Insumos: R$ {total_insumos:.2f}")
    label_total_insumos.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Total gasto geral (pode ser atualizado conforme necessário)
    total_gasto = 0  # Defina uma lógica para calcular o total de outras despesas, se necessário
    label_total_gasto = tk.Label(janela, text=f"Total Gasto: R$ {total_gasto:.2f}")
    label_total_gasto.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Tabela de despesas (aqui você pode implementar a lógica para mostrar uma tabela, se necessário)

    # Botão para voltar à tela principal
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=6, column=0, columnspan=2, pady=10)

# Função para calcular o total gasto em insumos
def calcular_total_insumos(insumos):
    total = 0
    for item in insumos.values():
        total += item["preco"] * item["quantidade"]  # Ajuste conforme sua lógica de precificação
    return total

# Função para aplicar filtro de data
def aplicar_filtro(data_inicial, data_final):
    try:
        # Converte as datas selecionadas para o formato apropriado
        data_inicial_str = data_inicial.strftime("%Y-%m-%d")
        data_final_str = data_final.strftime("%Y-%m-%d")

        # Inicializa a lista de despesas filtradas
        despesas_filtradas = []
        
        # Filtra as despesas entre as datas
        for despesa in despesas:
            if data_inicial_str <= despesa['data'] <= data_final_str:
                despesas_filtradas.append(despesa)

        # Atualiza a interface para mostrar as despesas filtradas
        mostrar_despesas_filtradas(despesas_filtradas)

        messagebox.showinfo("Filtro de Datas", "Filtro aplicado com sucesso!")  # Exemplo de mensagem
    except Exception as e:
        messagebox.showerror("Erro", str(e))  # Mensagem de erro genérica

# Função para mostrar despesas filtradas
def mostrar_despesas_filtradas(despesas_filtradas):
    # Limpa a janela atual
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Despesas Filtradas", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Cria uma Treeview para exibir as despesas em formato de tabela
    tree = ttk.Treeview(janela, columns=("Data", "Valor", "Descrição"), show="headings")
    tree.heading("Data", text="Data")
    tree.heading("Valor", text="Valor")
    tree.heading("Descrição", text="Descrição")
    
    # Configura largura das colunas
    tree.column("Data", width=100, anchor="center")
    tree.column("Valor", width=100, anchor="center")
    tree.column("Descrição", width=200, anchor="w")

    # Adiciona as despesas filtradas à Treeview
    for despesa in despesas_filtradas:
        tree.insert("", "end", values=(despesa["data"], f"R$ {despesa['valor']:.2f}", despesa.get("item", "Sem descrição")))

    # Exibe a Treeview
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Botão para voltar à tela principal
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=len(despesas_filtradas) + 2, column=0, columnspan=3, pady=10)

# ----------------------------------------------------------------------------------------------------------------------

def mostrar_fluxo_caixa():
    # Limpa a janela atual
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Fluxo de Caixa Mensal", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Campo para selecionar o mês
    tk.Label(janela, text="Mês (1-12):").grid(row=1, column=0, padx=10, pady=10)
    campo_mes = tk.Entry(janela, width=5)
    campo_mes.grid(row=1, column=1, padx=(0, 10))

    # Campo para selecionar o ano
    tk.Label(janela, text="Ano:").grid(row=2, column=0, padx=10, pady=10)
    campo_ano = tk.Entry(janela, width=10)
    campo_ano.grid(row=2, column=1, padx=(0, 10))

    def calcular_fluxo():
        try:
            mes = int(campo_mes.get())
            ano = int(campo_ano.get())

            # Converte o mês e ano para o primeiro e último dia do mês
            primeiro_dia = datetime(ano, mes, 1)
            ultimo_dia = (primeiro_dia + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            # Calcula total de entradas e saídas
            total_vendas = sum(pedido["total"] for pedido in pedidos 
                               if primeiro_dia <= datetime.strptime(pedido["data"], "%Y-%m-%d") <= ultimo_dia)
            total_despesas = sum(despesa["valor"] for despesa in despesas 
                                 if primeiro_dia <= datetime.strptime(despesa["data"], "%Y-%m-%d") <= ultimo_dia)

            # Calcula fluxo de caixa
            fluxo_caixa = total_vendas - total_despesas

            # Exibe os resultados
            mostrar_fluxo_caixa_resultados(total_vendas, total_despesas, fluxo_caixa)

        except ValueError:
            messagebox.showwarning("Erro", "Por favor, insira valores válidos para mês e ano.")

    ttk.Button(janela, text="Calcular Fluxo de Caixa", command=calcular_fluxo).grid(row=3, column=0, columnspan=2, pady=10)

    # Botão para voltar à tela principal
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=4, column=0, columnspan=2, pady=20)

# Função para mostrar os resultados do fluxo de caixa em formato tabular
def mostrar_fluxo_caixa_resultados(total_vendas, total_despesas, fluxo_caixa):
    # Limpa a janela atual
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Resultados do Fluxo de Caixa", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Exibe os totais em formato tabular
    tk.Label(janela, text="Total de Vendas:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(janela, text=f"R$ {total_vendas:.2f}", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela, text="Total de Despesas:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    tk.Label(janela, text=f"R$ {total_despesas:.2f}", font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela, text="Fluxo de Caixa Resultante:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    tk.Label(janela, text=f"R$ {fluxo_caixa:.2f}", font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=5)

    # Botão para voltar à tela principal
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=4, column=0, columnspan=2, pady=10)

def mostrar_impostos():
    messagebox.showinfo("Impostos", "Função de Impostos ainda não implementada.")

# ----------------------------------------------------------------------------------------------------------------------
   
# Função para criar a calculadora
def criar_calculadora():
    global entrada
    janela_calculadora = tk.Tk()
    janela_calculadora.title("Calculadora")

    entrada = tk.Entry(janela_calculadora, width=20, font=("Arial", 16))
    entrada.grid(row=0, column=0, columnspan=4)

    # Adicionando o binding do teclado
    janela_calculadora.bind('<Key>', tecla_press)

    botoes = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
        ('=', 5, 0), ('%', 5, 1),
    ]

    for (texto, linha, coluna) in botoes:
        if texto == '=':
            botao = tk.Button(janela_calculadora, text=texto, command=lambda: calcular(''))
        elif texto == 'C':
            botao = tk.Button(janela_calculadora, text=texto, command=lambda: entrada.delete(0, tk.END))
        elif texto == '%':
            botao = tk.Button(janela_calculadora, text=texto, command=lambda: calcular('%'))
        else:
            botao = tk.Button(janela_calculadora, text=texto, command=lambda num=texto: adicionar_numero(num))

        botao.grid(row=linha, column=coluna, sticky="nsew", padx=5, pady=5)

    for i in range(6):
        janela_calculadora.grid_rowconfigure(i, weight=1)
        janela_calculadora.grid_columnconfigure(i, weight=1)

    janela_calculadora.mainloop()

# Função para adicionar número na entrada da calculadora
def adicionar_numero(num):
    entrada.insert(tk.END, num)

# Função para calcular
def calcular(op):
    global entrada
    try:
        if op == '%':
            resultado = eval(entrada.get()) / 100
        else:
            resultado = eval(entrada.get())
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, str(resultado))
    except Exception as e:
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, "Erro")

# Função para capturar a tecla pressionada
def tecla_press(event):
    if event.char in '0123456789.+-*/%':
        adicionar_numero(event.char)
    elif event.keysym == 'Return':  # Enter
        calcular('')
    elif event.keysym == 'BackSpace':  # Apagar último caractere
        entrada.delete(len(entrada.get())-1)

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

    # Campo para adicionar a observação
    tk.Label(janela, text="Observação:").grid(row=2, column=0, padx=10, pady=10)
    campo_observacao = tk.Entry(janela, width=30)
    campo_observacao.grid(row=2, column=1, padx=(0, 10))  # Espaçamento à direita do campo de observação

    # Campo para adicionar a taxa de entrega
    tk.Label(janela, text="Taxa de Entrega:").grid(row=3, column=0, padx=10, pady=10)
    campo_taxa_entrega = tk.Entry(janela, width=30)  # Campo para taxa de entrega
    campo_taxa_entrega.grid(row=3, column=1, padx=(0, 10))  # Espaçamento à direita do campo de taxa de entrega

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
        hora = datetime.now().strftime("%H:%M")
        id_pedido = numero_pedido  # Usa o número do pedido atual
        total = sum(preco for _, preco in lista_pedidos)

        # Adiciona a observação ao pedido
        observacao = campo_observacao.get()
        
        # Adiciona a taxa de entrega ao pedido
        taxa_entrega = campo_taxa_entrega.get()
        taxa_entrega = float(taxa_entrega) if taxa_entrega else 0.0  # Converte a taxa para float, ou 0.0 se vazio

        pedidos.append({
            "data": data,
            "hora": hora,
            "numero_pedido": id_pedido,
            "itens": lista_pedidos,
            "total": total + taxa_entrega,  # Adiciona a taxa de entrega ao total
            "observacao": observacao,  # Adicionando a observação ao pedido
            "taxa_entrega": taxa_entrega,  # Adicionando a taxa de entrega ao pedido
            "id": id_pedido
        })
        salvar_dados(pedidos, arquivo_pedidos)

        # Salvar o número do pedido atualizado
        salvar_numero_pedido(numero_pedido)

        messagebox.showinfo("Pedido Finalizado", f"Pedido #{id_pedido} finalizado com sucesso!")
        lista_pedidos.clear()
        lista_pedidos_display.delete(0, tk.END)
        campo_observacao.delete(0, tk.END)  # Limpa o campo de observação
        campo_taxa_entrega.delete(0, tk.END)  # Limpa o campo de taxa de entrega

        numero_pedido += 1
        label_numero_pedido.config(text=f"Número do Pedido: {numero_pedido}")  # Atualiza o rótulo com o novo número

    tk.Label(janela, text="Selecione um item:").grid(row=4, column=0, padx=10, pady=10)

    combo_itens = ttk.Combobox(janela, values=list(itens_menu.keys()))
    combo_itens.grid(row=4, column=1)

    ttk.Button(janela, text="Adicionar ao Pedido", command=adicionar_pedido).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(janela, text="Finalizar Pedido", command=finalizar_pedido).grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(janela, text="Itens no Pedido:").grid(row=7, column=0, columnspan=2)
    lista_pedidos_display = tk.Listbox(janela, width=40, height=10)
    lista_pedidos_display.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=9, column=0, columnspan=2, pady=20)



# ---------------------------------------------------------------------------------------------------------------------
# Função para visualizar a lista de pedidos
def visualizar_pedidos():
    global pedidos  # Acesso à lista global de pedidos
    
    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Lista de Pedidos", font=("Arial", 14))
    label_titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Obter anos, meses e dias únicos dos pedidos
    anos = sorted(set(pedido['data'][:4] for pedido in pedidos))
    meses = sorted(set(pedido['data'][5:7] for pedido in pedidos))
    dias = sorted(set(pedido['data'][8:10] for pedido in pedidos))

    # Campos para filtrar pedidos por ano, mês e dia
    tk.Label(janela, text="Ano:").grid(row=1, column=0)
    combo_ano = ttk.Combobox(janela, values=anos)
    combo_ano.grid(row=1, column=1)

    tk.Label(janela, text="Mês:").grid(row=1, column=2)
    combo_mes = ttk.Combobox(janela, values=meses)
    combo_mes.grid(row=1, column=3)

    tk.Label(janela, text="Dia:").grid(row=1, column=4)
    combo_dia = ttk.Combobox(janela, values=dias)
    combo_dia.grid(row=1, column=5)

    def aplicar_filtro():
        ano_filtro = combo_ano.get()
        mes_filtro = combo_mes.get()
        dia_filtro = combo_dia.get()

        # Filtra pedidos com base no ano, mês e dia selecionados
        pedidos_filtrados = [
            pedido for pedido in pedidos
            if (pedido['data'].startswith(ano_filtro) if ano_filtro else True) and
               (pedido['data'][5:7] == mes_filtro if mes_filtro else True) and
               (pedido['data'][8:10] == dia_filtro if dia_filtro else True)
        ]

        # Limpa a área de pedidos antes de mostrar os filtrados
        for widget in janela.winfo_children():
            if widget not in {label_titulo, combo_ano, combo_mes, combo_dia}:
                widget.destroy()

        # Exibir resultados do filtro
        if not pedidos_filtrados:
            tk.Label(janela, text="Nenhum pedido encontrado para essa data.", fg="red").grid(row=3, column=0, columnspan=4)
        else:
            for index, pedido in enumerate(pedidos_filtrados, start=1):
                tk.Label(janela, text=pedido["data"]).grid(row=index + 3, column=0)
                tk.Label(janela, text=pedido["hora"]).grid(row=index + 3, column=1)
                tk.Label(janela, text=pedido["numero_pedido"]).grid(row=index + 3, column=2)
                ttk.Button(janela, text="Detalhes", command=lambda p=pedido: mostrar_detalhes_pedido(p)).grid(row=index + 3, column=3)

        # Botão "Voltar" para retornar à tela principal após o filtro
        ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=len(pedidos_filtrados) + 4, column=0, columnspan=4, pady=20)

    # Botão para aplicar o filtro
    ttk.Button(janela, text="Aplicar Filtro", command=aplicar_filtro).grid(row=1, column=6, pady=10)

    # Verificar se a lista de pedidos está vazia
    if not pedidos:
        tk.Label(janela, text="Nenhum pedido registrado.").grid(row=2, column=0, columnspan=4)
    else:
        for index, pedido in enumerate(pedidos, start=1):
            tk.Label(janela, text=pedido["data"]).grid(row=index + 2, column=0)
            tk.Label(janela, text=pedido["hora"]).grid(row=index + 2, column=1)
            tk.Label(janela, text=pedido["numero_pedido"]).grid(row=index + 2, column=2)
            ttk.Button(janela, text="Detalhes", command=lambda p=pedido: mostrar_detalhes_pedido(p)).grid(row=index + 2, column=3)

    # Botão "Voltar" antes de aplicar o filtro
    ttk.Button(janela, text="Voltar", command=tela_principal).grid(row=len(pedidos) + 4, column=0, columnspan=4, pady=20)

# ---------------------------------------------------------------------------------------------------------------------
# Função para mostrar detalhes de um pedido
def mostrar_detalhes_pedido(pedido):
    detalhes = "\n".join(f"{item[0]} R$ {item[1]:.2f}" for item in pedido["itens"])
    
    # Verifica se a chave 'observacao' existe e atribui um valor padrão se não existir
    observacao = pedido.get("observacao", "Nenhuma observação")  # Valor padrão se não houver observação
    taxa_entrega = pedido.get("taxa_entrega", 0.0)  # Valor padrão se não houver taxa de entrega

    mensagem = (
        f"Pedido ID: {pedido['id']}\n"
        f"Data e Hora: {pedido['data']} {pedido['hora']}\n"
        f"Itens:\n{detalhes}\n"
        f"Total: R$ {pedido['total']:.2f}\n"
        f"Observação: {observacao}\n"  # Adiciona a observação
        f"Taxa de Entrega: R$ {taxa_entrega:.2f}"  # Adiciona a taxa de entrega
    )
    
    messagebox.showinfo("Detalhes do Pedido", mensagem)

# Salvar os pedidos em .CSV

# ----------------------------------------------------------------------------------------------------------------------

def salvar_pedidos_csv():
    # Nome do arquivo .csv
    nome_arquivo = "pedidos.csv"

    # Definir os campos (colunas) do arquivo CSV
    campos = ["ID", "Data", "Hora", "Número do Pedido", "Itens", "Total", "Observação", "Taxa de Entrega"]

    try:
        # Abrir o arquivo no modo de escrita
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)

            # Escrever o cabeçalho no arquivo
            escritor_csv.writeheader()

            # Iterar sobre os pedidos e escrever os dados de cada pedido no arquivo
            for pedido in pedidos:
                # Preparar os itens como string concatenada para o CSV
                itens_str = "; ".join(f"{item[0]} R$ {item[1]:.2f}" for item in pedido["itens"])

                # Escrever uma linha no arquivo CSV
                escritor_csv.writerow({
                    "ID": pedido["id"],
                    "Data": pedido["data"],
                    "Hora": pedido["hora"],
                    "Número do Pedido": pedido["numero_pedido"],
                    "Itens": itens_str,
                    "Total": f"R$ {pedido['total']:.2f}",
                    "Observação": pedido.get("observacao", "Nenhuma observação"),
                    "Taxa de Entrega": f"R$ {pedido.get('taxa_entrega', 0.0):.2f}"
                })

        # Mensagem de sucesso ao salvar o arquivo
        messagebox.showinfo("Sucesso", f"Pedidos salvos em {nome_arquivo} com sucesso!")

    except Exception as e:
        # Mensagem de erro caso algo dê errado
        messagebox.showerror("Erro", f"Erro ao salvar pedidos em CSV: {e}")

# ---------------------------------------------------------------------------------------------------------------------
# Criando a janela principal
janela = tk.Tk()
janela.title("Avalon Burger")

# Iniciar na tela principal
tela_principal()

# Iniciar o loop da interface gráfica
janela.mainloop()

