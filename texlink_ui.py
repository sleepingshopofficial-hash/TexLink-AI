import streamlit as st
import requests
import json

# --- 1. Enterprise Page Configuration ---
st.set_page_config(page_title="TexLink | Football AI", page_icon="⚽", layout="wide")

url = "http://localhost:11434/api/generate"

# --- 2. Football-Exclusive Database ---
sialkot_suppliers = """
1. Striker Apparel Co: Specializes in 100% Polyester Sublimation. Best for Match Kits (Jerseys & Shorts).
2. Titan Gear Mfg: Specializes in Micro-polyester and Fleece. Best for Training Tracksuits and Winter Drill Tops.
3. Apex Latex Industries: Specializes in German Latex foam and PU. Best for Pro Goalkeeper Gloves and protective gear.
4. FlexFit Textiles: Specializes in Spandex/Elastane blends with flatlock stitching. Best for Compression Wear and Base Layers.
"""

# --- 3. Left Sidebar (System Metrics) ---
with st.sidebar:
    st.header("⚙️ Agentic Core")
    st.success("Status: Secure & Offline")
    st.write("**Active Niche:** Football Apparel")
    st.markdown("---")
    st.write("📊 **Database Metrics:**")
    st.write("- Verified Suppliers: 4")
    st.write("- QC Rules Active: Yes")
    st.markdown("---")
    st.caption("Zero-Trust Architecture v1.0")

# --- 4. Main Dashboard Header ---
st.title("⚽ TexLink B2B Routing Engine")
st.markdown("*Intelligent Matchmaking for Sialkot's Football Manufacturing*")
st.markdown("---")

# --- 5. Split Screen UI ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📥 Incoming Buyer Request")
    buyer_email = st.text_area("Paste Raw Buyer Email Here:", height=200, placeholder="Example: Need 250 sublimation jerseys...")
    execute_btn = st.button("🚀 Initialize Routing Agents", use_container_width=True)

with col2:
    st.subheader("🖥️ Live System Logs")
    log_box = st.empty()
    if not execute_btn:
        log_box.info("Awaiting input data...")

# --- 6. The Execution Engine (Agent Pipeline) ---
if execute_btn:
    if buyer_email:
        with col2:
            # -----------------------------------------
            # AGENT 1: THE EXTRACTOR
            # -----------------------------------------
            st.info("[Agent 1] Extracting item & materials...")
            prompt_1 = f"Extract the exact clothing item, material, and total quantity from this email: '{buyer_email}'. Return ONLY a JSON object with keys 'item', 'material', and 'quantity'."
            response_1 = requests.post(url, json={"model": "llama3.2", "prompt": prompt_1, "stream": False}).json()['response']
            st.write(response_1)
            
            try:
                clean_json = response_1.strip().strip('`').removeprefix('json')
                extracted_data = json.loads(clean_json)
                item = extracted_data.get('item', 'Unknown')
                materials = extracted_data.get('material', 'Unknown')
                quantity = extracted_data.get('quantity', 'Unknown')
            except:
                st.error("Andon Triggered! Agent 1 failed to generate valid JSON.")
                st.stop()
            
            # -----------------------------------------
            # AGENT 2: THE MATCHMAKER
            # -----------------------------------------
            st.warning("[Agent 2] Searching Sialkot Database...")
            prompt_2 = f"Based on this database of Sialkot suppliers: {sialkot_suppliers}. Which factory is the best match for manufacturing {quantity} {item} made of {materials}? Return ONLY the factory name and a 1-sentence reason."
            response_2 = requests.post(url, json={"model": "llama3.2", "prompt": prompt_2, "stream": False}).json()['response']
            st.write(response_2)
            
            # -----------------------------------------
            # AGENT 3: THE CLOSER (Updated with Kaizen)
            # -----------------------------------------
            st.success("[Agent 3] Drafting B2B Quotation...")
            prompt_3 = f"""
            You are the Lead Sourcing Consultant for TexLink. 
            The buyer requested: '{buyer_email}'.
            We extracted: Item: {item}, Materials: {materials}, Quantity: {quantity}.
            Matched Factory: {response_2}.
            
            Write a highly professional B2B email to the buyer. 
            Structure:
            1. Acknowledge the exact item and materials.
            2. EXPLICITLY state the total quantity requested AND the exact size breakdown. (This is mandatory).
            3. Introduce the matched Sialkot factory and why their expertise fits.
            4. State that our local QC team will personally oversee the production.
            5. End with a strong call to action to approve the sample phase.
            Do not use brackets or placeholders. Write the final draft ready to send.
            """
            draft_reply = requests.post(url, json={"model": "llama3.2", "prompt": prompt_3, "stream": False}).json()['response']
            
            # -----------------------------------------
            # AGENT 4: THE QC VERIFIER (Poka-Yoke Gate)
            # -----------------------------------------
            st.error("[Agent 4] Executing Strict Poka-Yoke Verification...")
            prompt_4 = f"""
            You are the strict Quality Control Verifier for TexLink. 
            You must inspect this drafted quotation: '{draft_reply}' against the original buyer request: '{buyer_email}'.
            
            Apply these 3 strict rules:
            1. Size & Quantity Match: Does the draft explicitly mention the total quantity and the exact size breakdown requested?
            2. Material Accuracy: Does the draft promise exactly the extracted materials '{materials}' without hallucinating alternatives?
            3. No Fake Commitments: Did the draft invent any fake delivery dates or unsupported stitching promises?
            
            If the draft passes ALL 3 rules, output exactly and only: "PASS". 
            If it fails ANY rule, output: "FAIL: [State the exact error]".
            """
            qc_result = requests.post(url, json={"model": "llama3.2", "prompt": prompt_4, "stream": False}).json()['response'].strip()
            st.write(f"QC Status: {qc_result}")
            
        with col1:
            st.markdown("---")
            if qc_result.startswith("PASS"):
                st.success("✅ Jidoka Passed: Quality Control Verified. Ready to Send.")
                st.subheader("✅ Final Approved Quotation")
                st.write(f"**Selected Factory:** {response_2}")
                st.text_area("Ready-to-Send Email:", value=draft_reply, height=350)
            else:
                st.error(f"🚨 Andon Triggered! Quality Check Failed.\nReason: {qc_result}")
                st.info("System halted. Please review Agent 3's output and adjust the system prompts.")
    else:
        st.error("Please paste an email first.")
