import textwrap
from datetime import datetime


class Veiculo:
    def __init__(self, nome, numeroPlaca, cor, ano, tipoCombustivel, numeroPortas, quilometragem, renavam, chassi, valorLocacao=0.0, modelo=None):
        self.nome = nome
        self.numeroPlaca = numeroPlaca
        self.cor = cor
        self.ano = ano
        self.tipoCombustivel = tipoCombustivel
        self.numeroPortas = numeroPortas
        self.quilometragem = quilometragem
        self.renavam = renavam
        self.chassi = chassi
        self.valorLocacao = valorLocacao
        self.modelo = modelo
        self.disponivel = True
        self.alugado_por = None

    @property
    def renavam(self):
        return self._renavam

    @renavam.setter
    def renavam(self, renavam):
        self._renavam = renavam

    @property
    def chassi(self):
        return self._chassi

    @chassi.setter
    def chassi(self, chassi):
        self._chassi = chassi

    def alugar(self, cliente):
        if not self.disponivel:
            print("Este veículo já está alugado.")
        else:
            self.disponivel = False
            self.alugado_por = cliente
            print(f"O veículo {self.nome} foi alugado por {cliente.nome}.")

    def devolver(self):
        if not self.disponivel:
            self.disponivel = True
            self.alugado_por = None
            print(f"O veículo {self.nome} foi devolvido com sucesso.")
        else:
            print("Este veículo já está disponível para locação.")


class RegistroLocacao:
    def __init__(self, dataLocacao: datetime, dataDevolucao: datetime, veiculo: Veiculo, cliente: 'Cliente'):
        self.dataLocacao = dataLocacao
        self.dataDevolucao = dataDevolucao
        self.veiculo = veiculo
        self.cliente = cliente


class Cliente:
    def __init__(self, nome: str, email: str, telefone: str, endereco: str):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.veiculos_alugados = []

    @classmethod
    def criar_conta(cls):
        print("=== Criar Conta ===")
        nome = input("Nome: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        endereco = input("Endereço: ")
        return cls(nome, email, telefone, endereco)


class AluguelDevolucao:
    def __init__(self):
        self.veiculos = {}

    def adicionar_veiculo(self, veiculo):
        if veiculo.nome in self.veiculos:
            self.veiculos[veiculo.nome].append(veiculo)
        else:
            self.veiculos[veiculo.nome] = [veiculo]

    def listar_veiculos_disponiveis(self):
        veiculos_disponiveis = []
        for nome, lista_veiculos in self.veiculos.items():
            for veiculo in lista_veiculos:
                if veiculo.disponivel:
                    veiculos_disponiveis.append(veiculo)
        return veiculos_disponiveis


def menu():
    menu_text = """
=============== MENU ================
[1]\tAlugar veículo
[2]\tDevolver veículo
[3]\tCriar conta
[4]\tSair
=====================================
Escolha uma opção: """
    opcao = input(textwrap.dedent(menu_text))
    while not opcao.isdigit() or not 1 <= int(opcao) <= 4:
        print("Opção inválida. Por favor, escolha uma opção de 1 a 4.")
        opcao = input("=> ")
    return opcao


def main():
    aluguel_devolucao = AluguelDevolucao()
    aluguel_devolucao.adicionar_veiculo(Veiculo("Toyota Corolla", "ABC1234", "Preto", 2020, "Gasolina", 4, 10000, "123456", "ABCDE", 100.00, "Sedan"))
    aluguel_devolucao.adicionar_veiculo(Veiculo("Honda Civic", "DEF5678", "Branco", 2018, "Diesel", 4, 8000, "789012", "FGHIJ", 120.00, "Sedan"))
    aluguel_devolucao.adicionar_veiculo(Veiculo("Volkswagen Gol", "GHI9101", "Azul", 2019, "Flex", 4, 7000, "101112", "KLMNO", 80.00, "Hatch"))
    aluguel_devolucao.adicionar_veiculo(Veiculo("Chevrolet Onix", "PQR2345", "Prata", 2017, "Flex", 4, 6000, "345678", "PQRST", 90.00, "Hatch"))
    cliente_atual = None

    while True:
        opcao = menu()

        if opcao == "1":
            if cliente_atual:
                veiculos_disponiveis = aluguel_devolucao.listar_veiculos_disponiveis()
                if veiculos_disponiveis:
                    print("Veículos disponíveis para locação:")
                    for index, veiculo in enumerate(veiculos_disponiveis, start=1):
                        print(f"{index}. {veiculo.nome} - Modelo: {veiculo.modelo} - Placa: {veiculo.numeroPlaca} - Cor: {veiculo.cor} - Valor do aluguel: R${veiculo.valorLocacao:.2f}")
                    opcao_veiculo = int(input("Escolha o veículo que deseja alugar: "))
                    if 1 <= opcao_veiculo <= len(veiculos_disponiveis):
                        veiculo_escolhido = veiculos_disponiveis[opcao_veiculo - 1]
                        veiculo_escolhido.alugar(cliente_atual)
                        cliente_atual.veiculos_alugados.append(veiculo_escolhido)
                    else:
                        print("Opção inválida.")
                else:
                    print("Não há veículos disponíveis para locação.")
            else:
                print("Por favor, crie uma conta primeiro.")
        elif opcao == "2":
            if cliente_atual:
                veiculos_alugados = [veiculo for lista in aluguel_devolucao.veiculos.values() for veiculo in lista if not veiculo.disponivel and veiculo.alugado_por == cliente_atual]
                if veiculos_alugados:
                    print("Veículos disponíveis para devolução:")
                    for index, veiculo in enumerate(veiculos_alugados, start=1):
                        print(f"{index}. {veiculo.nome} - Modelo: {veiculo.modelo} - Placa: {veiculo.numeroPlaca} - Cor: {veiculo.cor}")
                    opcao_veiculo = int(input("Escolha o veículo que deseja devolver: "))
                    if 1 <= opcao_veiculo <= len(veiculos_alugados):
                        veiculo_escolhido = veiculos_alugados[opcao_veiculo - 1]
                        veiculo_escolhido.devolver()
                        cliente_atual.veiculos_alugados.remove(veiculo_escolhido)
                    else:
                        print("Opção inválida.")
                else:
                    print("Não há veículos alugados para devolução.")
            else:
                print("Por favor, crie uma conta primeiro.")
        elif opcao == "3":
            cliente_atual = Cliente.criar_conta()
            print("Conta criada com sucesso!")
        elif opcao == "4":
            if cliente_atual:
                print("Deslogando cliente:", cliente_atual.nome)
            print("Saindo do programa...")
            break


if __name__ == "__main__":
    main()
