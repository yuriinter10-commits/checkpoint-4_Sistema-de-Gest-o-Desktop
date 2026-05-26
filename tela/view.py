import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from controlador.controll import (cadastrar_validar_cadastro, listar_produto,
                                   excluir_produto_ctrl, realizar_venda,
                                   listar_vendas, dados_dashboard)

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CORES = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
         "#1abc9c", "#e67e22", "#e91e63", "#00bcd4", "#8bc34a"]

carrinho = []
tema_atual = "Dark"  # ✅ CORRIGIDO: variável global declarada aqui

# ==========================================
# 1. NAVEGAÇÃO
# ==========================================
def mostrar_pagina(frame):
    for f in [frame_cadastro, frame_listagem, frame_venda, frame_historico, frame_dashboard]:
        f.pack_forget()
    frame.pack(fill="both", expand=True, padx=30, pady=20)

# ==========================================
# 2. TEMA
# ==========================================
def alternar_tema():
    global tema_atual  # ✅ CORRIGIDO: global antes de qualquer atribuição
    if tema_atual == "Dark":
        tema_atual = "Light"
        ctk.set_appearance_mode("Light")
        btn_tema.configure(text="🌙 Tema Escuro")
    else:
        tema_atual = "Dark"
        ctk.set_appearance_mode("Dark")
        btn_tema.configure(text="☀️ Tema Claro")

# ==========================================
# 3. CADASTRO
# ==========================================
def ao_clicar():
    sucesso, mensagem = cadastrar_validar_cadastro(cx_nome.get(), cx_preco.get(), cx_qtd.get())
    if sucesso:
        lbl_aviso.configure(text=mensagem, text_color="#2ecc71")
        cx_nome.delete(0, "end")
        cx_preco.delete(0, "end")
        cx_qtd.delete(0, "end")
    else:
        lbl_aviso.configure(text=mensagem, text_color="#e74c3c")

# ==========================================
# 4. LISTAGEM
# ==========================================
def ao_excluir(id_produto):
    sucesso = excluir_produto_ctrl(id_produto)
    lbl_aviso_lista.configure(
        text=f"Produto ID {id_produto} excluído!" if sucesso else f"Erro: ID {id_produto} não encontrado.",
        text_color="#2ecc71" if sucesso else "#e74c3c"
    )
    ao_listar()

def ao_listar():
    mostrar_pagina(frame_listagem)
    produtos = listar_produto()
    for widget in frame_tabela.winfo_children():
        widget.destroy()

    if not produtos:
        ctk.CTkLabel(frame_tabela, text="Nenhum produto cadastrado.", text_color="#f39c12").pack(pady=20)
        return

    cabecalho = ctk.CTkFrame(frame_tabela, fg_color="#2c3e50")
    cabecalho.pack(fill="x", pady=(0, 2))
    for texto, largura in [("ID", 50), ("Nome", 160), ("Preço", 100), ("Qtd", 60), ("Ação", 100)]:
        ctk.CTkLabel(cabecalho, text=texto, width=largura, font=("Arial", 12, "bold")).pack(side="left", padx=5, pady=8)

    for i, p in enumerate(produtos):
        cor = "#1a252f" if i % 2 == 0 else "#1e2d3d"
        linha = ctk.CTkFrame(frame_tabela, fg_color=cor)
        linha.pack(fill="x", pady=1)
        for texto, largura in [(p['id'], 50), (p['nome'], 160), (f"R$ {p['preco']:.2f}", 100), (p['qtd'], 60)]:
            ctk.CTkLabel(linha, text=str(texto), width=largura).pack(side="left", padx=5, pady=6)
        ctk.CTkButton(linha, text="Excluir", width=90, fg_color="#e74c3c", hover_color="#c0392b",
                      command=lambda id_p=p['id']: ao_excluir(id_p)).pack(side="left", padx=5, pady=4)

# ==========================================
# 5. VENDA / CARRINHO
# ==========================================
def ao_abrir_venda():
    mostrar_pagina(frame_venda)
    lbl_aviso_venda.configure(text="")
    atualizar_dropdown()
    renderizar_carrinho()

