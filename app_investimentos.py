import streamlit as st
import pandas as pd

st.set_page_config(page_title="Carteira Bruno - Controlo de Pesos", layout="wide")

st.title("📊 Gestão de Carteira: Bruno")

# --- 1. CONFIGURAÇÃO DOS ATIVOS ---
def get_base_assets():
    return [
        {"Ativo": "INVESCO NASDAQ-100", "Ticker": "EQQB.DE", "Alvo %": 15.0},
        {"Ativo": "MSCI WORLD QUALITY", "Ticker": "IWQU.DE", "Alvo %": 10.0},
        {"Ativo": "MSCI WORLD MIN VOL", "Ticker": "XDEB.DE", "Alvo %": 10.0},
        {"Ativo": "GLOBAL SMALL CAP VALUE", "Ticker": "AVWS.DE", "Alvo %": 10.0},
        {"Ativo": "VANGUARD DEV EUROPE", "Ticker": "VWCG.DE", "Alvo %": 20.0},
        {"Ativo": "SPDR MSCI EM", "Ticker": "SPYM.DE", "Alvo %": 15.0},
        {"Ativo": "GLOBAL INFRASTRUCTURE", "Ticker": "CBUX.DE", "Alvo %": 5.0},
        {"Ativo": "PHYSICAL GOLD", "Ticker": "PHGP.DE", "Alvo %": 10.0},
        {"Ativo": "OUTRO ESPECIAL", "Ticker": "VÁRIOS", "Alvo %": 5.0},
    ]

# Inicializar estados das contas
if 'df_xtb' not in st.session_state:
    st.session_state.df_xtb = pd.DataFrame(get_base_assets()).assign(Qtd=0.0, Preco=0.0)
    st.session_state.df_xtb.at[8, "Ativo"] = "COMMODITIES (LYTR)"
if 'df_t212' not in st.session_state:
    st.session_state.df_t212 = pd.DataFrame(get_base_assets()).assign(Qtd=0.0, Preco=0.0)
    st.session_state.df_t212.at[0, "Ticker"] = "EQAC.DE" # Ajuste T212
    st.session_state.df_t212.at[8, "Ativo"] = "CRYPTO (HODL)"
if 'df_tr' not in st.session_state:
    st.session_state.df_tr = pd.DataFrame(get_base_assets()).assign(Qtd=0.0, Preco=0.0)
    st.session_state.df_tr.at[8, "Ativo"] = "PROPERTY (SXRA)"

# --- 2. INPUT DE REFORÇO ---
st.sidebar.header("📥 Novo Aporte")
reforco_input = st.sidebar.number_input("Valor total para investir hoje (€)", min_value=0.0, value=1000.0)

# --- 3. LÓGICA DAS ABAS ---
tabs = st.tabs(["🏛️ XTB", "📱 Trading 212", "🇪🇺 Trade Republic"])

def render_aba(df, key_suffix):
    st.subheader(f"Configuração de Ativos - {key_suffix}")
    
    # Tabela de Edição
    df_edited = st.data_editor(
        df,
        column_config={
            "Alvo %": st.column_config.NumberColumn("Alvo %", format="%.1f%%"),
            "Qtd": st.column_config.NumberColumn("Quantidade", min_value=0.0),
            "Preco": st.column_config.NumberColumn("Preço Atual (€)", min_value=0.0),
        },
        hide_index=True,
        use_container_width=True,
        key=f"editor_{key_suffix}"
    )

    # CÁLCULOS
    df_edited["Valor Total (€)"] = df_edited["Qtd"] * df_edited["Preco"]
    total_atual = df_edited["Valor Total (€)"].sum()
    
    # % Real que cada ativo representa agora
    if total_atual > 0:
        df_edited["% Real"] = (df_edited["Valor Total (€)"] / total_atual) * 100
    else:
        df_edited["% Real"] = 0.0

    # Lógica de Reforço: Total Atual + Novo Dinheiro
    total_projetado = total_atual + reforco_input
    
    # Quanto devia ter (Valor Ideal) e quanto falta comprar
    df_edited["Valor Ideal (€)"] = total_projetado * (df_edited["Alvo %"] / 100)
    df_edited["Reforço Necessário (€)"] = (df_edited["Valor Ideal (€)"] - df_edited["Valor Total (€)"]).clip(lower=0)

    # EXIBIÇÃO DO RESULTADO FINAL
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Valor Atual na Conta", f"{total_atual:.2f} €")
    col2.metric("Reforço a Aplicar", f"{reforco_input:.2f} €")
    col3.metric("Total Final Estimado", f"{total_projetado:.2f} €")

    st.write("### 📊 Análise de Alocação e Sugestão de Compra")
    
    # Formatação para a tabela de visualização
    df_view = df_edited[[
        "Ativo", "Alvo %", "% Real", "Valor Total (€)", "Reforço Necessário (€)"
    ]].copy()
    
    st.dataframe(
        df_view.style.format({
            "Alvo %": "{:.1f}%",
            "% Real": "{:.1f}%",
            "Valor Total (€)": "{:.2f} €",
            "Reforço Necessário (€)": "{:.2f} €"
        }).background_gradient(subset=["Reforço Necessário (€)"], cmap="Greens"),
        use_container_width=True,
        hide_index=True
    )
    return df_edited

with tabs[0]:
    st.session_state.df_xtb = render_aba(st.session_state.df_xtb, "XTB")
with tabs[1]:
    st.session_state.df_t212 = render_aba(st.session_state.df_t212, "T212")
with tabs[2]:
    st.session_state.df_tr = render_aba(st.session_state.df_tr, "TR")

st.divider()
st.info("Para atualizar, basta mudar a Quantidade ou o Preço diretamente na tabela. O cálculo é instantâneo.")