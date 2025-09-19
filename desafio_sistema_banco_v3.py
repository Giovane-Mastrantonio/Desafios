from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Transacao(ABC):
    """Interface para transações bancárias"""
    
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    """Classe para operações de depósito"""
    
    def __init__(self, valor: float):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    """Classe para operações de saque"""
    
    def __init__(self, valor: float):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    """Classe para gerenciar histórico de transações"""
    
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao: Transacao):
        """Adiciona uma transação ao histórico"""
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })
    
    def gerar_relatorio(self):
        """Gera relatório do histórico de transações"""
        if not self._transacoes:
            return "Não foram realizadas movimentações."
        
        relatorio = ""
        for transacao in self._transacoes:
            relatorio += f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - {transacao['data']}\n"
        return relatorio


class Cliente:
    """Classe base para clientes do banco"""
    
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao: Transacao):
        """Realiza uma transação em uma conta específica"""
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente"""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Classe para clientes pessoa física"""
    
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    """Classe base para contas bancárias"""
    
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        """Método de classe para criar uma nova conta"""
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor: float) -> bool:
        """Realiza saque na conta"""
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        
        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        return True
    
    def depositar(self, valor: float) -> bool:
        """Realiza depósito na conta"""
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    """Classe para conta corrente com limite e limite de saques"""
    
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor: float) -> bool:
        """Realiza saque com validações específicas da conta corrente"""
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        numero_saques = len([t for t in self.historico._transacoes if t["tipo"] == "Saque"])
        
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        excedeu_saldo = valor > self._saldo
        
        if excedeu_limite:
            print(f"Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
        elif excedeu_saques:
            print(f"Operação falhou! Número máximo de {self._limite_saques} saques diários excedido.")
        elif excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class SistemaBancario:
    """Classe principal do sistema bancário"""
    
    def __init__(self):
        self.clientes = []
        self.contas = []
        self._agencia = "0001"
        self._numero_conta = 1
    
    def filtrar_cliente(self, cpf: str):
        """Filtra cliente por CPF"""
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    
    def recuperar_conta_cliente(self, cliente: PessoaFisica):
        """Recupera conta do cliente (retorna a primeira conta encontrada)"""
        if not cliente.contas:
            print("Cliente não possui conta!")
            return None
        
        # Retorna a primeira conta do cliente
        return cliente.contas[0]
    
    def criar_cliente(self):
        """Cria um novo cliente"""
        cpf = input("Informe o CPF (somente números): ")
        cliente = self.filtrar_cliente(cpf)
        
        if cliente:
            print("Já existe cliente com esse CPF!")
            return
        
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        
        cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
        self.clientes.append(cliente)
        print("Cliente criado com sucesso!")
    
    def criar_conta(self):
        """Cria uma nova conta corrente"""
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)
        
        if not cliente:
            print("Cliente não encontrado! Fluxo de criação de conta encerrado.")
            return
        
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=self._numero_conta)
        self.contas.append(conta)
        cliente.adicionar_conta(conta)
        self._numero_conta += 1
        print("Conta criada com sucesso!")
    
    def listar_contas(self):
        """Lista todas as contas cadastradas"""
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        
        for conta in self.contas:
            print("=" * 50)
            print(str(conta))
    
    def depositar(self):
        """Realiza operação de depósito"""
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        
        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)
    
    def sacar(self):
        """Realiza operação de saque"""
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        
        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)
    
    def exibir_extrato(self):
        """Exibe extrato da conta"""
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        print("\n================ EXTRATO ================")
        print(conta.historico.gerar_relatorio())
        print(f"\nSaldo: R$ {conta.saldo:.2f}")
        print("==========================================")
    
    def executar(self):
        """Executa o menu principal do sistema"""
        menu = """
========= BANCO DAS GALÁXIAS ===========

Escolha uma operação:
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[nu] Novo usuário
[lc] Listar contas
[q]  Sair

=> """
        
        while True:
            opcao = input(menu)
            
            if opcao == "d":
                self.depositar()
            
            elif opcao == "s":
                self.sacar()
            
            elif opcao == "e":
                self.exibir_extrato()
            
            elif opcao == "nc":
                self.criar_conta()
            
            elif opcao == "nu":
                self.criar_cliente()
            
            elif opcao == "lc":
                self.listar_contas()
            
            elif opcao == "q":
                print("Obrigado por usar o Banco das Galáxias!")
                break
            
            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")


def main():
    sistema = SistemaBancario()
    sistema.executar()


if __name__ == "__main__":
    main()