
from banco import conectar


# REALIZAR AGENDAMENTO
def realizar_agendamento():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n===== REALIZAR AGENDAMENTO =====")

    cursor.execute("SELECT ID_cliente, Nome FROM Cliente ORDER BY Nome")
    clientes = cursor.fetchall()

    if not clientes:
        print("Nenhum cliente cadastrado. Cadastre um cliente primeiro!")
        conexao.close()
        return

    print("\n--- CLIENTES DISPONÍVEIS ---")
    for cliente in clientes:
        print(f"{cliente[0]} - {cliente[1]}")

    try:
        id_cliente = int(input("\nDigite o ID do cliente: "))
    except ValueError:
        print("ID inválido!")
        conexao.close()
        return

    if not any(cliente[0] == id_cliente for cliente in clientes):
        print("Cliente não encontrado!")
        conexao.close()
        return

    cursor.execute("SELECT ID_servico, Nome, Preco FROM Servico")
    servicos = cursor.fetchall()

    if not servicos:
        print("Nenhum serviço disponível!")
        conexao.close()
        return

    print("\n--- SERVIÇOS DISPONÍVEIS ---")
    for servico in servicos:
        print(f"{servico[0]} - {servico[1]} | R$ {servico[2]:.2f}")

    try:
        id_servico = int(input("\nDigite o ID do serviço: "))
    except ValueError:
        print("ID inválido!")
        conexao.close()
        return

    if not any(servico[0] == id_servico for servico in servicos):
        print("Serviço não encontrado!")
        conexao.close()
        return

    cursor.execute("SELECT ID_barbeiro FROM Barbeiro LIMIT 1")
    barbeiro = cursor.fetchone()

    if barbeiro is None:
        print("Nenhum barbeiro cadastrado!")
        conexao.close()
        return

    id_barbeiro = barbeiro[0]


    data = input("\nDigite a data (DD/MM/AAAA): ").strip()
    horario = input("Digite o horário (HH:MM): ").strip()

    if not data or not horario:
        print("Data e horário são obrigatórios!")
        conexao.close()
        return

    cursor.execute("""
        SELECT ID_agendamento
        FROM Agendamento
        WHERE Data = ?
        AND Horario = ?
        AND Status != 'Cancelado'
    """, (data, horario))

    horario_ocupado = cursor.fetchone()

    if horario_ocupado:
        print("\nEsse horário já está ocupado!")
        conexao.close()
        return

    cursor.execute("""
        INSERT INTO Agendamento
        (Data, Horario, Status, ID_cliente, ID_barbeiro, ID_servico)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data, horario, "Confirmado", id_cliente, id_barbeiro, id_servico))

    conexao.commit()
    conexao.close()

    print("\nAgendamento realizado com sucesso!")


def consultar_agendamentos():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n===== AGENDA DO BARBEIRO =====")

    cursor.execute("""
        SELECT
            A.ID_agendamento,
            C.Nome,
            S.Nome,
            A.Data,
            A.Horario,
            A.Status
        FROM Agendamento A
        INNER JOIN Cliente C
            ON A.ID_cliente = C.ID_cliente
        INNER JOIN Servico S
            ON A.ID_servico = S.ID_servico
        ORDER BY A.ID_agendamento
    """)

    agendamentos = cursor.fetchall()
    conexao.close()

    if not agendamentos:
        print("Nenhum agendamento encontrado.")
        return

    for agendamento in agendamentos:
        print("\n------------------------------")
        print(f"ID: {agendamento[0]}")
        print(f"Cliente: {agendamento[1]}")
        print(f"Serviço: {agendamento[2]}")
        print(f"Data: {agendamento[3]}")
        print(f"Horário: {agendamento[4]}")
        print(f"Status: {agendamento[5]}")
        print("------------------------------")


def cancelar_agendamento():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n===== CANCELAR AGENDAMENTO =====")

    cursor.execute("""
        SELECT ID_agendamento, Status
        FROM Agendamento
    """)

    agendamentos = cursor.fetchall()

    if not agendamentos:
        print("Não existem agendamentos cadastrados.")
        conexao.close()
        return

    print("\nAgendamentos disponíveis:")

    for agendamento in agendamentos:
        print(f"ID: {agendamento[0]} | Status: {agendamento[1]}")

    try:
        id_agendamento = int(
            input("\nDigite o ID do agendamento que deseja cancelar: ")
        )
    except ValueError:
        print("ID inválido!")
        conexao.close()
        return

    cursor.execute("""
        SELECT Status
        FROM Agendamento
        WHERE ID_agendamento = ?
    """, (id_agendamento,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("Agendamento não encontrado!")

    elif resultado[0] == "Cancelado":
        print("Este agendamento já está cancelado!")

    else:
        cursor.execute("""
            UPDATE Agendamento
            SET Status = 'Cancelado'
            WHERE ID_agendamento = ?
        """, (id_agendamento,))

        conexao.commit()
        print("Agendamento cancelado com sucesso!")

    conexao.close()
