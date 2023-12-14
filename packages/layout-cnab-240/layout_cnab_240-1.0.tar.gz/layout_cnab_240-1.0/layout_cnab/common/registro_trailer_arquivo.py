from . import *


@dataclass
class RegistroTrailerArquivo:
    cod_banco: str = field(default='')
    lote_servico: str = field(default='')
    tipo_registro: str = field(default='9')
    qtd_lote_arquivo: str = field(default='1')
    qtd_registros_arquivo: str = field(default='')

    def build(self) -> str:
        fields = [f'field{i}' for i in range(7)]
        data = {
            f'{fields[0]}': f'{self.cod_banco:0>3}'[:3],
            f'{fields[1]}': f'{self.lote_servico:9>4}'[:4],
            f'{fields[2]}': f'{self.tipo_registro:1}'[-1],
            f'{fields[3]}': f'{"":<9}'[:9],
            f'{fields[4]}': f'{self.qtd_lote_arquivo:0>6}'[:6],
            f'{fields[5]}': f'{self.qtd_registros_arquivo:0>6}'[:6],
            f'{fields[6]}': f'{"":<211}'[:211],
        }

        return ''.join([*data.values()])
