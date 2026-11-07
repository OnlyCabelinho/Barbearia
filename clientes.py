from banco import conectar

def cadastrar_cliente():
    print("\n===== CADASTRO DE CLIENTE =====")

    nome = input("Digite o nome do cliente: ").strip()
    telefone = input("Digite o telefone do cliente: ").strip()

    if not nome or not telefone:
        print("Erro: todos os campos são obrigatórios!")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO Cliente (Nome, Telefone) VALUES (?, ?)",
        (nome, telefone)
    )

    conexao.commit()
    conexao.close()

    print("\nCliente cadastrado com sucesso!")
