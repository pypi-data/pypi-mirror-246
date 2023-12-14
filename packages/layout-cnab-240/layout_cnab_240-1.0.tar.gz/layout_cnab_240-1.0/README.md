# Layout CNAB 240 - Pagamentos PIX

### Versão 1.0 - Apenas para banco Santander
> Exemplo de arquivo gerado:
>
> 03300000         1000999213168850033999900490000015109999 0000010007999 NOME DA EMPRESA               BANCO SANTANDER                         13010202019432900001306000000                                        G4007PF00450                 
> 03300011C2045031 1000999213168850033999900490000015109999 0000010007999 NOME DA EMPRESA                                                                                     00000                                   00000000                    
> 0330001300001A0000090330099900000010313819 NOME DO FAVORECIDO 1          BR01 1207 11        01092021BRL000000000000000000000000000011                    00000000000000000000000                                        01          0          
> 0330001300002B05 100099570998847                              00000                                                  00000000  010920210000000000000110000000000000000000000000000000000000000000000000000000000000000           00000          
> 0330001300003A0000090330099900000010313819 NOME DO FAVORECIDO 2          BR01 1207 21        01092021BRL000000000000000000000000000022                    00000000000000000000000                                        01          0          
> 0330001300004B05 100099570998847                              00000                                                  00000000  010920210000000000000220000000000000000000000000000000000000000000000000000000000000000           00000          
> 0330001300005A0000090330099900000010313819 NOME DO FAVORECIDO 3          BR01 1207 31        01092021BRL000000000000000000000000000033                    00000000000000000000000                                        01          0          
> 0330001300006B05 100099570998847                              00000                                                  00000000  010920210000000000000330000000000000000000000000000000000000000000000000000000000000000           00000          
> 0330001300007A0000090330099900000010313819 NOME DO FAVORECIDO 4          BR01 1207 41        01092021BRL000000000000000000000000000045                    00000000000000000000000                                        01          0          
> 0330001300008B05 100099570998847                              00000                                                  00000000  010920210000000000000450000000000000000000000000000000000000000000000000000000000000000           00000          
> 03300015         000010000000000000000111000000000000000000                                                                                                                                                                                     
> 03399999         000001000012                                                                                                                                                                                                                   
>

##### Utilização

```python
import pandas as pd
from ..common import DefaultConfiguration, \
    Layout, DataFrameColumns, TipoPessoa, Converter

config: DefaultConfiguration = {
    "codigo_banco": "033",
    "tipo_inscricao": "2",
    "numero_inscricao_empresa": "123456456",
    "codigo_convenio": "10123123132",
    "agencia_mantenedora_conta": "0002",
    "numero_conta_corrente": "1234562",
    "digito_verificador_conta": "5",
    "nome_empresa": "ADAN EINSTEIN SA",
    "nome_banco": "BANCO SANTANDER",
    "endereco": "RUA A",
    "numero": "10",
    "cidade": "SUZANO",
    "cep": "11012",
    "uf": "SP",
    "complemento_cep": "000",
    "versao_header_lote": "031",
    "versao_header_arquivo": "060",
    "g010": "1",
    "g011": "0",
    "g012": "00",
    "g013a": "99",
    "g013b": "99999",
    "g013c": "CC",
    "g015": "20",
    "g016": "",
    "g002": "45",
    "g005": "BRL",
    "g014": "009",
    "g018": "0",
    "g032": "05",
}

class Columns(DataFrameColumns):
    AGENCIA = 'ag'
    TIPO_PESSOA = 'tp'
    CODIGO_BANCO = 'cp'
    NOME_FAVORECIDO = 'nm'
    DATA_PAGAMENTO = 'dp'
    CPFJ_FAVORECIDO = 'nd'
    CONTA_CORRENTE = 'cc'
    VALOR_PAGAMENTO = 'vp'

df = pd.DataFrame({
    'ag': ['123', '456'],
    'tp': [TipoPessoa.FISICA, TipoPessoa.JURIDICA],
    'cp': ['033', '140'],
    'nm': ['ADAN', 'EINSTEIN'],
    'dp': ['01/01/01', '26/08/01'],
    'nd': ['12345612345', '78945612345'],
    'cc': ['1231212', '12324545'],
    'vp': ['100,00', '100.00'],
})

layout = Layout(data_frame=df, default_options=config, df_columns=Columns)

build = Converter(layout).build()

with open('result.txt', 'w') as file:
    file.write(build.read().decode('utf8'))
```

> OUTPUT: result.txt

```txt
03300000         2000001234564560000000001012312313200002 0000012345625 ADAN EINSTEIN SA              BANCO SANTANDER                         11212202317342600000106000000                                                                     
03300011C2045031 2000001234564560000000001012312313200002 0000012345625 ADAN EINSTEIN SA                                                      RUA A                         00010               SUZANO              11012000SP                  
0330001300001A00000903300123 000001231212  ADAN                          12345612345         01012001BRL000000000000000000000000010000                    12122023000000000000000                                        9999999CC   0          
0330001300002B05 100012345612345                                                                                                                                                                                                                
0330001300003A00000914000456 000012324545  EINSTEIN                      78945612345         26082001BRL000000000000000000000000010000                    12122023000000000000000                                        9999999CC   0          
0330001300004B05 200078945612345                                                                                                                                                                                                                
03300015         000006000000000000020000000000000000000000000000                                                                                                                                                                               
03399999         000001000008                                                                                                                                                                                                                   
```