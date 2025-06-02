#criar o esquema de orientação a objetos, dividir o código em funções e menu
#Criar menu de gerenciamento de produto final
#adicionar um esquema de datas no 
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from os import system, name

con = sqlite3.connect('produtos.db') #Se conecta com o BD e inicia o cursor
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS produtos (   
        id INTEGER PRIMARY KEY, 
        nome VARCHAR(20), 
        quantidade INTEGER
    )
''') #cria a tabela produtos com as colunas id, nome, quantidade

cur.execute('''
    CREATE TABLE IF NOT EXISTS financeiro (
        produto_id INTEGER, 
        preço_unitario FLOAT, 
        preço_total FLOAT,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
''') #cria a tabela financeiro com as colunas produto_id (que está ligada ao id do produto), preço_unitario e preço_total

cur.execute('''
    CREATE TABLE IF NOT EXISTS produto_final(
        produto_final_id INTEGER PRIMARY KEY,
        nome_produto_final VARCHAR(20),
        quantidade INTEGER,
        preço FLOAT                
    )         
''') #cria a tabela produto_final com as colunas produto_final_id, nome_produto_final, quantidade e preço

cur.execute('''
    CREATE TABLE IF NOT EXISTS controle_de_receita(
            receitas VARCHAR(30),
            preço_receitas FLOAT
            )            
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS controle_de_despesas(
            despesas VARCHAR(30),
            preço_despesas FLOAT
            )            
''') 
con.commit() #salva as alterações no bd




def escolha_uma_opcao(): #cria um visual pro menu ficar mais estético
    print(f'{20 * "-="}')
    print(f"{10 * ' '}Escolha uma opção")
    print(f'{20 * "-="}')



def limpar_tela(): #é responsável por limpar a tela dps de uma interação com o menu
    system('cls' if name == 'nt' else 'clear')
    


#def definir_preco_total():

#funções responsáveis pelo produto final

def calcular_produto_final():
      precos_produtos = []
      quantidade_produtos_usados = int(input('Quantos ingredientes foram usados para fazer o produto final: '))
      for i in range(quantidade_produtos_usados):
        while True:
            produto_usado = input(f'Digite o nome do {i+1}º produto utilizado: \nCaso queira sair, digite: sair\n').lower().strip()
            cur.execute("SELECT * FROM produtos WHERE nome = ?", (produto_usado,))
            resultado_produto_utilizado = cur.fetchone()

            if not resultado_produto_utilizado:
                input('Produto não encontrado ❌ \nTente novamente...')
                continue

            try:
                quantidade_produtos = int(input(f"Digite a quantidade de {produto_usado} utilizada: "))
            except ValueError:
                input("Quantidade inválida ❌ \nTente novamente...")
                continue

            if quantidade_produtos <= 0 or quantidade_produtos > resultado_produto_utilizado[2]:
                input('Quantidade insuficiente ❌ \nTente novamente...')
                continue

            # Produto encontrado e quantidade válida
            id_produto_utilizado = resultado_produto_utilizado[0]
            quantidade_produtos_utilizado = resultado_produto_utilizado[2]

            cur.execute("SELECT * FROM financeiro WHERE produto_id = ?", (id_produto_utilizado,))
            resultado_financeiro_preco = cur.fetchone()
            preco_produto_utilizado = resultado_financeiro_preco[1]

            nova_quantidade_produto_utilizado = quantidade_produtos_utilizado - quantidade_produtos

            cur.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade_produto_utilizado, id_produto_utilizado))
            preco_total_pago = quantidade_produtos * preco_produto_utilizado
            precos_produtos.append(preco_total_pago)

            if nova_quantidade_produto_utilizado == 0:
                cur.execute("DELETE FROM produtos WHERE nome = ?", (produto_usado,))
            
            break      
      produto_final = str(input("Digite o nome do produto que foi criado: ")).lower().strip()
      quantidade_produtos_finais = int(input("Digite a quantidade de produtos finais gerados: "))
      precos_totais_dos_produtos = []
      for i in range(quantidade_produtos_usados):
            preco_do_produto = precos_produtos[i]
            preco_produto_final = preco_do_produto / quantidade_produtos_finais
            precos_totais_dos_produtos.append(preco_produto_final)
      preco_total_produto_final = sum(precos_totais_dos_produtos)
      cur.execute("INSERT INTO produto_final (nome_produto_final, quantidade, preço) VALUES (?, ?, ?)", (produto_final, quantidade_produtos_finais, preco_total_produto_final,))
      input('Produto adicionado com sucesso ✅')     
con.commit()



def remover_produtos_finais():
    produto_final_rmv = str(input("Digite o nome do produto: ")).lower().strip()
    cur.execute("SELECT * FROM produto_final WHERE nome_produto_final = ?", (produto_final_rmv,))
    resultado_prod_final = cur.fetchone()
    if not resultado_prod_final:
        input("Produto não encontrado, tente novamente.")
    else:
        cur.execute("DELETE FROM produto_final WHERE nome_produto_final = ?", (produto_final_rmv,))
        con.commit()
        input("✅ Produto removido com sucesso. \nAperte Enter para continuar...")


def remover_quantidade_produto_final():
    produto_final_rmv = str(input("Digite o nome do produto: ")).lower().strip()
    quantidade_final_rmv = int(input("Digite a quantidade: "))
    cur.execute("SELECT * FROM produto_final WHERE nome_produto_final = ?", (produto_final_rmv,))
    resultado = cur.fetchone()
    id_produto_rmv_quantidade = resultado[0]
    if not resultado:
        input("Produto não encontrado, tente novamente.")
    else:
        quantidade_produto = resultado[2]
        nova_quantidade_produto = quantidade_produto - quantidade_final_rmv

        if nova_quantidade_produto < 0:
            input("A quantidade digitada é maior do que a disponível em estoque. Tente novamente.")
        else:
            cur.execute("UPDATE produto_final SET quantidade = ? WHERE produto_final_id = ?", (nova_quantidade_produto, id_produto_rmv_quantidade))
            print(f"A quantidade de {produto_final_rmv} foi alterada com sucesso! ✅")
            input("Aperte enter para continuar...")

        if nova_quantidade_produto == 0:
            cur.execute("DELETE FROM produtos WHERE nome = ?", (produto_final_rmv,))
            cur.execute("DELETE FROM financeiro WHERE produto_id = ?", (id_produto_rmv_quantidade,))



def listar_produto_final():
    nome_produto_final_listar = str(input('Digite o nome do produto: '))
    cur.execute('SELECT * FROM produto_final WHERE nome_produto_final = ?', (nome_produto_final_listar,))
    produto_final_listado = cur.fetchone()
    if produto_final_listado:
        print(f'Produto: {produto_final_listado[1]:<15}  Quantidade: {produto_final_listado[2]:<10} Preço: {produto_final_listado[3]:<5}')
        input('Pressione enter para continuar...')
    else:
        input('Produto não encontrado ❌')



def listar_todos_produtos_finais():
    cur.execute('SELECT * FROM produto_final')
    resultado_todos_finais = cur.fetchall()
    if resultado_todos_finais:
        for resultado in resultado_todos_finais:
            print(f'Produto: {resultado[1]:<15}  Quantidade: {resultado[2]:<10}  Preço: {resultado[3]}')
        input('Pressione enter para continuar...')
    else:
        input('Nenhum produto encontrado ❌')
        



#Funções responsáveis por gerenciamento de produtos brutos:

def adicionar_produtos_db(): #função responsável por adicionar o produto e o preço unitário no banco de dados e se o produto já existir, ele adiciona apenas a quantidade()
    produto_add = str(input("Digite o nome do produto: ")).lower()
    quantidade_produtos_add = int(input("Digite a quantidade de produtos: "))
    

    cur.execute('SELECT * FROM produtos WHERE nome = ?', (produto_add,))#zebra
    resultado = cur.fetchone()
    

    if not resultado:
        preco = float(input("Digite o preço unitário do produto: "))
        preco_total = quantidade_produtos_add * preco

        cur.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (produto_add, quantidade_produtos_add))
        produto_last_id = cur.lastrowid
        cur.execute("INSERT INTO financeiro (produto_id, preço_unitario, preço_total) VALUES (?, ?, ?)", (produto_last_id, preco, preco_total))
        con.commit()
        input("✅ Produto novo adicionado com sucesso. \nAperte Enter para continuar...")

    else:
        produto_id = resultado[0]
        quantidade_atual = resultado[2]
        nova_quantidade = quantidade_atual + quantidade_produtos_add
        
        cur.execute("SELECT preço_total FROM financeiro WHERE produto_id = ?", (produto_id,))
        resultado2 = cur.fetchone()
        _=resultado2

        cur.execute("SELECT preço_unitario FROM financeiro WHERE produto_id = ?", (produto_id,))
        resultado_preco = cur.fetchone()
        print(resultado_preco)

        cur.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, produto_id))
        preco_atualizado = resultado2[0] + (quantidade_produtos_add * resultado_preco[0])
        cur.execute("UPDATE financeiro SET preço_total = ? WHERE produto_id = ?", (preco_atualizado, produto_id,))
        con.commit()
        input("✅ Quantidade atualizada com sucesso. \nAperte Enter para continuar...")



def remover_produtos_db():   #função responsável por deletar o produto 
    produto_rmv = str(input("Digite o nome do produto: ")).lower().strip()
    cur.execute("SELECT * FROM produtos WHERE nome = ?", (produto_rmv,))#zebra
    resultado = cur.fetchone()
    if not resultado:
        input("Produto não encontrado, tente novamente.")
    else:
        id_produto = resultado[0]
        cur.execute("DELETE FROM produtos WHERE nome = ?", (produto_rmv,))
        cur.execute("DELETE FROM financeiro WHERE produto_id = ?", (id_produto,))
        con.commit()
        input("✅ Produto removido com sucesso. \nAperte Enter para continuar...")


def remover_quantidade_produto_bruto(): #função responsável por cuidar da parte de "uso" dos produtos, caso tenha sido usado uma quantidade, ele deleta apenas a quantidade, se tudo tiver sido usado, deleta a quantidade e o produto do bd
    produto_rmv = str(input("Digite o nome do produto: ")).lower().strip()
    quantidade_rmv = int(input("Digite a quantidade: "))
    cur.execute("SELECT * FROM produtos WHERE nome = ?", (produto_rmv,))
    resultado = cur.fetchone()
    id_produto_rmvquantidade = resultado[0] 
    if not resultado:
        input("Produto não encontrado, tente novamente.")
    else:
        produto_id = resultado[0]
        quantidade_produto = resultado[2]
        nova_quantidade_produto = quantidade_produto - quantidade_rmv

        if nova_quantidade_produto < 0:
            input("A quantidade digitada é maior do que a disponível em estoque. Tente novamente.")
        else:
            cur.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade_produto, produto_id))
            print(f"A quantidade de {produto_rmv} foi alterada com sucesso! ✅")
            input("Aperte enter para continuar...")

        if nova_quantidade_produto == 0:
            cur.execute("DELETE FROM produtos WHERE nome = ?", (produto_rmv,))
            cur.execute("DELETE FROM financeiro WHERE produto_id = ?", (id_produto_rmvquantidade,))



def listar_produtos_db(produto_db): #lista um produto com base em pesquisa ou lista todos os produtos do banco
    cur.execute("SELECT * FROM produtos WHERE nome = ?", (produto_db,))#zebra
    resultado = cur.fetchall()
    if resultado:
        for produto in resultado:
            print(f"Nome: {produto[1]:<15}  Quantidade: {produto[2]:<10}")
    else:
        print("❌ Produto não encontrado.")


#Funções responsáveis pela administração de capital:

def adicionar_receita_fluxo(): #recebe as receitas
    nome_receita = str(input('Nome: ')).lower().strip()
    valor_receita = float(input('Valor: '))
    cur.execute('SELECT * FROM controle_de_receita WHERE receitas = ?', (nome_receita,))
    existe_receita = cur.fetchone()
    if not existe_receita:
        cur.execute("INSERT INTO controle_de_receita (receitas, preço_receitas) VALUES (?, ?)", (nome_receita, valor_receita,))
        con.commit()
        input("Receita adicionada com sucesso ✅")
    #Se já houver uma receita adiciona o valor digitado ao valor existente da própria receita
    else:
        atualizar_valor_despesa = existe_receita[1] + valor_receita
        cur.execute('UPDATE controle_de_receita SET preço_receitas = ? WHERE receitas = ?', (atualizar_valor_despesa, nome_receita,))
        con.commit()
        input('Valor da receita atualizado com sucesso ✅')


def remover_receita_fluxo():
    nome_receita_remover = input(str("Digite o nome da receita que você deseja remover: ")).lower().strip()
    cur.execute("SELECT * FROM controle_de_receita WHERE receitas = ?", (nome_receita_remover,))
    controle_de_erro_remover_receita = cur.fetchall()
    if controle_de_erro_remover_receita:
        cur.execute("DELETE FROM controle_de_receita WHERE receitas = ?", (nome_receita_remover,))
        input("Receita excluída com sucesso ✅")
        con.commit()
    else: 
        input("Receita não encontrada ❌. Tente novamente...")



def adicionar_despesa_fluxo(): #recebe as despesas
    nome_despesa = str(input("Nome: ")).lower().strip()
    valor_despesa = float(input("Valor: "))
    cur.execute('SELECT * FROM controle_de_despesas')
    existe_despesa = cur.fetchone()
    if not existe_despesa:
        cur.execute("INSERT INTO controle_de_despesas (despesas, preço_despesas) VALUES (?, ?)", (nome_despesa, valor_despesa,))
        con.commit()
        input("Despesa adicionada com sucesso ✅")
    #Se já houver uma receita adiciona o valor digitado ao valor existente da própria receita
    else:
        atualizar_valor_despesa = existe_despesa[1] + valor_despesa
        cur.execute('UPDATE controle_de_despesas SET preço_despesas = ? WHERE despesas = ?', (atualizar_valor_despesa, nome_despesa,))
        con.commit()
        input('Valor da despesa atualizado com sucesso ✅')



def remover_despesa_fluxo():
    nome_despesa_remover = input(str("Digite o nome da despesa que você deseja remover: ")).lower().strip()
    cur.execute("SELECT * FROM controle_de_despesas WHERE despesas = ?", (nome_despesa_remover,))
    controle_de_erro_remover_despesa = cur.fetchall()
    if controle_de_erro_remover_despesa:
        cur.execute("DELETE FROM controle_de_despesas WHERE despesas = ?", (nome_despesa_remover,))
        input("Despesa excluída com sucesso ✅")
        con.commit()
    else: 
        input("Despesa não encontrada ❌. Tente novamente...")



def calcular_receita(): #calcula o total de receitas - o total de despesas
    lista_receita_total = []
    lista_despesa_total = []
    cur.execute("SELECT preço_receitas FROM controle_de_receita")
    total_receita = cur.fetchall()
    cur.execute("SELECT preço_despesas FROM controle_de_despesas")
    total_despesa = cur.fetchall()
    if total_receita:
        for receita in total_receita:
            lista_receita_total.append(receita[0])
        for despesa in total_despesa:
            lista_despesa_total.append(despesa[0])
    calculo_total_receita = sum(lista_receita_total) - sum(lista_despesa_total)

    print(f"O capital restante é: >>{calculo_total_receita}<<")
    

def verificar_fluxo(): # procura as despesas e receitas e as exibe em ordem.
    limpar_tela()
    cur.execute("SELECT * FROM controle_de_receita")
    resultado_receita = cur.fetchall()
    cur.execute("SELECT * FROM controle_de_despesas")
    resultado_despesa = cur.fetchall()
    
    if resultado_receita and resultado_despesa:
        for receita in resultado_receita:
            print(f"Receita: {receita[0]:<15} Valor: {receita[1]:<10}")
        for despesa in resultado_despesa:
            print(f"Despesa: {despesa[0]:<15} Valor: {despesa[1]:<10}")
        calcular_receita()
        input("\nPressione enter para continuar... ")
    
    elif resultado_receita and not resultado_despesa:
        for receita in resultado_receita:
            print(f"Receita: {receita[0]:<15} Valor: {receita[1]:<10}")
        input("\nPressione enter para continuar... ")

    elif not resultado_receita and resultado_despesa:
        for despesa in resultado_despesa:
            print(f"Despesa: {despesa[0]:<15} Valor: {despesa[1]:<10}")
        input("\nPressione enter para continuar... ")

    else:
        limpar_tela()
        input("Não há registro de despesas ou receitas. \nPressione enter para continuar...")
    



def apagar_fluxo(): #apaga todas as receitas e despesas
    limpar_tela()
    cur.execute('SELECT * from controle_de_despesas')
    resultado_existe_despesas = cur.fetchall()
    cur.execute('SELECT * from controle_de_receita')
    resultado_existe_receitas = cur.fetchall() 

    if resultado_existe_despesas and resultado_existe_receitas:
        cur.execute('DELETE FROM controle_de_despesas')
        cur.execute('DELETE FROM controle_de_receita')
        input('Tudo foi removido ✅')
    elif resultado_existe_receitas and not resultado_existe_despesas:
        cur.execute('DELETE FROM controle_de_receita')
        input('Receitas excluídas. Não há despesas a serem excluídas.')
    elif resultado_existe_despesas and not resultado_existe_receitas:
        cur.execute('DELETE FROM controle_de_despesas')
        input('Despesas excluídas. Não há receitas a serem excluídas.')
    else:
        input('Não há nada a ser apagado. ')
    con.commit()



#funções de gráficos e relatórios
def mostrar_grafico():
    df = pd.read_excel('tabelas_vendas.xlsx')
    tabela = df.groupby(['Dia', 'Turno'])['Vendas_total'].sum().unstack()
    tabela.plot(kind='bar', figsize=(12, 6))
    plt.title('Total de vendas por Dia e Turno')
    plt.xlabel('Dia')
    plt.ylabel('Vendas totais')
    plt.legend(title='Turno')
    plt.tight_layout()
    plt.show()

    
while True:
    escolha_uma_opcao()
    #menu Principal
    escolhaMenu = int(input(' 1 - Gerenciar produto final \n 2 - Gerenciar produtos brutos \n 3 - Relatórios \n 4 - Controle de finanças \n 5 - sair ')) 
    if escolhaMenu == 1: # parte responsável pelo gerenciamento do produto final
        while True:
            limpar_tela()
            escolha_uma_opcao()
            escolha_menu_produto_final = int(input(' 1 - Adicionar produto final \n 2 - Remover produtos finais \n 3 - Ver produtos finais \n 4 - Voltar \n→ '))
            if escolha_menu_produto_final == 1:
                limpar_tela()
                calcular_produto_final()
            elif escolha_menu_produto_final == 2:
                limpar_tela()
                escolha_uma_opcao()
                #menu de remover produto final ou a quantidade
                escolha_remover_final = int(input(' 1 - Remover quantidades do produto \n 2 - Remover produtos \n 3 - Voltar \n → '))
                if escolha_remover_final == 1:
                    limpar_tela()
                    remover_quantidade_produto_final()
                elif escolha_remover_final == 2:
                    limpar_tela()
                    remover_produtos_finais()
                elif escolha_remover_final == 3:
                    limpar_tela()
                    break
            elif escolha_menu_produto_final == 3:
                limpar_tela()
                listar_produto_final()
            elif escolha_menu_produto_final == 4:
                limpar_tela()
                break
            else:
                input('Opção inválida, tente novamente.')

    elif escolhaMenu == 2: # parte responsável pelo gerenciamento dos produtos brutos
        limpar_tela()
        
        #menu de gerenciamento produtos brutos
        while True:
            escolha_uma_opcao()
            escolha_menu_produto_bruto = int(input(' 1 - Adicionar produto \n 2 - Remover produtos \n 3 - Ver produtos\n 4 - Voltar\n→ '))
            if escolha_menu_produto_bruto == 1: 
            # opção responsável por adicionar produtos brutos ao bd
                while True:
                    limpar_tela()
                    escolha_uma_opcao()
                    opcao_escolha1 = int(input(' 1 - Adicionar um produto \n 2 - Sair para o menu\n→ '))
                    if opcao_escolha1 == 1:
                        limpar_tela()
                        adicionar_produtos_db()
                    elif opcao_escolha1 == 2:
                        limpar_tela()
                        break
            elif escolha_menu_produto_bruto == 2:
                # opção responsável por remover produtos ou quantidades
                while True:
                    limpar_tela()
                    escolha_uma_opcao()
                    escolha_rmv = int(input(' 1 - Remover um produto \n 2 - Alterar a quantidade de um produto\n 3 - Sair '))
                    if escolha_rmv == 1:
                        limpar_tela()
                        remover_produtos_db()
                    elif escolha_rmv == 2:
                        remover_quantidade_produto_bruto()
                        limpar_tela()
                    elif escolha_rmv == 3:
                        limpar_tela()
                        break
            elif escolha_menu_produto_bruto == 3:
                # opção responsável por listar os produtos existentes
                while True:
                    limpar_tela()
                    escolha_uma_opcao()
                    opcao_escolha3 = int(input(' 1 - Ver um produto específico \n 2 - Ver todos os produtos \n 3 - Sair\n→ '))
                    if opcao_escolha3 == 1:
                        limpar_tela()
                        nome_produto = input("Digite o nome do produto a buscar: ").lower().strip()
                        listar_produtos_db(nome_produto)
                        input("\nAperte Enter para continuar...")
                    elif opcao_escolha3 == 2:
                        limpar_tela()
                        cur.execute("SELECT * FROM produtos")#zebra
                        produtos = cur.fetchall()
                        for produto in produtos:
                            print(f"Nome: {produto[1]:<15} Quantidade: {produto[2]:<10}")
                        input("\nAperte Enter para continuar...")
                    elif opcao_escolha3 == 3:
                        limpar_tela()
                        break
            elif escolha_menu_produto_bruto == 4:
                # encerra o menu de produtos brutos
                limpar_tela()
                break
    elif escolhaMenu == 3:
        limpar_tela()
        mostrar_grafico()
    elif escolhaMenu == 4:
        while True:
            limpar_tela()
            #menu
            escolha_uma_opcao()
            print(f""" 1 - Adicionar receita \n 2 - Adicionar despesa \n 3 - Verificar Fluxo \n 4 - Remover Despesa/Receita \n 5 - Sair \n """)
            escolha_menu_fluxo = int(input('Digite a opção:\n'))
            #adicionar receita
            if escolha_menu_fluxo == 1:
                limpar_tela()
                adicionar_receita_fluxo()
            #adicionar despesa
            elif escolha_menu_fluxo == 2:
                limpar_tela()
                adicionar_despesa_fluxo()
            #verificar fluxo
            elif escolha_menu_fluxo == 3:
                verificar_fluxo()
            #interromper menu
            elif escolha_menu_fluxo == 4:
                while True:
                    limpar_tela()
                    escolha_uma_opcao()
                    opcao_menu_remover = int(input("1 - Remover Receita \n2 - Remover Despesa \n3 - Remover tudo \n4 - Voltar \n"))
                    if opcao_menu_remover == 1:
                        limpar_tela()
                        remover_receita_fluxo()
                    elif opcao_menu_remover == 2:
                        limpar_tela()
                        remover_despesa_fluxo()
                    elif opcao_menu_remover == 3:
                        apagar_fluxo()
                    elif opcao_menu_remover == 4:
                        break
                    else: input("Digite uma opção válida.") 
            elif escolha_menu_fluxo == 5:
                limpar_tela()
                break
            #caso digite uma opção inválida
            else:
                print('Opção inválida, digite uma opção válida.')
    elif escolhaMenu == 5: # encerra o programa
        limpar_tela()
        print("👋 Saindo do programa...")
        break
con.commit() #salva todas as alterações
con.close() #fecha o bd
