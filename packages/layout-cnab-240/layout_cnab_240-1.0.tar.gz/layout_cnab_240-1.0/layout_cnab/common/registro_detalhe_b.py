from . import *


@dataclass
class RegistroDetalheB:
    cod_banco: str = field(default='33')
    lote_servico: str = field(default='1')
    tipo_registro: str = field(default='3')
    num_sequencial_registro_lote: str = field(default='')
    cod_segmento_registro_detalhe: str = field(default='B')
    forma_iniciacao: str = field(default='')
    tipo_inscricao_favorecido: str = field(default='')
    cpf_cnpj_favorecido: str = field(default='')
    info10: str = field(default='')
    info11: str = field(default='')
    info12: str = field(default='')
    identificacao_spb: str = field(default='')

    def build(self) -> str:
        fields = [f'field{i}' for i in range(14)]
        data = {
            f'{fields[0]}': f'{self.cod_banco:0>3}'[:3],
            f'{fields[1]}': f'{self.lote_servico:0>4}'[:4],
            f'{fields[2]}': f'{self.tipo_registro:1}'[-1],
            f'{fields[3]}': f'{self.num_sequencial_registro_lote:0>5}'[:5],
            f'{fields[4]}': f'{self.cod_segmento_registro_detalhe:1}'[-1],
            f'{fields[5]}': f'{self.forma_iniciacao:<2}'[:2],
            f'{fields[6]}': f'{"":1}'[-1],
            f'{fields[7]}': f'{self.tipo_inscricao_favorecido:0>1}'[-1],
            f'{fields[8]}': f'{self.cpf_cnpj_favorecido:0>14}'[:14],
            f'{fields[9]}': f'{self.info10:<35}'[:35],
            f'{fields[10]}': f'{self.info11:<60}'[:60],
            f'{fields[11]}': f'{self.info12:<99}'[:99],
            f'{fields[12]}': f'{"":<6}'[:6],
            f'{fields[13]}': f'{"":<8}'[:8],
        }

        return ''.join([*data.values()])
