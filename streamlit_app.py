import streamlit as st
import json
import os
import httpx
from pathlib import Path
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# Set Streamlit page config
st.set_page_config(
    page_title="Intent-to-Action Bridge Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import local models and services directly
from app.models.schemas import BridgeEngineInput, BridgeEngineResponse, PersonalEmergencyContact
from app.services.intent_bridge_service import intent_bridge_service

# Load engine presets
PRESETS_FILE = Path(__file__).resolve().parent / "app" / "demo_cases" / "engine_presets.json"
presets = []
if PRESETS_FILE.exists():
    with open(PRESETS_FILE, "r", encoding="utf-8") as f:
        presets = json.load(f)

# Initialize Session State
if "engine_response" not in st.session_state:
    st.session_state.engine_response = None
if "selected_preset_id" not in st.session_state:
    st.session_state.selected_preset_id = None
if "safety_confirmed" not in st.session_state:
    st.session_state.safety_confirmed = None
if "bystander_answer" not in st.session_state:
    st.session_state.bystander_answer = ""

# Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("⚡ Engine Telemetry")
    st.caption("Gemini-Powered Intent-to-Action Bridge")
    
    st.markdown("---")
    # API Key Configuration
    st.subheader("🔑 Gemini Intelligence")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Provide a Google Gemini API key to activate live Gemini multimodal reasoning, or leave empty to use the high-fidelity offline cognitive simulation."
    )
    if st.button("Apply API Key", use_container_width=True):
        if api_key_input:
            intent_bridge_service.set_api_key(api_key_input)
            st.success("API key configured!")
        else:
            st.info("Operating in high-fidelity cognitive simulation mode.")

    engine_mode = "🟢 Live Gemini 2.5/1.5 Flash" if intent_bridge_service.has_active_key else "🔵 High-Fidelity Simulation"
    st.info(f"**Engine Mode:** {engine_mode}")

    st.markdown("---")
    st.subheader("🛡️ Core Principles")
    st.markdown("""
    1. **PARSE**: Extract entities & urgency; state ambiguity explicitly.
    2. **FUSE**: Fail-safe contradiction resolution (higher urgency overrides).
    3. **VERIFY**: Confidence scores (High/Med/Low); zero hallucinations.
    4. **STRUCTURE**: Dual JSON normalization.
    5. **ACT**: 1 clear directive + 1 plain-sentence rationale.
    """)

    st.markdown("---")
    st.caption("PromptWars Hackathon Edition • CivicBridge")


# Main Header
st.title("⚡ Intent-to-Action Bridge Engine")
st.markdown(
    "Transforming **unstructured, noisy, emotional, and degraded real-world inputs** "
    "into **structured, verified, life-critical action directives** with zero ambiguity."
)

st.markdown("---")

# Presets Bar
st.subheader("🎯 1-Click High-Stakes Test Scenarios")
preset_titles = {p["id"]: f"{p['title']} ({p['badge']})" for p in presets}
selected_id = st.selectbox(
    "Choose a pre-configured incident to test engine reasoning:",
    options=list(preset_titles.keys()),
    format_func=lambda x: preset_titles[x]
)

selected_preset = next((p for p in presets if p["id"] == selected_id), None)

col_p1, col_p2 = st.columns([4, 1])
with col_p1:
    if selected_preset:
        st.info(f"**Scenario Context:** {selected_preset['description']}")
with col_p2:
    if st.button("⚡ Load Preset Data", use_container_width=True):
        st.session_state.selected_preset_id = selected_id
        st.session_state.engine_response = None
        st.session_state.safety_confirmed = None
        st.session_state.bystander_answer = ""
        st.rerun()

st.markdown("---")

# Pre-populate fields if a preset is selected
p_input = selected_preset["input"] if (selected_preset and st.session_state.selected_preset_id == selected_id) else {}

# Accessibility Modes Toggle
acc_col1, acc_col2, acc_col3 = st.columns(3)
with acc_col1:
    is_single_tap = st.toggle("👵 Single-Tap Mode ('Something is Wrong')", value=p_input.get("is_single_tap_mode", False), help="For elderly or non-tech-savvy users needing conversational intake without complex forms.")
