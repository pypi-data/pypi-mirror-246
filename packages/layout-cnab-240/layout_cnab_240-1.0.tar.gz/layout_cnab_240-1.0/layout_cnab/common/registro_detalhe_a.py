from . import *


@dataclass
class RegistroDetalheA:
    cod_banco: str = field(default='33')
    lote_servico: str = field(default='1')
    tipo_registro: str = field(default='3')
    num_sequencial_registro_lote: str = field(default='')
    cod_segmento_registro_detalhe: str = field(default='A')
    tipo_movimento: str = field(default='')
    cod_instrucao_movimento: str = field(default='')
    cod_camara_compensacao: str = field(default='')
    cod_banco_favorecido: str = field(default='')
    cod_ag_favorecido: str = field(default='')
    dig_verificador_ag: str = ''
    conta_corrente_favorecido: str = field(default='')
    dig_verificador_conta: str = field(default='')
    dig_verificador_ag_conta: str = field(default='')
    nome_favorecido: str = field(default='')
    num_documento_cliente: str = field(default='')
    dt_pagamento: str = field(default='')
    tipo_moeda: str = field(default='')
    qtd_moeda: str = field(default='')
    valor_pagamento: str = field(default='')
    num_documento_banco: str = field(default='')
    dt_real_pagamento: str = field(default='')
    valor_real_pagamento: str = field(default='')
    info_msg2: str = field(default='')
    finalidade_doc: str = field(default='')
    finalidade_ted: str = field(default='')
    cod_finalidade_complementar: str = field(default='')
    emissao_aviso_favorecido: str = field(default='')

    def build(self) -> str:
        fields = [f'field{i}' for i in range(30)]
        data = {
            f'{fields[0]}': f'{self.cod_banco:0>3}'[:3],
            f'{fields[1]}': f'{self.lote_servico:0>4}'[:4],
            f'{fields[2]}': f'{self.tipo_registro:1}'[-1],
            f'{fields[3]}': f'{self.num_sequencial_registro_lote:0>5}'[:5],
            f'{fields[4]}': f'{self.cod_segmento_registro_detalhe:1}'[-1],
            f'{fields[5]}': f'{self.tipo_movimento:1}'[-1],
            f'{fields[6]}': f'{self.cod_instrucao_movimento:0>2}'[:2],
            f'{fields[7]}': f'{self.cod_camara_compensacao:0>3}'[:3],
            f'{fields[8]}': f'{self.cod_banco_favorecido:0>3}'[:3],
            f'{fields[9]}': f'{self.cod_ag_favorecido:0>5}'[:5],
            f'{fields[10]}': f'{self.dig_verificador_ag:1}'[-1],
            f'{fields[11]}': f'{self.conta_corrente_favorecido:0>12}'[:12],
            f'{fields[12]}': f'{self.dig_verificador_conta:1}'[-1],
            f'{fields[13]}': f'{self.dig_verificador_ag_conta:1}'[-1],
            f'{fields[14]}': f'{self.nome_favorecido:<30}'[:30],
            f'{fields[15]}': f'{self.num_documento_cliente:<20}'[:20],
            f'{fields[16]}': f'{self.dt_pagamento:0>8}'[:8],
            f'{fields[17]}': f'{self.tipo_moeda:<3}'[:3],
            f'{fields[18]}': f'{self.qtd_moeda:0>15}'[:15],
            f'{fields[19]}': f'{self.valor_pagamento:0>15}'[:15],
            f'{fields[20]}': f'{self.num_documento_banco:<20}'[:20],
            f'{fields[21]}': f'{self.dt_real_pagamento:0>8}'[:8],
            f'{fields[22]}': f'{self.valor_real_pagamento:0>15}'[:15],
            f'{fields[23]}': f'{self.info_msg2:<40}'[:40],
            f'{fields[24]}': f'{self.finalidade_doc:<2}'[:2],
            f'{fields[25]}': f'{self.finalidade_ted:<5}'[:5],
            f'{fields[26]}': f'{self.cod_finalidade_complementar:<2}'[:2],
            f'{fields[27]}': f'{"":3}',
            f'{fields[28]}': f'{self.emissao_aviso_favorecido:1}'[-1],
            f'{fields[29]}': f'{"":<10}'[:10],

        }
        return ''.join([*data.values()])
