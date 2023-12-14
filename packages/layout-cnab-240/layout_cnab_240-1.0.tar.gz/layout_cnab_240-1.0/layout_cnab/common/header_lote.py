from . import *


@dataclass
class HeaderLote:
    cod_banco: str = field(default='')
    lote_servico: str = field(default='1')
    tipo_registro: str = field(default='1')
    tipo_operacao: str = field(default='C')
    tipo_servico: str = field(default='')
    forma_lancamento: str = field(default='')
    num_versao_lote: str = field(default='')
    tp_inscricao_empresa: str = field(default='')
    num_inscricao_empresa: str = field(default='')
    cod_convenio: str = field(default='')
    ag_mantenedora_conta: str = field(default='')
    dig_verificador_ag: str = field(default='')
    num_conta_corrente: str = field(default='')
    dig_verificador_conta: str = field(default='')
    dig_verificador_ag_conta: str = field(default='')
    nome_empresa: str = field(default='')
    info1_msg: str = field(default='')
    endereco: str = field(default='')
    numero: str = field(default='')
    complemento_endereco: str = field(default='')
    cidade: str = field(default='')
    cep: str = field(default='')
    complemento_cep: str = field(default='')
    uf: str = field(default='')

    def build(self) -> str:
        fields = [f'field{i}' for i in range(27)]
        data = {
            f'{fields[0]}': f'{self.cod_banco:0>3}'[:3],
            f'{fields[1]}': f'{self.lote_servico:0>4}'[:4],
            f'{fields[2]}': f'{self.tipo_registro:1}'[-1],
            f'{fields[3]}': f'{self.tipo_operacao:1}'[-1],
            f'{fields[4]}': f'{self.tipo_servico:0>2}'[:2],
            f'{fields[5]}': f'{self.forma_lancamento:0>2}'[:2],
            f'{fields[6]}': f'{self.num_versao_lote:0>3}'[:3],
            f'{fields[7]}': f'{"":1}',
            f'{fields[8]}': f'{self.tp_inscricao_empresa:1}'[-1],
            f'{fields[9]}': f'{self.num_inscricao_empresa:0>14}'[:14],
            f'{fields[10]}': f'{self.cod_convenio:0>20}'[:20],
            f'{fields[11]}': f'{self.ag_mantenedora_conta:0>5}'[:5],
            f'{fields[12]}': f'{self.dig_verificador_ag:1}'[-1],
            f'{fields[13]}': f'{self.num_conta_corrente:0>12}'[:12],
            f'{fields[14]}': f'{self.dig_verificador_conta:1}'[-1],
            f'{fields[15]}': f'{self.dig_verificador_ag_conta:1}'[-1],
            f'{fields[16]}': f'{self.nome_empresa:<30}'[:30],
            f'{fields[17]}': f'{self.info1_msg:<40}'[:40],
            f'{fields[18]}': f'{self.endereco:<30}'[:30],
            f'{fields[19]}': f'{self.numero:0>5}'[:5],
            f'{fields[20]}': f'{self.complemento_endereco:<15}'[:15],
            f'{fields[21]}': f'{self.cidade:<20}'[:20],
            f'{fields[22]}': f'{self.cep:0>5}'[:5],
            f'{fields[23]}': f'{self.complemento_cep:0>3}'[:3],
            f'{fields[24]}': f'{self.uf:>2}'[:2],
            f'{fields[25]}': f'{"":8}',
            f'{fields[26]}': f'{"":<10}',
        }
        return ''.join([*data.values()])
