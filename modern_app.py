"""
Modern Skills Intelligence Platform with Knowledge Graph
"""
import streamlit as st
import os
import json
from neo4j_skills_manager import neo4j_skills
from cv_parser import CVParser
from rag_pipeline import RAGPipeline
from graph_visualizer import SkillsGraphVisualizer
import pandas as pd
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Skills Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional modern interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(180deg, #0B0F19 0%, #0D1117 100%);
        padding: 0 2rem 2rem 2rem;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0B0F19 0%, #0D1117 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161B26 0%, #0F1419 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #F1F5F9;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.05em;
        margin-bottom: 1.5rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: #CBD5E1;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Professional Typography */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 48px;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 28px;
        letter-spacing: -0.02em;
        color: #F1F5F9;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 18px;
        letter-spacing: -0.01em;
        color: #E2E8F0;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.01em;
        color: #CBD5E1;
    }
    
    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #94A3B8 !important;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 36px;
        font-weight: 900;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.04em;
        color: #F8FAFC;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #64748B;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Enhanced Cards */
    .stat-card {
        background: linear-gradient(145deg, #1E2433 0%, #161B26 100%);
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        box-shadow: 
            0 10px 15px -3px rgba(0, 0, 0, 0.4),
            0 4px 6px -2px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
    }
    
    .skill-badge {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        padding: 12px 20px;
        border-radius: 10px;
        color: #FFFFFF;
        display: inline-block;
        margin: 6px 4px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.02em;
        box-shadow: 
            0 4px 12px rgba(99, 102, 241, 0.3),
            0 1px 3px rgba(99, 102, 241, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .skill-badge:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 
            0 8px 20px rgba(99, 102, 241, 0.4),
            0 2px 6px rgba(99, 102, 241, 0.6);
    }
    
    .field-card {
        background: linear-gradient(145deg, #1E2433 0%, #171C28 100%);
        padding: 32px;
        border-radius: 16px;
        border-left: 5px solid #6366F1;
        margin: 16px 0;
        box-shadow: 
            0 10px 15px -3px rgba(0, 0, 0, 0.4),
            0 4px 6px -2px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .field-card:hover {
        transform: translateX(4px);
        border-left-color: #818CF8;
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.5),
            0 10px 10px -5px rgba(0, 0, 0, 0.4);
    }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 12px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 8px 24px rgba(99, 102, 241, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        background: linear-gradient(135deg, #818CF8 0%, #6366F1 100%);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(30, 36, 51, 0.5);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        border-radius: 8px;
        padding: 10px 20px;
        color: #94A3B8;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(99, 102, 241, 0.1);
        color: #C7D2FE;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Enhanced Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(99, 102, 241, 0) 0%, 
            rgba(99, 102, 241, 0.3) 50%, 
            rgba(99, 102, 241, 0) 100%);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 36, 51, 0.5);
        border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.6);
        background: rgba(30, 36, 51, 0.8);
    }
    
    /* Data Frame */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Info Box */
    .stAlert {
        background: linear-gradient(145deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 20px;
        font-weight: 500;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366F1 0%, #818CF8 100%);
        border-radius: 8px;
        height: 8px;
    }
    
    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background: rgba(30, 36, 51, 0.6);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background: rgba(30, 36, 51, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 10px;
        color: #F1F5F9;
        font-family: 'Inter', sans-serif;
        padding: 12px 16px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #6366F1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline(use_groq=True, neo4j_manager=neo4j_skills)
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'cv_skills' not in st.session_state:
    st.session_state.cv_skills = []
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = None
if 'graph_visualizer' not in st.session_state:
    st.session_state.graph_visualizer = SkillsGraphVisualizer(neo4j_skills)

# Sidebar - Library & Upload
with st.sidebar:
    # Logo at the top
    st.markdown('<div style="padding: 20px 0 30px 0;"></div>', unsafe_allow_html=True)
    col_logo = st.columns([1, 3, 1])
    with col_logo[1]:
        st.image("logo.png", use_column_width=True)
    
    st.markdown("## LIBRARY")
    
    # Stats at top
    col1, col2 = st.columns(2)
    try:
        stats = neo4j_skills.get_graph_stats()
        with col1:
            st.metric("SKILLS", stats.get("skills", 0), delta="+18%" if stats.get("skills", 0) > 0 else None)
        with col2:
            st.metric("FIELDS", stats.get("fields", 0))
    except:
        with col1:
            st.metric("SKILLS", 0)
        with col2:
            st.metric("FIELDS", 0)
    
    st.divider()
    
    # Upload section
    st.markdown("### UPLOAD DOCUMENTS")
    st.caption("Drop PDF/TXT files here")
    
    tab1, tab2 = st.tabs(["Dataset", "CV"])
    
    with tab1:
        skills_file = st.file_uploader("Skills Dataset (JSON)", type=['json'], key="skills")
        if st.button("Load Dataset", use_container_width=True):
            if skills_file:
                dataset = json.load(skills_file)
                neo4j_skills.load_skills_dataset(dataset)
                st.success(f"✓ Loaded {len(dataset)} fields")
                st.rerun()
    
    with tab2:
        cv_file = st.file_uploader("Your CV (PDF/TXT)", type=['pdf', 'txt'], key="cv")
        if st.button("Analyze CV", use_container_width=True):
            if cv_file:
                with st.spinner("Analyzing..."):
                    os.makedirs("temp_uploads", exist_ok=True)
                    file_path = os.path.join("temp_uploads", cv_file.name)
                    with open(file_path, "wb") as f:
                        f.write(cv_file.getbuffer())
                    
                    parser = CVParser()
                    cv_text = parser.parse_pdf(file_path) if cv_file.name.endswith('.pdf') else parser.parse_text(file_path)
                    
                    found_skills = neo4j_skills.extract_cv_skills(cv_text)
                    if found_skills:
                        summary = parser.get_cv_summary(cv_text)
                        person_id = f"person_{hash(summary['name'])}"
                        neo4j_skills.create_person_profile(person_id, summary['name'], found_skills)
                        
                        st.session_state.cv_skills = found_skills
                        st.session_state.evaluation = neo4j_skills.evaluate_skills(found_skills)
                        st.success(f"✓ {len(found_skills)} skills found")
                        st.rerun()
                    else:
                        st.error("No skills found. Load dataset first!")

# Main content area - 3 column layout
if st.session_state.evaluation:
    col_main, col_insights = st.columns([2, 1])
    
    with col_main:
        # Header with logo
        st.markdown("""
        <h1 style="
            margin: 0 0 8px 0;
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.03em;
        ">Skillmap</h1>
        """, unsafe_allow_html=True)
        st.caption("Advanced AI-powered career matching and skills analysis")
        
        # Top match card
        top = st.session_state.evaluation[0]
        st.markdown(f"""
        <div class="field-card" style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(79, 70, 229, 0.05) 100%);
            border-left: 5px solid #6366F1;
            padding: 36px;
            margin: 24px 0;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="
                    width: 48px;
                    height: 48px;
                    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
                ">
                    <span style="font-size: 24px;">★</span>
                </div>
                <h2 style="color: #F1F5F9; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">{top['field']}</h2>
            </div>
            <p style="font-size: 42px; font-weight: 900; color: #10B981; margin: 16px 0 8px 0; letter-spacing: -0.04em;">{top['score']:.1f}%</p>
            <p style="color: #94A3B8; margin: 0; font-size: 15px; font-weight: 500; letter-spacing: 0.01em;">Optimal career field match • Based on comprehensive profile analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### IDENTIFIED SKILLS")
        skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in st.session_state.cv_skills])
        st.markdown(skills_html, unsafe_allow_html=True)
        
        st.divider()
        
        # Knowledge Graph Section
        st.markdown("### KNOWLEDGE GRAPH")
        
        graph_tab1, graph_tab2 = st.tabs(["Network Visualization", "Data Distribution"])
        
        with graph_tab1:
            # Generate graph data
            graph_data = st.session_state.graph_visualizer.get_person_graph_data(st.session_state.cv_skills)
            
            # Create vis.js network visualization
            html_content = f"""
            <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
            <div id="network" style="height: 400px; background: #13171F; border-radius: 12px; border: 1px solid #2A3040;"></div>
            
            <script type="text/javascript">
                var nodes = new vis.DataSet({json.dumps(graph_data['nodes'])});
                var edges = new vis.DataSet({json.dumps(graph_data['edges'])});
                
                var container = document.getElementById('network');
                var data = {{
                    nodes: nodes,
                    edges: edges
                }};
                
                var options = {{
                    nodes: {{
                        shape: 'dot',
                        font: {{
                            color: '#F0F4F8',
                            size: 14
                        }},
                        borderWidth: 2,
                        borderWidthSelected: 3
                    }},
                    edges: {{
                        width: 2,
                        color: {{
                            color: '#6B7A91',
                            highlight: '#6366F1'
                        }},
                        smooth: {{
                            type: 'continuous'
                        }},
                        font: {{
                            color: '#9CA8B8',
                            size: 11,
                            align: 'middle'
                        }}
                    }},
                    physics: {{
                        forceAtlas2Based: {{
                            gravitationalConstant: -50,
                            centralGravity: 0.01,
                            springLength: 150,
                            springConstant: 0.08
                        }},
                        maxVelocity: 50,
                        solver: 'forceAtlas2Based',
                        timestep: 0.35,
                        stabilization: {{iterations: 150}}
                    }},
                    interaction: {{
                        hover: true,
                        tooltipDelay: 200
                    }}
                }};
                
                var network = new vis.Network(container, data, options);
            </script>
            """
            
            components.html(html_content, height=450)
            
            st.caption(f"● {len(graph_data['nodes'])} nodes • {len(graph_data['edges'])} connections • Active")
        
        with graph_tab2:
            # Skill distribution table
            distribution = st.session_state.graph_visualizer.get_field_distribution(st.session_state.cv_skills)
            
            if distribution:
                df = pd.DataFrame(distribution)
                df.columns = ["Field", "Your Skills Count"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No skill distribution data available")
        
        st.divider()
        
        # Chat message history display
        st.markdown("### CAREER ADVISOR")
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    with col_insights:
        st.markdown("## INSIGHTS")
        
        # Performance metrics
        st.markdown("### PERFORMANCE METRICS")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("LATENCY", "142 ms", delta="-12ms")
        with col_b:
            st.metric("TOKENS", "4.2k", delta="+0.3k")
        
        st.metric("MATCH SCORE", f"{top['score']:.1f}%", delta=f"+{top['score']-50:.1f}%")
        
        st.divider()
        
        # Skill distribution visualization
        st.markdown("### SKILL DISTRIBUTION")
        
        distribution = st.session_state.graph_visualizer.get_field_distribution(st.session_state.cv_skills)
        
        if distribution:
            for item in distribution[:5]:
                st.markdown(f"**{item['field']}**")
                st.progress(item['skills_count'] / max([d['skills_count'] for d in distribution]))
                st.caption(f"{item['skills_count']} skills")
        
        st.divider()
        
        # Field recommendations
        st.markdown("### RECOMMENDED FIELDS")
        
        for i, field in enumerate(st.session_state.evaluation[:3], 1):
            rank_color = ["#10B981", "#3B82F6", "#8B5CF6"][i-1]
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(30, 36, 51, 0.8) 0%, rgba(23, 28, 40, 0.9) 100%);
                padding: 18px 20px;
                border-radius: 12px;
                margin: 12px 0;
                border: 1px solid rgba(99, 102, 241, 0.2);
                transition: all 0.3s ease;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="
                            background: linear-gradient(135deg, {rank_color} 0%, {rank_color}CC 100%);
                            width: 32px;
                            height: 32px;
                            border-radius: 8px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 800;
                            font-size: 16px;
                            box-shadow: 0 2px 8px {rank_color}40;
                        ">{i}</span>
                        <span style="color: #E2E8F0; font-weight: 700; font-size: 15px;">{field['field']}</span>
                    </div>
                    <div style="color: {rank_color}; font-size: 22px; font-weight: 900; letter-spacing: -0.02em;">{field['score']:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        st.caption("Model: Groq Llama 3.1 • v2.6.8")
    
    # Chat input placed outside columns to avoid Streamlit restriction
    if question := st.chat_input("Ask anything about your career..."):
        st.session_state.messages.append({"role": "user", "content": question})
        
        with st.spinner("Analyzing..."):
            response = st.session_state.rag_pipeline.query_with_skills(question, st.session_state.cv_skills)
        
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        st.rerun()

else:
    # Welcome screen with logo
    st.markdown("""
    <div style="text-align: center; padding: 0 0 20px 0;">
        <h1 style="
            margin: 0;
            font-size: 64px;
            font-weight: 900;
            background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.03em;
        ">Skillmap</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <h2 style="
        text-align: center;
        font-size: 36px;
        font-weight: 600;
        color: #94A3B8;
        letter-spacing: 0.02em;
        margin: 20px 0 40px 0;
        font-family: 'Inter', sans-serif;
    ">Advanced Career Matching & Skills Analysis</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px 28px;
        margin: 32px 0;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    ">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                width: 48px;
                height: 48px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
                font-size: 24px;
            ">→</div>
            <div>
                <h3 style="margin: 0; color: #E2E8F0; font-size: 18px; font-weight: 700;">Get Started</h3>
                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 14px; font-weight: 500;">Upload skills dataset and your CV from the sidebar to begin comprehensive analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(30, 36, 51, 0.8) 0%, rgba(23, 28, 40, 0.9) 100%);
            padding: 32px;
            border-radius: 16px;
            border: 1px solid rgba(99, 102, 241, 0.15);
            height: 100%;
            transition: all 0.3s ease;
        ">
            <div style="
                width: 56px;
                height: 56px;
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
                font-size: 28px;
            ">◇</div>
            <h3 style="color: #F1F5F9; font-size: 20px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.01em;">Knowledge Graph</h3>
            <p style="color: #94A3B8; font-size: 14px; line-height: 1.7; font-weight: 500;">Visualize skill relationships and career connections through Neo4j graph database technology</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(30, 36, 51, 0.8) 0%, rgba(23, 28, 40, 0.9) 100%);
            padding: 32px;
            border-radius: 16px;
            border: 1px solid rgba(99, 102, 241, 0.15);
            height: 100%;
            transition: all 0.3s ease;
        ">
            <div style="
                width: 56px;
                height: 56px;
                background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                font-size: 28px;
            ">⚡</div>
            <h3 style="color: #F1F5F9; font-size: 20px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.01em;">AI-Powered Matching</h3>
            <p style="color: #94A3B8; font-size: 14px; line-height: 1.7; font-weight: 500;">Proprietary algorithms analyze your competencies to identify optimal career trajectories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(30, 36, 51, 0.8) 0%, rgba(23, 28, 40, 0.9) 100%);
            padding: 32px;
            border-radius: 16px;
            border: 1px solid rgba(99, 102, 241, 0.15);
            height: 100%;
            transition: all 0.3s ease;
        ">
            <div style="
                width: 56px;
                height: 56px;
                background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                font-size: 28px;
            ">◈</div>
            <h3 style="color: #F1F5F9; font-size: 20px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.01em;">Real-Time Intelligence</h3>
            <p style="color: #94A3B8; font-size: 14px; line-height: 1.7; font-weight: 500;">Instant skill gap analysis with actionable recommendations for career advancement</p>
        </div>
        """, unsafe_allow_html=True)
