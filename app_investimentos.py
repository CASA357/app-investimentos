import streamlit as st
import pandas as pd

st.set_page_config(page_title="Carteira Bruno - Manual & Auto", layout="wide")

st.title("📊 Gestão de Portefólio: Carteira Bruno")

# --- 1. CONFIGURAÇÃO DOS ATIVOS (CARTEIRA DO BRUNO) ---
# Tickers sugeridos para busca automática futura (Yahoo Finance)
ativos_bruno = [
    {"Ativo": "INVESCO NASDAQ-100 (EQQB)", "Ticker": "EQQB.DE", "Alvo %": 15.0},
    {"Ativo": "MSCI WORLD QUALITY (IWQU)", "Ticker": "IWQU.DE", "Alvo %": 10.0},
    {"Ativo": "MSCI WORLD MIN VOL (XDEB)", "Ticker": "XDEB.DE", "Alvo %": 10.0},
    {"Ativo": "GLOBAL SMALL CAP VALUE (AVWS)", "Ticker": "AVWS.DE", "Alvo %": 10.0},
    {"Ativo": "VANGUARD DEV EUROPE (VWCG)", "Ticker": "VWCG.DE", "Alvo %": 20.0},
    {"Ativo": "SPDR MSCI EM (SPYM)", "Ticker": "SPYM.DE", "Alvo %": 15.0},
    {"Ativo": "GLOBAL INFRASTRUCTURE (CBUX)", "Ticker": "CBUX.DE", "Alvo %": 5.0},
    {"Ativo": "PHYSICAL GOLD (PHGP)", "Ticker": "PHGP.DE", "Alvo %": 10.0},
    {"Ativo": "OUTRO (COMMODITIES / CRYPTO / PROP)", "Ticker": "VÁRIOS", "Alvo %": 5.0},
]

# Inicializar dados se não existirem
if 'df_xtb' not in st.session_state:
    st.session_state.df_xtb = pd.DataFrame(ativos_bruno).assign(Qtd=0.0, Preco_Manual=0.0)
if 'df_t212' not in st.session_state:
    st.session_state.df_t212 = pd.DataFrame(ativos_bruno).assign(Qtd=0.0, Preco_Manual=0.0)
    # Ajuste do último ativo da T212 (Crypto)
    st.session_state.df_t212.at[8, "Ativo"] = "21SHARES CRYPTO (HODL)"
if 'df_tr' not in st.session_state:
    st.session_state.df_tr = pd.DataFrame(ativos_bruno).assign(Qtd=0.0, Preco_Manual=0.0)
    # Ajuste do último ativo da TR (Property)
    st.session_state.df_tr.at[8, "Ativo"] = "DM PROPERTY (SXRA)"

# --- 2. ENTRADA DE DADOS ---
st.sidebar.header("💰 Plano de Reforço")
reforco_total = st.sidebar.number_input("Quanto vais investir hoje no total? (€)", min_value=0.0, value=500.0)

st.info("💡 Preenche a **Quantidade** e o **Preço Atual** em cada aba. A App calcula o reforço automaticamente.")

tab1, tab2, tab3 = st.tabs(["🏛️ XTB", "📱 Trading 212", "🇪🇺 Trade Republic"])

def processar_aba(df, chave):
    # Tabela editável
    df_edit = st.data_editor(
        df, 
        column_config={
            "Alvo %": st.column_config.NumberColumn(format="%.1f%%"),
            "Preco_Manual": "Preço Atual (€)",
            "Qtd": "Quantidade"
        },
        hide_index=True, 
        use_container_width=True,
        key=chave
    )
    
    # Cálculos internos
    df_edit["Valor Atual (€)"] = df_edit["Qtd"] * df_edit["Preco_Manual"]
    total_atual = df_edit["Valor Atual (€)"].sum()
    
    # Distribuir o reforço (exemplo: dividimos o reforço total por 3 contas ou defines por conta)
    # Aqui vamos assumir que o valor na sidebar é para ser usado NESTA CONTA específica para simplificar
    valor_futuro = total_atual + reforco_total 
    
    df_edit["Valor Ideal (€)"] = valor_futuro * (df_edit["Alvo %"] / 100)
    df_edit["Reforço (€)"] = (df_edit["Valor Ideal (€)"] - df_edit["Valor Atual (€)"]).clip(lower=0)
    
    # Resumo da Conta
    c1, c2 = st.columns(2)
    c1.metric(f"Total Atual", f"{total_atual:.2f} €")
    c2.metric(f"Com o Reforço", f"{valor_futuro:.2f} €")
    
    st.write("### ✅ Onde investir nesta conta:")
    reforcos = df_edit[df_edit["Reforço (€)"] > 0.01][["Ativo", "Alvo %", "Valor Atual (€)", "Reforço (€)"]]
    st.dataframe(reforcos.style.format({"Valor Atual (€)": "{:.2f} €", "Reforço (€)": "{:.2f} €"}), use_container_width=True)
    return df_edit

with tab1:
    st.session_state.df_xtb = processar_aba(st.session_state.df_xtb, "xtb_ed")
with tab2:
    st.session_state.df_t212 = processar_aba(st.session_state.df_t212, "t212_ed")
with tab3:
    st.session_state.df_tr = processar_aba(st.session_state.df_tr, "tr_ed")

st.divider()
st.caption("Nota: O cálculo de reforço considera o 'Reforço Total' da barra lateral aplicado a cada conta individualmente.")