def atualizar_dropdown():
    produtos = listar_produto()
    opcoes = [f"{p['id']} - {p['nome']} (Qtd: {p['qtd']})  R$ {p['preco']:.2f}" for p in produtos] if produtos else ["Nenhum produto cadastrado"]
    dropdown_produto.configure(values=opcoes)
    dropdown_produto.set(opcoes[0])

def ao_adicionar_carrinho():
    selecionado = dropdown_produto.get()
    quantidade  = cx_qtd_venda.get()

    if "Nenhum" in selecionado:
        lbl_aviso_venda.configure(text="Nenhum produto disponível.", text_color="#e74c3c")
        return
    try:
        qtd = int(quantidade)
        if qtd <= 0:
            raise ValueError
    except ValueError:
        lbl_aviso_venda.configure(text="Digite uma quantidade válida.", text_color="#e74c3c")
        return

    partes     = selecionado.split(" - ")
    id_produto = int(partes[0])
    nome       = partes[1].split(" (Qtd:")[0]
    preco      = float(selecionado.split("R$ ")[1])

    produtos = listar_produto()
    produto  = next((p for p in produtos if p['id'] == id_produto), None)
    if not produto:
        lbl_aviso_venda.configure(text="Produto não encontrado.", text_color="#e74c3c")
        return

    qtd_no_carrinho = sum(i['quantidade'] for i in carrinho if i['id'] == id_produto)
    if qtd + qtd_no_carrinho > produto['qtd']:
        lbl_aviso_venda.configure(text=f"Estoque insuficiente. Disponível: {produto['qtd'] - qtd_no_carrinho}", text_color="#e74c3c")
        return

    for item in carrinho:
        if item['id'] == id_produto:
            item['quantidade'] += qtd
            lbl_aviso_venda.configure(text=f"'{nome}' atualizado no carrinho.", text_color="#f39c12")
            cx_qtd_venda.delete(0, "end")
            renderizar_carrinho()
            return

    carrinho.append({"id": id_produto, "nome": nome, "preco": preco, "quantidade": qtd})
    lbl_aviso_venda.configure(text=f"'{nome}' adicionado ao carrinho!", text_color="#2ecc71")
    cx_qtd_venda.delete(0, "end")
    renderizar_carrinho()

def ao_remover_carrinho(id_produto):
    global carrinho
    carrinho = [i for i in carrinho if i['id'] != id_produto]
    renderizar_carrinho()
    lbl_aviso_venda.configure(text="Item removido do carrinho.", text_color="#f39c12")

def renderizar_carrinho():
    for widget in frame_carrinho.winfo_children():
        widget.destroy()

    if not carrinho:
        ctk.CTkLabel(frame_carrinho, text="Carrinho vazio.", text_color="#7f8c8d", font=("Arial", 11)).pack(pady=10)
        lbl_total.configure(text="Total: R$ 0,00")
        btn_finalizar.configure(state="disabled")
        return

    cab = ctk.CTkFrame(frame_carrinho, fg_color="#1a3a4a")
    cab.pack(fill="x", pady=(0, 2))
    for texto, largura in [("Produto", 160), ("Preço", 90), ("Qtd", 50), ("Subtotal", 90), ("", 80)]:
        ctk.CTkLabel(cab, text=texto, width=largura, font=("Arial", 11, "bold")).pack(side="left", padx=4, pady=6)

    total = 0
    for item in carrinho:
        subtotal = item['preco'] * item['quantidade']
        total += subtotal
        linha = ctk.CTkFrame(frame_carrinho, fg_color="#1e2d3d")
        linha.pack(fill="x", pady=1)
        for texto, largura in [(item['nome'], 160), (f"R$ {item['preco']:.2f}", 90),
                                (item['quantidade'], 50), (f"R$ {subtotal:.2f}", 90)]:
            ctk.CTkLabel(linha, text=str(texto), width=largura, font=("Arial", 11)).pack(side="left", padx=4, pady=5)
        ctk.CTkButton(linha, text="Remover", width=75, height=26, fg_color="#c0392b", hover_color="#a93226",
                      command=lambda id_p=item['id']: ao_remover_carrinho(id_p)).pack(side="left", padx=4)

    lbl_total.configure(text=f"Total: R$ {total:.2f}")
    btn_finalizar.configure(state="normal")

