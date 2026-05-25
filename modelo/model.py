import sqlite3


def conectar():
    return sqlite3.connect("banco.db")

def criar_tabela():
    try:    
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco FLOAT NOT NULL,                         
                qtd INT NOT NULL 
    )""")
        
        
        conexao.commit()
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")   

def inserir_produto(nome, preco, qtd):
    try:    
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO produtos (nome, preco, qtd) VALUES (?,?,?)", (nome, preco, qtd ))
                   
            conexao.commit()
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")    
   
def buscar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM produtos")
    resultados = cursor.fetchall()
    
    if len(resultados) == 0:
        print("Nenhum produto cadastrado ainda.")       
    conexao.close()

def atualizar_preco(novo_preco, id_produto):
    conexao = conectar()
    cursor = conexao.cursor()
    
    sql = "UPDATE produtos SET preco = ? WHERE id = ?"
    cursor.execute(sql, (novo_preco, id_produto))
    conexao.commit()
    
    if cursor.rowcount == 0:
        print("❌ ERRO: Produto não encontrado.")
    else:
        print("✅ Produto atualizado com sucesso!")
        
    conexao.close()

def excluir_produto(id_produtos):
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    sql = "DELETE FROM produtos WHERE id = ?"
    cursor.execute(sql, (id_produtos, ))
    conexao.commit()
    
    if cursor.rowcount == 0:
        print("❌ ERRO: Produto não existe.")
    else:
        print("✅ Produto excluído do sistema.")
        
    conexao.close()

if __name__ == "__main__":
    criar_tabela() 
    #inserir_produto("Cadeira gamer", 44.98, 20 )
    atualizar_preco(89.70, 3 )
    #excluir_produto()