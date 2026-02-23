import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="OPC Klinik Karar Destek Sistemi",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STİL VE CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2, h3 {
        color: #34495e;
    }
    .stButton>button {
        background-color: #2980b9;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #3498db;
        border-color: #3498db;
    }
    .metric-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK VE GİRİŞ ---
st.title("🧬 Orofaringeal Kanser (OPC) Sağkalım Analizi - XAI Modeli")
st.markdown("""
Bu sistem, **Hibrit Topluluk Öğrenme (Ensemble Learning)** ve **XAI (Açıklanabilir Yapay Zeka)** teknolojilerini kullanarak hasta verilerine dayalı kişiselleştirilmiş risk analizi yapar.
""")

col1, col2 = st.columns([1, 2], gap="large")

# --- SOL MENÜ (VERİ GİRİŞİ) ---
with col1:
    st.sidebar.header("📋 Hasta Verileri")
    st.sidebar.info("Lütfen klinik parametreleri giriniz:")
    
    # Sidebar Inputs
    age = st.sidebar.number_input("Yaş", min_value=18, max_value=100, value=55)
    sex = st.sidebar.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    
    st.sidebar.subheader("Tümör Bilgileri")
    stage = st.sidebar.selectbox("TNM Evresi (Stage)", ["I", "II", "III", "IV"])
    tumor_size = st.sidebar.slider("Tümör Boyutu (cm)", 0.0, 10.0, 3.5, step=0.1)
    lymph_n = st.sidebar.selectbox("Lenf Nodu Tutulumu", ["Yok (N0)", "Var (N+)"])
    
    st.sidebar.subheader("Alışkanlıklar")
    smoking = st.sidebar.radio("Sigara Kullanımı", ["İçmiyor", "İçiyor/Geçmişi Var"])
    alcohol = st.sidebar.radio("Alkol Geçmişi", ["Yok", "Var"])
    
    st.sidebar.subheader("Biyobelirteçler")
    hpv_status = st.sidebar.checkbox("HPV Pozitif (+)", value=True, help="Human Papilloma Virus durumu prognoz için önemlidir.")

    # Analizi Başlat Butonu (Sidebar'ın altına veya ana ekrana koyabiliriz, istekte 'Sağ tarafta' denmiş ama sidebar mantıklı)
    # Kullanıcı isteği: "Sağ tarafta (Ana ekran) 'Analizi Başlat' butonu olsun."
    # Ancak sidebar inputs sol tarafta. Butonu sidebar'ın altına koymak daha temiz olabilir ama isteğe uyalım.
    
    # Sidebar bitişi