def ao_finalizar_venda():
    if not carrinho:
        lbl_aviso_venda.configure(text="Carrinho vazio.", text_color="#e74c3c")
        return

    erros = []
    for item in carrinho:
        sucesso, mensagem = realizar_venda(item['id'], item['quantidade'])
        if not sucesso:
            erros.append(f"{item['nome']}: {mensagem}")

    carrinho.clear()
    if erros:
        lbl_aviso_venda.configure(text="Erros: " + " | ".join(erros), text_color="#e74c3c")
    else:
        lbl_aviso_venda.configure(text="✅ Venda finalizada com sucesso!", text_color="#2ecc71")

    renderizar_carrinho()
    atualizar_dropdown()

# ==========================================
# 6. HISTÓRICO
# ==========================================
def ao_historico():
    mostrar_pagina(frame_historico)
    vendas = listar_vendas()
    for widget in frame_tabela_vendas.winfo_children():
        widget.destroy()

    if not vendas:
        ctk.CTkLabel(frame_tabela_vendas, text="Nenhuma venda registrada.", text_color="#f39c12").pack(pady=20)
        return

    cabecalho = ctk.CTkFrame(frame_tabela_vendas, fg_color="#2c3e50")
    cabecalho.pack(fill="x", pady=(0, 2))
    for texto, largura in [("ID", 40), ("Produto", 160), ("Qtd", 50), ("Total", 100), ("Data", 160)]:
        ctk.CTkLabel(cabecalho, text=texto, width=largura, font=("Arial", 12, "bold")).pack(side="left", padx=5, pady=8)

    for i, v in enumerate(vendas):
        cor = "#1a252f" if i % 2 == 0 else "#1e2d3d"
        linha = ctk.CTkFrame(frame_tabela_vendas, fg_color=cor)
        linha.pack(fill="x", pady=1)
        for texto, largura in [(v['id'], 40), (v['nome_produto'], 160), (v['quantidade'], 50),
                                (f"R$ {v['valor_total']:.2f}", 100), (v['data_venda'], 160)]:
            ctk.CTkLabel(linha, text=str(texto), width=largura).pack(side="left", padx=5, pady=6)

# ==========================================
# 7. DASHBOARD
# ==========================================
def ao_dashboard():
    mostrar_pagina(frame_dashboard)
    renderizar_graficos()

def renderizar_graficos():
    for widget in frame_graficos.winfo_children():
        widget.destroy()

    dados = dados_dashboard()

    if not dados:
        ctk.CTkLabel(frame_graficos, text="Nenhuma venda registrada para exibir.",
                     text_color="#f39c12", font=("Arial", 13)).pack(pady=40)
        return

    nomes        = [d['nome'] for d in dados]
    quantidades  = [d['quantidade'] for d in dados]
    faturamentos = [d['faturamento'] for d in dados]
    cores        = CORES[:len(nomes)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.8), facecolor="#1a1a2e")

    for ax, valores, titulo in [
        (ax1, quantidades, "Quantidade Vendida"),
        (ax2, faturamentos, "Faturamento (R$)")
    ]:
        ax.set_facecolor("#1a1a2e")
        _, _, autotexts = ax.pie(valores, labels=None, autopct="%1.1f%%", colors=cores,
                                  startangle=90, wedgeprops={"edgecolor": "#1a1a2e", "linewidth": 2})
        for at in autotexts:
            at.set_color("white")
            at.set_fontsize(8)
        ax.set_title(titulo, color="white", fontsize=11, pad=10)

    patches = [mpatches.Patch(color=cores[i], label=nomes[i]) for i in range(len(nomes))]
    fig.legend(handles=patches, loc="lower center", ncol=min(len(nomes), 4),
               fontsize=8, facecolor="#2c3e50", labelcolor="white",
               framealpha=1, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=[0, 0.08, 1, 1])

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)

