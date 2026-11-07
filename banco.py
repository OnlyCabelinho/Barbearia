import sqlite3

def conectar():
    conexao = sqlite3.connect("barbearia.db")
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cliente (
            ID_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Telefone TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Barbeiro (
            ID_barbeiro INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Telefone TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Servico (
            ID_servico INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Preco REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Agendamento (
            ID_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
            Data TEXT NOT NULL,
            Horario TEXT NOT NULL,
            Status TEXT NOT NULL,
            ID_cliente INTEGER NOT NULL,
            ID_barbeiro INTEGER NOT NULL,
            ID_servico INTEGER NOT NULL,

            FOREIGN KEY (ID_cliente) REFERENCES Cliente(ID_cliente),
            FOREIGN KEY (ID_barbeiro) REFERENCES Barbeiro(ID_barbeiro),
            FOREIGN KEY (ID_servico) REFERENCES Servico(ID_servico)
        )
    """)

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_tabelas()

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()

    print("Tabelas encontradas:")
    for tabela in tabelas:
        print(tabela[0])

    conexao.close()

    
def inserir_dados_iniciais():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO Barbeiro (Nome, Telefone)
        SELECT 'Barbeiro Principal', '11999999999'
        WHERE NOT EXISTS (SELECT 1 FROM Barbeiro)
    """)

    cursor.execute("""
        INSERT INTO Servico (Nome, Preco)
        SELECT 'Corte de cabelo', 40.00
        WHERE NOT EXISTS (SELECT 1 FROM Servico)
    """)

    conexao.commit()
    conexao.close()
