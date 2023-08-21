import streamlit as st
import streamlit.components.v1 as components

#---------------------------------------------------------------------------------------------------------#
#-------------------------------- SIDEBAR ----------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
def description():
        """
        Cria uma descrição do contexto do problema de negócio, os desafios, as perguntas a serem respondidas e as premissas assumidas para a análise.

        Retorna:
                None
        """
        with st.sidebar:
            components.html("""
                            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="large" data-theme="light" data-type="VERTICAL" data-vanity="oliveiramatheuss" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/oliveiramatheuss?trk=profile-badge"></a></div>
                            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>              
                    """, height= 310)

        st.markdown("""
                        # 1. Agenda

                        1. Contexto
                        2. Desafio
                        3. Desenvolvimento da Solução
                        4. Conclusão e Demonstração
                        
                        # 2. Contexto 
                        - Reunião Mensal de Resultados
                        - CFO pediu uma Previsão de Vendas das Próximas 6 semanas para cada Loja

                        # 3. Desafio

                        ## 3.1 Problema
                        - Definição do Budget para a Reforma das Lojas.

                        ## 3.2 Causas
                        - Predição de Vendas Atual apresentada muita Divergência
                        - O processo de Predição de Vendas é baseado em Experiências Passadas.
                        - Todo a Previsão de Vendas é feita Manualmente pelas 1.115 Lojas da Rossmann.
                        - A visualização das Vendas é Limitada ao Computador.
                        
        """)