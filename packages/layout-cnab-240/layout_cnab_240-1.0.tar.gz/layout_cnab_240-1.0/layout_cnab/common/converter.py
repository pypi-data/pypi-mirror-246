from . import *


@dataclass
class Converter:
    _layout: Layout

    def build(self) -> BytesIO:
        data = bytes('\n'.join([self._layout.amount_header_arquivo(),
                                self._layout.amount_header_lote(),
                                self._layout.amount_registro_detalhe(),
                                self._layout.amount_registro_trailer_lote(),
                                self._layout.amount_resgistro_trailer_arquivo()]),
                     encoding='utf-8')
        file = BytesIO(data)
        return file
