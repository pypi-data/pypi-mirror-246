from . import *


@dataclass
class HeaderArquivo:
    cod_banco: str = field(default='')
    lote_servico: str = field(default='')
    tipo_registro: str = field(default='0')
    tipo_inscricao_empresa: str = field(default='')
    num_inscricao_empresa: str = field(default='')
    cod_convenio: str = field(default='')
    ag_mantenedora_conta: str = field(default='')
    dig_verificador_ag: str = field(default='')
    num_conta_corrente: str = field(default='')
    dig_verificador_conta: str = field(default='')
    dig_verificador_ag_conta: str = field(default='')
    nome_empresa: str = field(default='')
    nome_banco: str = field(default='')
    cod_remessa_retorno: str = field(default='')
    dt_geracao_arquivo: str = field(default='')
    hr_geracao_arquivo: str = field(default='')
    num_sequencial_arquivo: str = field(default='')
    num_versao_layout: str = field(default='')
    densidade_gravacao_arquivo: str = field(default='')

    def build(self) -> str:
        fields = [f'field{i}' for i in range(25)]
        data = {
            f'{fields[0]}': f'{self.cod_banco:0>3}'[:3],
            f'{fields[1]}': f'{self.lote_servico:0>4}'[:4],
            f'{fields[2]}': f'{self.tipo_registro:1}'[-1],
            f'{fields[3]}': f'{"":9}',
            f'{fields[4]}': f'{self.tipo_inscricao_empresa:1}'[-1],
            f'{fields[5]}': f'{self.num_inscricao_empresa:0>14}'[:14],
            f'{fields[6]}': f'{self.cod_convenio:0>20}'[:20],
            f'{fields[7]}': f'{self.ag_mantenedora_conta:0>5}'[:5],
            f'{fields[8]}': f'{self.dig_verificador_ag:1}'[-1],
            f'{fields[9]}': f'{self.num_conta_corrente:0>12}'[:12],
            f'{fields[10]}': f'{self.dig_verificador_conta:1}'[-1],
            f'{fields[11]}': f'{self.dig_verificador_ag_conta:1}'[-1],
            f'{fields[12]}': f'{self.nome_empresa:<30}'[:30],
            f'{fields[13]}': f'{self.nome_banco:<30}'[:30],
            f'{fields[14]}': f'{"":10}',
            f'{fields[15]}': f'{self.cod_remessa_retorno:1}'[-1],
            f'{fields[16]}': f'{self.dt_geracao_arquivo:0>8}'[:8],
            f'{fields[17]}': f'{self.hr_geracao_arquivo:0>6}'[:6],
            f'{fields[18]}': f'{self.num_sequencial_arquivo:0>6}'[:6],
            f'{fields[19]}': f'{self.num_versao_layout:0>3}'[:3],
            f'{fields[20]}': f'{self.densidade_gravacao_arquivo:0>5}'[:5],
            f'{fields[21]}': f'{"":20}',
            f'{fields[22]}': f'{"":20}',
            f'{fields[23]}': f'{"":19}',
            f'{fields[24]}': f'{"":10}',
        }
        return ''.join([*data.values()])

    # @classmethod
    # def get_num_sequencial_arquivo(cls):
    #     global base_sequence
    #     if base_sequence >= 999999:
    #         return f'{LayoutResources.SEQUENCIA_BASE_HEADER_ARQUIVO_INICIO}'
    #     return f'{base_sequence + 1}'
