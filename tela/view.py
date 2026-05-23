import customtkinter as ctk
import controlador

def iniciar_janela_principal():
    global janela, cx_nome, lbl_aviso

    janela = ctk.CTk()
    janela.title("Exemplo Padrão MVC")
    janela.geometry("600x400")

    lbl_titulo = ctk.CTkLabel(janela, text="Cadastrar Cliente")
    lbl_titulo.pack(pady=20)

    cx_nome = ctk.CTkEntry(janela, placeholder_text="Digite o nome do cliente...")
    cx_nome.pack(pady=10)

    lbl_aviso = ctk.CTkLabel(janela, text="")
    lbl_aviso.pack(pady=5)

    btn_salvar = ctk.CTkButton(
        janela,
        text="Salvar",
        command= ao_cadastrar
    )
    btn_salvar.pack(pady=10)

    janela.mainloop()