# ==========================================
# 8. JANELA PRINCIPAL
# ==========================================
janela = ctk.CTk()
janela.title("Sistema de Gestão Desktop - Padrão MVC")
janela.geometry("860x640")
janela.resizable(False, False)

# ==========================================
# 9. MENU LATERAL
# ==========================================
frame_menu = ctk.CTkFrame(janela, width=200, corner_radius=0)
frame_menu.pack(side="left", fill="y")

ctk.CTkLabel(frame_menu, text="MENU", font=("Arial", 16, "bold")).pack(pady=30, padx=20)
ctk.CTkButton(frame_menu, text="Cadastrar", fg_color="transparent", border_width=1,
              command=lambda: mostrar_pagina(frame_cadastro)).pack(pady=8, padx=20, fill="x")
ctk.CTkButton(frame_menu, text="Listar Produtos", fg_color="transparent", border_width=1,
              command=ao_listar).pack(pady=8, padx=20, fill="x")
ctk.CTkButton(frame_menu, text="Realizar Venda", fg_color="#2980b9", hover_color="#1a6fa8",
              command=ao_abrir_venda).pack(pady=8, padx=20, fill="x")
ctk.CTkButton(frame_menu, text="Histórico de Vendas", fg_color="transparent", border_width=1,
              command=ao_historico).pack(pady=8, padx=20, fill="x")
ctk.CTkButton(frame_menu, text="📊 Dashboard", fg_color="#8e44ad", hover_color="#6c3483",
              command=ao_dashboard).pack(pady=8, padx=20, fill="x")

# separador e btn_tema criados AQUI, depois que frame_menu existe
ctk.CTkFrame(frame_menu, height=2, fg_color="#34495e").pack(fill="x", padx=15, pady=10)
btn_tema = ctk.CTkButton(frame_menu, text="☀️ Tema Claro", fg_color="transparent",
                          border_width=1, command=alternar_tema)
btn_tema.pack(pady=8, padx=20, fill="x", side="bottom")

# ==========================================
# 10. ÁREA CENTRAL
# ==========================================
frame_area = ctk.CTkFrame(janela, fg_color="transparent")
frame_area.pack(side="right", fill="both", expand=True)

# --- PÁGINA 1: Cadastro ---
frame_cadastro = ctk.CTkFrame(frame_area, fg_color="transparent")
ctk.CTkLabel(frame_cadastro, text="Cadastrar Produto", font=("Arial", 20, "bold")).pack(pady=(20, 20))
cx_nome  = ctk.CTkEntry(frame_cadastro, placeholder_text="Nome do produto...", width=300)
cx_nome.pack(pady=10)
cx_preco = ctk.CTkEntry(frame_cadastro, placeholder_text="Preço...", width=300)
cx_preco.pack(pady=10)
cx_qtd   = ctk.CTkEntry(frame_cadastro, placeholder_text="Quantidade...", width=300)
cx_qtd.pack(pady=10)
lbl_aviso = ctk.CTkLabel(frame_cadastro, text="", font=("Arial", 12), wraplength=400)
lbl_aviso.pack(pady=5)
ctk.CTkButton(frame_cadastro, text="Salvar Produto", command=ao_clicar, width=150).pack(pady=10)

# --- PÁGINA 2: Listagem do produto ---
frame_listagem = ctk.CTkFrame(frame_area, fg_color="transparent")
ctk.CTkLabel(frame_listagem, text="Produtos Cadastrados", font=("Arial", 20, "bold")).pack(pady=(20, 5))
ctk.CTkButton(frame_listagem, text="↻ Atualizar", command=ao_listar, width=120, fg_color="#27ae60").pack(pady=(0, 5))
lbl_aviso_lista = ctk.CTkLabel(frame_listagem, text="", font=("Arial", 12))
lbl_aviso_lista.pack()
frame_scroll = ctk.CTkScrollableFrame(frame_listagem, fg_color="transparent")
frame_scroll.pack(fill="both", expand=True, padx=20, pady=10)
frame_tabela = ctk.CTkFrame(frame_scroll, fg_color="transparent")
frame_tabela.pack(fill="both", expand=True)

