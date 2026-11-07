from banco import criar_tabelas, inserir_dados_iniciais
from clientes import cadastrar_cliente
from agendamentos import realizar_agendamento, consultar_agendamentos, cancelar_agendamento

criar_tabelas()
inserir_dados_iniciais()
print("Banco de dados conectado e tabelas verificadas.")

print("================================")
print("     SISTEMA BARBEARIA")
print("================================")

print("1 - Cadastrar cliente")
print("2 - Realizar agendamento")
print("3 - Consultar agendamentos")
print("4 - Cancelar agendamento")
print("5 - Sair")

opcao = input("Escolha uma opção: ")

if opcao == "1":
    cadastrar_cliente()

elif opcao == "2":
    realizar_agendamento()

elif opcao == "3":
    consultar_agendamentos()

elif opcao == "4":
    cancelar_agendamento()

elif opcao == "5":
    print("Encerrando o sistema...")

else:
    print("Opção inválida!")