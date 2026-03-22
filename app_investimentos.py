import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Carteira Bruno - Gestão Total", layout="wide")

st.title("🚀 Carteira Bruno: XTB, Trading 212 & Trade Republic")

# --- 1. CONFIGURAÇÃO INICIAL DOS ATIVOS ---
# Nota: Adicionei ".DE" aos tickers porque a maioria destes ETFs UCITS são negociados na Xetra (Alemanha) em Euros.
if 'dados_carteira' not in st.session_state:
    data = [
        # XTB
        {"Conta": "XTB", "Ativo": "INVESCO NASDAQ-100", "Ticker": "EQQB.DE", "Alvo %": 15.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "MSCI WORLD QUALITY", "Ticker": "IWQU.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "MSCI WORLD MIN VOL", "Ticker": "XDEB.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "GLOBAL SMALL CAP VALUE", "Ticker": "AVWS.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "VANGUARD DEV EUROPE", "Ticker": "VWCG.DE", "Alvo %": 20.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "SPDR MSCI EM", "Ticker": "SPYM.DE", "Alvo %": 15.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "GLOBAL INFRASTRUCTURE", "Ticker": "CBUX.DE", "Alvo %": 5.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "PHYSICAL GOLD", "Ticker": "PHGP.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "XTB", "Ativo": "COMMODITIES EX-AGRI", "Ticker": "LYTR.DE", "Alvo %": 5.0, "Qtd": 0.0},
        
        # TRADING 212
        {"Conta": "T212", "Ativo": "INVESCO NASDAQ-100", "Ticker": "EQAC.DE", "Alvo %": 15.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "MSCI WORLD QUALITY", "Ticker": "IWQU.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "MSCI WORLD MIN VOL", "Ticker": "XDEB.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "GLOBAL SMALL CAP VALUE", "Ticker": "AVWS.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "VANGUARD DEV EUROPE", "Ticker": "VWCG.DE", "Alvo %": 20.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "SPDR MSCI EM", "Ticker": "SPYM.DE", "Alvo %": 15.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "GLOBAL INFRASTRUCTURE", "Ticker": "CBUX.DE", "Alvo %": 5.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "PHYSICAL GOLD", "Ticker": "PHGP.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "T212", "Ativo": "CRYPTO BASKET HODL", "Ticker": "HODL.SW", "Alvo %": 5.0, "Qtd": 0.0},

        # TRADE REPUBLIC
        {"Conta": "TR", "Ativo": "INVESCO NASDAQ-100", "Ticker": "EQQB.DE", "Alvo %": 15.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "MSCI WORLD QUALITY", "Ticker": "IWQU.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "MSCI WORLD MIN VOL", "Ticker": "XDEB.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "GLOBAL SMALL CAP VALUE", "Ticker": "AVWS.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "VANGUARD DEV EUROPE", "Ticker": "VWCG.DE", "Alvo %": 20.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "SPDR MSCI EM", "Ticker": "SPYM.DE", "Alvo %": 15.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "GLOBAL INFRASTRUCTURE", "Ticker": "CBUX.DE", "Alvo %": 5.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "PHYSICAL GOLD", "Ticker": "PHGP.DE", "Alvo %": 10.0, "Qtd": 0.0},
        {"Conta": "TR", "Ativo": "DEV MARKETS PROPERTY", "Ticker": "SXRA.DE", "Alvo %": 5.0, "Qtd": 0.0},
    ]
    st.session_state.dados_carteira = pd.DataFrame(data)

# --- 2. ENTRADA DE DADOS E ABAS ---
st.sidebar.header("💵 Novo Capital")
valor_reforco = st.sidebar.number_input("Valor para investir hoje (€)", min_value=0.0, value=1000.0)

tab1, tab2, tab3 = st.tabs(["🏛️ XTB", "📱 Trading 212", "🇪🇺 Trade Republic"])

def editar_conta(nome_conta):
    df_filtrado = st.session_state.dados_carteira[st.session_state.dados_carteira["Conta"] == nome_conta]
    return st.data_editor(df_filtrado, hide_index=True, use_container_width=True, key=f"editor_{nome_conta}")

with tab1:
    df_xtb = editar_conta("XTB")
with tab2:
    df_t212 = editar_conta("T212")
with tab3:
    df_tr = editar_conta("TR")

# --- 3. CÁLCULO REAL ---
if st.button("🔄 Calcular Reforço em Tempo Real"):
    # Juntar tudo
    df_total = pd.concat([df_xtb, df_t212, df_tr])
    
    with st.spinner('A atualizar preços dos 27 ativos...'):
        tickers_unicos = df_total["Ticker"].unique().tolist()
        precos = {}
        for t in tickers_unicos:
            try:
                precos[t] = yf.Ticker(t).history(period="1d")["Close"].iloc[-1]
            except:
                precos[t] = 0.0

        df_total["Preço (€)"] = df_total["Ticker"].map(precos)
        df_total["Valor Atual (€)"] = df_total["Qtd"] * df_total["Preço (€)"]
        
        # O cálculo de alvo é baseado no total de CADA CONTA ou GLOBAL? 
        # Vou assumir que queres manter a % dentro de cada conta.
        resultados_finais = []
        for conta in ["XTB", "T212", "TR"]:
            df_c = df_total[df_total["Conta"] == conta].copy()
            # Assumindo que o reforço é distribuído proporcionalmente ou escolhes uma conta?
            # Para simplificar: o reforço aqui é tratado por conta.
            total_conta = df_c["Valor Atual (€)"].sum()
            # Se quiseres dividir os 1000€ pelas 3 contas, teríamos de ajustar. 
            # Aqui vou assumir que o 'valor_reforco' é o que tens para gastar NO TOTAL.
            # Vou dividir o reforço pelo peso de cada conta atual.
            total_global_atual = df_total["Valor Atual (€)"].sum()
            peso_conta = total_conta / total_global_atual if total_global_atual > 0 else 0.33
            
            reforco_conta = valor_reforco * peso_conta
            novo_total_conta = total_conta + reforco_conta
            
            df_c["Valor Ideal (€)"] = novo_total_conta * (df_c["Alvo %"] / 100)
            df_c["Comprar (€)"] = (df_c["Valor Ideal (€)"] - df_c["Valor Atual (€)"]).clip(lower=0)
            resultados_finais.append(df_c)

        df_final = pd.concat(resultados_finais)

        # MOSTRAR RESULTADOS
        st.success("Cálculo Concluído!")
        col1, col2 = st.columns(2)
        col1.metric("Património Total", f"{df_total['Valor Atual (€)'].sum():.2f} €")
        col2.metric("Reforço Total", f"{valor_reforco:.2f} €")

        st.write("### 🛒 Lista de Compras (Onde colocar o dinheiro)")
        compras = df_final[df_final["Comprar (€)"] > 0.01][["Conta", "Ativo", "Ticker", "Comprar (€)"]]
        st.table(compras.style.format({"Comprar (€)": "{:.2f} €"}))

# Guardar estados
st.session_state.dados_carteira = pd.concat([df_xtb, df_t212, df_tr])