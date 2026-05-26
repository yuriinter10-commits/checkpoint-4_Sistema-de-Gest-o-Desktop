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
        # ✅ NOVO: tabela de vendas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                nome_produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total FLOAT NOT NULL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_produto) REFERENCES produtos(id)
        )""")
        conexao.commit()
        conexao.close()
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")

def inserir_produto(nome, preco, qtd):
    try:    
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO produtos (nome, preco, qtd) VALUES (?,?,?)", (nome, preco, qtd))
            conexao.commit()
            return True
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return False

def buscar_produtos():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        resultados = cursor.fetchall()
        conexao.close()
        return resultados
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return []

def atualizar_preco(novo_preco, id_produto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_preco, id_produto))
        conexao.commit()
        sucesso = cursor.rowcount > 0
        conexao.close()
        return sucesso
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return False

def excluir_produto(id_produto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conexao.commit()
        sucesso = cursor.rowcount > 0
        conexao.close()
        return sucesso
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return False

def buscar_vendas_por_produto():
    """Retorna quantidade total vendida e faturamento agrupados por produto"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT nome_produto,
                   SUM(quantidade)   AS total_qtd,
                   SUM(valor_total)  AS total_faturamento
            FROM vendas
            GROUP BY nome_produto
            ORDER BY total_faturamento DESC
        """)
        resultados = cursor.fetchall()
        conexao.close()
        return resultados
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return []

# registra a venda e diminui o estoque
def registrar_venda(id_produto, quantidade):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Busca o produto para verificar estoque e pegar o preço
        cursor.execute("SELECT nome, preco, qtd FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            conexao.close()
            return False, "Produto não encontrado."

        nome, preco, estoque = produto

        if quantidade > estoque:
            conexao.close()
            return False, f"Estoque insuficiente. Disponível: {estoque}"

        valor_total = preco * quantidade

        # Diminui o estoque
        cursor.execute("UPDATE produtos SET qtd = qtd - ? WHERE id = ?", (quantidade, id_produto))

        # Registra a venda
        cursor.execute("""
            INSERT INTO vendas (id_produto, nome_produto, quantidade, valor_total)
            VALUES (?, ?, ?, ?)
        """, (id_produto, nome, quantidade, valor_total))

        conexao.commit()
        conexao.close()
        return True, f"Venda de '{nome}' realizada! Total: R$ {valor_total:.2f}"

    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return False, "Erro ao registrar venda."

# busca histórico de vendas
def buscar_vendas():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC")
        resultados = cursor.fetchall()
        conexao.close()
        return resultados
    except sqlite3.Error as erro:
        print(f"OCORREU UM ERRO: {erro}")
        return []

if __name__ == "__main__":
    criar_tabela()