import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
import controlador.controll  # Agora ele vai encontrar 

# Configurações globais de tema e cor (Deixa o app moderno e uniforme)
ctk.set_appearance_mode("Dark")       # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")   # Temas: "blue", "green", "dark-blue"

# ==========================================
# 1. FUNÇÕES DE AÇÃO (Lógica do App)
# ==========================================
def ao_clicar():
    nome_digitado = cx_nome.get() 
    if nome_digitado:
        lbl_aviso.configure(text=f"Produto '{nome_digitado}' salvo!", text_color="#2ecc71")
        print(f"O usuário digitou: {nome_digitado}")
    else:
        lbl_aviso.configure(text="Por favor, digite o nome do produto.", text_color="#e74c3c")

def atualizar_tela():
    texto = caixa_texto.get()
    if texto:
        msg_final.configure(text=f"Olá, {texto}!")
    else:
        msg_final.configure(text="Digite algo na caixa de boas-vindas!")

# ==========================================
# 2. JANELA PRINCIPAL
# ==========================================
janela = ctk.CTk()
janela.title("Sistema de Gestão Desktop - Padrão MVC")
janela.geometry("800x500")
janela.resizable(False, False) # Evita que o usuário quebre o layout esticando a tela

# ==========================================
# 3. LAYOUT: MENU LATERAL (Navegação)
# ==========================================
frame_menu = ctk.CTkFrame(janela, width=200, corner_radius=0)
frame_menu.pack(side="left", fill="y")

# Título do Menu
lbl_menu_titulo = ctk.CTkLabel(frame_menu, text="MENU", font=("Arial", 16, "bold"))
lbl_menu_titulo.pack(pady=30, padx=20)

# Botões do Menu
btn_inicio = ctk.CTkButton(frame_menu, text="Início", fg_color="transparent", border_width=1)
btn_inicio.pack(pady=10, padx=20, fill="x")

btn_config = ctk.CTkButton(frame_menu, text="Configurações", fg_color="transparent", border_width=1)
btn_config.pack(pady=10, padx=20, fill="x")

# ==========================================
# 4. LAYOUT: ÁREA CENTRAL (Conteúdo Principal)
# ==========================================
frame_conteudo = ctk.CTkFrame(janela, fg_color="transparent")
frame_conteudo.pack(side="right", fill="both", expand=True, padx=30, pady=20)

# --- Bloco 1: Cadastro de Produto ---
lbl_titulo = ctk.CTkLabel(frame_conteudo, text="Cadastrar Produto", font=("Arial", 20, "bold"))
lbl_titulo.pack(pady=(10, 20))

cx_nome = ctk.CTkEntry(frame_conteudo, placeholder_text="Digite o nome do produto...", width=300)
cx_nome.pack(pady=10)

lbl_aviso = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 12))
lbl_aviso.pack(pady=5)

# Associado à função 'ao_clicar' (Ou use controlador.controll se estiver em arquivos separados)
btn_salvar = ctk.CTkButton(frame_conteudo, text="Salvar Produto", command=ao_clicar, width=150)
btn_salvar.pack(pady=10)

# Separador visual sutil entre as seções
separador = ctk.CTkFrame(frame_conteudo, height=2, fg_color="#34495e")
separador.pack(fill="x", pady=25)

# --- Bloco 2: Seção de Boas-Vindas ---
caixa_texto = ctk.CTkEntry(frame_conteudo, placeholder_text="Digite seu nome para boas-vindas...", width=300)
caixa_texto.pack(pady=10)

botao_entrar = ctk.CTkButton(frame_conteudo, text="Entrar", command=atualizar_tela, width=150)
botao_entrar.pack(pady=10)

msg_final = ctk.CTkLabel(frame_conteudo, text="", font=("Arial", 14, "italic"))
msg_final.pack(pady=10)

# ==========================================
# 5. INICIALIZAÇÃO
# ==========================================
janela.mainloop()

