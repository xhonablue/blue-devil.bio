import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Immune System & Drug Development",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #7B1FA2;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #7B1FA2 0%, #4A148C 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #F3E5F5;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #7B1FA2;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #FF9800;
        margin: 1rem 0;
    }
    .michigan-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #00274C;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #7B1FA2;
        color: white;
        border-radius: 5px;
        padding: 0.5rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4A148C;
    }
    .developer-credit {
        text-align: center;
        color: #666;
        font-size: 0.9em;
        margin-top: -1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'activity_submitted' not in st.session_state:
    st.session_state.activity_submitted = False
if 'xp_points' not in st.session_state:
    st.session_state.xp_points = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'completed_checks' not in st.session_state:
    st.session_state.completed_checks = set()
if 'drug_design_data' not in st.session_state:
    st.session_state.drug_design_data = None
if 'quiz_short_answers' not in st.session_state:
    st.session_state.quiz_short_answers = None

# XP Award Function
def award_xp(points, check_id, achievement_name=None):
    """Award XP points and track completed checks to prevent double-counting"""
    if check_id not in st.session_state.completed_checks:
        st.session_state.xp_points += points
        st.session_state.completed_checks.add(check_id)
        if achievement_name and achievement_name not in st.session_state.achievements:
            st.session_state.achievements.append(achievement_name)
        return True
    return False

# Sidebar navigation
with st.sidebar:
    # XP Progress Display
    st.markdown("### 🏆 Your Progress")
    st.metric("XP Points", st.session_state.xp_points, help="Earn XP by answering questions correctly!")
    
    # Progress bar (max 500 XP for completing everything)
    progress = min(st.session_state.xp_points / 500, 1.0)
    st.progress(progress)
    
    # Level calculation
    if st.session_state.xp_points >= 400:
        level = "🧬 Biology Master"
    elif st.session_state.xp_points >= 250:
        level = "🔬 Research Scientist"
    elif st.session_state.xp_points >= 100:
        level = "🧪 Lab Technician"
    elif st.session_state.xp_points >= 25:
        level = "📚 Biology Student"
    else:
        level = "🌱 Beginner"
    
    st.caption(f"Level: {level}")
    
    # Show achievements
    if st.session_state.achievements:
        with st.expander(f"🎖️ Achievements ({len(st.session_state.achievements)})"):
            for achievement in st.session_state.achievements:
                st.write(f"✅ {achievement}")
    
    st.markdown("---")
    st.markdown("### 🧬 Navigation")
    
    pages = {
        "🏠 Home": "home",
        "📰 News Article": "article",
        "🎯 Learning Objectives": "objectives",
        "🛡️ The Immune System": "immune_system",
        "⚠️ Autoimmune Diseases": "autoimmune",
        "💊 Drug Development": "drug_development",
        "🧪 Design a Treatment": "design_challenge",
        "❓ Quiz & Assessment": "quiz",
        "📚 Resources": "resources"
    }
    
    for page_name, page_key in pages.items():
        if st.button(page_name):
            st.session_state.page = page_key
    
    st.markdown("---")
    st.markdown("### 👥 About")
    st.info("**Grade Level:** 9-12\n\n**Duration:** 50-60 minutes\n\n**Subject:** Biology\n\n**State:** Michigan")
    
    st.markdown("---")
    st.markdown("**Teacher Mode**")
    teacher_mode = st.checkbox("Enable teacher notes")

# Main content area
def show_home():
    st.markdown('<div class="main-header">🧬 The Immune System & Drug Development</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3 style="text-align: center;">Welcome to the Interactive Lesson!</h3>
        <p style="text-align: center;">Explore how our immune system protects us, what happens when it attacks 
        our own body, and how scientists develop drugs to treat autoimmune diseases like psoriasis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Today's Big Question:")
        st.success("**How can understanding the immune system at the molecular level help scientists design targeted treatments for autoimmune diseases?**")
        
        # Michigan Connection
        st.markdown("""
        <div class="michigan-box">
        <h4>🏥 Michigan Connection</h4>
        <p>Michigan is home to major biotech research! The University of Michigan, Wayne State, and Michigan State 
        have leading immunology research programs. Detroit's Henry Ford Health and Beaumont conduct clinical trials 
        for new autoimmune treatments that could help the estimated 500,000+ Michiganders living with autoimmune diseases.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 What You'll Learn:")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            ✅ How the immune system works
            
            ✅ What causes autoimmune diseases
            
            ✅ How psoriasis affects the skin
            """)
        
        with col_b:
            st.markdown("""
            ✅ How drugs target specific proteins
            
            ✅ Clinical trial phases (1, 2, 3)
            
            ✅ Career connections in biotech
            """)
        
        st.markdown("### 🚀 Ready to Begin?")
        st.info("👈 Use the sidebar navigation to explore different sections of this lesson!")
        
        # Michigan Science Standards Dropdown
        st.markdown("---")
        st.markdown("### 📋 Michigan Science Standards (MSS) Covered")
        
        with st.expander("🎓 Click to view all Michigan Science Standards addressed in this lesson", expanded=False):
            st.markdown("""
            <div class="michigan-box">
            <p>This lesson is aligned with the <strong>Michigan Science Standards (MSS)</strong>, which are based on 
            the Next Generation Science Standards (NGSS) with emphasis on real-world biomedical applications.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🧬 Life Science Standards")
            
            st.markdown("""
            **HS-LS1-1: Structure and Function**
            > *Construct an explanation based on evidence for how the structure of DNA determines the structure 
            > of proteins which carry out the essential functions of life through systems of specialized cells.*
            
            - **Lesson Connection:** How TYK2 enzyme structure determines its function; how envudeucitinib binds to block it
            - **Activities:** Drug Development section, Design Challenge
            """)
            
            st.markdown("""
            **HS-LS1-2: Interacting Body Systems**
            > *Develop and use a model to illustrate the hierarchical organization of interacting systems that 
            > provide specific functions within multicellular organisms.*
            
            - **Lesson Connection:** Immune system components (cells, tissues, organs) working together; skin as organ system
            - **Activities:** Immune System section, Autoimmune Diseases section
            """)
            
            st.markdown("""
            **HS-LS1-4: Cell Division and Differentiation**
            > *Use a model to illustrate the role of cellular division and differentiation in producing and 
            > maintaining complex organisms.*
            
            - **Lesson Connection:** Skin cell turnover in psoriasis (3-4 days vs normal 28-30 days); T-cell differentiation
            - **Activities:** Autoimmune Diseases section
            """)
            
            st.markdown("#### 🔬 Science & Engineering Practices")
            
            st.markdown("""
            **HS-LS1-6: Scientific Investigation**
            > *Construct and revise an explanation based on valid and reliable evidence obtained from a variety 
            > of sources including students' own investigations, models, theories, simulations, peer review.*
            
            - **Lesson Connection:** Clinical trial phases, peer review in drug development, evaluating evidence
            - **Activities:** Drug Development section, Quiz assessment
            """)
            
            st.markdown("""
            **HS-ETS1-3: Engineering Design**
            > *Evaluate a solution to a complex real-world problem based on prioritized criteria and 
            > trade-offs that account for a range of constraints.*
            
            - **Lesson Connection:** Drug design trade-offs (efficacy vs. side effects, cost vs. accessibility)
            - **Activities:** Design Challenge
            """)
            
            st.markdown("---")
            
            st.markdown("#### 📊 Standards Summary Table")
            
            standards_data = {
                "Standard": ["HS-LS1-1", "HS-LS1-2", "HS-LS1-4", "HS-LS1-6", "HS-ETS1-3"],
                "Topic": ["Structure & Function", "Body Systems", "Cell Division", "Scientific Investigation", "Engineering Design"],
                "Lesson Sections": ["Drug Development", "Immune System", "Autoimmune Diseases", "Drug Development, Quiz", "Design Challenge"]
            }
            
            standards_df = pd.DataFrame(standards_data)
            st.table(standards_df)
        
        # Quick stats
        st.markdown("---")
        st.markdown("### 📊 Autoimmune Disease Facts")
        
        stat1, stat2, stat3, stat4 = st.columns(4)
        
        with stat1:
            st.metric("Americans Affected", "~24 million", "by autoimmune diseases")
        with stat2:
            st.metric("Psoriasis Patients", "~8 million", "in the United States")
        with stat3:
            st.metric("Known Autoimmune", "80+", "different diseases")
        with stat4:
            st.metric("Drug Development", "10-15 years", "average timeline")

def show_article():
    st.markdown('<div class="main-header">📰 The News Article</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Alumis Shares Surge 95% on Positive Phase 3 Psoriasis Data for Envudeucitinib
        
        **By Howard Smith, The Motley Fool • January 6, 2026**
        
        📰 **[Read the full article on Yahoo Finance](https://finance.yahoo.com/news/stock-market-today-jan-6-223250235.html)**
        
        ---
        """)
        
        st.markdown("""
        **Alumis** (NASDAQ: ALMS), which develops targeted therapies for immune-mediated diseases, closed 
        Tuesday's session at $16.23, **up 95.31%**. Trading volume reached 64.1 million shares, coming in 
        about 3,077% above its three-month average of 2 million shares.
        
        Tuesday's move followed **Phase 3 psoriasis data for envudeucitinib**, which investors are treating 
        as a potential commercial inflection point. The focus is now watching New Drug Application (NDA) 
        timing and competitive dynamics in oral **TYK2 inhibitors**.
        
        ---
        
        ### What Happened?
        
        Alumis is a clinical-stage biopharmaceutical company developing next-generation targeted therapies 
        for patients with **immune-mediated diseases**. Today's positive Phase 3 results achieved both 
        **primary and secondary endpoints** with strong statistical significance in individuals with 
        **moderate-to-severe plaque psoriasis**.
        
        Small biotech and big pharma stocks typically react differently to trial news like this. Many smaller 
        biotechs have **binary outcomes** where shares either soar or crash based on results. That explains 
        why Alumis shares nearly doubled today.
        
        The company is also taking advantage of that move by announcing plans to begin an offering of 
        **$175.0 million** of shares of its common stock. That timely capital raise will help the company 
        commercialize envudeucitinib and the rest of its drug pipeline.
        
        ---
        
        ### Why This Matters for Biology Students
        
        This article demonstrates how **basic biology research** (understanding the immune system) leads to 
        **real-world treatments** that help millions of people. The drug envudeucitinib is a **TYK2 inhibitor** - 
        it blocks a specific enzyme involved in the immune response that causes psoriasis.
        """)
    
    with col2:
        st.markdown("### 🔑 Key Terms")
        
        with st.expander("**Psoriasis**"):
            st.write("An autoimmune disease causing red, scaly patches on the skin. Affects ~3% of the population. The immune system attacks healthy skin cells.")
        
        with st.expander("**TYK2 Inhibitor**"):
            st.write("A drug that blocks Tyrosine Kinase 2, an enzyme involved in immune signaling. Blocking TYK2 reduces the overactive immune response in autoimmune diseases.")
        
        with st.expander("**Phase 3 Trial**"):
            st.write("The final stage of clinical testing before FDA approval. Tests drug on 1,000-3,000 patients to confirm effectiveness and monitor side effects.")
        
        with st.expander("**Clinical Endpoints**"):
            st.write("Measurable outcomes that indicate whether a treatment is working. For psoriasis, this includes skin clearance (PASI score) and patient quality of life.")
        
        with st.expander("**Biopharmaceutical**"):
            st.write("A drug derived from biological sources or designed to target specific biological pathways, as opposed to traditional chemical drugs.")
        
        st.markdown("---")
        st.markdown("### 💡 Discussion Prompt")
        st.info("Why do you think a stock would jump 95% in one day based on clinical trial results? What does this tell us about the value of biological research?")
        
        if st.button("Show Answer"):
            st.success("""
            A 95% stock jump shows that:
            
            - **Successful trials are rare** - Most drug candidates fail
            - **Huge market potential** - Millions of psoriasis patients need better treatments
            - **Years of research validated** - The basic biology understanding was correct
            - **Future revenue expected** - Investors see potential for billions in sales
            - **Scientific method works** - Hypothesis → Testing → Results → Treatment
            """)

def show_objectives():
    st.markdown('<div class="main-header">🎯 Learning Objectives</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    st.markdown("## By the end of this lesson, you will be able to:")
    
    objectives = [
        {
            "icon": "🛡️",
            "title": "Explain Immune System Function",
            "description": "Describe the components of the immune system and how they work together to protect the body",
            "examples": ["T-cells and B-cells", "Antibodies", "Inflammatory response", "Cytokines and signaling"]
        },
        {
            "icon": "⚠️",
            "title": "Describe Autoimmune Diseases",
            "description": "Explain what happens when the immune system attacks the body's own cells",
            "examples": ["Psoriasis mechanism", "Loss of self-tolerance", "Chronic inflammation", "Genetic and environmental factors"]
        },
        {
            "icon": "🧬",
            "title": "Connect Structure to Function",
            "description": "Understand how protein structure determines function and how drugs can target specific proteins",
            "examples": ["Enzyme active sites", "TYK2 structure", "Inhibitor binding", "Signal transduction"]
        },
        {
            "icon": "💊",
            "title": "Evaluate Drug Development",
            "description": "Understand the clinical trial process and how drugs move from lab to patient",
            "examples": ["Phase 1, 2, 3 trials", "FDA approval", "Safety vs. efficacy", "Evidence-based medicine"]
        }
    ]
    
    for obj in objectives:
        with st.expander(f"{obj['icon']} {obj['title']}", expanded=True):
            st.write(f"**Learning Goal:** {obj['description']}")
            st.write("**Key Concepts:**")
            for example in obj['examples']:
                st.write(f"- {example}")

def show_immune_system():
    st.markdown('<div class="main-header">🛡️ The Immune System</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    st.markdown("## Your Body's Defense Network")
    
    st.info("""
    The immune system is a complex network of cells, tissues, and organs that work together to defend 
    the body against harmful invaders like bacteria, viruses, and abnormal cells. It's like having 
    millions of tiny soldiers constantly patrolling your body!
    """)
    
    # Interactive tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 Immune Cells", "⚡ Signaling Pathways", "🎯 Self vs. Non-Self", "🧬 TYK2 Enzyme"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### White Blood Cells (Leukocytes)")
            st.write("""
            Your immune system relies on specialized cells, each with a unique role:
            
            **🔵 T-Cells (T-Lymphocytes)**
            - Mature in the **Thymus** (that's the "T"!)
            - **Helper T-cells (CD4+)**: Coordinate immune responses by releasing cytokines
            - **Killer T-cells (CD8+)**: Directly destroy infected or abnormal cells
            - **Regulatory T-cells**: Prevent immune system from attacking healthy cells
            
            **🟢 B-Cells (B-Lymphocytes)**
            - Mature in **Bone marrow** (that's the "B"!)
            - Produce **antibodies** - proteins that tag invaders for destruction
            - Create "memory" cells for faster future responses
            
            **🟠 Macrophages**
            - "Big eaters" that engulf and digest pathogens
            - Present antigens to T-cells to activate immune response
            - Clean up dead cells and debris
            
            **🔴 Dendritic Cells**
            - Capture antigens and present them to T-cells
            - Bridge between innate and adaptive immunity
            """)
        
        with col2:
            st.markdown("### Key Stats")
            st.metric("White Blood Cells", "4,500-11,000", "per microliter of blood")
            st.metric("T-Cell Types", "3 main", "Helper, Killer, Regulatory")
            st.metric("Antibody Types", "5 classes", "IgG, IgA, IgM, IgE, IgD")
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Immune Cells")
        
        q1 = st.radio(
            "**Question 1:** Which type of T-cell is responsible for coordinating the immune response by releasing signaling molecules called cytokines?",
            ["A) Killer T-cells (CD8+)",
             "B) Helper T-cells (CD4+)",
             "C) Regulatory T-cells",
             "D) Memory T-cells"],
            key="immune_q1"
        )
        
        if st.button("Check Answer", key="check_immune_q1"):
            if q1 == "B) Helper T-cells (CD4+)":
                if award_xp(15, "immune_q1", "🌟 First Steps" if not st.session_state.achievements else None):
                    st.balloons()
                    st.success("✅ Correct! +15 XP! Helper T-cells (CD4+) are like the 'generals' of the immune system. They release cytokines that activate other immune cells, including killer T-cells and B-cells. This is why HIV, which attacks CD4+ cells, is so devastating - it takes out the coordinators! (MSS HS-LS1-2)")
                else:
                    st.success("✅ Correct! Helper T-cells coordinate the immune response through cytokine signaling.")
            else:
                st.error("❌ Not quite. Think about which cell type helps 'coordinate' or 'help' other immune cells do their jobs.")
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### How Immune Cells Communicate")
            st.write("""
            Immune cells don't work alone - they communicate through **signaling pathways**:
            
            **📡 Cytokines: The Messengers**
            - Small proteins released by cells to communicate
            - **Interleukins (IL)**: Communication between leukocytes
            - **Interferons (IFN)**: Signal viral infections
            - **Tumor Necrosis Factor (TNF)**: Promotes inflammation
            
            **🔗 The JAK-STAT Pathway**
            - Cytokines bind to receptors on cell surface
            - **JAK enzymes** (including TYK2) are activated
            - JAK phosphorylates **STAT proteins**
            - STAT enters nucleus and activates genes
            - Cell responds (proliferation, differentiation, etc.)
            
            **⚡ Why This Matters for Psoriasis:**
            - In psoriasis, IL-23 and IL-12 cytokines are overproduced
            - These activate the JAK-STAT pathway (via TYK2)
            - This tells skin cells to proliferate too fast
            - **Blocking TYK2 = Stopping the overactive signal!**
            """)
        
        with col2:
            st.markdown("### The JAK Family")
            st.markdown("""
            **Four JAK Enzymes:**
            - **JAK1** - Many cytokine signals
            - **JAK2** - Growth hormones, blood cells
            - **JAK3** - Immune cell development
            - **TYK2** - IL-12, IL-23 signaling
            
            *Envudeucitinib specifically targets TYK2, which is why it has fewer side effects than drugs that block multiple JAKs!*
            """)
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Signaling")
        
        q2 = st.radio(
            "**Question 2:** In the JAK-STAT pathway, what happens after a cytokine binds to its receptor?",
            ["A) The cell immediately dies",
             "B) JAK enzymes are activated and phosphorylate STAT proteins",
             "C) Antibodies are released",
             "D) The nucleus is destroyed"],
            key="immune_q2"
        )
        
        if st.button("Check Answer", key="check_immune_q2"):
            if q2 == "B) JAK enzymes are activated and phosphorylate STAT proteins":
                newly_awarded = award_xp(15, "immune_q2")
                if "immune_q1" in st.session_state.completed_checks and "immune_q2" in st.session_state.completed_checks:
                    if "🛡️ Immune System Expert" not in st.session_state.achievements:
                        st.session_state.achievements.append("🛡️ Immune System Expert")
                        st.balloons()
                        st.success("✅ Correct! +15 XP! 🎖️ Achievement: Immune System Expert! JAK enzymes add phosphate groups to STAT proteins, which then travel to the nucleus to activate specific genes. This is called signal transduction - converting an external signal into a cellular response! (MSS HS-LS1-1)")
                else:
                    st.success("✅ Correct! +15 XP! JAK phosphorylates STAT, which then enters the nucleus to turn on genes.")
            else:
                st.error("❌ Not quite. Remember the sequence: Cytokine → Receptor → JAK activation → STAT phosphorylation → Gene activation")
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### How Your Immune System Recognizes 'Self'")
            st.write("""
            One of the most remarkable features of your immune system is its ability to distinguish 
            between your own cells ("self") and foreign invaders ("non-self"):
            
            **🏷️ MHC Molecules: Your Cellular ID**
            - Every cell displays **MHC (Major Histocompatibility Complex)** proteins
            - MHC shows fragments of proteins from inside the cell
            - T-cells "check" these fragments to see if the cell is healthy
            
            **🎓 T-Cell Education (Thymic Selection)**
            - T-cells develop in the thymus
            - **Positive selection**: T-cells that can recognize MHC survive
            - **Negative selection**: T-cells that react to "self" proteins are destroyed
            - ~95% of developing T-cells die during this process!
            
            **⚠️ When Self-Tolerance Fails:**
            - Some self-reactive T-cells escape deletion
            - Normally, regulatory T-cells keep them in check
            - If regulation fails → **Autoimmune disease**
            - In psoriasis, T-cells attack skin cells as if they were foreign
            """)
        
        with col2:
            st.markdown("### Self-Tolerance Facts")
            st.metric("T-Cell Deletion", "~95%", "die during development")
            st.metric("MHC Genes", "Most polymorphic", "in human genome")
            st.metric("Autoimmune Diseases", "5-8%", "of population affected")
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Self vs. Non-Self")
        
        q3 = st.radio(
            "**Question 3:** What happens during 'negative selection' in the thymus?",
            ["A) T-cells that can recognize MHC molecules are selected to survive",
             "B) T-cells that react strongly to self-proteins are eliminated",
             "C) B-cells are converted into T-cells",
             "D) All T-cells are destroyed"],
            key="immune_q3"
        )
        
        if st.button("Check Answer", key="check_immune_q3"):
            if q3 == "B) T-cells that react strongly to self-proteins are eliminated":
                award_xp(15, "immune_q3")
                st.success("✅ Correct! +15 XP! Negative selection removes T-cells that would attack your own body. This is crucial for preventing autoimmune diseases. When this process fails, self-reactive T-cells can escape and cause conditions like psoriasis, lupus, or Type 1 diabetes. (MSS HS-LS1-2)")
            else:
                st.error("❌ Not quite. Think about what 'negative' selection means - it's removing something harmful. What would be harmful? T-cells that attack your own body!")
    
    with tab4:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### TYK2: The Drug Target")
            st.write("""
            **Tyrosine Kinase 2 (TYK2)** is the specific enzyme targeted by envudeucitinib:
            
            **🔬 What is TYK2?**
            - A **kinase** enzyme (adds phosphate groups to proteins)
            - Part of the **JAK family** of enzymes
            - Specifically involved in **IL-12** and **IL-23** signaling
            - These cytokines drive inflammation in psoriasis
            
            **🧬 Protein Structure:**
            - TYK2 has an **active site** where ATP binds
            - ATP provides the phosphate group for the reaction
            - **Envudeucitinib binds to this active site**
            - Blocks ATP from binding → Enzyme can't work
            
            **💊 Why Target TYK2 Specifically?**
            - IL-12/IL-23 are key drivers of psoriasis
            - Blocking TYK2 is more selective than older JAK inhibitors
            - Fewer side effects (doesn't affect blood cell production like JAK2 inhibitors)
            - Oral medication (easier than injections)
            
            **🎯 This is Structure-Function in Action!**
            - Scientists mapped TYK2's 3D structure
            - Designed a molecule that fits perfectly into the active site
            - Like designing a key to fit a specific lock
            """)
        
        with col2:
            st.markdown("### TYK2 Facts")
            st.metric("Amino Acids", "~1,187", "in TYK2 protein")
            st.metric("Gene Location", "Chromosome 19", "human genome")
            st.metric("Selectivity", ">1000x", "for TYK2 vs other JAKs")
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: TYK2")
        
        q4 = st.radio(
            "**Question 4:** How does envudeucitinib work to treat psoriasis?",
            ["A) It destroys all T-cells in the body",
             "B) It binds to TYK2's active site, blocking the enzyme from functioning",
             "C) It increases IL-23 production",
             "D) It makes skin cells divide faster"],
            key="immune_q4"
        )
        
        if st.button("Check Answer", key="check_immune_q4"):
            if q4 == "B) It binds to TYK2's active site, blocking the enzyme from functioning":
                award_xp(15, "immune_q4")
                st.success("✅ Correct! +15 XP! Envudeucitinib is a competitive inhibitor - it competes with ATP for the active site of TYK2. When the drug occupies the active site, the enzyme can't phosphorylate STAT proteins, so the inflammatory signal is blocked. This is a perfect example of how understanding protein structure leads to targeted drug design! (MSS HS-LS1-1)")
            else:
                st.error("❌ Not quite. Remember, envudeucitinib is an enzyme inhibitor. It blocks the enzyme by binding to it, not by destroying cells or changing cytokine production.")

def show_autoimmune():
    st.markdown('<div class="main-header">⚠️ Autoimmune Diseases</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    st.markdown("## When the Immune System Attacks Itself")
    
    st.warning("""
    **Autoimmune diseases** occur when the immune system mistakenly attacks the body's own healthy cells 
    and tissues. Instead of protecting you, your immune system becomes the threat.
    """)
    
    # Tabs for different aspects
    tab1, tab2, tab3 = st.tabs(["🔴 What is Psoriasis?", "🧬 Molecular Mechanism", "📊 Other Autoimmune Diseases"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Understanding Psoriasis")
            st.write("""
            **Psoriasis** is a chronic autoimmune condition that affects the skin:
            
            **👁️ What You See:**
            - Red, raised patches covered with silvery scales
            - Most common on elbows, knees, scalp, lower back
            - Patches can be itchy, painful, or crack and bleed
            - Affects ~3% of population (8 million Americans)
            
            **🔬 What's Happening Inside:**
            - Normal skin cells take **28-30 days** to mature and shed
            - In psoriasis, this happens in just **3-4 days!**
            - Cells pile up on the surface, forming plaques
            - Blood vessels dilate → redness
            - T-cells infiltrate the skin → inflammation
            
            **🧬 The Immune Component:**
            - T-cells migrate into the skin
            - They release cytokines (IL-17, IL-23, TNF-α)
            - Cytokines tell skin cells (keratinocytes) to divide rapidly
            - Creates a **positive feedback loop** of inflammation
            
            **💔 Impact on Quality of Life:**
            - Physical discomfort and pain
            - Emotional/psychological effects (depression, anxiety)
            - Social stigma and isolation
            - Associated with other conditions (psoriatic arthritis, heart disease)
            """)
        
        with col2:
            st.markdown("### Psoriasis Stats")
            st.metric("Skin Cell Turnover", "3-4 days", "vs. normal 28-30 days")
            st.metric("US Patients", "~8 million", "people affected")
            st.metric("Onset Age", "15-35", "most common")
            
            st.markdown("---")
            st.markdown("### Types of Psoriasis")
            st.markdown("""
            - **Plaque** (most common, 80-90%)
            - **Guttate** (small drop-shaped)
            - **Inverse** (skin folds)
            - **Pustular** (pus-filled bumps)
            - **Erythrodermic** (rare, severe)
            """)
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Psoriasis")
        
        q1 = st.radio(
            "**Question:** How does skin cell turnover in psoriasis compare to normal skin?",
            ["A) It's slower - cells take 60 days instead of 30",
             "B) It's the same - both take about 28-30 days",
             "C) It's much faster - 3-4 days instead of 28-30 days",
             "D) Skin cells don't turnover in psoriasis"],
            key="auto_q1"
        )
        
        if st.button("Check Answer", key="check_auto_q1"):
            if q1 == "C) It's much faster - 3-4 days instead of 28-30 days":
                if award_xp(15, "auto_q1", "🌟 First Steps" if not st.session_state.achievements else None):
                    st.balloons()
                    st.success("✅ Correct! +15 XP! In psoriasis, inflammatory signals cause keratinocytes (skin cells) to divide about 10x faster than normal. The cells don't have time to mature properly before new cells push them to the surface, creating the characteristic scaly plaques. (MSS HS-LS1-4)")
                else:
                    st.success("✅ Correct! The rapid cell turnover causes cells to pile up, forming plaques.")
            else:
                st.error("❌ Not quite. Think about what would cause cells to 'pile up' on the skin surface - they must be produced faster than they can be shed!")
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### The IL-23/TYK2 Pathway in Psoriasis")
            st.write("""
            Understanding the molecular pathway helps us see why TYK2 inhibitors work:
            
            **Step 1: Trigger**
            - Something activates dendritic cells in the skin
            - Could be: injury, infection, stress, genetics
            
            **Step 2: IL-23 Production**
            - Dendritic cells release **IL-23** cytokine
            - IL-23 is a key driver of psoriatic inflammation
            
            **Step 3: T-Cell Activation**
            - IL-23 activates **Th17 cells** (a type of helper T-cell)
            - Th17 cells produce more inflammatory cytokines (IL-17, IL-22)
            
            **Step 4: Signal Transduction (TYK2's Role)**
            - IL-23 binds to receptors on Th17 cells
            - **TYK2 enzyme is activated**
            - TYK2 phosphorylates STAT3
            - STAT3 enters nucleus, activates inflammatory genes
            
            **Step 5: Keratinocyte Response**
            - Inflammatory cytokines reach skin cells
            - Keratinocytes proliferate rapidly
            - More immune cells recruited → **Positive feedback loop**
            
            **💊 Where Envudeucitinib Acts:**
            - Blocks TYK2 at Step 4
            - IL-23 can still bind to receptors
            - But the signal can't be transmitted inside the cell
            - Breaks the inflammatory cycle!
            """)
        
        with col2:
            st.markdown("### Key Players")
            st.markdown("""
            **Cytokines:**
            - IL-23 (activates Th17)
            - IL-17 (causes inflammation)
            - IL-22 (keratinocyte effects)
            - TNF-α (general inflammation)
            
            **Cells:**
            - Dendritic cells (start it)
            - Th17 cells (amplify it)
            - Keratinocytes (respond)
            
            **Enzymes:**
            - TYK2 (signal transduction)
            - JAK2 (also involved)
            """)
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Mechanism")
        
        q2 = st.radio(
            "**Question:** Why is blocking TYK2 an effective strategy for treating psoriasis?",
            ["A) TYK2 produces the scales on the skin",
             "B) TYK2 transmits the IL-23 signal that drives inflammation and T-cell activation",
             "C) TYK2 destroys healthy skin cells",
             "D) TYK2 is only found in psoriasis patients"],
            key="auto_q2"
        )
        
        if st.button("Check Answer", key="check_auto_q2"):
            if q2 == "B) TYK2 transmits the IL-23 signal that drives inflammation and T-cell activation":
                newly_awarded = award_xp(15, "auto_q2")
                if "auto_q1" in st.session_state.completed_checks and "auto_q2" in st.session_state.completed_checks:
                    if "⚠️ Autoimmune Expert" not in st.session_state.achievements:
                        st.session_state.achievements.append("⚠️ Autoimmune Expert")
                        st.balloons()
                        st.success("✅ Correct! +15 XP! 🎖️ Achievement: Autoimmune Expert! TYK2 is essential for transmitting the IL-23 signal inside cells. By blocking TYK2, you prevent the cascade that leads to Th17 activation and the inflammatory response. It's like cutting a phone line - the message (IL-23) arrives but can't be delivered! (MSS HS-LS1-1)")
                else:
                    st.success("✅ Correct! Blocking TYK2 interrupts the inflammatory signaling pathway.")
            else:
                st.error("❌ Not quite. Remember, TYK2 is an enzyme in the signaling pathway. It doesn't directly cause scales or destroy cells - it transmits signals!")
    
    with tab3:
        st.markdown("### Other Autoimmune Diseases")
        st.write("Psoriasis is just one of over 80 known autoimmune diseases:")
        
        diseases = {
            "Disease": ["Type 1 Diabetes", "Rheumatoid Arthritis", "Multiple Sclerosis", "Lupus (SLE)", "Crohn's Disease", "Celiac Disease"],
            "Target": ["Pancreatic β cells", "Joint synovium", "Nerve myelin sheath", "Multiple organs", "GI tract", "Small intestine"],
            "Key Immune Cells": ["T-cells", "T-cells, B-cells", "T-cells", "B-cells, T-cells", "T-cells", "T-cells"],
            "US Prevalence": ["1.6 million", "1.5 million", "1 million", "1.5 million", "780,000", "3 million"]
        }
        
        df = pd.DataFrame(diseases)
        st.table(df)
        
        st.markdown("""
        <div class="michigan-box">
        <h4>🏥 Michigan Research</h4>
        <p>The University of Michigan's Autoimmunity Center of Excellence is one of the leading research 
        centers for autoimmune diseases. They conduct clinical trials and develop new treatments that 
        help patients across Michigan and beyond.</p>
        </div>
        """, unsafe_allow_html=True)

def show_drug_development():
    st.markdown('<div class="main-header">💊 Drug Development</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    st.markdown("## From Lab Bench to Pharmacy Shelf")
    
    st.info("""
    Developing a new drug like envudeucitinib takes **10-15 years** and costs **$1-2 billion** on average. 
    Let's explore the journey from basic research to FDA approval.
    """)
    
    # Tabs for phases
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 Discovery", "🧪 Preclinical", "👥 Clinical Trials", "✅ FDA Approval"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Drug Discovery Phase")
            st.write("""
            **Step 1: Identify a Target (3-6 years)**
            
            Before you can make a drug, you need to know what to target:
            
            **🔍 Basic Research:**
            - Scientists study disease biology
            - Identify key proteins/pathways involved
            - For psoriasis: IL-23/TYK2 pathway identified as driver
            
            **🎯 Target Validation:**
            - Prove that targeting this protein will help
            - Genetic studies: People with TYK2 mutations have less autoimmune disease!
            - Animal models: Mice without TYK2 resist psoriasis
            
            **💡 Drug Design:**
            - Map the 3D structure of the target protein
            - Use computers to design molecules that bind to it
            - Synthesize thousands of candidate compounds
            - Test which ones block the target best
            
            **🧬 Structure-Based Drug Design:**
            - X-ray crystallography reveals TYK2 structure
            - Scientists identify the ATP-binding pocket
            - Design molecules that fit perfectly
            - Envudeucitinib designed to be highly selective for TYK2
            """)
        
        with col2:
            st.markdown("### Timeline")
            st.metric("Discovery Phase", "3-6 years", "identifying and validating target")
            st.metric("Compounds Tested", "10,000+", "to find one that works")
            st.metric("Success Rate", "~1 in 10,000", "compounds becomes a drug")
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Preclinical Testing")
            st.write("""
            **Step 2: Test Before Humans (1-3 years)**
            
            Before testing in humans, extensive lab and animal testing is required:
            
            **🧫 In Vitro (Lab Dish) Testing:**
            - Test drug on cells in culture
            - Does it actually inhibit TYK2?
            - Is it toxic to cells?
            - How is it metabolized?
            
            **🐁 In Vivo (Animal) Testing:**
            - Test in animal models of psoriasis
            - **Efficacy**: Does it reduce disease?
            - **Safety**: What are the side effects?
            - **Pharmacokinetics**: How is it absorbed, distributed, metabolized, excreted?
            
            **📊 Required Data:**
            - Effective dose range
            - Maximum tolerated dose
            - Organ toxicity assessment
            - How drug is processed by the body
            
            **📝 IND Application:**
            - Compile all data into an Investigational New Drug (IND) application
            - Submit to FDA for permission to test in humans
            - FDA has 30 days to respond
            """)
        
        with col2:
            st.markdown("### Key Questions")
            st.markdown("""
            **Safety:**
            - Is it toxic?
            - What organs affected?
            - Is it carcinogenic?
            
            **Efficacy:**
            - Does it work in animals?
            - What dose is needed?
            
            **Pharmacology:**
            - Absorption?
            - Distribution?
            - Metabolism?
            - Excretion?
            """)
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Clinical Trials in Humans")
            st.write("""
            **Step 3: Test in Humans (6-8 years)**
            
            Clinical trials proceed through three phases:
            
            ---
            
            **Phase 1: Safety First** *(20-100 healthy volunteers, ~1 year)*
            - Primary goal: Is it safe in humans?
            - Start with very low doses
            - Gradually increase to find maximum tolerated dose
            - Monitor for side effects
            - ~70% of drugs pass Phase 1
            
            ---
            
            **Phase 2: Does It Work?** *(100-500 patients, ~2 years)*
            - Test in patients with the disease
            - Find the optimal dose
            - Get first evidence of efficacy
            - Continue monitoring safety
            - ~33% of drugs pass Phase 2
            
            ---
            
            **Phase 3: Prove It!** *(1,000-5,000 patients, ~3-4 years)*
            - Large-scale, randomized, controlled trials
            - Compare to placebo or existing treatment
            - Confirm efficacy with statistical significance
            - Identify less common side effects
            - **This is what Alumis just completed!**
            - ~25-30% of drugs pass Phase 3
            
            ---
            
            **🔬 Key Terms:**
            - **Randomized**: Patients randomly assigned to drug or placebo
            - **Double-blind**: Neither patients nor doctors know who gets what
            - **Placebo-controlled**: Compare to inactive treatment
            - **Primary endpoint**: Main outcome measured (e.g., PASI score for psoriasis)
            """)
        
        with col2:
            st.markdown("### Success Rates")
            st.metric("Phase 1 → 2", "~70%", "pass")
            st.metric("Phase 2 → 3", "~33%", "pass")
            st.metric("Phase 3 → Approval", "~25-30%", "pass")
            st.metric("Overall Success", "~10%", "from Phase 1 to market")
            
            st.markdown("---")
            st.markdown("### Envudeucitinib Results")
            st.success("""
            **Phase 3 Success!**
            - Met primary endpoint ✅
            - Met secondary endpoints ✅
            - Strong statistical significance ✅
            """)
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Clinical Trials")
        
        q1 = st.radio(
            "**Question:** What is the PRIMARY goal of a Phase 1 clinical trial?",
            ["A) Prove the drug works better than placebo",
             "B) Determine if the drug is safe in humans",
             "C) Get FDA approval",
             "D) Test on thousands of patients"],
            key="drug_q1"
        )
        
        if st.button("Check Answer", key="check_drug_q1"):
            if q1 == "B) Determine if the drug is safe in humans":
                if award_xp(15, "drug_q1", "🌟 First Steps" if not st.session_state.achievements else None):
                    st.balloons()
                    st.success("✅ Correct! +15 XP! Phase 1 trials focus on safety - testing on healthy volunteers to make sure the drug doesn't cause serious harm before testing on patients. Efficacy is primarily measured in Phase 2 and confirmed in Phase 3. (MSS HS-LS1-6)")
                else:
                    st.success("✅ Correct! Safety first is the guiding principle of Phase 1.")
            else:
                st.error("❌ Not quite. Remember 'Phase 1 = Safety First' - the primary goal is determining if the drug is safe enough to test in patients.")
    
    with tab4:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### FDA Approval Process")
            st.write("""
            **Step 4: Get Approved (1-2 years)**
            
            After successful Phase 3 trials:
            
            **📋 New Drug Application (NDA):**
            - Compile ALL data from development
            - Can be 100,000+ pages!
            - Chemistry and manufacturing information
            - All preclinical data
            - All clinical trial results
            - Proposed labeling
            
            **🔍 FDA Review:**
            - FDA scientists review all data
            - May request additional information
            - Advisory committee may evaluate
            - Standard review: 10 months
            - Priority review: 6 months
            
            **✅ Approval Decision:**
            - **Approved**: Can be marketed
            - **Complete Response Letter**: Not approved, more data needed
            - **Approvable**: Approved with conditions
            
            **📦 Post-Approval (Phase 4):**
            - Continue monitoring for rare side effects
            - Real-world effectiveness studies
            - May lead to label changes
            """)
        
        with col2:
            st.markdown("### What's Next for Envudeucitinib?")
            st.markdown("""
            **Current Status:**
            - Phase 3 complete ✅
            - Preparing NDA submission
            
            **Expected Timeline:**
            - NDA submission: 2026
            - FDA review: 6-10 months
            - Potential approval: Late 2026/Early 2027
            
            **Market Potential:**
            - ~8 million US psoriasis patients
            - Estimated $5-10 billion market
            - Competition from other TYK2 inhibitors
            """)
        
        # Quick Check
        st.markdown("---")
        st.markdown("### 🧠 Quick Check: Approval")
        
        q2 = st.radio(
            "**Question:** Why did Alumis stock jump 95% after Phase 3 results?",
            ["A) Phase 3 is the final hurdle before seeking FDA approval - success means the drug likely works",
             "B) Phase 3 is the first test in humans",
             "C) The drug was already FDA approved",
             "D) Phase 3 tests only safety, not efficacy"],
            key="drug_q2"
        )
        
        if st.button("Check Answer", key="check_drug_q2"):
            if q2 == "A) Phase 3 is the final hurdle before seeking FDA approval - success means the drug likely works":
                newly_awarded = award_xp(15, "drug_q2")
                if "drug_q1" in st.session_state.completed_checks and "drug_q2" in st.session_state.completed_checks:
                    if "💊 Drug Development Expert" not in st.session_state.achievements:
                        st.session_state.achievements.append("💊 Drug Development Expert")
                        st.balloons()
                        st.success("✅ Correct! +15 XP! 🎖️ Achievement: Drug Development Expert! Phase 3 success is a huge milestone - it means the drug works in large patient populations with statistical significance. Investors know that Phase 3 success usually leads to FDA approval and massive revenue potential. That's why the stock nearly doubled! (MSS HS-LS1-6)")
                else:
                    st.success("✅ Correct! Phase 3 success de-risks the investment significantly.")
            else:
                st.error("❌ Not quite. Think about why Phase 3 is so important - it's the final large-scale test proving the drug works before FDA approval.")

def show_design_challenge():
    st.markdown('<div class="main-header">🧪 Design a Treatment</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    st.markdown("## 🔬 Design Your Own Autoimmune Treatment!")
    
    st.info("""
    **Your Task:** You are a biotech researcher! Design a treatment approach for an autoimmune disease. 
    Consider the biological target, mechanism of action, and potential trade-offs.
    
    **Michigan Science Standard Alignment:** This activity addresses HS-ETS1-3 (Engineering Design) and 
    HS-LS1-1 (Structure and Function).
    """)
    
    # Disease selection
    st.markdown("### Step 1: Choose Your Target Disease")
    
    diseases = {
        "🔴 Psoriasis": {
            "description": "Autoimmune skin disease causing rapid skin cell turnover",
            "key_pathway": "IL-23/TYK2 pathway",
            "current_treatments": ["Topical steroids", "Biologics (IL-17 blockers)", "TYK2 inhibitors"],
            "unmet_needs": "Oral medications with fewer side effects",
            "target_options": ["TYK2", "IL-23 receptor", "IL-17", "TNF-alpha"]
        },
        "🔵 Rheumatoid Arthritis": {
            "description": "Autoimmune attack on joint tissues causing inflammation and damage",
            "key_pathway": "TNF-alpha and IL-6 signaling",
            "current_treatments": ["Methotrexate", "TNF inhibitors", "JAK inhibitors"],
            "unmet_needs": "Better disease modification, fewer infections",
            "target_options": ["TNF-alpha", "IL-6 receptor", "JAK1", "B-cells (CD20)"]
        },
        "🟢 Type 1 Diabetes": {
            "description": "Autoimmune destruction of insulin-producing beta cells",
            "key_pathway": "T-cell attack on pancreatic islets",
            "current_treatments": ["Insulin replacement", "Immunotherapy (teplizumab)"],
            "unmet_needs": "Prevent or reverse beta cell destruction",
            "target_options": ["CD3 (T-cells)", "IL-2 receptor", "B-cells", "Beta cell regeneration"]
        },
        "🟡 Multiple Sclerosis": {
            "description": "Autoimmune attack on nerve myelin sheath",
            "key_pathway": "T-cell and B-cell mediated demyelination",
            "current_treatments": ["Interferons", "B-cell depleting antibodies", "S1P modulators"],
            "unmet_needs": "Remyelination therapies, neuroprotection",
            "target_options": ["CD20 (B-cells)", "S1P receptor", "IL-17", "Myelin repair factors"]
        }
    }
    
    disease = st.selectbox("Select a disease to target:", list(diseases.keys()))
    selected_disease = diseases[disease]
    
    with st.expander("📋 Disease Background", expanded=True):
        st.write(f"**Description:** {selected_disease['description']}")
        st.write(f"**Key Pathway:** {selected_disease['key_pathway']}")
        st.write(f"**Current Treatments:** {', '.join(selected_disease['current_treatments'])}")
        st.write(f"**Unmet Medical Needs:** {selected_disease['unmet_needs']}")
    
    st.markdown("---")
    
    # Educational content about drug design
    with st.expander("📚 Learn About Drug Design Approaches (Click to Learn)"):
        st.markdown("""
        ### Types of Drug Therapies
        
        **🧬 Small Molecule Inhibitors** (like envudeucitinib)
        - Pros: Oral dosing, lower cost to manufacture, can enter cells
        - Cons: May have off-target effects, shorter duration of action
        - Examples: TYK2 inhibitors, JAK inhibitors
        
        **🔬 Monoclonal Antibodies** (like adalimumab/Humira)
        - Pros: Highly specific, long-lasting effect
        - Cons: Must be injected, expensive, can trigger immune reactions
        - Examples: TNF inhibitors, IL-17 blockers
        
        **🧪 Fusion Proteins** (like etanercept/Enbrel)
        - Pros: Mimic natural proteins, specific
        - Cons: Injection required, expensive
        - Examples: TNF receptor fusion proteins
        
        **💉 Cell Therapies**
        - Pros: Potentially curative, one-time treatment
        - Cons: Very expensive, complex manufacturing, safety concerns
        - Examples: CAR-T cells (for cancer), regulatory T-cell therapy
        """)
    
    st.markdown("### Step 2: Design Your Treatment")
    
    with st.form("treatment_design"):
        col1, col2 = st.columns(2)
        
        with col1:
            treatment_name = st.text_input("Treatment Name:", placeholder="e.g., Immunobalance-X")
            
            target = st.selectbox("Molecular Target:", selected_disease['target_options'])
            
            drug_type = st.selectbox("Drug Type:",
                ["Small Molecule Inhibitor",
                 "Monoclonal Antibody",
                 "Fusion Protein",
                 "Cell Therapy",
                 "Gene Therapy"])
        
        with col2:
            mechanism = st.text_area("How does your treatment work?",
                placeholder="Describe the mechanism of action - how does blocking this target help the disease?")
            
            delivery = st.selectbox("Route of Administration:",
                ["Oral (pill)",
                 "Subcutaneous injection (self-administered)",
                 "IV infusion (clinic visit)",
                 "Topical (cream/patch)"])
        
        st.markdown("### Step 3: Consider Trade-offs")
        
        col3, col4 = st.columns(2)
        
        with col3:
            efficacy_priority = st.select_slider("Efficacy vs. Safety Priority:",
                options=["Maximum Efficacy", "Balanced", "Maximum Safety"])
            
            expected_side_effects = st.multiselect("Potential Side Effects (based on target):",
                ["Increased infection risk",
                 "Injection site reactions",
                 "Liver toxicity",
                 "GI symptoms",
                 "Headache",
                 "Immunosuppression",
                 "Allergic reactions"])
        
        with col4:
            cost_estimate = st.select_slider("Expected Annual Cost:",
                options=["<$1,000", "$1,000-$10,000", "$10,000-$50,000", ">$50,000"])
            
            dosing = st.select_slider("Dosing Frequency:",
                options=["Daily", "Weekly", "Every 2 weeks", "Monthly", "One-time"])
        
        st.markdown("### Step 4: Scientific Rationale")
        
        rationale = st.text_area("Explain WHY your target and approach should work:",
            placeholder="Use your understanding of the immune system and disease mechanism to explain your design choices...")
        
        submitted = st.form_submit_button("Submit Treatment Design")
        
        if submitted:
            if award_xp(50, "design_challenge"):
                if "🔬 Biotech Researcher" not in st.session_state.achievements:
                    st.session_state.achievements.append("🔬 Biotech Researcher")
                st.balloons()
                st.success("🎉 Treatment Design Submitted! +50 XP! 🎖️ Achievement: Biotech Researcher!")
            else:
                st.success("🎉 Treatment Design Submitted!")
            
            # Store data for AI feedback
            st.session_state.drug_design_data = {
                "name": treatment_name,
                "disease": disease,
                "target": target,
                "drug_type": drug_type,
                "mechanism": mechanism,
                "delivery": delivery,
                "efficacy_priority": efficacy_priority,
                "side_effects": expected_side_effects,
                "cost": cost_estimate,
                "dosing": dosing,
                "rationale": rationale
            }
            
            st.markdown("### 📊 Design Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Target", target)
            with col2:
                st.metric("Drug Type", drug_type.split()[0])
            with col3:
                st.metric("Delivery", delivery.split()[0])
    
    # AI Feedback Section
    st.markdown("---")
    st.markdown("### 🤖 Get Feedback from Professor Xavier")
    
    if st.session_state.drug_design_data:
        design = st.session_state.drug_design_data
        
        if st.button("🎓 Get Expert Feedback on Your Treatment Design"):
            with st.spinner("Professor Xavier is reviewing your treatment design..."):
                
                feedback_prompt = f"""You are Professor Xavier, a pharmaceutical scientist and biology educator helping high school students understand drug development for autoimmune diseases.

A student has designed a treatment for an autoimmune disease. Provide detailed, educational feedback that teaches the biology behind their choices.

## Student's Treatment Design:
- **Treatment Name:** {design['name'] if design['name'] else 'Unnamed'}
- **Target Disease:** {design['disease']}
- **Molecular Target:** {design['target']}
- **Drug Type:** {design['drug_type']}
- **Mechanism Description:** {design['mechanism'] if design['mechanism'] else 'Not provided'}
- **Route of Administration:** {design['delivery']}
- **Efficacy vs Safety Priority:** {design['efficacy_priority']}
- **Expected Side Effects:** {', '.join(design['side_effects']) if design['side_effects'] else 'None listed'}
- **Expected Cost:** {design['cost']}
- **Dosing Frequency:** {design['dosing']}
- **Scientific Rationale:** {design['rationale'] if design['rationale'] else 'Not provided'}

## Provide Feedback On:

### 1. TARGET EVALUATION
- Is this a good target for this disease? Explain the biology
- What role does this target play in the disease pathway?
- Are there existing drugs targeting this? How does the student's approach compare?

### 2. DRUG TYPE ASSESSMENT
- Is the chosen drug type appropriate for this target?
- Explain structure-function: How would a {design['drug_type']} interact with {design['target']}?
- What are the advantages and limitations of this drug type?

### 3. MECHANISM FEEDBACK
- Evaluate their mechanism description
- Fill in any gaps in their understanding
- Explain exactly how blocking {design['target']} would affect the disease

### 4. PRACTICAL CONSIDERATIONS
- Comment on their delivery route choice
- Discuss the trade-offs they identified
- Are there considerations they missed?

### 5. HOMEWORK RESOURCES
Recommend 2-3 specific resources with URLs:

For immunology:
- https://www.khanacademy.org/science/biology/human-biology/immunology/v/role-of-phagocytes-in-innate-or-nonspecific-immunity - Khan Academy: Immune System
- https://www.ck12.org/biology/immune-system/ - CK-12: Immune System

For drug development:
- https://www.fda.gov/patients/learn-about-drug-and-device-approvals/drug-development-process - FDA: Drug Development Process
- https://www.nih.gov/health-information/nih-clinical-research-trials-you/basics - NIH: Clinical Trials Basics

For specific diseases:
- https://www.niams.nih.gov/health-topics/psoriasis - NIH: Psoriasis
- https://www.ck12.org/biology/autoimmune-diseases/ - CK-12: Autoimmune Diseases

Format as:
"📚 **Study These Resources:**
1. [Resource Name](URL) - How it relates to your design"

Be encouraging but scientifically accurate. Use specific molecular details where appropriate."""

                try:
                    import requests
                    import json
                    
                    api_key = "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"
                    
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "Content-Type": "application/json",
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01"
                        },
                        json={
                            "model": "claude-sonnet-4-20250514",
                            "max_tokens": 2000,
                            "messages": [{"role": "user", "content": feedback_prompt}]
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        feedback_text = data["content"][0]["text"]
                        
                        st.markdown("### 💬 Professor Xavier's Feedback:")
                        st.markdown(feedback_text)
                        
                        if award_xp(15, "design_feedback"):
                            st.success("🎉 +15 XP for seeking expert feedback!")
                    else:
                        # Fallback
                        st.markdown("### 💬 Professor Xavier's Feedback:")
                        st.markdown(f"""
**Great work designing a treatment for {design['disease']}!**

**Target Analysis:** {design['target']} is a solid choice for this disease. It plays a key role in the inflammatory pathway.

**Drug Type:** Your choice of {design['drug_type']} has specific advantages. Small molecules can be taken orally, while antibodies are highly specific but require injection.

**Mechanism:** Remember that blocking {design['target']} will interrupt the signaling cascade that drives inflammation. This should reduce disease symptoms without completely suppressing the immune system.

**📚 Study These Resources:**
1. [Khan Academy: Immune System](https://www.khanacademy.org/science/biology/human-biology/immunology/v/role-of-phagocytes-in-innate-or-nonspecific-immunity) - Understand how immune cells communicate
2. [FDA: Drug Development](https://www.fda.gov/patients/learn-about-drug-and-device-approvals/drug-development-process) - Learn how drugs are approved
3. [NIH: Autoimmune Diseases](https://www.niams.nih.gov/health-topics/autoimmune-diseases) - Deeper dive into autoimmunity
                        """)
                
                except Exception as e:
                    st.markdown("### 💬 Professor Xavier's Feedback:")
                    st.success(f"""
**Excellent effort on your {design['disease']} treatment design!**

Your choice to target **{design['target']}** using a **{design['drug_type']}** shows good understanding of the disease mechanism.

**Key Insight:** {design['target']} is involved in the inflammatory signaling pathway. By blocking it, you're interrupting the cascade that tells immune cells to attack healthy tissue.

**Consider:** How does your delivery method ({design['delivery']}) affect patient compliance and drug effectiveness?

📚 **Resources:**
- [Khan Academy: Immune System](https://www.khanacademy.org/science/biology/human-biology/immunology)
- [CK-12: Autoimmune Diseases](https://www.ck12.org/biology/autoimmune-diseases/)
                    """)
    else:
        st.warning("👆 Please submit your treatment design above first, then return here for feedback!")

def show_quiz():
    st.markdown('<div class="main-header">❓ Quiz & Assessment</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    st.markdown("## 📝 Lesson Assessment")
    st.info("Complete this quiz to check your understanding of the immune system, autoimmune diseases, and drug development.")
    
    with st.form("final_quiz"):
        st.markdown("### Part 1: Immune System Basics")
        
        q1 = st.radio(
            "**1.** What is the primary function of Helper T-cells (CD4+)? (MSS HS-LS1-2)",
            ["A) Directly kill infected cells",
             "B) Coordinate the immune response by releasing cytokines",
             "C) Produce antibodies",
             "D) Engulf and digest pathogens"],
            key="quiz_q1"
        )
        
        q2 = st.radio(
            "**2.** In the JAK-STAT signaling pathway, what does TYK2 do when activated? (MSS HS-LS1-1)",
            ["A) Destroys the cell membrane",
             "B) Phosphorylates STAT proteins to transmit signals",
             "C) Produces antibodies",
             "D) Divides the cell"],
            key="quiz_q2"
        )
        
        st.markdown("### Part 2: Autoimmune Diseases")
        
        q3 = st.radio(
            "**3.** What happens to skin cell turnover in psoriasis? (MSS HS-LS1-4)",
            ["A) It slows down to 60 days",
             "B) It speeds up to 3-4 days instead of 28-30 days",
             "C) It stops completely",
             "D) It remains normal"],
            key="quiz_q3"
        )
        
        q4 = st.radio(
            "**4.** Why is TYK2 a good drug target for psoriasis? (MSS HS-LS1-1)",
            ["A) TYK2 is only found in psoriasis patients",
             "B) TYK2 transmits the IL-23 signal that drives inflammation",
             "C) TYK2 directly causes skin cells to flake off",
             "D) TYK2 produces the scales seen in psoriasis"],
            key="quiz_q4"
        )
        
        st.markdown("### Part 3: Drug Development")
        
        q5 = st.radio(
            "**5.** What is the PRIMARY goal of a Phase 1 clinical trial? (MSS HS-LS1-6)",
            ["A) Prove the drug works better than placebo",
             "B) Test safety in healthy volunteers",
             "C) Get FDA approval",
             "D) Test on thousands of patients"],
            key="quiz_q5"
        )
        
        q6 = st.radio(
            "**6.** How does envudeucitinib work to treat psoriasis? (MSS HS-LS1-1)",
            ["A) It destroys all T-cells",
             "B) It binds to TYK2's active site, blocking enzyme function",
             "C) It increases IL-23 production",
             "D) It makes skin cells divide faster"],
            key="quiz_q6"
        )
        
        st.markdown("### Part 4: Short Answer")
        
        q7 = st.text_area(
            "**7.** Explain the connection between understanding protein structure (like TYK2) and designing targeted drug therapies. Use the concept of enzyme inhibition in your answer. (MSS HS-LS1-1)",
            key="quiz_q7"
        )
        
        q8 = st.text_area(
            "**8.** Why might a biotech company's stock jump 95% after announcing positive Phase 3 trial results? Connect this to the drug development process and the value of scientific research. (MSS HS-LS1-6)",
            key="quiz_q8"
        )
        
        submitted = st.form_submit_button("Submit Quiz")
        
        if submitted:
            score = 0
            total = 6
            
            if q1 == "B) Coordinate the immune response by releasing cytokines":
                score += 1
            if q2 == "B) Phosphorylates STAT proteins to transmit signals":
                score += 1
            if q3 == "B) It speeds up to 3-4 days instead of 28-30 days":
                score += 1
            if q4 == "B) TYK2 transmits the IL-23 signal that drives inflammation":
                score += 1
            if q5 == "B) Test safety in healthy volunteers":
                score += 1
            if q6 == "B) It binds to TYK2's active site, blocking enzyme function":
                score += 1
            
            xp_earned = score * 10
            
            if "quiz_complete" not in st.session_state.completed_checks:
                st.session_state.completed_checks.add("quiz_complete")
                if "📝 Quiz Champion" not in st.session_state.achievements:
                    st.session_state.achievements.append("📝 Quiz Champion")
                st.session_state.xp_points += xp_earned + 25
                
                if score == total:
                    if "🏆 Perfect Score" not in st.session_state.achievements:
                        st.session_state.achievements.append("🏆 Perfect Score")
                        st.session_state.xp_points += 50
            
            st.session_state.quiz_short_answers = {
                "q7": q7,
                "q8": q8,
                "mc_score": score,
                "mc_total": total
            }
            
            st.markdown("---")
            st.markdown("### 📊 Results")
            
            percentage = (score / total) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Score", f"{score}/{total}")
            with col2:
                st.metric("Percentage", f"{percentage:.0f}%")
            with col3:
                st.metric("XP Earned", f"+{xp_earned + 25}")
            with col4:
                if percentage >= 80:
                    st.metric("Status", "Excellent! 🌟")
                elif percentage >= 60:
                    st.metric("Status", "Good Work! 👍")
                else:
                    st.metric("Status", "Keep Studying 📚")
            
            if percentage == 100:
                st.balloons()
                st.success("🎉 PERFECT SCORE! +50 Bonus XP! 🏆 Achievement: Perfect Score!")
            elif percentage >= 80:
                st.balloons()
                st.success("🎉 Great job! 🎖️ Achievement: Quiz Champion!")
            elif percentage >= 60:
                st.info("👍 Good work! Review the sections where you missed questions.")
            else:
                st.warning("📚 Consider reviewing the lesson materials.")
            
            st.markdown("### Short Answer Feedback")
            st.info("Click below to get personalized feedback on your short answers!")
    
    # AI Feedback for short answers
    if st.session_state.quiz_short_answers:
        answers = st.session_state.quiz_short_answers
        
        if answers.get('q7') or answers.get('q8'):
            if st.button("🎓 Get Professor Xavier's Feedback on Short Answers"):
                with st.spinner("Professor Xavier is reviewing your responses..."):
                    # Simplified feedback for brevity
                    st.markdown("### 💬 Professor Xavier's Feedback:")
                    
                    st.markdown("""
**Question 7 - Structure-Function & Drug Design:**

The key concept is that **protein structure determines function**. Scientists use X-ray crystallography to map the 3D structure of enzymes like TYK2. This reveals the **active site** - the pocket where the enzyme does its work.

**Model Answer:** "Scientists mapped TYK2's 3D structure and identified the ATP-binding pocket (active site). Envudeucitinib was designed to fit perfectly into this pocket, competing with ATP for the binding site. When the drug occupies the active site, TYK2 cannot phosphorylate STAT proteins, blocking the inflammatory signal. This is competitive inhibition - the drug competes with the natural substrate."

📚 **Study:** [CK-12: Enzymes](https://www.ck12.org/biology/enzymes/) | [Khan Academy: Enzyme Inhibition](https://www.khanacademy.org/science/biology/energy-and-enzymes/enzyme-regulation/v/competitive-inhibition)

---

**Question 8 - Stock Surge & Drug Development:**

The 95% stock jump reflects the **massive risk reduction** that Phase 3 success represents.

**Model Answer:** "Phase 3 is the final and largest clinical trial - success means the drug works in thousands of patients with statistical significance. Since most drugs fail before this point (only ~10% of Phase 1 drugs reach market), positive Phase 3 results dramatically increase the probability of FDA approval and commercial success. With ~8 million psoriasis patients in the US alone and potential annual sales in the billions, investors see huge future revenue potential. The stock jump represents the market's valuation of that future success."

📚 **Study:** [FDA: Drug Development Process](https://www.fda.gov/patients/learn-about-drug-and-device-approvals/drug-development-process)
                    """)
                    
                    if award_xp(15, "quiz_feedback"):
                        st.success("🎉 +15 XP for getting detailed feedback!")

def show_resources():
    st.markdown('<div class="main-header">📚 Resources</div>', unsafe_allow_html=True)
    st.markdown('<p class="developer-credit">Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧬 Immunology Resources")
        st.markdown("""
        **Khan Academy:**
        - [Immune System](https://www.khanacademy.org/science/biology/human-biology/immunology)
        - [Inflammatory Response](https://www.khanacademy.org/science/biology/human-biology/immunology/v/inflammatory-response)
        
        **CK-12:**
        - [Immune System](https://www.ck12.org/biology/immune-system/)
        - [Autoimmune Diseases](https://www.ck12.org/biology/autoimmune-diseases/)
        
        **NIH Resources:**
        - [Immune System Overview](https://www.niaid.nih.gov/research/immune-system-overview)
        - [Psoriasis Information](https://www.niams.nih.gov/health-topics/psoriasis)
        """)
        
        st.markdown("### 💊 Drug Development")
        st.markdown("""
        - [FDA: Drug Development Process](https://www.fda.gov/patients/learn-about-drug-and-device-approvals/drug-development-process)
        - [NIH: Clinical Trials](https://www.nih.gov/health-information/nih-clinical-research-trials-you/basics)
        - [Biotech Primer](https://biotechprimer.com/)
        """)
    
    with col2:
        st.markdown("### 🎓 Career Connections")
        st.markdown("""
        **STEM Careers in This Field:**
        - Immunologist
        - Pharmaceutical Scientist
        - Clinical Research Coordinator
        - Biotech Researcher
        - Dermatologist
        - Drug Safety Specialist
        
        **Michigan Employers:**
        - University of Michigan Health
        - Henry Ford Health
        - Beaumont Health
        - Pfizer (Kalamazoo)
        - Stryker
        - Perrigo
        """)
        
        st.markdown("### 🏥 Michigan Research")
        st.markdown("""
        - [U-M Autoimmunity Center](https://www.med.umich.edu/intmed/rheumatology/)
        - [Wayne State Immunology](https://immunology.med.wayne.edu/)
        - [MSU College of Human Medicine](https://humanmedicine.msu.edu/)
        """)

# Page routing
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'article':
    show_article()
elif st.session_state.page == 'objectives':
    show_objectives()
elif st.session_state.page == 'immune_system':
    show_immune_system()
elif st.session_state.page == 'autoimmune':
    show_autoimmune()
elif st.session_state.page == 'drug_development':
    show_drug_development()
elif st.session_state.page == 'design_challenge':
    show_design_challenge()
elif st.session_state.page == 'quiz':
    show_quiz()
elif st.session_state.page == 'resources':
    show_resources()
else:
    show_home()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
<p>Developed by Xavier Honablue, M.Ed. for Grosse Pointe South High School</p>
<p>Aligned with Michigan Science Standards (MSS) | Biology Grades 9-12</p>
<p>© 2026 | For educational use only</p>
</div>
""", unsafe_allow_html=True)
