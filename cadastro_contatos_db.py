import sqlite3

def conectar():
    conn = sqlite3.connect("contatos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def adicionar_contato():
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone, email))
    conn.commit()
    conn.close()
    print("✅ Contato adicionado com sucesso!")

def listar_contatos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos")
    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        print("\n📋 Lista de contatos:")
        for c in resultados:
            print(f"ID: {c[0]} | Nome: {c[1]} | Telefone: {c[2]} | E-mail: {c[3]}")
    else:
        print("📭 Nenhum contato cadastrado.")

def buscar_contato():
    termo = input("Digite o nome para buscar: ").lower()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos WHERE LOWER(nome) LIKE ?", ('%' + termo + '%',))
    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        print("\n🔍 Contatos encontrados:")
        for c in resultados:
            print(f"ID: {c[0]} | Nome: {c[1]} | Telefone: {c[2]} | E-mail: {c[3]}")
    else:
        print("❌ Nenhum contato encontrado com esse nome.")

def atualizar_contato():
    listar_contatos()
    try:
        id_contato = int(input("Digite o ID do contato a atualizar: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contatos WHERE id = ?", (id_contato,))
        contato = cursor.fetchone()

        if contato:
            print("Deixe em branco para manter o valor atual.")
            novo_nome = input(f"Nome ({contato[1]}): ") or contato[1]
            novo_telefone = input(f"Telefone ({contato[2]}): ") or contato[2]
            novo_email = input(f"E-mail ({contato[3]}): ") or contato[3]

            cursor.execute("""
                UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?
            """, (novo_nome, novo_telefone, novo_email, id_contato))

            conn.commit()
            conn.close()
            print("✏️ Contato atualizado com sucesso!")
        else:
            print("⚠️ Contato não encontrado.")

    except ValueError:
        print("⚠️ ID inválido.")

def remover_contato():
    listar_contatos()
    try:
        id_contato = int(input("Digite o ID do contato a remover: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contatos WHERE id = ?", (id_contato,))
        contato = cursor.fetchone()

        if contato:
            confirmacao = input(f"Tem certeza que deseja remover '{contato[1]}'? (s/n): ").lower()
            if confirmacao == "s":
                cursor.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))
                conn.commit()
                conn.close()
                print("❌ Contato removido com sucesso!")
            else:
                print("✅ Ação cancelada.")
        else:
            print("⚠️ Contato não encontrado.")

    except ValueError:
        print("⚠️ ID inválido.")

while True:
    print("\n📒 MENU DE CONTATOS (com banco de dados)")
    print("1 - Adicionar contato")
    print("2 - Listar contatos")
    print("3 - Buscar contato por nome")
    print("4 - Atualizar contato por ID")
    print("5 - Remover contato por ID")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_contato()
    elif opcao == "2":
        listar_contatos()
    elif opcao == "3":
        buscar_contato()
    elif opcao == "4":
        atualizar_contato()
    elif opcao == "5":
        remover_contato()
    elif opcao == "0":
        print("👋 Encerrando o programa.")
        break
    else:
        print("⚠️ Opção inválida.")
