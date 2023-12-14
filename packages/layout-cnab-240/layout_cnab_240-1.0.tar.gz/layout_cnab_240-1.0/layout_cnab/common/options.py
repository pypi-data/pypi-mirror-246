from . import *

class TipoPessoa:
    FISICA = 'Física'
    JURIDICA = 'Jurídica'


class DefaultConfiguration(TypedDict):
    codigo_banco: str
    tipo_inscricao: str
    numero_inscricao_empresa: str
    codigo_convenio: str
    agencia_mantenedora_conta: str
    numero_conta_corrente: str
    digito_verificador_conta: str
    nome_empresa: str
    nome_banco: str
    endereco: str
    numero: str
    cidade: str
    cep: str
    complemento_cep: str
    uf: str
    versao_header_lote: str
    versao_header_arquivo: str
    #Notas
    g002: str
    g005: str
    g010: str
    g011: str
    g012: str
    g013a: str
    g013b: str
    g013c: str
    g014: str
    g015: str
    g016: str
    g018: str
    g032: str


class DataFrameColumns:
    AGENCIA = 'Agência'
    TIPO_PESSOA = 'Tipo Pessoa'
    CODIGO_BANCO = 'Cód Portador'
    NOME_FAVORECIDO = 'Cedente'
    DATA_PAGAMENTO = 'Data do Pagto'
    CPFJ_FAVORECIDO = 'Numero de doc'
    CONTA_CORRENTE = 'Conta Corrente'
    VALOR_PAGAMENTO = 'Valor do Pagto'
    