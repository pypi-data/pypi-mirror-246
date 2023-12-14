from . import *


@dataclass
class RegistroTrailerLote:
    cod_banco: str = field(default='')
    lote_servico: str = field(default='1')
    tipo_registro: str = field(default='5')
    qtd_registros_lote: str = field(default='')
    somatoria_valores: str = field(default='')
    somatoria_qtd_moeda: str = field(default='')
    num_aviso_debito: str = field(default='')

    def build(self) -> str:
        fields = [f'field{i}' for i in range(10)]
        data = {
            f'{fields[0]}': f'{self.cod_banco:0>3}'[-3:],
            f'{fields[1]}': f'{self.lote_servico:0>4}'[-4:],
            f'{fields[2]}': f'{self.tipo_registro:1}'[-1],
            f'{fields[3]}': f'{"":<9}'[-9:],
            f'{fields[4]}': f'{self.qtd_registros_lote:0>6}'[-6:],
            f'{fields[5]}': f'{self.somatoria_valores:0>18}'[-18:],
            f'{fields[6]}': f'{self.somatoria_qtd_moeda:0>18}'[-18:],
            f'{fields[7]}': f'{self.num_aviso_debito:0>6}'[-6:],
            f'{fields[8]}': f'{"":<165}'[-165:],
            f'{fields[9]}': f'{"":<10}'[-10:],
        }

        return ''.join([*data.values()])
