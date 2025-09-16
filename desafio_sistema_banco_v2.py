# Principais alterações:
# 1. Modularização com funções separadas:

# sacar(): Recebe argumentos apenas por nome (keyword only) usando *
# depositar(): Recebe argumentos apenas por posição (positional only)
# exibir_extrato(): Combina argumentos posicionais e nomeados usando / e *

# 2. Novas funcionalidades:

# Cadastro de usuário (criar_usuario): Armazena nome, data de nascimento, CPF e endereço
# Criação de conta corrente (criar_conta): Vincula conta ao usuário via CPF
# Listagem de contas (listar_contas): Exibe todas as contas cadastradas

# 3. Validações implementadas:

# Verificação de CPF duplicado no cadastro de usuários
# Filtro de usuários por CPF para criação de contas
# Numeração sequencial automática das contas (iniciando em 1)
# Agência fixa "0001"

# 4. Estrutura de dados:

# Usuários: Lista de dicionários com dados pessoais
# Contas: Lista de dicionários com agência, número e referência ao usuário

# 5. Menu expandido:
# Adicionadas as opções [nu] Novo usuário, [nc] Nova conta e [lc] Listar contas ao menu original.

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Função para realizar saques com argumentos nomeados apenas (keyword only).
    Retorna: saldo atualizado e extrato atualizado.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")
    elif excedeu_saques:
        print(f"Operação falhou! Número máximo de {limite_saques} saques diários excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        return saldo, extrato
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato


def depositar(saldo, valor, extrato):
    """
    Função para realizar depósitos com argumentos posicionais apenas.
    Retorna: saldo atualizado e extrato atualizado.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """
    Função para exibir extrato com argumentos posicionais e nomeados.
    Argumentos posicionais: saldo
    Argumentos nomeados: extrato
    """
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    """
    Função para cadastrar um novo usuário.
    Verifica se o CPF já está cadastrado antes de adicionar.
    """
    cpf = input("Informe o CPF (somente números): ")
    
    # Verifica se o CPF já está cadastrado
    usuario_existente = filtrar_usuario(cpf, usuarios)
    if usuario_existente:
        print("Já existe usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    
    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    """
    Função para filtrar usuário por CPF.
    Retorna o usuário se encontrado, None caso contrário.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    """
    Função para criar uma nova conta corrente.
    Vincula a conta a um usuário existente através do CPF.
    """
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print(f"Conta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
    
    print("Usuário não encontrado! Fluxo de criação de conta encerrado.")
    return None


def listar_contas(contas):
    """
    Função para listar todas as contas cadastradas.
    """
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    for conta in contas:
        linha = f"Agência: {conta['agencia']}, C/C: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}"
        print("=" * len(linha))
        print(linha)


def main():
    menu = """
========= BANCO DAS GALÁXIAS ===========

Escolha uma operação:
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair

=> """

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    AGENCIA = "0001"
    numero_conta_sequencial = 1

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta_sequencial, usuarios)
            if conta:
                contas.append(conta)
                numero_conta_sequencial += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar o Banco das Galáxias!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()