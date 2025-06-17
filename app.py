import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Real Estate Agent Decoder",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .tagline {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #d32f2f;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title and tagline
st.markdown('<h1 class="main-header">🏠 Real Estate Agent Decoder</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Uncover hidden costs and conflicts of interest in your real estate transaction</p>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #d32f2f;">Don\'t Get Sold - Get Decoded</h3>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏠 Navigation")
main_tool = st.sidebar.selectbox(
    "Choose a Tool:",
    ["Quick Start", "Document Analysis", "Commission Calculator", "Conflict Checker", 
     "Agent Compensation Database", "Realtor-Speak Decoder", "Sales Tactic Decoder", 
     "Contract Decoder", "Meeting Prep Tool"]
)

# Sub-navigation based on main tool selection
if main_tool != "Quick Start":
    st.sidebar.markdown("---")
    sub_tool = st.sidebar.selectbox(
        "Choose Sub-Tool:",
        ["Overview", "Psychological Tactics", "What They Said", "Fee Terms Glossary", 
         "Psychology", "Scripts", "Defense", "Red Flag Checker", "Killer Questions"]
    )

# Data for the app
realtor_speak = {
    "Priced to sell": "This property may be overpriced for the market, and the agent is trying to create urgency.",
    "Seller is motivated": "The seller may be desperate, which could mean negotiation opportunities for you.",
    "This won't last long": "Creating false urgency to prevent you from shopping around or negotiating.",
    "Other buyers are interested": "Often a lie to create competition and rush your decision.",
    "The market is really hot": "Trying to justify high prices and discourage negotiation.",
    "You need to make an offer today": "High-pressure tactic to prevent you from doing due diligence.",
    "Don't worry about the inspection": "Agent wants to avoid delays or deal-killing discoveries.",
    "We should go in strong": "May result in you overpaying when a lower offer could work.",
    "This is a great investment": "Deflecting from the home's suitability as a place to live.",
    "The seller won't negotiate": "Often untrue - most sellers will negotiate to some degree.",
    "You can always refinance later": "Encouraging you to accept bad loan terms now.",
    "This is the best we can do": "Agents almost always have more room to negotiate."
}

psychological_tactics = {
    "Urgency": {
        "Description": "Creating false time pressure to rush decisions",
        "Examples": ["Other buyers looking", "Price going up tomorrow", "Only showing today"],
        "Defense": "Always take time to think. Real opportunities don't disappear in hours."
    },
    "Scarcity": {
        "Description": "Making the property seem rare or unique when it's not",
        "Examples": ["Last house in the neighborhood", "Rare find", "One of a kind"],
        "Defense": "Research comparable properties. Most homes have similar alternatives."
    },
    "Social Proof": {
        "Description": "Using others' behavior to influence your decisions",
        "Examples": ["Everyone else is bidding", "All my clients love this area", "Most buyers choose this"],
        "Defense": "Make decisions based on your needs, not what others supposedly do."
    },
    "Authority": {
        "Description": "Using their experience/credentials to shut down questions",
        "Examples": ["Trust me, I've been doing this 20 years", "As a professional...", "You should listen to me"],
        "Defense": "Your questions are valid regardless of their experience."
    }
}

red_flags = [
    "Pressure to sign immediately without reading",
    "Reluctance to explain commission structure",
    "Discouraging you from getting inspections",
    "Pushing you toward their preferred lender/attorney",
    "Not disclosing dual agency relationships",
    "Showing only overpriced properties",
    "Avoiding your questions about market analysis",
    "Rushing through contract details",
    "Discouraging you from bringing representation",
    "Not providing comparable sales data"
]

killer_questions = [
    "What is your exact commission rate and who pays it?",
    "Are you representing both buyer and seller in this transaction?",
    "How many days has this property been on the market?",
    "What were the last 5 comparable sales in this area?",
    "What problems were found in the last inspection that fell through?",
    "How much below asking price have you accepted in the last 6 months?",
    "What referral fees do you receive from lenders/inspectors you recommend?",
    "What is the lowest offer you think the seller would accept?",
    "How does your commission change if I buy a more expensive property?",
    "Can I see the seller's disclosure statement before making an offer?"
]

# Quick Start
if main_tool == "Quick Start":
    st.markdown('<h2 class="section-header">🚀 Quick Start Guide</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 What This Tool Does")
        st.write("This decoder helps you navigate real estate transactions by:")
        st.write("• Identifying hidden costs and fees")
        st.write("• Recognizing manipulation tactics")
        st.write("• Understanding agent motivations")
        st.write("• Providing defense strategies")
        st.write("• Preparing you for negotiations")
        
        st.markdown("### 🏠 Who This Helps")
        st.write("Perfect for everyday working people:")
        st.write("• First-time home buyers")
        st.write("• Anyone selling their home")
        st.write("• People feeling pressured by agents")
        st.write("• Those who want to understand the process")
    
    with col2:
        st.markdown("### ⚡ Start Here")
        st.info("**New to real estate?** Start with 'Realtor-Speak Decoder' to understand common phrases.")
        st.warning("**Feeling pressured?** Go to 'Sales Tactic Decoder' > 'Defense' for immediate help.")
        st.success("**Before any meeting?** Use 'Meeting Prep Tool' > 'Killer Questions' to prepare.")
        
        st.markdown("### 🚨 Emergency Red Flags")
        st.error("**STOP** if agent says:")
        st.write("• 'Sign now or lose the deal'")
        st.write("• 'Don't worry about reading that'")
        st.write("• 'Trust me on this one'")
        st.write("• 'Everyone else is doing it'")

# Document Analysis
elif main_tool == "Document Analysis":
    if sub_tool == "Overview":
        st.markdown('<h2 class="section-header">📄 Document Analysis</h2>', unsafe_allow_html=True)
        st.write("Upload your real estate documents to identify hidden fees and problematic clauses.")
        
        uploaded_file = st.file_uploader(
            "Upload Document (PDF, TXT, DOCX)",
            type=['pdf', 'txt', 'docx'],
            help="Upload listing agreements, purchase contracts, disclosure forms, or any real estate document"
        )
        
        if uploaded_file:
            st.success("Document uploaded successfully!")
            st.info("**Note:** In a full implementation, this would analyze your document for:")
            st.write("• Hidden fees and charges")
            st.write("• Dual agency disclosures")
            st.write("• Commission structures")
            st.write("• Problematic contract clauses")
            st.write("• Missing protections")
            
            # Simulate analysis results
            st.markdown("### 🔍 Analysis Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ⚠️ Potential Issues Found")
                st.write("• Buyer's premium not clearly disclosed")
                st.write("• Agent represents both parties")
                st.write("• Commission rate above market average")
                st.write("• Limited inspection contingency period")
            
            with col2:
                st.markdown("#### ✅ Protections in Place")
                st.write("• Financing contingency included")
                st.write("• Clear closing date specified")
                st.write("• Property condition disclosures present")

# Commission Calculator
elif main_tool == "Commission Calculator":
    if sub_tool == "Overview":
        st.markdown('<h2 class="section-header">💰 Commission Calculator</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Calculate Real Estate Commissions")
            home_price = st.number_input("Home Sale Price ($)", value=300000, step=5000)
            total_commission = st.slider("Total Commission Rate (%)", 4.0, 8.0, 6.0, 0.1)
            
            # Calculate commissions
            total_commission_amount = home_price * (total_commission / 100)
            listing_agent_share = total_commission_amount / 2
            buying_agent_share = total_commission_amount / 2
            
        with col2:
            st.markdown("### 💡 Commission Breakdown")
            st.metric("Total Commission", f"${total_commission_amount:,.0f}")
            st.metric("Listing Agent Gets", f"${listing_agent_share:,.0f}")
            st.metric("Buying Agent Gets", f"${buying_agent_share:,.0f}")
            
            if total_commission > 6.5:
                st.error("⚠️ This commission rate is above average (typically 5-6%)")
            elif total_commission < 5.0:
                st.warning("This rate may indicate limited services")
            else:
                st.success("✅ This rate is within normal range")
        
        st.markdown("### 🧮 Alternative Fee Structures")
        st.write("**Flat Fee:** Some agents charge $3,000-$5,000 regardless of home price")
        st.write("**Reduced Commission:** Negotiable, especially on higher-priced homes")
        st.write("**For Sale By Owner:** $0 agent commission, but you handle everything")

# Other tools (abbreviated for space, following the same pattern)
elif main_tool == "Realtor-Speak Decoder":
    if sub_tool == "What They Said":
        st.markdown('<h2 class="section-header">🗣️ What They Said - Decoder</h2>', unsafe_allow_html=True)
        
        phrase_input = st.text_input("Enter a phrase your agent said:")
        
        if phrase_input:
            # Simple matching logic
            found_match = False
            for phrase, meaning in realtor_speak.items():
                if phrase.lower() in phrase_input.lower():
                    st.markdown(f"### 🎯 Phrase: '{phrase}'")
                    st.markdown(f'<div class="warning-box"><strong>What it really means:</strong> {meaning}</div>', unsafe_allow_html=True)
                    found_match = True
                    break
            
            if not found_match:
                st.info("No direct match found. Try some common phrases below or describe the situation in your own words.")
        
        st.markdown("### 🔍 Common Phrases to Watch For")
        for phrase, meaning in realtor_speak.items():
            with st.expander(f"'{phrase}'"):
                st.write(f"**Translation:** {meaning}")

    elif sub_tool == "Psychological Tactics":
        st.markdown('<h2 class="section-header">🧠 Psychological Tactics</h2>', unsafe_allow_html=True)
        
        for tactic, details in psychological_tactics.items():
            with st.expander(f"🎯 {tactic}"):
                st.write(f"**What it is:** {details['Description']}")
                st.write("**Examples:**")
                for example in details['Examples']:
                    st.write(f"• '{example}'")
                st.markdown(f'<div class="success-box"><strong>Your Defense:</strong> {details["Defense"]}</div>', unsafe_allow_html=True)

elif main_tool == "Sales Tactic Decoder":
    if sub_tool == "Red Flag Checker":
        st.markdown('<h2 class="section-header">🚩 Red Flag Checker</h2>', unsafe_allow_html=True)
        
        st.write("Check off any behaviors you've experienced with your agent:")
        
        flagged_items = []
        for flag in red_flags:
            if st.checkbox(flag):
                flagged_items.append(flag)
        
        if flagged_items:
            st.markdown(f'<div class="danger-box"><strong>⚠️ Warning:</strong> You\'ve identified {len(flagged_items)} red flags. Consider getting a second opinion or switching agents.</div>', unsafe_allow_html=True)
            
            st.markdown("### 🛡️ Recommended Actions:")
            st.write("• Document all interactions in writing")
            st.write("• Get multiple agent opinions")
            st.write("• Consider switching to a different agent")
            st.write("• Consult with a real estate attorney")
        else:
            st.success("✅ No red flags detected. Continue with caution and stay informed!")

elif main_tool == "Meeting Prep Tool":
    if sub_tool == "Killer Questions":
        st.markdown('<h2 class="section-header">❓ Killer Questions</h2>', unsafe_allow_html=True)
        st.write("These questions will expose your agent's true motivations and protect your interests:")
        
        for i, question in enumerate(killer_questions, 1):
            with st.expander(f"Question {i}: {question}"):
                st.write("**Why this matters:** This question reveals important information about costs, conflicts of interest, or market conditions that agents often don't volunteer.")
                st.write("**What to watch for:** Evasive answers, anger, or reluctance to provide clear information.")
        
        st.markdown("### 📝 Pro Tips")
        st.markdown("""
        - Ask these questions in writing when possible
        - Don't accept vague answers like "don't worry about that"
        - If they can't answer, they might not be qualified to help you
        - Good agents welcome informed clients and tough questions
        """)

# Footer
st.markdown("---")
st.markdown("**Decoder Universe** - Empowering everyday people to make better financial decisions")
st.markdown("*Part of the consumer advocacy suite for working families*")