with acc_col2:
    is_silent_mode = st.toggle("🤫 Silent SOS Mode (Deaf / Mute / Covert)", value=p_input.get("is_silent_mode", False), help="Flags silent tactical approach, suppresses audible callbacks, and ensures covert handling.")
with acc_col3:
    reporter_role = st.selectbox(
        "Reporter Role",
        options=["auto", "victim", "bystander"],
        index=["auto", "victim", "bystander"].index(p_input.get("reporter_role", "auto")),
        help="Victims skip confirmation; bystanders may trigger 1 quick clarifying check."
    )

# Multimodal Input Console
st.subheader("📥 Multimodal Incident Intake")

col_left, col_right = st.columns(2)

with col_left:
    text_input = st.text_area(
        "🗣️ Free-form Voice Transcript or Text Narrative",
        value=p_input.get("text", ""),
        height=130,
        placeholder="e.g. My dad just collapsed clutching his chest, lips turning blue..."
    )
    
    st.markdown("##### 📷 Multimodal Media Intake (6 Input Streams)")
    media_tab1, media_tab2 = st.tabs(["📁 Upload Files", "🔴 Live Capture"])

    with media_tab1:
        st.caption("1. UPLOAD FILES SECTION")
        uploaded_photos = st.file_uploader("Upload Saved Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        uploaded_video = st.file_uploader("Upload Saved Video", type=["mp4", "mov", "avi"])
        uploaded_audio = st.file_uploader("Upload Saved Audio/Voice Note", type=["mp3", "wav", "m4a"])

        if uploaded_photos:
            with st.expander(f"📷 Attached Saved Photos ({len(uploaded_photos)})", expanded=False):
                pcols = st.columns(min(len(uploaded_photos), 4))
                for idx, p in enumerate(uploaded_photos):
                    with pcols[idx % min(len(uploaded_photos), 4)]:
                        st.image(p, caption=p.name, use_container_width=True)
        if uploaded_video:
            with st.expander("🎥 Attached Saved Video Preview", expanded=False):
                st.video(uploaded_video)
        if uploaded_audio:
            with st.expander("🎵 Attached Saved Audio Preview", expanded=False):
                st.audio(uploaded_audio)

    with media_tab2:
        st.caption("2. LIVE CAPTURE SECTION")
        live_snapshot = st.camera_input("Take Live Photo Snapshot")
        st.markdown("**Live Video Feed:**")
        live_video = webrtc_streamer(key="live-video-capture")
        live_audio = st.audio_input("Record Live Voice Note")

        if live_snapshot:
            with st.expander("📸 Live Snapshot Preview", expanded=False):
                st.image(live_snapshot, caption="Live Photo Snapshot", use_container_width=True)
        if live_audio:
            with st.expander("🎙️ Recorded Voice Note Preview", expanded=False):
                st.audio(live_audio)
    
    loc_col1, loc_col2 = st.columns(2)
    with loc_col1:
        gps_input = st.text_input(
            "📍 Sensor Live GPS (Lat, Long)",
            value=p_input.get("gps_coordinates", ""),
            placeholder="e.g. 37.774929, -122.419416"
        )
    with loc_col2:
        address_input = st.text_input(
            "🏷️ Stated Address / Landmark",
            value=p_input.get("address_stated", ""),
            placeholder="e.g. 5th and Market, Apt 3B"
        )

    env_input = st.text_input(
        "⛅ Environmental / Live Context Feed",
        value=p_input.get("environmental_feed", ""),
        placeholder="e.g. Wind 18 mph NE, dense residential traffic"
    )

with col_right:
    media_input = st.text_area(
        "📷 Degraded Media Observation (Photos/Video/Audio)",
        value=p_input.get("media_description", ""),
        height=130,
        placeholder="e.g. Shaky dark video: heavy black smoke billowing from 3rd floor, visible flames..."
    )

    medical_input = st.text_area(
        "📋 Unstructured Messy Medical History",
        value=p_input.get("messy_medical_history", ""),
        height=90,
        placeholder="e.g. LAD stent 2021, on Plavix, ALLERGY: Anaphylaxis to Penicillin..."
    )

# Emergency Contacts
contacts_data = p_input.get("emergency_contacts", [])
contact_name = contacts_data[0]["name"] if contacts_data else "Elena Vance (Family Contact)"
contact_phone = contacts_data[0]["phone"] if contacts_data else "+1-555-017-3321"

with st.expander("👥 Designated Emergency Contacts (Auto-Notification)", expanded=False):
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        c_name = st.text_input("Contact Name", value=contact_name)
    with c_col2:
        c_phone = st.text_input("Phone Number", value=contact_phone)

# Action Trigger Button
st.markdown("<br>", unsafe_allow_html=True)
exec_button = st.button("🚀 EXECUTE INTENT-TO-ACTION BRIDGE ENGINE", type="primary", use_container_width=True)

if exec_button:
    with st.spinner("Bundling 6 media streams & processing via FastAPI backend (port 8000)..."):
        # Construct emergency contacts
        contacts_list = []
        contacts_dicts = []
        if c_name and c_phone:
            contacts_list.append(PersonalEmergencyContact(name=c_name, phone=c_phone, relation="Emergency Contact"))
            contacts_dicts.append({"name": c_name, "phone": c_phone, "relation": "Emergency Contact"})

        # Bundle all 6 potential media streams into multipart payload
        files_payload = []
        attached_labels = []

        # 1. Saved Photos
        if uploaded_photos:
            for p in uploaded_photos:
                files_payload.append(("uploaded_photos", (p.name, p.getvalue(), p.type or "image/jpeg")))
                attached_labels.append(f"Saved Photo: {p.name}")

        # 2. Saved Video
        if uploaded_video:
            files_payload.append(("uploaded_video", (uploaded_video.name, uploaded_video.getvalue(), uploaded_video.type or "video/mp4")))
            attached_labels.append(f"Saved Video: {uploaded_video.name}")

        # 3. Saved Audio
        if uploaded_audio:
            files_payload.append(("uploaded_audio", (uploaded_audio.name, uploaded_audio.getvalue(), uploaded_audio.type or "audio/mpeg")))
            attached_labels.append(f"Saved Audio: {uploaded_audio.name}")

        # 4. Live Photo Snapshot
        if live_snapshot:
            files_payload.append(("live_snapshot", ("live_snapshot.jpg", live_snapshot.getvalue(), "image/jpeg")))
            attached_labels.append("Live Photo Snapshot (live_snapshot.jpg)")

        # 5. Live Video Stream
        if live_video and live_video.state and live_video.state.playing:
            files_payload.append(("live_video", ("webrtc_stream.txt", b"WebRTC Live Video Stream Active", "text/plain")))
            attached_labels.append("Live WebRTC Video Stream (Active)")

        # 6. Live Voice Note
        if live_audio:
            files_payload.append(("live_audio", ("live_voice_note.wav", live_audio.getvalue(), "audio/wav")))
            attached_labels.append("Live Recorded Voice Note (live_voice_note.wav)")

        effective_media_desc = media_input
        if attached_labels:
            joined_labels = "; ".join(attached_labels)
            effective_media_desc = f"{effective_media_desc} | Media Intake: {joined_labels}".strip(" |")

        form_data = {
            "text": text_input or "",
            "gps_coordinates": gps_input or "",
            "address_stated": address_input or "",
            "reporter_role": reporter_role or "auto",
            "messy_medical_history": medical_input or "",
            "environmental_feed": env_input or "",
            "is_silent_mode": "true" if is_silent_mode else "false",
            "is_single_tap_mode": "true" if is_single_tap else "false",
            "device_id": p_input.get("device_id", "web-demo-user"),
            "media_description": effective_media_desc or "",
            "emergency_contacts": json.dumps(contacts_dicts) if contacts_dicts else ""
        }

        # Send multipart form payload to FastAPI backend server on port 8000
        fastapi_url = "http://localhost:8000/api/engine/process-multipart"
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(fastapi_url, data=form_data, files=files_payload)
                if resp.status_code == 200:
                    st.session_state.engine_response = BridgeEngineResponse.model_validate(resp.json())
                    st.session_state.safety_confirmed = None
                    st.toast(f"✅ Ingested via FastAPI backend on port 8000 ({len(files_payload)} media streams)", icon="🚀")
                else:
                    st.error(f"FastAPI backend returned status {resp.status_code}: {resp.text}")
        except Exception as err:
            st.warning(f"FastAPI backend on port 8000 unreachable ({err}). Executing via local cognitive engine...")
            engine_input = BridgeEngineInput(
                text=text_input,
                media_description=effective_media_desc,
                media_file_name=", ".join(attached_labels) if attached_labels else p_input.get("media_file_name"),
                gps_coordinates=gps_input,
                address_stated=address_input,
                reporter_role=reporter_role,
                messy_medical_history=medical_input,
                environmental_feed=env_input,
                emergency_contacts=contacts_list,
                is_silent_mode=is_silent_mode,
                is_single_tap_mode=is_single_tap,
                device_id=p_input.get("device_id", "web-demo-user")
            )
            st.session_state.engine_response = intent_bridge_service.process_input(engine_input)
            st.session_state.safety_confirmed = None

# Render Output Results
if st.session_state.engine_response:
    res = st.session_state.engine_response
    st.markdown("---")
    
    # Hero Directive Banner
    urgency_colors = {
        "critical": "red",
        "high": "orange",
        "moderate": "blue",
        "low": "green"
    }
    badge_color = urgency_colors.get(res.structure.urgency_level.lower(), "gray")

    st.markdown(f"""
    <div style="background-color: #0f172a; padding: 24px; border-radius: 12px; border-left: 8px solid {badge_color}; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; color: #94a3b8; font-weight: bold;">
                ⚡ IMMEDIATE DIRECTIVE • REF: {res.session_id}
            </span>
            <span style="background-color: {badge_color}; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: bold; text-transform: uppercase; font-size: 12px;">
                URGENCY: {res.structure.urgency_level}
            </span>
        </div>
        <h2 style="color: #f8fafc; margin-top: 10px; margin-bottom: 8px; font-size: 24px;">
            👉 {res.act_directive}
        </h2>
        <p style="color: #cbd5e1; font-size: 16px; margin: 0;">
            <strong>Why:</strong> {res.structure.action_rationale}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5-Step Core Engine Execution View
    st.subheader("🧠 5-Step Core Reasoning Pipeline")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. PARSE (Entities & Ambiguity)",
        "2. FUSE (Contradiction Check)",
        "3. VERIFY (Fact Confidence)",
        "4. STRUCTURE (Normalized JSON)",
        "5. ACT (Immediate Next Step)"
    ])

    with tab1:
        st.markdown("#### Step 1: Parse Entities, Urgency & Ambiguities")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.write("**Extracted Intent:**", res.parse.extracted_intent)
            st.write("**Raw Urgency Detected:**", res.parse.raw_urgency_detected)
            st.write("**Key Entities Identified:**")
            st.json(res.parse.entities_extracted)
        with p_col2:
            st.write("**Explicit Ambiguities (Zero Guessing):**")
            if res.parse.explicit_ambiguities:
                for amb in res.parse.explicit_ambiguities:
                    st.warning(f"⚠️ {amb}")
            else:
                st.success("✅ No critical ambiguities detected in input streams.")

    with tab2:
        st.markdown("#### Step 2: Cross-Modal Fusion & Contradiction Resolution")
        st.write("**Streams Fused:**", ", ".join(res.fuse.streams_fused))
        
        if res.fuse.contradiction_detected:
            st.error(f"🚨 **CONTRADICTION DETECTED:** {res.fuse.mismatch_description}")
            st.info(f"🛡️ **Resolution:** {res.fuse.urgency_resolution}")
        else:
            st.success(f"✅ **Streams Concordant:** {res.fuse.urgency_resolution}")

    with tab3:
        st.markdown("#### Step 3: Verified Claims & Fact Cross-Checking")
        if res.verify:
            for v in res.verify:
                conf_color = "green" if v.confidence == "High" else ("orange" if v.confidence == "Medium" else "red")
                st.markdown(f"""
                - **Claim:** {v.claim}  
                  *Source:* `{v.context_source}` | *Confidence:* **:{conf_color}[{v.confidence}]** | *Verified:* {'✅' if v.verified else '❌'}
                """)
        else:
            st.info("No explicit empirical claims to verify.")

    with tab4:
        st.markdown("#### Step 4: Standard Structured Output Schema")
        st.json(res.structure.model_dump())
        if res.structure.missing_information:
            st.caption("Missing Information Logged:")
            for m in res.structure.missing_information:
                st.markdown(f"- ❓ {m}")

    with tab5:
        st.markdown("#### Step 5: Action Directive")
        st.success(f"**Action:** {res.act_directive}")
        st.write(f"**Rationale:** {res.structure.action_rationale}")

    # Emergency Operations Center (if triggered)
    if res.is_emergency and res.dispatch_packet:
        st.markdown("---")
        st.subheader("🚨 Emergency Operations & Dispatch Center")

        e_col1, e_col2 = st.columns([3, 2])

        with e_col1:
            st.markdown("### 📋 Structured Dispatch Packet")
            dp = res.dispatch_packet
            st.json(dp.model_dump())

            if dp.medical_context and dp.medical_context != "No prior medical records available on scene.":
                st.error(f"🩺 **CRITICAL MEDICAL CONTEXT FOR RESPONDERS:**\n{dp.medical_context}")

        with e_col2:
            st.markdown("### 🚒 Parallel Authority Dispatches")
            for route in res.authority_routes:
                st.markdown(f"""
                <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #3b82f6;">
                    <strong>{route.agency}</strong> • <span style="color: #ef4444; font-weight: bold;">{route.priority}</span><br>
                    <small style="color: #94a3b8;">Status: {route.status}</small><br>
                    <code>{route.payload}</code>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 📱 Emergency Contact Notifications")
            if res.contact_alerts:
                for ca in res.contact_alerts:
                    st.info(f"**To {ca.recipient_name} ({ca.phone}):**\n\n{ca.message}")
            else:
                st.caption("No designated personal contacts configured.")

            if res.low_bandwidth_fallback:
                st.markdown("### 📶 Low-Bandwidth SMS Fallback")
                st.code(res.low_bandwidth_fallback.payload, language="text")
                st.caption(f"Payload Size: {res.low_bandwidth_fallback.character_count} chars • Ready for direct cellular gateway")

        # Safeguards and Bystander Handling
        st.markdown("---")
        safe_col1, safe_col2 = st.columns(2)
        with safe_col1:
            st.subheader("🛡️ Safeguard & Anomaly Audit")
            st.write(f"**Anomaly Flag:** {res.safeguards.anomaly_flag}")
            st.write(f"**Audit Notes:** {res.safeguards.risk_notes}")
            
            if res.safeguards.bystander_clarifying_question:
                st.warning(f"💬 **Non-Blocking Bystander Clarification:** {res.safeguards.bystander_clarifying_question}")
                bystander_resp = st.text_input("Quick reply (dispatch already transmitted):", key="bystander_reply_box")
                if st.button("Submit Clarification"):
                    st.success("Clarification logged and forwarded to en-route units.")

        with safe_col2:
            st.subheader("🔄 Post-Incident Safety Check-In Loop")
            st.info(f"📢 **Dispatcher:** *\"{res.post_incident.message_to_reporter}\"*")
            
            if st.session_state.safety_confirmed is None:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Confirm I Am Safe", use_container_width=True):
                        log = intent_bridge_service.log_safety_confirmation(res.session_id, True)
                        st.session_state.safety_confirmed = True
                        st.success("Status Updated: CONFIRMED SAFE")
                        st.rerun()
                with c2:
                    if st.button("⚠️ Still In Danger", use_container_width=True):
                        log = intent_bridge_service.log_safety_confirmation(res.session_id, False, "Reporter indicates active peril")
                        st.session_state.safety_confirmed = False
                        st.error("Secondary urgent escalation dispatched!")
                        st.rerun()
            else:
                if st.session_state.safety_confirmed:
                    st.success("🎉 **Status:** Incident Closed — Reporter confirmed safe.")
                else:
                    st.error("🚨 **Status:** Active Emergency — Secondary units alerted to persistent danger.")
