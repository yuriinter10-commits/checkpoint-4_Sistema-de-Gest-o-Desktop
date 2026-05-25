import sys
import os

# Adiciona a pasta pai (raiz do projeto) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelo.model import inserir_produto

def cadastrar_validar_cadastro(nome, preco, qtd):
    if nome.strip() == "":
        print("Erro: Nome está vazio!")
        return False
    try:
        # CORRIGIDO: Agora converte corretamente os valores recebidos
        preco_convertido = float(preco)
        qtd_convertida = int(qtd)
        return True 
        
    except ValueError:
        # CORRIGIDO: Primeiro printa a mensagem, depois retorna False
        print("ERRO: Digite apenas numeros")
        return False

 
# Lista global para simular o banco de dados temporário
lista_produto = [
    {"id": 1, "nome": "Teclado", "qtd": 1, "preco": 1000},
    {"id": 2, "nome": "Mouse", "qtd": 1, "preco": 1000}
]
proximo_id = 3  # Controla o autoincremento para novos cadastros


def listar(lista_produto):
    if not lista_produto:
        print("Nenhum produto cadastrado.")
        return []
    
    print("\n--- LISTA DE PRODUTOS ---")
    for produto in lista_produto:
        print(f"ID: {produto['id']} | Nome: {produto['nome']} | Quantidade: {produto['qtd']} | Preço: {produto['preco']}")
    
    return lista_produto


def buscar(id_produto):
    for produto in lista_produto:
        if produto["id"] == int(id_produto):
            print(f"Produto encontrado: {produto['nome']}")
            return produto
            
    # Mapeado para fora do 'for'. 
    # Só vai rodar isso se o 'for' terminar e não achar nenhum produto.
    print(f"Produto com ID {id_produto} não foi encontrado.")
    return None
   

def editar(id_produto, novos_dados):
    produto = buscar(id_produto)
    if produto:
        # Atualiza apenas os campos que foram enviados em 'novos_dados'
        for chave, valor in novos_dados.items():
            if chave in produto:
                produto[chave] = valor
        print(f"Produto ID {id_produto} atualizado com sucesso!")
        return True
        
    return False


def excluir(id_produto):
    produto = buscar(id_produto)
    if produto:
        lista_produto.remove(produto)
        print(f"Produto ID {id_produto} excluído com sucesso!")
        return True
        
    return False

# --- APENAS PARA TESTAR SE ESTÁ FUNCIONANDO ---
if __name__ == "__main__":
    # Testando a função listar
    listar(lista_produto)
    
    # Testando a função buscar
    print("\nTestando a busca:")
    buscar(3)