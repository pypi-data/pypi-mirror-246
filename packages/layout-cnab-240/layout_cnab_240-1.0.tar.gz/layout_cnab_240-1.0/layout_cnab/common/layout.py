from . import *

@dataclass
class Layout:
    data_frame: pd.DataFrame = field(default_factory=raiseLayoutCNABException('DataFrame is not defined'))
    df_columns: DataFrameColumns = field(default=DataFrameColumns)
    default_options: DefaultConfiguration = field(default_factory=raiseLayoutCNABException('DefaultOptions is not defined'))
    header_arquivo: HeaderArquivo = field(default=None)
    header_lote: HeaderLote = field(default=None)
    registros_detalhes: list[tuple[RegistroDetalheA, RegistroDetalheB]] = field(default_factory=lambda: [])
    registro_trailer_lote: RegistroTrailerLote = field(default=None)
    registro_trailer_arquivo: RegistroTrailerArquivo = field(default=None)

    def amount_header_arquivo(self) -> str:
        now = datetime.now()
        params = {
            'cod_banco': self.default_options.get('codigo_banco'),
            'tipo_inscricao_empresa': self.default_options.get('tipo_inscricao'),
            'num_inscricao_empresa': self.default_options.get('numero_inscricao_empresa'),
            'cod_convenio': self.default_options.get('codigo_convenio'),
            'ag_mantenedora_conta': self.default_options.get('agencia_mantenedora_conta'),
            'num_conta_corrente': self.default_options.get('numero_conta_corrente'),
            'dig_verificador_conta': self.default_options.get('digito_verificador_conta'),
            'nome_empresa': self.default_options.get('nome_empresa'),
            'nome_banco': self.default_options.get('nome_banco'),
            'cod_remessa_retorno': '1',
            'dt_geracao_arquivo': now.strftime('%d%m%Y'),
            'hr_geracao_arquivo': now.strftime('%H%M%S'),
            'num_sequencial_arquivo': self.default_options.get('g010', '1'),
            'num_versao_layout': self.default_options.get('versao_header_arquivo'),
        }
        self.header_arquivo = HeaderArquivo(**params)
        return self.header_arquivo.build()

    def amount_header_lote(self) -> str:
        params = {
            'cod_banco': self.default_options.get('codigo_banco'),
            'tipo_servico': self.default_options.get('g015', ''),
            'forma_lancamento': self.default_options.get('g002'),
            'num_versao_lote': self.default_options.get('versao_header_lote'),
            'tp_inscricao_empresa': self.default_options.get('tipo_inscricao'),
            'num_inscricao_empresa': self.default_options.get('numero_inscricao_empresa'),
            'cod_convenio': self.default_options.get('codigo_convenio'),
            'ag_mantenedora_conta': self.default_options.get('agencia_mantenedora_conta'),
            'num_conta_corrente': self.default_options.get('numero_conta_corrente'),
            'dig_verificador_conta': self.default_options.get('digito_verificador_conta'),
            'nome_empresa': self.default_options.get('nome_empresa'),
            'info1_msg': self.default_options.get('g016', ''),
            'endereco': self.default_options.get('endereco'),
            'numero': self.default_options.get('numero'),
            'cidade': self.default_options.get('cidade'),
            'cep': self.default_options.get('cep'),
            'complemento_cep': self.default_options.get('complemento_cep'),
            'uf': self.default_options.get('uf'),
        }
        self.header_lote = HeaderLote(**params)
        return self.header_lote.build()

    def amount_registro_detalhe(self) -> str:
        df = self.data_frame.dropna()
        now = datetime.now()
        num_sequencial_registro_lote = 1
        for index, row in df.iterrows():
            agencia, digito_ag = str(row[self.df_columns.AGENCIA]).split('-') \
                if '-' in row[self.df_columns.AGENCIA] \
                else [row[self.df_columns.AGENCIA], '']

            conta, digito_cnt = str(row[self.df_columns.CONTA_CORRENTE]).split('-') \
                if '-' in row[self.df_columns.CONTA_CORRENTE] \
                else [row[self.df_columns.CONTA_CORRENTE], '']

            valor = ''.join(str('%.2f' % float(f'{str(row[self.df_columns.VALOR_PAGAMENTO]).replace(",", ".")}')).split('.'))
            tipo_inscricao_favorecido = '1' if row[self.df_columns.TIPO_PESSOA] == TipoPessoa.FISICA else '2'
            detalhe_a = {
                'cod_banco': self.default_options.get('codigo_banco'),
                'num_sequencial_registro_lote': num_sequencial_registro_lote,
                'tipo_movimento': self.default_options.get('g011', ''),
                'cod_instrucao_movimento': self.default_options.get('g012', ''),
                'cod_camara_compensacao': self.default_options.get('g014'),
                'cod_banco_favorecido': row[self.df_columns.CODIGO_BANCO],
                'cod_ag_favorecido': agencia,
                'dig_verificador_ag': digito_ag,
                'conta_corrente_favorecido': conta,
                'dig_verificador_conta': digito_cnt,
                'nome_favorecido': row[self.df_columns.NOME_FAVORECIDO],
                'num_documento_cliente': row[self.df_columns.CPFJ_FAVORECIDO],
                'dt_pagamento': datetime.strptime(row[self.df_columns.DATA_PAGAMENTO], '%d/%m/%y').strftime('%d%m%Y'),
                'tipo_moeda': self.default_options.get('g005'),
                'valor_pagamento': valor,
                'dt_real_pagamento': now.strftime('%d%m%Y'),
                'info_msg2': self.default_options.get('g016', ''),
                'finalidade_doc': self.default_options.get('g013a', ''),
                'finalidade_ted': self.default_options.get('g013b', ''),
                'cod_finalidade_complementar': self.default_options.get('g013c', ''),
                'emissao_aviso_favorecido': self.default_options.get('g018'),
            }
            registro_detalhe_a = RegistroDetalheA(**detalhe_a)
            num_sequencial_registro_lote += 1
            detalhe_b = {
                'cod_banco': self.default_options.get('codigo_banco'),
                'num_sequencial_registro_lote': num_sequencial_registro_lote,
                'forma_iniciacao': self.default_options.get('g032'),
                'tipo_inscricao_favorecido': tipo_inscricao_favorecido,
                'cpf_cnpj_favorecido': row[self.df_columns.CPFJ_FAVORECIDO],
            }
            num_sequencial_registro_lote += 1
            registro_detalhe_b = RegistroDetalheB(**detalhe_b)
            self.registros_detalhes.append((registro_detalhe_a, registro_detalhe_b))
        return '\n'.join(map(lambda x: x.build(), [item for _tuple in self.registros_detalhes for item in _tuple]))

    def amount_registro_trailer_lote(self) -> str:
        registros_flatted = [item.__dict__ for _tuple in self.registros_detalhes for item in _tuple]
        qtd_registros_lote = [self.header_lote, self.registro_trailer_lote, *registros_flatted]
        somatoria_valores = list(filter(lambda x: 'valor_pagamento' in x, registros_flatted))
        params = {
            'cod_banco': self.default_options.get('codigo_banco'),
            'qtd_registros_lote': f'{len(qtd_registros_lote)}',
            'somatoria_valores': f'{sum(map(int, map(lambda x: x["valor_pagamento"], somatoria_valores)))}',
        }
        self.registro_trailer_lote = RegistroTrailerLote(**params)
        return self.registro_trailer_lote.build()

    def amount_resgistro_trailer_arquivo(self) -> str:
        qtd_registros_arquivo = [self.header_arquivo, self.header_lote, self.registro_trailer_lote,
                                 self.registro_trailer_arquivo,
                                 *[item for _tuple in self.registros_detalhes for item in _tuple]]
        params = {
            'cod_banco': self.default_options.get('codigo_banco'),
            'qtd_registros_arquivo': f'{len(list(qtd_registros_arquivo))}',
        }
        self.registro_trailer_arquivo = RegistroTrailerArquivo(**params)
        return self.registro_trailer_arquivo.build()
