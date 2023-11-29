import re
import os
from pathlib import Path


class ParserListaCotasIades:

    def parser_nome_cotas(self, caminho_arquivo_nome_cotas: Path) -> list[dict[str, str]]:
        """Extrai nomes da lista de cotas."""
        dados = []

        with open(caminho_arquivo_nome_cotas, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

            # Itera sobre as linhas pulando de 3 em 3 (cada conjunto de dados)
            for i in range(0, len(linhas), 3):
                numero = linhas[i].strip()
                inscricao = linhas[i + 1].strip()
                nome = linhas[i + 2].strip()

                # Adiciona os dados à lista como um dicionário
                dados.append({
                    "numero": numero,
                    "inscricao": inscricao,
                    "nome": nome
                })

        return dados

    def extrair_nomes_do_arquivo(self, caminho_arquivo_todos: Path) -> list[str]:
        """Extrai nomes da lista total de nomes."""
        nomes = []

        with open(caminho_arquivo_todos, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()

            # Procura por padrões usando expressões regulares
            padrao = re.compile(r'\d{10}\s([A-Z\s]+)\s\d+\sPS')
            nomes = re.findall(padrao, conteudo)

        return nomes

    def extrair_nomes_especificos(self, caminho_arquivo_cre_plano: Path) -> list[str]:
        """Extrai nomes da lista total de nomes com final específico - ATIVIDADES - DIURNO CRE PLANO PILOTO/ CRUZEIRO ..."""
        nomes_especificos = []

        with open(caminho_arquivo_cre_plano, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()

            # Procura por padrões usando expressões regulares
            padrao = re.compile(
                r'\d+\s([A-Z\s]+)\s\d+\sPS\s‐\sATIVIDADES\s‐\sDIURNO\sCRE\sPLANO\sPILOTO\/\sCRUZEIRO')
            nomes_especificos = re.findall(padrao, conteudo)

        return nomes_especificos

    def comparar_listas(self, data1: list[str], data2: list[dict[str, str]]) -> set:
        """Compara duas listas de nomes para encontrar nomes em comum."""
        nomes_minusculos = set(map(str.lower, data1))
        nomes_analisados = set(item['nome'].lower() for item in data2)

        # Calcula os nomes comuns
        nomes_comuns = nomes_minusculos.intersection(nomes_analisados)

        return nomes_comuns

    def salvar_nomes_em_txt(self, dados, caminho_arquivo_saida: Path):
            """Salva uma lista de nomes em .txt """
            with open(caminho_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
                for nome in dados:
                    arquivo_saida.write(nome + '\n')

    def main(self) -> None:
        """Execução."""
        diretorio_atual = os.getcwd()
        pasta_source = Path(diretorio_atual) / 'source'
        pasta_data = Path(diretorio_atual) / 'data'
        pasta_output = Path(diretorio_atual) / 'output'

        caminho_arquivo_nome_cotas = pasta_data / 'lista01.txt'
        caminho_arquivo_todos = pasta_data / 'lista02.txt'
        caminho_arquivo_cre_plano = pasta_data / 'lista03.txt'

        #nomes = self.extrair_nomes_do_arquivo(caminho_arquivo_todos)
        nomes_cotas = self.parser_nome_cotas(caminho_arquivo_nome_cotas)
        nomes_especificos = self.extrair_nomes_especificos(caminho_arquivo_cre_plano)
        nomes_comuns = self.comparar_listas(nomes_especificos, nomes_cotas)

        # Salva os nomes comuns em um novo arquivo
        self.salvar_nomes_em_txt(
            nomes_comuns, pasta_output / 'nomes_comuns_arquivo_saida.txt')

        # salvar_nomes_em_txt(nomes, pasta_output / 'nomes_arquivo_saida.txt')
        self.salvar_nomes_em_txt(nomes_especificos,
                            pasta_output / 'nomes_especificos_arquivo_saida.txt')

        # print('Lista Nomes')
        # print(len(nomes))
        print('Lista Nomes Cotas')
        print(len(nomes_cotas))
        print('Lista Nomes no Plano Piloto')
        print(len(nomes_especificos))
        print('Nomes comuns nas duas listas (COTAS PLANO PILOTO):')
        print(len(nomes_comuns))

if __name__ == "__main__":
    parser_lista_cotas_iades = ParserListaCotasIades()
    parser_lista_cotas_iades.main()
