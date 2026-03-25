import streamlit as st
from supabase import create_client, Client
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="TexLink AI | Sialkot", page_icon="⚽", layout="wide")

st.title("⚽ TexLink AI Command Center")
st.markdown("**Autonomous 4-Agent Pipeline for Sialkot Football Exporters**")
st.markdown("---")

# --- 1. LIVE CLOUD DATABASE (Supabase Integration) ---
@st.cache_resource
def init_connection():
    # Streamlit Secrets se API keys uthana
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# Database connect karne ki koshish (Poka-Yoke: Error handling)
try:
    supabase = init_connection()
    db_status = True
except Exception as e:
    st.error(f"Database Connection Failed: {e}")
    db_status = False

@st.cache_data(ttl=600)
def get_suppliers():
    # Sialkot factories ka data cloud se fetch karna
    response = supabase.table("sialkot_factories").select("*").execute()
    
    suppliers_str = ""
    for item in response.data:
        suppliers_str += f"- {item['factory_name']}: Specializes in {item['specialty']}. Best for {item['best_for']}.\n"
    return suppliers_str

# --- 2. DASHBOARD UI & LOGIC ---
if db_status:
    with st.spinner("Connecting to Sialkot Cloud Database..."):
        sialkot_suppliers = get_suppliers()
    
    # Success message aur data preview
    st.success("✅ Database Online! Factory roster loaded.")
    with st.expander("View Sialkot Factory Database (Live from Supabase)"):
        st.text(sialkot_suppliers)
    
    st.markdown("### 📥 Incoming Buyer Request")
    buyer_email = st.text_area(
        "Paste the buyer's email here:", 
        height=150, 
        placeholder="Example: Hi, we are looking for a manufacturer in Sialkot for 500 sublimated 100% polyester football kits..."
    )

    # The Execution Button
    if st.button("Run TexLink Engine 🚀", type="primary"):
        if not buyer_email:
            st.warning("⚠️ Poka-Yoke Alert: Please paste a buyer email first!")
        else:
            st.info("Initializing Agent 1: The Extractor...")
            
            # Dummy loading for now to show UI flow
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.02)
                progress_bar.progress(percent_complete + 1)
                
            st.success("Pipeline Executed! (Backend connection pending)")