# --- SAĞ TARAF (ANA EKRAN) ---
with col2:
    st.write("### Analiz Ekranı")
    st.write("Hasta verilerini sol taraftan girdikten sonra analizi başlatın.")
    
    predict_btn = st.button("🔍 Analizi Başlat", type="primary")

    if predict_btn:
        with st.spinner('Yapay Zeka Modeli Çalışıyor...'):
            # SİMÜLASYON MODU:
            # Gerçek model entegrasyonu öncesi sunum amaçlı simülasyon mantığı.
            
            base_risk = 0.20 # Baz risk
            
            # Basit Risk Artış Mantığı (Simülasyon)
            if stage == "III": base_risk += 0.20
            if stage == "IV": base_risk += 0.40
            if tumor_size > 4.0: base_risk += 0.15
            if smoking == "İçmiyor": base_risk -= 0.05
            if hpv_status: base_risk -= 0.15 # HPV pozitif genelde daha iyi prognoz demektir
            if age > 65: base_risk += 0.10
            if lymph_n == "Var (N+)": base_risk += 0.10
            
            # Skoru 0-1 arasına sıkıştır
            risk_score = min(max(base_risk, 0.01), 0.99)
            risk_percent = risk_score * 100
            
            st.divider()
            
            # 1. RİSK SKORU GÖSTERİMİ
            st.subheader("📊 Tahmin Sonucu")
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                if risk_percent < 50:
                    st.success(f"Düşük Risk Grubu (Sağkalım Olasılığı Yüksek)")
                    st.metric(label="Tahmini Risk Skoru", value=f"%{risk_percent:.1f}", delta="- Güvenli Bölge")
                else:
                    st.error(f"Yüksek Risk Grubu (Dikkatli İzlem Gerekir)")
                    st.metric(label="Tahmini Risk Skoru", value=f"%{risk_percent:.1f}", delta_color="inverse", delta="+ Riskli Bölge")
            
            with col_res2:
                 st.write("Risk Seviyesi:")
                 st.progress(risk_score)
                 st.caption("Bu skor, 5 yıllık sağkalım riskini simüle etmektedir.")
            
            # 2. XAI (SHAP) GÖRSELLEŞTİRME SİMÜLASYONU
            st.divider()
            st.subheader("🧠 Yapay Zeka Neden Bu Kararı Verdi? (XAI)")
            st.markdown("**SHAP Analizi (Waterfall Simülasyonu):** Modelin kararına etki eden faktörler.")

            # SHAP benzeri grafik çizimi
            features = ['HPV Durumu', 'TNM Evresi', 'Tümör Boyutu', 'Lenf Nodu', 'Yaş', 'Sigara']
            
            # Simüle edilmiş etki değerleri (Kırmızı risk artırır, Mavi azaltır)
            # Mantık: Risk artıranlar pozitif, azaltanlar negatif
            
            # HPV
            hpv_effect = -0.15 if hpv_status else 0.05
            
            # Stage
            stage_effect = 0.25 if stage in ["III", "IV"] else -0.05
            
            # Tumor Size
            size_effect = 0.10 if tumor_size > 4.0 else -0.02
            
            # Lymph Node
            lymph_effect = 0.08 if lymph_n == "Var (N+)" else -0.03
            
            # Age
            age_effect = 0.05 if age > 60 else -0.02
            
            # Smoking
            smoke_effect = 0.05 if smoking == "İçmiyor" else 0.08 # Sigara içmiyorsa risk düşer, içiyorsa artar
            # Düzeltme: Sigara içmiyorsa risk düşmeli (negatif etki), içiyorsa artmalı (pozitif etki)
            smoke_effect = -0.05 if smoking == "İçmiyor" else 0.08

            values = [hpv_effect, stage_effect, size_effect, lymph_effect, age_effect, smoke_effect]
            
            # Renkler: Pozitif (Risk artırıcı) -> Kırmızı, Negatif (Risk düşürücü) -> Mavi
            colors = ['#e74c3c' if x > 0 else '#3498db' for x in values]
            
            fig, ax = plt.subplots(figsize=(10, 5))
            y_pos = np.arange(len(features))
            
            # Bar chart
            bars = ax.barh(y_pos, values, align='center', color=colors)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(features)
            ax.set_xlabel('SHAP Değeri (Modele Etkisi)')
            ax.set_title('Klinik Özelliklerin Risk Skoruna Etkisi')
            ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
            
            # Barların ucuna değerleri yazalım
            for i, v in enumerate(values):
                ax.text(v + (0.01 if v > 0 else -0.01), i, f"{v:+.2f}", va='center', fontsize=9, 
                        ha='left' if v > 0 else 'right', color='black')

            # Çerçeve temizliği
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            st.pyplot(fig)
            
            st.info("""
            ℹ️ **Grafik Okuma:** 
            * **Kırmızı Çubuklar:** Riski artıran faktörler (Örn: İleri evre, büyük tümör, sigara).
            * **Mavi Çubuklar:** Riski düşüren/koruyucu faktörler (Örn: HPV Pozitifliği, Genç yaş).
            """)

    else:
        # Başlangıç ekranı (Boş durum)
        st.info("👈 Lütfen sol taraftaki menüden hasta verilerini girip **'Analizi Başlat'** butonuna basınız.")
        
        # Örnek bir görsel veya açıklama
        st.markdown("""
        ### Sistem Nasıl Çalışır?
        1.  **Veri Girişi:** Sol panelden hastanın klinik verilerini girin.
        2.  **Analiz:** Yapay zeka modeli verileri işler.
        3.  **Sonuç:** Risk skoru ve kararı etkileyen faktörler (SHAP) görüntülenir.
        """)