# --- PÁGINA 3: Venda ---
frame_venda = ctk.CTkFrame(frame_area, fg_color="transparent")
ctk.CTkLabel(frame_venda, text="Realizar Venda", font=("Arial", 20, "bold")).pack(pady=(15, 10))
frame_selecao = ctk.CTkFrame(frame_venda, fg_color="transparent")
frame_selecao.pack(fill="x", padx=20)
ctk.CTkLabel(frame_selecao, text="Produto:", width=80, anchor="w").pack(side="left")
dropdown_produto = ctk.CTkOptionMenu(frame_selecao, values=[""], width=280)
dropdown_produto.pack(side="left", padx=5)
cx_qtd_venda = ctk.CTkEntry(frame_selecao, placeholder_text="Qtd", width=60)
cx_qtd_venda.pack(side="left", padx=5)
ctk.CTkButton(frame_selecao, text="+ Adicionar", width=100, fg_color="#27ae60",
              command=ao_adicionar_carrinho).pack(side="left", padx=5)
lbl_aviso_venda = ctk.CTkLabel(frame_venda, text="", font=("Arial", 11), wraplength=500)
lbl_aviso_venda.pack(pady=5)
ctk.CTkLabel(frame_venda, text="Carrinho:", font=("Arial", 13, "bold"), anchor="w").pack(fill="x", padx=20)
frame_scroll_carrinho = ctk.CTkScrollableFrame(frame_venda, fg_color="transparent", height=180)
frame_scroll_carrinho.pack(fill="x", padx=20, pady=5)
frame_carrinho = ctk.CTkFrame(frame_scroll_carrinho, fg_color="transparent")
frame_carrinho.pack(fill="both", expand=True)
frame_rodape = ctk.CTkFrame(frame_venda, fg_color="#1a252f")
frame_rodape.pack(fill="x", padx=20, pady=10)
lbl_total = ctk.CTkLabel(frame_rodape, text="Total: R$ 0,00", font=("Arial", 14, "bold"), text_color="#2ecc71")
lbl_total.pack(side="left", padx=15, pady=10)
btn_finalizar = ctk.CTkButton(frame_rodape, text="✅ Finalizar Venda", width=150,
                               fg_color="#2980b9", hover_color="#1a6fa8",
                               command=ao_finalizar_venda, state="disabled")
btn_finalizar.pack(side="right", padx=15, pady=10)

# --- PÁGINA 4: Histórico de vendas ---
frame_historico = ctk.CTkFrame(frame_area, fg_color="transparent")
ctk.CTkLabel(frame_historico, text="Histórico de Vendas", font=("Arial", 20, "bold")).pack(pady=(20, 5))
ctk.CTkButton(frame_historico, text="↻ Atualizar", command=ao_historico, width=120, fg_color="#27ae60").pack(pady=(0, 10))
frame_scroll_vendas = ctk.CTkScrollableFrame(frame_historico, fg_color="transparent")
frame_scroll_vendas.pack(fill="both", expand=True, padx=20, pady=10)
frame_tabela_vendas = ctk.CTkFrame(frame_scroll_vendas, fg_color="transparent")
frame_tabela_vendas.pack(fill="both", expand=True)

# --- PÁGINA 5: Dashboard ---
frame_dashboard = ctk.CTkFrame(frame_area, fg_color="transparent")
ctk.CTkLabel(frame_dashboard, text="📊 Dashboard de Vendas", font=("Arial", 20, "bold")).pack(pady=(15, 5))
ctk.CTkButton(frame_dashboard, text="↻ Atualizar", command=ao_dashboard, width=120, fg_color="#8e44ad").pack(pady=(0, 10))
frame_graficos = ctk.CTkFrame(frame_dashboard, fg_color="transparent")
frame_graficos.pack(fill="both", expand=True, padx=10)

# ==========================================
# 11. INICIALIZAÇÃO
# ==========================================
mostrar_pagina(frame_cadastro)
janela.mainloop()