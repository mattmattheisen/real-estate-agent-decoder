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
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# COMPREHENSIVE DATABASE SECTIONS
# =====================================

# Enhanced Glossary Database
glossary_database = {
    "Commission": {
        "definition": "Percentage of sale price paid to agents (typically 5-6%). Split between listing and buyer's agent.",
        "consumer_impact": "On a $300k home, this is $15k-18k. This cost is built into home prices.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Financial",
        "what_to_ask": "Is your commission rate negotiable, especially on higher-priced homes?"
    },
    
    "Dual Agency": {
        "definition": "When one agent or brokerage represents both buyer and seller in the same transaction.",
        "consumer_impact": "Agent gets full commission but has conflicts of interest. Cannot fully advocate for either party.",
        "negotiable": True,
        "red_flag_level": "High", 
        "category": "Financial",
        "what_to_ask": "Do you ever represent both parties? How do you handle conflicts of interest?"
    },
    
    "Buyer's Premium": {
        "definition": "Additional fee paid by buyer on top of purchase price, often not disclosed until closing.",
        "consumer_impact": "Can add $500-2000+ to closing costs without warning.",
        "negotiable": True,
        "red_flag_level": "High",
        "category": "Financial", 
        "what_to_ask": "Are there any additional fees beyond the purchase price and standard closing costs?"
    },
    
    "Transaction Fee": {
        "definition": "Administrative fee charged by brokerage, typically $200-500 per transaction.",
        "consumer_impact": "Often not disclosed upfront. Pure profit for brokerage with no additional services.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Financial",
        "what_to_ask": "What administrative or transaction fees will I be charged?"
    },
    
    "PMI (Private Mortgage Insurance)": {
        "definition": "Insurance required when down payment is less than 20%, protects lender not buyer.",
        "consumer_impact": "Adds $100-400/month to mortgage payment. Can be removed once you have 20% equity.",
        "negotiable": False,
        "red_flag_level": "Low",
        "category": "Financial",
        "what_to_ask": "When can PMI be removed and what's the process?"
    },
    
    "Points": {
        "definition": "Upfront fee to reduce interest rate (1 point = 1% of loan amount).",
        "consumer_impact": "May or may not save money long-term. Calculate break-even point before paying.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Financial",
        "what_to_ask": "Show me the math on how long it takes to break even on points."
    },
    
    "Contingency": {
        "definition": "Condition that must be met for sale to proceed (inspection, financing, appraisal).",
        "consumer_impact": "Your escape routes if something goes wrong. Agents may pressure you to waive these.",
        "negotiable": True,
        "red_flag_level": "High",
        "category": "Property",
        "what_to_ask": "Why are you recommending I waive any contingencies?"
    },
    
    "Inspection": {
        "definition": "Professional examination of property condition, typically costs $300-500.",
        "consumer_impact": "Can save thousands by finding major problems. Never skip this step.",
        "negotiable": False,
        "red_flag_level": "High",
        "category": "Property", 
        "what_to_ask": "Why wouldn't you recommend a full inspection?"
    },
    
    "Appraisal": {
        "definition": "Professional property valuation required by lender to ensure home is worth loan amount.",
        "consumer_impact": "Protects you from overpaying. If appraisal is low, you can renegotiate or walk away.",
        "negotiable": False,
        "red_flag_level": "Medium",
        "category": "Property",
        "what_to_ask": "What happens if the appraisal comes in lower than our offer?"
    },
    
    "Days on Market (DOM)": {
        "definition": "How long property has been listed for sale, including previous listings.",
        "consumer_impact": "Longer DOM usually means more room to negotiate. Agents may hide this information.",
        "negotiable": False,
        "red_flag_level": "Medium", 
        "category": "Market",
        "what_to_ask": "How long has this property been on the market, including previous listings?"
    },
    
    "Comparable Sales (Comps)": {
        "definition": "Recently sold similar properties used to determine fair market value.",
        "consumer_impact": "Essential for knowing if you're paying fair price. Should be free from your agent.",
        "negotiable": False,
        "red_flag_level": "Medium",
        "category": "Market",
        "what_to_ask": "Can you show me the actual MLS data for comparable sales?"
    },
    
    "Earnest Money": {
        "definition": "Good faith deposit showing you're serious about buying, typically 1-3% of offer.",
        "consumer_impact": "You lose this if you back out without valid contingency. Keep it reasonable.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Legal",
        "what_to_ask": "What's the minimum earnest money required, and when do I get it back?"
    },
    
    "Closing Costs": {
        "definition": "Fees paid at closing, typically 2-5% of home price for buyers.",
        "consumer_impact": "Can be $6k-15k on average home. Many fees are negotiable or can be reduced.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Legal",
        "what_to_ask": "Give me an itemized estimate of all closing costs and which ones are negotiable."
    },
    
    "Title Insurance": {
        "definition": "One-time fee protecting against ownership disputes, required by most lenders.",
        "consumer_impact": "Shop around - prices vary significantly between companies for same coverage.",
        "negotiable": True,
        "red_flag_level": "Low",
        "category": "Legal",
        "what_to_ask": "Can I choose my own title company to get better rates?"
    },
    
    "MLS": {
        "definition": "Multiple Listing Service - database of properties for sale that agents access.",
        "consumer_impact": "Contains detailed property information. Ask to see actual MLS sheets, not just pretty brochures.",
        "negotiable": False,
        "red_flag_level": "Low",
        "category": "Market",
        "what_to_ask": "Can you show me the actual MLS listing with all the details?"
    }
}

# Enhanced Red Flag Database
red_flag_database = {
    "Agent won't disclose commission rate": {
        "severity": "High",
        "category": "Financial",
        "description": "Refuses to tell you how much they're making from your transaction",
        "why_dangerous": "Commission affects their motivation and advice. Legal requirement to disclose in most states.",
        "immediate_action": "Demand written disclosure of all compensation",
        "legal_status": "Required disclosure in most states"
    },
    
    "Pushes dual agency without explaining conflicts": {
        "severity": "Critical", 
        "category": "Financial",
        "description": "Represents both buyer and seller without clear conflict disclosure",
        "why_dangerous": "Cannot fully represent your interests. Gets double commission.",
        "immediate_action": "Get separate representation immediately",
        "legal_status": "Must disclose conflicts in writing"
    },
    
    "Hidden fees not disclosed until closing": {
        "severity": "High",
        "category": "Financial", 
        "description": "Spring surprise fees at closing when it's too late to negotiate",
        "why_dangerous": "Can add thousands to your costs when you can't back out",
        "immediate_action": "Demand itemized fee list upfront",
        "legal_status": "Violation of fair dealing requirements"
    },
    
    "Pressures you to use their preferred lender without shopping": {
        "severity": "High",
        "category": "Financial",
        "description": "Insists you use specific lender and discourages rate shopping", 
        "why_dangerous": "May receive kickbacks. You could get worse rates/terms.",
        "immediate_action": "Shop with at least 3 lenders",
        "legal_status": "Must disclose any referral fees"
    },
    
    "Creates false urgency to rush decisions": {
        "severity": "High",
        "category": "Pressure",
        "description": "'Other buyers coming', 'price going up tomorrow', 'sign today or lose it'",
        "why_dangerous": "Prevents due diligence and careful consideration of major financial decision",
        "immediate_action": "Take time anyway. Real opportunities don't vanish in hours.",
        "legal_status": "Unethical but not always illegal"
    },
    
    "Discourages inspection or contingencies": {
        "severity": "Critical",
        "category": "Pressure", 
        "description": "Suggests waiving inspection or other buyer protections",
        "why_dangerous": "Could cost tens of thousands in hidden repairs or force bad purchase",
        "immediate_action": "Never waive inspection. Get everything in writing.",
        "legal_status": "Legal but highly unethical"
    },
    
    "Won't let you read contracts thoroughly": {
        "severity": "Critical",
        "category": "Pressure",
        "description": "Rushes you through paperwork or discourages careful reading",
        "why_dangerous": "You're signing legal obligations you don't understand",
        "immediate_action": "Take documents home to review or bring attorney",
        "legal_status": "Violation of duty to clients"
    },
    
    "Becomes angry when you ask questions": {
        "severity": "High",
        "category": "Pressure",
        "description": "Gets defensive, irritated, or dismissive when you seek clarification",
        "why_dangerous": "Professional should welcome informed clients. May be hiding something.",
        "immediate_action": "Find new agent immediately",
        "legal_status": "Unprofessional conduct"
    },
    
    "Can't answer basic market questions": {
        "severity": "Medium",
        "category": "Competence",
        "description": "Doesn't know recent sales, market trends, or neighborhood details",
        "why_dangerous": "Lack of knowledge can cost you money in negotiations",
        "immediate_action": "Test their knowledge with specific questions",
        "legal_status": "May violate competency requirements"
    },
    
    "Provides inaccurate information": {
        "severity": "High",
        "category": "Competence",
        "description": "Gives wrong info about prices, processes, or legal requirements", 
        "why_dangerous": "Bad information leads to bad decisions and potential legal issues",
        "immediate_action": "Verify all information independently",
        "legal_status": "May violate licensing requirements"
    },
    
    "Shows homes they have financial interest in without disclosure": {
        "severity": "Critical",
        "category": "Ethical",
        "description": "Recommends properties they own, co-own, or have listing agreements on",
        "why_dangerous": "Massive conflict of interest. They profit more from these sales.",
        "immediate_action": "Ask about any financial interest in properties shown",
        "legal_status": "Must disclose financial interests"
    },
    
    "Asks you to lie on loan applications": {
        "severity": "Critical",
        "category": "Ethical",
        "description": "Suggests inflating income, hiding debts, or other loan fraud",
        "why_dangerous": "Federal crime. You could face prosecution and lose home.",
        "immediate_action": "Refuse and report to authorities immediately",
        "legal_status": "Federal crime - loan fraud"
    }
}

# Psychology Database
psychology_database = {
    "Urgency": {
        "description": "Creating artificial time pressure to force quick decisions",
        "how_it_works": "Triggers fear of missing out (FOMO) and bypasses rational decision-making",
        "examples": [
            "Other buyers are coming to see it this afternoon",
            "The seller is reviewing offers tonight",
            "Prices in this area are going up next month",
            "Interest rates are rising, you need to lock in now"
        ],
        "psychology_behind": "Exploits loss aversion - people hate losing opportunities more than they like gaining them",
        "defense": "Real opportunities don't disappear in hours. Take at least 24 hours to decide on major purchases.",
        "counter_phrases": [
            "If it's the right house for me, I'll still want it tomorrow",
            "When is the actual deadline?", 
            "I need time to make an informed decision"
        ]
    },
    
    "Scarcity": {
        "description": "Making properties seem rare or unique when they're not",
        "how_it_works": "Artificial scarcity increases perceived value and urgency",
        "examples": [
            "You won't find another house like this",
            "This is the last available lot",
            "Properties in this price range are rare",
            "This floor plan isn't available anymore"
        ],
        "psychology_behind": "Scarcity principle - we value things more when they seem rare or limited",
        "defense": "Research comparable properties yourself. Most homes have similar alternatives nearby.",
        "counter_phrases": [
            "Show me what makes this truly unique",
            "What other similar properties are available?",
            "I'd like to see comparable options"
        ]
    },
    
    "Social Proof": {
        "description": "Using others' behavior to influence your decisions",
        "how_it_works": "People copy what others do, especially under uncertainty",
        "examples": [
            "All my clients love this neighborhood", 
            "Most buyers choose this floor plan",
            "Everyone else is bidding above asking",
            "Smart buyers always get inspections (when they want you to)"
        ],
        "psychology_behind": "Social proof heuristic - we assume others know something we don't",
        "defense": "Make decisions based on your needs and research, not what others supposedly do.",
        "counter_phrases": [
            "What's right for others may not be right for me",
            "I need to evaluate this based on my situation",
            "Can you show me actual data on that?"
        ]
    },
    
    "Authority": {
        "description": "Using credentials or experience to shut down questions",
        "how_it_works": "People defer to perceived authority figures even when inappropriate",
        "examples": [
            "Trust me, I've been doing this for 20 years",
            "As a professional, I'm telling you...",
            "You should listen to me on this",
            "I know what's best for my clients"
        ],
        "psychology_behind": "Authority bias - we're programmed to follow expert guidance",
        "defense": "Your questions are valid regardless of their experience. Demand explanations.",
        "counter_phrases": [
            "Help me understand your reasoning",
            "I appreciate your experience, but I need more information", 
            "Can you explain why that's your recommendation?"
        ]
    },
    
    "Anchoring": {
        "description": "Setting a high initial number to make everything else seem reasonable",
        "how_it_works": "First number mentioned becomes reference point for all subsequent negotiations",
        "examples": [
            "Houses in this area go for $400k (when showing $350k house)",
            "The seller was asking $300k but will take $280k",
            "You could spend up to $500k with your income",
            "Most buyers put down 20% ($60k on $300k house)"
        ],
        "psychology_behind": "Anchoring bias - first number disproportionately influences all judgments",
        "defense": "Research true market values independently. Ignore their initial numbers.",
        "counter_phrases": [
            "What have similar homes actually sold for?",
            "I need to see comparable sales data",
            "Let's focus on real market values"
        ]
    },
    
    "Reciprocity": {
        "description": "Doing small favors to create obligation for larger commitments",
        "how_it_works": "People feel obligated to return favors, even when unequal",
        "examples": [
            "I'll show you houses for free (expecting you to buy through them)",
            "Let me get you a great deal on inspection (expecting loyalty)",
            "I'll negotiate hard for you (expecting you not to negotiate their commission)",
            "I'll work weekends for you (creating guilt about switching agents)"
        ],
        "psychology_behind": "Reciprocity rule - we're obligated to repay debts, even imaginary ones",
        "defense": "Professional services aren't personal favors. Don't let small gestures obligate you to major decisions.",
        "counter_phrases": [
            "I appreciate your service, but I need to make the best decision for me",
            "Thank you, but I don't feel obligated by your professional duties",
            "I'm paying for your services through commission"
        ]
    }
}

# Realtor-speak phrases for decoder
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
    "This is the best we can do": "Agents almost always have more room to negotiate.",
    "Everyone else is bidding above asking": "Creating false competition and FOMO.",
    "You don't want to lose this one": "Pure pressure tactic with no factual basis.",
    "The seller is firm on price": "Usually means they haven't tried to negotiate yet."
}

# Main title and tagline
st.markdown('<h1 class="main-header">🏠 Real Estate Agent Decoder</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Uncover hidden costs and conflicts of interest in your real estate transaction</p>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #d32f2f;">Don\'t Get Sold - Get Decoded</h3>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; font-size: 0.9rem; margin: 1rem 0; padding: 1rem; background-color: #f8f9fa; border-radius: 5px;"><strong>Disclaimer:</strong> This tool is for educational purposes only. Always consult with qualified professionals for financial advice.</div>', unsafe_allow_html=True)
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
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# COMPREHENSIVE DATABASE SECTIONS
# =====================================

# Enhanced Glossary Database
glossary_database = {
    "Commission": {
        "definition": "Percentage of sale price paid to agents (typically 5-6%). Split between listing and buyer's agent.",
        "consumer_impact": "On a $300k home, this is $15k-18k. This cost is built into home prices.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Financial",
        "what_to_ask": "Is your commission rate negotiable, especially on higher-priced homes?"
    },
    
    "Dual Agency": {
        "definition": "When one agent or brokerage represents both buyer and seller in the same transaction.",
        "consumer_impact": "Agent gets full commission but has conflicts of interest. Cannot fully advocate for either party.",
        "negotiable": True,
        "red_flag_level": "High", 
        "category": "Financial",
        "what_to_ask": "Do you ever represent both parties? How do you handle conflicts of interest?"
    },
    
    "Buyer's Premium": {
        "definition": "Additional fee paid by buyer on top of purchase price, often not disclosed until closing.",
        "consumer_impact": "Can add $500-2000+ to closing costs without warning.",
        "negotiable": True,
        "red_flag_level": "High",
        "category": "Financial", 
        "what_to_ask": "Are there any additional fees beyond the purchase price and standard closing costs?"
    },
    
    "Transaction Fee": {
        "definition": "Administrative fee charged by brokerage, typically $200-500 per transaction.",
        "consumer_impact": "Often not disclosed upfront. Pure profit for brokerage with no additional services.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Financial",
        "what_to_ask": "What administrative or transaction fees will I be charged?"
    },
    
    "PMI (Private Mortgage Insurance)": {
        "definition": "Insurance required when down payment is less than 20%, protects lender not buyer.",
        "consumer_impact": "Adds $100-400/month to mortgage payment. Can be removed once you have 20% equity.",
        "negotiable": False,
        "red_flag_level": "Low",
        "category": "Financial",
        "what_to_ask": "When can PMI be removed and what's the process?"
    },
    
    "Points": {
        "definition": "Upfront fee to reduce interest rate (1 point = 1% of loan amount).",
        "consumer_impact": "May or may not save money long-term. Calculate break-even point before paying.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Financial",
        "what_to_ask": "Show me the math on how long it takes to break even on points."
    },
    
    "Contingency": {
        "definition": "Condition that must be met for sale to proceed (inspection, financing, appraisal).",
        "consumer_impact": "Your escape routes if something goes wrong. Agents may pressure you to waive these.",
        "negotiable": True,
        "red_flag_level": "High",
        "category": "Property",
        "what_to_ask": "Why are you recommending I waive any contingencies?"
    },
    
    "Inspection": {
        "definition": "Professional examination of property condition, typically costs $300-500.",
        "consumer_impact": "Can save thousands by finding major problems. Never skip this step.",
        "negotiable": False,
        "red_flag_level": "High",
        "category": "Property", 
        "what_to_ask": "Why wouldn't you recommend a full inspection?"
    },
    
    "Appraisal": {
        "definition": "Professional property valuation required by lender to ensure home is worth loan amount.",
        "consumer_impact": "Protects you from overpaying. If appraisal is low, you can renegotiate or walk away.",
        "negotiable": False,
        "red_flag_level": "Medium",
        "category": "Property",
        "what_to_ask": "What happens if the appraisal comes in lower than our offer?"
    },
    
    "Days on Market (DOM)": {
        "definition": "How long property has been listed for sale, including previous listings.",
        "consumer_impact": "Longer DOM usually means more room to negotiate. Agents may hide this information.",
        "negotiable": False,
        "red_flag_level": "Medium", 
        "category": "Market",
        "what_to_ask": "How long has this property been on the market, including previous listings?"
    },
    
    "Comparable Sales (Comps)": {
        "definition": "Recently sold similar properties used to determine fair market value.",
        "consumer_impact": "Essential for knowing if you're paying fair price. Should be free from your agent.",
        "negotiable": False,
        "red_flag_level": "Medium",
        "category": "Market",
        "what_to_ask": "Can you show me the actual MLS data for comparable sales?"
    },
    
    "Earnest Money": {
        "definition": "Good faith deposit showing you're serious about buying, typically 1-3% of offer.",
        "consumer_impact": "You lose this if you back out without valid contingency. Keep it reasonable.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Legal",
        "what_to_ask": "What's the minimum earnest money required, and when do I get it back?"
    },
    
    "Closing Costs": {
        "definition": "Fees paid at closing, typically 2-5% of home price for buyers.",
        "consumer_impact": "Can be $6k-15k on average home. Many fees are negotiable or can be reduced.",
        "negotiable": True,
        "red_flag_level": "Medium",
        "category": "Legal",
        "what_to_ask": "Give me an itemized estimate of all closing costs and which ones are negotiable."
    },
    
    "Title Insurance": {
        "definition": "One-time fee protecting against ownership disputes, required by most lenders.",
        "consumer_impact": "Shop around - prices vary significantly between companies for same coverage.",
        "negotiable": True,
        "red_flag_level": "Low",
        "category": "Legal",
        "what_to_ask": "Can I choose my own title company to get better rates?"
    },
    
    "MLS": {
        "definition": "Multiple Listing Service - database of properties for sale that agents access.",
        "consumer_impact": "Contains detailed property information. Ask to see actual MLS sheets, not just pretty brochures.",
        "negotiable": False,
        "red_flag_level": "Low",
        "category": "Market",
        "what_to_ask": "Can you show me the actual MLS listing with all the details?"
    }
}

# Enhanced Red Flag Database
red_flag_database = {
    "Agent won't disclose commission rate": {
        "severity": "High",
        "category": "Financial",
        "description": "Refuses to tell you how much they're making from your transaction",
        "why_dangerous": "Commission affects their motivation and advice. Legal requirement to disclose in most states.",
        "immediate_action": "Demand written disclosure of all compensation",
        "legal_status": "Required disclosure in most states"
    },
    
    "Pushes dual agency without explaining conflicts": {
        "severity": "Critical", 
        "category": "Financial",
        "description": "Represents both buyer and seller without clear conflict disclosure",
        "why_dangerous": "Cannot fully represent your interests. Gets double commission.",
        "immediate_action": "Get separate representation immediately",
        "legal_status": "Must disclose conflicts in writing"
    },
    
    "Hidden fees not disclosed until closing": {
        "severity": "High",
        "category": "Financial", 
        "description": "Spring surprise fees at closing when it's too late to negotiate",
        "why_dangerous": "Can add thousands to your costs when you can't back out",
        "immediate_action": "Demand itemized fee list upfront",
        "legal_status": "Violation of fair dealing requirements"
    },
    
    "Pressures you to use their preferred lender without shopping": {
        "severity": "High",
        "category": "Financial",
        "description": "Insists you use specific lender and discourages rate shopping", 
        "why_dangerous": "May receive kickbacks. You could get worse rates/terms.",
        "immediate_action": "Shop with at least 3 lenders",
        "legal_status": "Must disclose any referral fees"
    },
    
    "Creates false urgency to rush decisions": {
        "severity": "High",
        "category": "Pressure",
        "description": "'Other buyers coming', 'price going up tomorrow', 'sign today or lose it'",
        "why_dangerous": "Prevents due diligence and careful consideration of major financial decision",
        "immediate_action": "Take time anyway. Real opportunities don't vanish in hours.",
        "legal_status": "Unethical but not always illegal"
    },
    
    "Discourages inspection or contingencies": {
        "severity": "Critical",
        "category": "Pressure", 
        "description": "Suggests waiving inspection or other buyer protections",
        "why_dangerous": "Could cost tens of thousands in hidden repairs or force bad purchase",
        "immediate_action": "Never waive inspection. Get everything in writing.",
        "legal_status": "Legal but highly unethical"
    },
    
    "Won't let you read contracts thoroughly": {
        "severity": "Critical",
        "category": "Pressure",
        "description": "Rushes you through paperwork or discourages careful reading",
        "why_dangerous": "You're signing legal obligations you don't understand",
        "immediate_action": "Take documents home to review or bring attorney",
        "legal_status": "Violation of duty to clients"
    },
    
    "Becomes angry when you ask questions": {
        "severity": "High",
        "category": "Pressure",
        "description": "Gets defensive, irritated, or dismissive when you seek clarification",
        "why_dangerous": "Professional should welcome informed clients. May be hiding something.",
        "immediate_action": "Find new agent immediately",
        "legal_status": "Unprofessional conduct"
    },
    
    "Can't answer basic market questions": {
        "severity": "Medium",
        "category": "Competence",
        "description": "Doesn't know recent sales, market trends, or neighborhood details",
        "why_dangerous": "Lack of knowledge can cost you money in negotiations",
        "immediate_action": "Test their knowledge with specific questions",
        "legal_status": "May violate competency requirements"
    },
    
    "Provides inaccurate information": {
        "severity": "High",
        "category": "Competence",
        "description": "Gives wrong info about prices, processes, or legal requirements", 
        "why_dangerous": "Bad information leads to bad decisions and potential legal issues",
        "immediate_action": "Verify all information independently",
        "legal_status": "May violate licensing requirements"
    },
    
    "Shows homes they have financial interest in without disclosure": {
        "severity": "Critical",
        "category": "Ethical",
        "description": "Recommends properties they own, co-own, or have listing agreements on",
        "why_dangerous": "Massive conflict of interest. They profit more from these sales.",
        "immediate_action": "Ask about any financial interest in properties shown",
        "legal_status": "Must disclose financial interests"
    },
    
    "Asks you to lie on loan applications": {
        "severity": "Critical",
        "category": "Ethical",
        "description": "Suggests inflating income, hiding debts, or other loan fraud",
        "why_dangerous": "Federal crime. You could face prosecution and lose home.",
        "immediate_action": "Refuse and report to authorities immediately",
        "legal_status": "Federal crime - loan fraud"
    }
}

# Psychology Database
psychology_database = {
    "Urgency": {
        "description": "Creating artificial time pressure to force quick decisions",
        "how_it_works": "Triggers fear of missing out (FOMO) and bypasses rational decision-making",
        "examples": [
            "Other buyers are coming to see it this afternoon",
            "The seller is reviewing offers tonight",
            "Prices in this area are going up next month",
            "Interest rates are rising, you need to lock in now"
        ],
        "psychology_behind": "Exploits loss aversion - people hate losing opportunities more than they like gaining them",
        "defense": "Real opportunities don't disappear in hours. Take at least 24 hours to decide on major purchases.",
        "counter_phrases": [
            "If it's the right house for me, I'll still want it tomorrow",
            "When is the actual deadline?", 
            "I need time to make an informed decision"
        ]
    },
    
    "Scarcity": {
        "description": "Making properties seem rare or unique when they're not",
        "how_it_works": "Artificial scarcity increases perceived value and urgency",
        "examples": [
            "You won't find another house like this",
            "This is the last available lot",
            "Properties in this price range are rare",
            "This floor plan isn't available anymore"
        ],
        "psychology_behind": "Scarcity principle - we value things more when they seem rare or limited",
        "defense": "Research comparable properties yourself. Most homes have similar alternatives nearby.",
        "counter_phrases": [
            "Show me what makes this truly unique",
            "What other similar properties are available?",
            "I'd like to see comparable options"
        ]
    },
    
    "Social Proof": {
        "description": "Using others' behavior to influence your decisions",
        "how_it_works": "People copy what others do, especially under uncertainty",
        "examples": [
            "All my clients love this neighborhood", 
            "Most buyers choose this floor plan",
            "Everyone else is bidding above asking",
            "Smart buyers always get inspections (when they want you to)"
        ],
        "psychology_behind": "Social proof heuristic - we assume others know something we don't",
        "defense": "Make decisions based on your needs and research, not what others supposedly do.",
        "counter_phrases": [
            "What's right for others may not be right for me",
            "I need to evaluate this based on my situation",
            "Can you show me actual data on that?"
        ]
    },
    
    "Authority": {
        "description": "Using credentials or experience to shut down questions",
        "how_it_works": "People defer to perceived authority figures even when inappropriate",
        "examples": [
            "Trust me, I've been doing this for 20 years",
            "As a professional, I'm telling you...",
            "You should listen to me on this",
            "I know what's best for my clients"
        ],
        "psychology_behind": "Authority bias - we're programmed to follow expert guidance",
        "defense": "Your questions are valid regardless of their experience. Demand explanations.",
        "counter_phrases": [
            "Help me understand your reasoning",
            "I appreciate your experience, but I need more information", 
            "Can you explain why that's your recommendation?"
        ]
    },
    
    "Anchoring": {
        "description": "Setting a high initial number to make everything else seem reasonable",
        "how_it_works": "First number mentioned becomes reference point for all subsequent negotiations",
        "examples": [
            "Houses in this area go for $400k (when showing $350k house)",
            "The seller was asking $300k but will take $280k",
            "You could spend up to $500k with your income",
            "Most buyers put down 20% ($60k on $300k house)"
        ],
        "psychology_behind": "Anchoring bias - first number disproportionately influences all judgments",
        "defense": "Research true market values independently. Ignore their initial numbers.",
        "counter_phrases": [
            "What have similar homes actually sold for?",
            "I need to see comparable sales data",
            "Let's focus on real market values"
        ]
    },
    
    "Reciprocity": {
        "description": "Doing small favors to create obligation for larger commitments",
        "how_it_works": "People feel obligated to return favors, even when unequal",
        "examples": [
            "I'll show you houses for free (expecting you to buy through them)",
            "Let me get you a great deal on inspection (expecting loyalty)",
            "I'll negotiate hard for you (expecting you not to negotiate their commission)",
            "I'll work weekends for you (creating guilt about switching agents)"
        ],
        "psychology_behind": "Reciprocity rule - we're obligated to repay debts, even imaginary ones",
        "defense": "Professional services aren't personal favors. Don't let small gestures obligate you to major decisions.",
        "counter_phrases": [
            "I appreciate your service, but I need to make the best decision for me",
            "Thank you, but I don't feel obligated by your professional duties",
            "I'm paying for your services through commission"
        ]
    }
}

# Realtor-speak phrases for decoder
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
    "This is the best we can do": "Agents almost always have more room to negotiate.",
    "Everyone else is bidding above asking": "Creating false competition and FOMO.",
    "You don't want to lose this one": "Pure pressure tactic with no factual basis.",
    "The seller is firm on price": "Usually means they haven't tried to negotiate yet."
}

# Main title and tagline
st.markdown('<h1 class="main-header">🏠 Real Estate Agent Decoder</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Uncover hidden costs and conflicts of interest in your real estate transaction</p>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #d32f2f;">Don\'t Get Sold - Get Decoded</h3>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; font-size: 0.9rem; margin: 1rem 0; padding: 1rem; background-color: #f8f9fa; border-radius: 5px;"><strong>Disclaimer:</strong> This tool is for educational purposes only. Always consult with qualified professionals for financial advice.</div>', unsafe_allow_html=True)
# Sidebar navigation
st.sidebar.title("🏠 Navigation")
main_tool = st.sidebar.selectbox(
    "Choose a Tool:",
    ["🚀 Quick Start", 
     "📄 Document Analysis", 
     "💰 Commission Calculator", 
     "⚠️ Conflict Checker",
     "🗣️ Realtor-Speak Decoder", 
     "🧠 Psychology",
     "🎯 Defense", 
     "🚩 Red Flag Checker",
     "📚 Glossary",
     "📝 Meeting Prep Tool"]
)

# Quick Start
if main_tool == "🚀 Quick Start":
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
        st.info("**New to real estate?** Start with 'Glossary' to understand key terms.")
        st.warning("**Feeling pressured?** Go to 'Defense' for immediate help.")
        st.success("**Before any meeting?** Use 'Meeting Prep Tool' to prepare.")
        
        st.markdown("### 🚨 Emergency Red Flags")
        st.error("**STOP** if agent says:")
        st.write("• 'Sign now or lose the deal'")
        st.write("• 'Don't worry about reading that'")
        st.write("• 'Trust me on this one'")
        st.write("• 'Everyone else is doing it'")

# Document Analysis
elif main_tool == "📄 Document Analysis":
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
elif main_tool == "💰 Commission Calculator":
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
    
    # Commission impact calculator
    st.markdown("### 💰 Commission Impact on Your Purchase")
    st.write(f"**Remember:** The seller pays commission, but it's built into the home price.")
    st.write(f"**Your real cost:** Commission is factored into what you pay for the home.")
    st.write(f"**Negotiation opportunity:** In a buyer's market, you may be able to negotiate commission into the price.")

# Conflict Checker
elif main_tool == "⚠️ Conflict Checker":
    st.markdown('<h2 class="section-header">⚠️ Conflict Checker</h2>', unsafe_allow_html=True)
    st.write("Identify potential conflicts of interest with your real estate agent.")
    
    st.markdown("### 🔍 Check for These Conflicts")
    
    conflicts = [
        "Agent represents both buyer and seller (dual agency)",
        "Agent receives kickbacks from recommended lenders",
        "Agent owns or has interest in the property",
        "Agent is related to the seller",
        "Agent gets higher commission from certain lenders",
        "Agent pushes specific properties they have listings on",
        "Agent discourages you from shopping around for services",
        "Agent has relationships with inspectors/appraisers",
        "Agent won't disclose their compensation structure",
        "Agent pressures you to use their title company"
    ]
    
    detected_conflicts = []
    for conflict in conflicts:
        if st.checkbox(conflict):
            detected_conflicts.append(conflict)
    
    if detected_conflicts:
        st.markdown(f'<div class="danger-box"><strong>🚨 {len(detected_conflicts)} Potential Conflicts Detected!</strong><br>These conflicts may not be illegal, but they could affect the advice you receive.</div>', unsafe_allow_html=True)
        
        st.markdown("### ⚖️ What This Means")
        st.write("• Your agent may prioritize their interests over yours")
        st.write("• You may not be getting the best deal available")
        st.write("• Consider getting independent advice")
        st.write("• Ask for written disclosure of all relationships")
        st.write("• You have the right to separate representation")
    else:
        st.success("✅ No obvious conflicts detected. Stay vigilant!")
    
    st.markdown("### 📋 Questions to Ask About Conflicts")
    conflict_questions = [
        "Do you represent both buyers and sellers?",
        "What compensation do you receive from lenders, title companies, or inspectors?",
        "Do you have any financial interest in properties you're showing me?",
        "How does your commission change based on the price or lender I choose?",
        "Are you related to or friends with the seller?",
        "Do you get bonuses for using certain service providers?"
    ]
    
    for question in conflict_questions:
        st.write(f"• {question}")

# Realtor-Speak Decoder
elif main_tool == "🗣️ Realtor-Speak Decoder":
    st.markdown('<h2 class="section-header">🗣️ Realtor-Speak Decoder</h2>', unsafe_allow_html=True)
    
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
            if "pressure" in meaning.lower() or "rush" in meaning.lower():
                st.warning("🚨 This is a pressure tactic!")

# Psychology
elif main_tool == "🧠 Psychology":
    st.markdown('<h2 class="section-header">🧠 Psychology Behind Real Estate Sales</h2>', unsafe_allow_html=True)
    
    st.write("Understanding the psychological tactics used in real estate can help you make better decisions and resist manipulation.")
    
    for tactic, details in psychology_database.items():
        with st.expander(f"🎯 {tactic}"):
            st.write(f"**What it is:** {details['description']}")
            st.write(f"**How it works:** {details['how_it_works']}")
            st.write("**Examples:**")
            for example in details['examples']:
                st.write(f"• '{example}'")
            st.markdown(f'<div class="info-box"><strong>Psychology Behind It:</strong> {details["psychology_behind"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="success-box"><strong>Your Defense:</strong> {details["defense"]}</div>', unsafe_allow_html=True)
            st.write("**Say this instead:**")
            for counter in details['counter_phrases']:
                st.write(f"• '{counter}'")
    
    st.markdown("### 🧠 Why These Tactics Work")
    st.write("**Fear of Missing Out (FOMO):** Agents create artificial scarcity to trigger quick decisions")
    st.write("**Authority Bias:** We tend to trust professionals even when they have conflicts of interest")
    st.write("**Time Pressure:** Rushed decisions prevent us from thinking clearly or getting second opinions")
    st.write("**Social Proof:** We assume if others are doing something, it must be right")
    
    st.markdown('<div class="warning-box"><strong>Remember:</strong> A good agent will encourage you to take time and ask questions. Pressure tactics are red flags.</div>', unsafe_allow_html=True)

# Defense
elif main_tool == "🎯 Defense":
    st.markdown('<h2 class="section-header">🎯 Defense Strategies</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🛡️ Defense Against Common Tactics")
    
    defense_strategies = {
        "When they say 'Act Now'": {
            "Response": "I need time to think about this decision. When is the actual deadline?",
            "Why it works": "Forces them to be specific and removes false urgency"
        },
        "When they push their lender": {
            "Response": "I'll need to compare rates from multiple lenders before deciding.",
            "Why it works": "Shows you're informed and won't be rushed into expensive financing"
        },
        "When they discourage inspections": {
            "Response": "I'm not comfortable waiving inspections. What are you worried we might find?",
            "Why it works": "Makes them explain their real concerns"
        },
        "When they say 'Trust me'": {
            "Response": "I appreciate your advice. Can you put that recommendation in writing?",
            "Why it works": "Professionals should stand behind their advice"
        },
        "When they push higher offers": {
            "Response": "What's the lowest offer you think might be accepted?",
            "Why it works": "Gets them thinking about realistic negotiation range"
        },
        "When they create urgency": {
            "Response": "If this is really the right house for me, I'll still want it tomorrow.",
            "Why it works": "Shows you won't be rushed and tests their claims"
        },
        "When they mention 'other interested buyers'": {
            "Response": "Can you show me written proof of other offers?",
            "Why it works": "Most agents can't prove this claim because it's often false"
        },
        "When they get defensive about questions": {
            "Response": "I'm just trying to make an informed decision. Can you help me understand?",
            "Why it works": "Professional agents should welcome questions, not resist them"
        }
    }
    
    for situation, defense in defense_strategies.items():
        with st.expander(situation):
            st.markdown(f"**Say this:** '{defense['Response']}'")
            st.markdown(f"**Why it works:** {defense['Why it works']}")
    
    st.markdown("### 📝 Universal Defense Rules")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Always Do")
        st.write("• Take time to think (at least 24 hours)")
        st.write("• Get everything in writing")
        st.write("• Compare at least 3 options")
        st.write("• Bring a knowledgeable friend")
        st.write("• Research comparable sales yourself")
        st.write("• Ask 'How does this benefit you?'")
        st.write("• Verify all information independently")
        st.write("• Set your maximum budget privately")
    
    with col2:
        st.markdown("#### 🚫 Never Do")
        st.write("• Sign anything the same day")
        st.write("• Accept verbal promises")
        st.write("• Let emotions drive decisions")
        st.write("• Work with agents who pressure you")
        st.write("• Skip due diligence steps")
        st.write("• Assume their interests align with yours")
        st.write("• Give full financial details upfront")
        st.write("• Waive inspections or contingencies")

# Red Flag Checker  
elif main_tool == "🚩 Red Flag Checker":
    st.markdown('<h2 class="section-header">🚩 Red Flag Checker</h2>', unsafe_allow_html=True)
    
    st.write("Check off any behaviors you've experienced with your agent:")
    
    # Organize red flags by category
    categories = {}
    for flag, details in red_flag_database.items():
        category = details['category']
        if category not in categories:
            categories[category] = []
        categories[category].append((flag, details))
    
    total_flagged = 0
    critical_flags = 0
    
    for category, flags in categories.items():
        st.markdown(f"### 🔍 {category} Red Flags")
        
        for flag, details in flags:
            if st.checkbox(flag):
                total_flagged += 1
                if details['severity'] == 'Critical':
                    critical_flags += 1
                
                # Show severity indicator
                if details['severity'] == 'Critical':
                    st.markdown(f'<div class="danger-box"><strong>🚨 CRITICAL:</strong> {details["why_dangerous"]}</div>', unsafe_allow_html=True)
                elif details['severity'] == 'High':
                    st.markdown(f'<div class="warning-box"><strong>⚠️ HIGH RISK:</strong> {details["why_dangerous"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="info-box"><strong>⚡ MEDIUM RISK:</strong> {details["why_dangerous"]}</div>', unsafe_allow_html=True)
                
                st.write(f"**Immediate Action:** {details['immediate_action']}")
                st.write(f"**Legal Status:** {details['legal_status']}")
                st.markdown("---")
    
    # Summary and recommendations
    if total_flagged > 0:
        if critical_flags > 0:
            st.markdown(f'<div class="danger-box"><strong>🚨 CRITICAL WARNING:</strong> You\'ve identified {critical_flags} critical red flags and {total_flagged} total red flags. Consider ending this relationship immediately and seeking legal advice.</div>', unsafe_allow_html=True)
        elif total_flagged >= 3:
            st.markdown(f'<div class="warning-box"><strong>⚠️ WARNING:</strong> You\'ve identified {total_flagged} red flags. This agent may not be working in your best interests. Consider switching agents.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-box"><strong>⚡ CAUTION:</strong> You\'ve identified {total_flagged} red flag(s). Stay vigilant and document all interactions.</div>', unsafe_allow_html=True)
        
        st.markdown("### 🛡️ Recommended Actions:")
        st.write("• Document all interactions in writing with dates/times")
        st.write("• Get multiple agent opinions on any major decisions")
        st.write("• Consider switching to a different agent")
        st.write("• Consult with a real estate attorney if needed")
        st.write("• Report serious violations to your state's real estate commission")
        st.write("• Don't proceed with major decisions until issues are resolved")
    else:
        st.success("✅ No red flags detected. Continue with caution and stay informed!")
    
    st.markdown("### 🚨 Emergency Red Flags")
    emergency_flags = [
        "Agent asks you to sign blank documents",
        "Agent refuses to provide written agreements",
        "Agent pressures you to lie on loan applications",
        "Agent won't let you read contracts thoroughly",
        "Agent demands payment upfront before services",
        "Agent threatens you for asking questions"
    ]
    
    st.markdown('<div class="danger-box"><strong>🚨 STOP IMMEDIATELY if any of these occur:</strong></div>', unsafe_allow_html=True)
    for flag in emergency_flags:
        st.write(f"• {flag}")

# Glossary
elif main_tool == "📚 Glossary":
    st.markdown('<h2 class="section-header">📚 Real Estate Glossary</h2>', unsafe_allow_html=True)
    
    # Search functionality
    search_term = st.text_input("🔍 Search for a term:")
    
    if search_term:
        filtered_terms = {}
        for term, details in glossary_database.items():
            if (search_term.lower() in term.lower() or 
                search_term.lower() in details['definition'].lower() or
                search_term.lower() in details['consumer_impact'].lower()):
                filtered_terms[term] = details
        
        if filtered_terms:
            for term, details in filtered_terms.items():
                with st.expander(f"📖 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    
                    # Red flag indicator
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 HIGH RED FLAG: {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ WATCH OUT: {details['what_to_ask']}")
                    else:
                        st.info(f"💡 GOOD TO KNOW: {details['what_to_ask']}")
                    
                    if details['negotiable']:
                        st.success("✅ This is often negotiable!")
                    else:
                        st.info("ℹ️ This is typically non-negotiable")
        else:
            st.info("No matching terms found. Try a different search or browse categories below.")
    else:
        # Category tabs
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial", "🏠 Property", "📈 Market", "📋 Legal"])
        
        financial_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Financial'}
        property_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Property'}
        market_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Market'}
        legal_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Legal'}
        
        with tab1:
            for term, details in financial_terms.items():
                with st.expander(f"💰 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
                    if details['negotiable']:
                        st.success("✅ Often negotiable!")
        
        with tab2:
            for term, details in property_terms.items():
                with st.expander(f"🏠 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
        
        with tab3:
            for term, details in market_terms.items():
                with st.expander(f"📈 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
        
        with tab4:
            for term, details in legal_terms.items():
                with st.expander(f"📋 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
                    if details['negotiable']:
                        st.success("✅ Often negotiable!")

# Meeting Prep Tool
elif main_tool == "📝 Meeting Prep Tool":
    st.markdown('<h2 class="section-header">📝 Meeting Prep Tool</h2>', unsafe_allow_html=True)
    
    meeting_type = st.selectbox("What type of meeting are you preparing for?", 
                               ["First meeting with agent", "Property viewing", "Making an offer", 
                                "Negotiation", "Contract review", "Closing preparation"])
    
    if meeting_type == "First meeting with agent":
        st.markdown("### 🎯 Essential Questions to Ask")
        questions = [
            "What is your commission rate and is it negotiable?",
            "Do you ever represent both buyers and sellers?",
            "How many homes have you sold in the last 12 months?",
            "What services do you provide for your commission?",
            "Can you provide references from recent clients?",
            "What is your strategy for finding/selling homes?",
            "How do you handle multiple offers?",
            "What other compensation do you receive in this transaction?",
            "Can you show me your license and any complaints against you?",
            "What happens if I'm not satisfied with your services?"
        ]
        for q in questions:
            st.write(f"• {q}")
            
        st.markdown("### 🚨 Red Flags in First Meeting")
        st.write("• Won't answer commission questions directly")
        st.write("• Pressures you to sign exclusive agreement immediately")
        st.write("• Can't provide recent client references")
        st.write("• Gets defensive about dual agency questions")
        st.write("• Won't show you their credentials")
            
    elif meeting_type == "Property viewing":
        st.markdown("### 🔍 What to Look For")
        st.write("**Red Flags:**")
        st.write("• Agent rushes you through the property")
        st.write("• Discourages questions about problems")
        st.write("• Pushes you to make immediate decisions")
        st.write("• Won't let you take photos or measurements")
        st.write("• Avoids showing you certain areas")
        
        st.markdown("### ❓ Important Questions")
        st.write("• How long has this been on the market?")
        st.write("• Why is the seller moving?")
        st.write("• What repairs or issues are known?")
        st.write("• What would you offer if you were buying?")
        st.write("• Are there any upcoming assessments or HOA changes?")
        st.write("• What were the results of the last inspection?")
        st.write("• Have there been any price reductions?")
        
    elif meeting_type == "Making an offer":
        st.markdown("### 💰 Negotiation Strategy")
        st.write("**Before the meeting:**")
        st.write("• Research comparable sales yourself")
        st.write("• Set your maximum budget (don't tell the agent)")
        st.write("• Decide on contingencies you want")
        st.write("• Prepare to walk away")
        st.write("• Get pre-approved by multiple lenders")
        
        st.markdown("### 🎯 Key Questions")
        st.write("• What's the lowest offer you think they'd accept?")
        st.write("• How many other offers are there really?")
        st.write("• What contingencies would you recommend?")
        st.write("• How will you present our offer to stand out?")
        st.write("• What are comparable homes selling for?")
        st.write("• What's your commission if we offer less?")
    
    elif meeting_type == "Negotiation":
        st.markdown("### 🤝 Negotiation Preparation")
        st.write("**Your Position:**")
        st.write("• Know your walk-away price")
        st.write("• Have financing pre-approved")
        st.write("• Research market conditions")
        st.write("• Identify property weaknesses")
        st.write("• Understand seller's motivation")
        
        st.markdown("### 💪 Negotiation Questions")
        st.write("• What motivated this counteroffer?")
        st.write("• Which terms are most important to the seller?")
        st.write("• What happens if we can't reach agreement?")
        st.write("• Are there other interested parties?")
        st.write("• What's the seller's timeline?")
    
    elif meeting_type == "Contract review":
        st.markdown("### 📋 Contract Review Checklist")
        st.write("**Must Review:**")
        st.write("• All financial terms and deadlines")
        st.write("• Contingency clauses")
        st.write("• Who pays which fees")
        st.write("• Repair responsibilities")
        st.write("• Closing date and possession")
        st.write("• Commission disclosure")
        
        st.markdown("### ⚠️ Watch Out For")
        st.write("• Blank spaces to be filled later")
        st.write("• Unusual or excessive fees")
        st.write("• Limited contingency periods")
        st.write("• Automatic renewal clauses")
        st.write("• Dual agency disclosures")
    
    elif meeting_type == "Closing preparation":
        st.markdown("### 🏁 Closing Preparation")
        st.write("**Bring to Closing:**")
        st.write("• Government-issued photo ID")
        st.write("• Certified funds for closing costs")
        st.write("• Homeowner's insurance proof")
        st.write("• Final walk-through notes")
        st.write("• Copy of purchase agreement")
        
        st.markdown("### 🔍 Final Questions")
        st.write("• Are all agreed-upon repairs completed?")
        st.write("• Are all utilities transferred?")
        st.write("• When do I get the keys?")
        st.write("• What happens if there are last-minute issues?")
        st.write("• Are all fees exactly as estimated?")
    
    st.markdown("### 📋 Universal Meeting Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Always Bring")
        st.write("• Written list of questions")
        st.write("• Calculator for quick math")
        st.write("• Notebook for taking notes")
        st.write("• Relevant documents")
        st.write("• A trusted advisor/friend")
        st.write("• Voice recorder (if legal in your state)")
    
    with col2:
        st.markdown("#### 🚫 Never Do")
        st.write("• Sign anything same day")
        st.write("• Give access to all your finances")
        st.write("• Agree to exclusivity immediately")
        st.write("• Accept verbal agreements only")
        st.write("• Make decisions under pressure")
        st.write("• Let emotions override logic")

else:
    st.error("Please select a tool from the sidebar to get started!")

# Footer
st.markdown("---")
st.markdown("**Decoder Universe** - Empowering everyday people to make better financial decisions")
st.markdown("*Part of the consumer advocacy suite for working families*")
st.markdown("**Version 11** - Complete integrated version with comprehensive databases")

# Sidebar navigation
st.sidebar.title("🏠 Navigation")
main_tool = st.sidebar.selectbox(
    "Choose a Tool:",
    ["🚀 Quick Start", 
     "📄 Document Analysis", 
     "💰 Commission Calculator", 
     "⚠️ Conflict Checker",
     "🗣️ Realtor-Speak Decoder", 
     "🧠 Psychology",
     "🎯 Defense", 
     "🚩 Red Flag Checker",
     "📚 Glossary",
     "📝 Meeting Prep Tool"]
)

# Quick Start
if main_tool == "🚀 Quick Start":
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
        st.info("**New to real estate?** Start with 'Glossary' to understand key terms.")
        st.warning("**Feeling pressured?** Go to 'Defense' for immediate help.")
        st.success("**Before any meeting?** Use 'Meeting Prep Tool' to prepare.")
        
        st.markdown("### 🚨 Emergency Red Flags")
        st.error("**STOP** if agent says:")
        st.write("• 'Sign now or lose the deal'")
        st.write("• 'Don't worry about reading that'")
        st.write("• 'Trust me on this one'")
        st.write("• 'Everyone else is doing it'")

# Document Analysis
elif main_tool == "📄 Document Analysis":
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
elif main_tool == "💰 Commission Calculator":
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
    
    # Commission impact calculator
    st.markdown("### 💰 Commission Impact on Your Purchase")
    st.write(f"**Remember:** The seller pays commission, but it's built into the home price.")
    st.write(f"**Your real cost:** Commission is factored into what you pay for the home.")
    st.write(f"**Negotiation opportunity:** In a buyer's market, you may be able to negotiate commission into the price.")

# Conflict Checker
elif main_tool == "⚠️ Conflict Checker":
    st.markdown('<h2 class="section-header">⚠️ Conflict Checker</h2>', unsafe_allow_html=True)
    st.write("Identify potential conflicts of interest with your real estate agent.")
    
    st.markdown("### 🔍 Check for These Conflicts")
    
    conflicts = [
        "Agent represents both buyer and seller (dual agency)",
        "Agent receives kickbacks from recommended lenders",
        "Agent owns or has interest in the property",
        "Agent is related to the seller",
        "Agent gets higher commission from certain lenders",
        "Agent pushes specific properties they have listings on",
        "Agent discourages you from shopping around for services",
        "Agent has relationships with inspectors/appraisers",
        "Agent won't disclose their compensation structure",
        "Agent pressures you to use their title company"
    ]
    
    detected_conflicts = []
    for conflict in conflicts:
        if st.checkbox(conflict):
            detected_conflicts.append(conflict)
    
    if detected_conflicts:
        st.markdown(f'<div class="danger-box"><strong>🚨 {len(detected_conflicts)} Potential Conflicts Detected!</strong><br>These conflicts may not be illegal, but they could affect the advice you receive.</div>', unsafe_allow_html=True)
        
        st.markdown("### ⚖️ What This Means")
        st.write("• Your agent may prioritize their interests over yours")
        st.write("• You may not be getting the best deal available")
        st.write("• Consider getting independent advice")
        st.write("• Ask for written disclosure of all relationships")
        st.write("• You have the right to separate representation")
    else:
        st.success("✅ No obvious conflicts detected. Stay vigilant!")
    
    st.markdown("### 📋 Questions to Ask About Conflicts")
    conflict_questions = [
        "Do you represent both buyers and sellers?",
        "What compensation do you receive from lenders, title companies, or inspectors?",
        "Do you have any financial interest in properties you're showing me?",
        "How does your commission change based on the price or lender I choose?",
        "Are you related to or friends with the seller?",
        "Do you get bonuses for using certain service providers?"
    ]
    
    for question in conflict_questions:
        st.write(f"• {question}")

# Realtor-Speak Decoder
elif main_tool == "🗣️ Realtor-Speak Decoder":
    st.markdown('<h2 class="section-header">🗣️ Realtor-Speak Decoder</h2>', unsafe_allow_html=True)
    
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
            if "pressure" in meaning.lower() or "rush" in meaning.lower():
                st.warning("🚨 This is a pressure tactic!")

# Psychology
elif main_tool == "🧠 Psychology":
    st.markdown('<h2 class="section-header">🧠 Psychology Behind Real Estate Sales</h2>', unsafe_allow_html=True)
    
    st.write("Understanding the psychological tactics used in real estate can help you make better decisions and resist manipulation.")
    
    for tactic, details in psychology_database.items():
        with st.expander(f"🎯 {tactic}"):
            st.write(f"**What it is:** {details['description']}")
            st.write(f"**How it works:** {details['how_it_works']}")
            st.write("**Examples:**")
            for example in details['examples']:
                st.write(f"• '{example}'")
            st.markdown(f'<div class="info-box"><strong>Psychology Behind It:</strong> {details["psychology_behind"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="success-box"><strong>Your Defense:</strong> {details["defense"]}</div>', unsafe_allow_html=True)
            st.write("**Say this instead:**")
            for counter in details['counter_phrases']:
                st.write(f"• '{counter}'")
    
    st.markdown("### 🧠 Why These Tactics Work")
    st.write("**Fear of Missing Out (FOMO):** Agents create artificial scarcity to trigger quick decisions")
    st.write("**Authority Bias:** We tend to trust professionals even when they have conflicts of interest")
    st.write("**Time Pressure:** Rushed decisions prevent us from thinking clearly or getting second opinions")
    st.write("**Social Proof:** We assume if others are doing something, it must be right")
    
    st.markdown('<div class="warning-box"><strong>Remember:</strong> A good agent will encourage you to take time and ask questions. Pressure tactics are red flags.</div>', unsafe_allow_html=True)

# Defense
elif main_tool == "🎯 Defense":
    st.markdown('<h2 class="section-header">🎯 Defense Strategies</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🛡️ Defense Against Common Tactics")
    
    defense_strategies = {
        "When they say 'Act Now'": {
            "Response": "I need time to think about this decision. When is the actual deadline?",
            "Why it works": "Forces them to be specific and removes false urgency"
        },
        "When they push their lender": {
            "Response": "I'll need to compare rates from multiple lenders before deciding.",
            "Why it works": "Shows you're informed and won't be rushed into expensive financing"
        },
        "When they discourage inspections": {
            "Response": "I'm not comfortable waiving inspections. What are you worried we might find?",
            "Why it works": "Makes them explain their real concerns"
        },
        "When they say 'Trust me'": {
            "Response": "I appreciate your advice. Can you put that recommendation in writing?",
            "Why it works": "Professionals should stand behind their advice"
        },
        "When they push higher offers": {
            "Response": "What's the lowest offer you think might be accepted?",
            "Why it works": "Gets them thinking about realistic negotiation range"
        },
        "When they create urgency": {
            "Response": "If this is really the right house for me, I'll still want it tomorrow.",
            "Why it works": "Shows you won't be rushed and tests their claims"
        },
        "When they mention 'other interested buyers'": {
            "Response": "Can you show me written proof of other offers?",
            "Why it works": "Most agents can't prove this claim because it's often false"
        },
        "When they get defensive about questions": {
            "Response": "I'm just trying to make an informed decision. Can you help me understand?",
            "Why it works": "Professional agents should welcome questions, not resist them"
        }
    }
    
    for situation, defense in defense_strategies.items():
        with st.expander(situation):
            st.markdown(f"**Say this:** '{defense['Response']}'")
            st.markdown(f"**Why it works:** {defense['Why it works']}")
    
    st.markdown("### 📝 Universal Defense Rules")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Always Do")
        st.write("• Take time to think (at least 24 hours)")
        st.write("• Get everything in writing")
        st.write("• Compare at least 3 options")
        st.write("• Bring a knowledgeable friend")
        st.write("• Research comparable sales yourself")
        st.write("• Ask 'How does this benefit you?'")
        st.write("• Verify all information independently")
        st.write("• Set your maximum budget privately")
    
    with col2:
        st.markdown("#### 🚫 Never Do")
        st.write("• Sign anything the same day")
        st.write("• Accept verbal promises")
        st.write("• Let emotions drive decisions")
        st.write("• Work with agents who pressure you")
        st.write("• Skip due diligence steps")
        st.write("• Assume their interests align with yours")
        st.write("• Give full financial details upfront")
        st.write("• Waive inspections or contingencies")

# Red Flag Checker  
elif main_tool == "🚩 Red Flag Checker":
    st.markdown('<h2 class="section-header">🚩 Red Flag Checker</h2>', unsafe_allow_html=True)
    
    st.write("Check off any behaviors you've experienced with your agent:")
    
    # Organize red flags by category
    categories = {}
    for flag, details in red_flag_database.items():
        category = details['category']
        if category not in categories:
            categories[category] = []
        categories[category].append((flag, details))
    
    total_flagged = 0
    critical_flags = 0
    
    for category, flags in categories.items():
        st.markdown(f"### 🔍 {category} Red Flags")
        
        for flag, details in flags:
            if st.checkbox(flag):
                total_flagged += 1
                if details['severity'] == 'Critical':
                    critical_flags += 1
                
                # Show severity indicator
                if details['severity'] == 'Critical':
                    st.markdown(f'<div class="danger-box"><strong>🚨 CRITICAL:</strong> {details["why_dangerous"]}</div>', unsafe_allow_html=True)
                elif details['severity'] == 'High':
                    st.markdown(f'<div class="warning-box"><strong>⚠️ HIGH RISK:</strong> {details["why_dangerous"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="info-box"><strong>⚡ MEDIUM RISK:</strong> {details["why_dangerous"]}</div>', unsafe_allow_html=True)
                
                st.write(f"**Immediate Action:** {details['immediate_action']}")
                st.write(f"**Legal Status:** {details['legal_status']}")
                st.markdown("---")
    
    # Summary and recommendations
    if total_flagged > 0:
        if critical_flags > 0:
            st.markdown(f'<div class="danger-box"><strong>🚨 CRITICAL WARNING:</strong> You\'ve identified {critical_flags} critical red flags and {total_flagged} total red flags. Consider ending this relationship immediately and seeking legal advice.</div>', unsafe_allow_html=True)
        elif total_flagged >= 3:
            st.markdown(f'<div class="warning-box"><strong>⚠️ WARNING:</strong> You\'ve identified {total_flagged} red flags. This agent may not be working in your best interests. Consider switching agents.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-box"><strong>⚡ CAUTION:</strong> You\'ve identified {total_flagged} red flag(s). Stay vigilant and document all interactions.</div>', unsafe_allow_html=True)
        
        st.markdown("### 🛡️ Recommended Actions:")
        st.write("• Document all interactions in writing with dates/times")
        st.write("• Get multiple agent opinions on any major decisions")
        st.write("• Consider switching to a different agent")
        st.write("• Consult with a real estate attorney if needed")
        st.write("• Report serious violations to your state's real estate commission")
        st.write("• Don't proceed with major decisions until issues are resolved")
    else:
        st.success("✅ No red flags detected. Continue with caution and stay informed!")
    
    st.markdown("### 🚨 Emergency Red Flags")
    emergency_flags = [
        "Agent asks you to sign blank documents",
        "Agent refuses to provide written agreements",
        "Agent pressures you to lie on loan applications",
        "Agent won't let you read contracts thoroughly",
        "Agent demands payment upfront before services",
        "Agent threatens you for asking questions"
    ]
    
    st.markdown('<div class="danger-box"><strong>🚨 STOP IMMEDIATELY if any of these occur:</strong></div>', unsafe_allow_html=True)
    for flag in emergency_flags:
        st.write(f"• {flag}")

# Glossary
elif main_tool == "📚 Glossary":
    st.markdown('<h2 class="section-header">📚 Real Estate Glossary</h2>', unsafe_allow_html=True)
    
    # Search functionality
    search_term = st.text_input("🔍 Search for a term:")
    
    if search_term:
        filtered_terms = {}
        for term, details in glossary_database.items():
            if (search_term.lower() in term.lower() or 
                search_term.lower() in details['definition'].lower() or
                search_term.lower() in details['consumer_impact'].lower()):
                filtered_terms[term] = details
        
        if filtered_terms:
            for term, details in filtered_terms.items():
                with st.expander(f"📖 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    
                    # Red flag indicator
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 HIGH RED FLAG: {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ WATCH OUT: {details['what_to_ask']}")
                    else:
                        st.info(f"💡 GOOD TO KNOW: {details['what_to_ask']}")
                    
                    if details['negotiable']:
                        st.success("✅ This is often negotiable!")
                    else:
                        st.info("ℹ️ This is typically non-negotiable")
        else:
            st.info("No matching terms found. Try a different search or browse categories below.")
    else:
        # Category tabs
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial", "🏠 Property", "📈 Market", "📋 Legal"])
        
        financial_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Financial'}
        property_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Property'}
        market_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Market'}
        legal_terms = {k: v for k, v in glossary_database.items() if v['category'] == 'Legal'}
        
        with tab1:
            for term, details in financial_terms.items():
                with st.expander(f"💰 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
                    if details['negotiable']:
                        st.success("✅ Often negotiable!")
        
        with tab2:
            for term, details in property_terms.items():
                with st.expander(f"🏠 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
        
        with tab3:
            for term, details in market_terms.items():
                with st.expander(f"📈 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
        
        with tab4:
            for term, details in legal_terms.items():
                with st.expander(f"📋 {term}"):
                    st.write(f"**Definition:** {details['definition']}")
                    st.markdown(f'<div class="info-box"><strong>Impact on You:</strong> {details["consumer_impact"]}</div>', unsafe_allow_html=True)
                    if details['red_flag_level'] == 'High':
                        st.error(f"🚨 {details['what_to_ask']}")
                    elif details['red_flag_level'] == 'Medium':
                        st.warning(f"⚠️ {details['what_to_ask']}")
                    if details['negotiable']:
                        st.success("✅ Often negotiable!")

# Meeting Prep Tool
elif main_tool == "📝 Meeting Prep Tool":
    st.markdown('<h2 class="section-header">📝 Meeting Prep Tool</h2>', unsafe_allow_html=True)
    
    meeting_type = st.selectbox("What type of meeting are you preparing for?", 
                               ["First meeting with agent", "Property viewing", "Making an offer", 
                                "Negotiation", "Contract review", "Closing preparation"])
    
    if meeting_type == "First meeting with agent":
        st.markdown("### 🎯 Essential Questions to Ask")
        questions = [
            "What is your commission rate and is it negotiable?",
            "Do you ever represent both buyers and sellers?",
            "How many homes have you sold in the last 12 months?",
            "What services do you provide for your commission?",
            "Can you provide references from recent clients?",
            "What is your strategy for finding/selling homes?",
            "How do you handle multiple offers?",
            "What other compensation do you receive in this transaction?",
            "Can you show me your license and any complaints against you?",
            "What happens if I'm not satisfied with your services?"
        ]
        for q in questions:
            st.write(f"• {q}")
            
        st.markdown("### 🚨 Red Flags in First Meeting")
        st.write("• Won't answer commission questions directly")
        st.write("• Pressures you to sign exclusive agreement immediately")
        st.write("• Can't provide recent client references")
        st.write("• Gets defensive about dual agency questions")
        st.write("• Won't show you their credentials")
            
    elif meeting_type == "Property viewing":
        st.markdown("### 🔍 What to Look For")
        st.write("**Red Flags:**")
        st.write("• Agent rushes you through the property")
        st.write("• Discourages questions about problems")
        st.write("• Pushes you to make immediate decisions")
        st.write("• Won't let you take photos or measurements")
        st.write("• Avoids showing you certain areas")
        
        st.markdown("### ❓ Important Questions")
        st.write("• How long has this been on the market?")
        st.write("• Why is the seller moving?")
        st.write("• What repairs or issues are known?")
        st.write("• What would you offer if you were buying?")
        st.write("• Are there any upcoming assessments or HOA changes?")
        st.write("• What were the results of the last inspection?")
        st.write("• Have there been any price reductions?")
        
    elif meeting_type == "Making an offer":
        st.markdown("### 💰 Negotiation Strategy")
        st.write("**Before the meeting:**")
        st.write("• Research comparable sales yourself")
        st.write("• Set your maximum budget (don't tell the agent)")
        st.write("• Decide on contingencies you want")
        st.write("• Prepare to walk away")
        st.write("• Get pre-approved by multiple lenders")
        
        st.markdown("### 🎯 Key Questions")
        st.write("• What's the lowest offer you think they'd accept?")
        st.write("• How many other offers are there really?")
        st.write("• What contingencies would you recommend?")
        st.write("• How will you present our offer to stand out?")
        st.write("• What are comparable homes selling for?")
        st.write("• What's your commission if we offer less?")
    
    elif meeting_type == "Negotiation":
        st.markdown("### 🤝 Negotiation Preparation")
        st.write("**Your Position:**")
        st.write("• Know your walk-away price")
        st.write("• Have financing pre-approved")
        st.write("• Research market conditions")
        st.write("• Identify property weaknesses")
        st.write("• Understand seller's motivation")
        
        st.markdown("### 💪 Negotiation Questions")
        st.write("• What motivated this counteroffer?")
        st.write("• Which terms are most important to the seller?")
        st.write("• What happens if we can't reach agreement?")
        st.write("• Are there other interested parties?")
        st.write("• What's the seller's timeline?")
    
    elif meeting_type == "Contract review":
        st.markdown("### 📋 Contract Review Checklist")
        st.write("**Must Review:**")
        st.write("• All financial terms and deadlines")
        st.write("• Contingency clauses")
        st.write("• Who pays which fees")
        st.write("• Repair responsibilities")
        st.write("• Closing date and possession")
        st.write("• Commission disclosure")
        
        st.markdown("### ⚠️ Watch Out For")
        st.write("• Blank spaces to be filled later")
        st.write("• Unusual or excessive fees")
        st.write("• Limited contingency periods")
        st.write("• Automatic renewal clauses")
        st.write("• Dual agency disclosures")
    
    elif meeting_type == "Closing preparation":
        st.markdown("### 🏁 Closing Preparation")
        st.write("**Bring to Closing:**")
        st.write("• Government-issued photo ID")
        st.write("• Certified funds for closing costs")
        st.write("• Homeowner's insurance proof")
        st.write("• Final walk-through notes")
        st.write("• Copy of purchase agreement")
        
        st.markdown("### 🔍 Final Questions")
        st.write("• Are all agreed-upon repairs completed?")
        st.write("• Are all utilities transferred?")
        st.write("• When do I get the keys?")
        st.write("• What happens if there are last-minute issues?")
        st.write("• Are all fees exactly as estimated?")
    
    st.markdown("### 📋 Universal Meeting Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Always Bring")
        st.write("• Written list of questions")
        st.write("• Calculator for quick math")
        st.write("• Notebook for taking notes")
        st.write("• Relevant documents")
        st.write("• A trusted advisor/friend")
        st.write("• Voice recorder (if legal in your state)")
    
    with col2:
        st.markdown("#### 🚫 Never Do")
        st.write("• Sign anything same day")
        st.write("• Give access to all your finances")
        st.write("• Agree to exclusivity immediately")
        st.write("• Accept verbal agreements only")
        st.write("• Make decisions under pressure")
        st.write("• Let emotions override logic")

else:
    st.error("Please select a tool from the sidebar to get started!")

# Footer
st.markdown("---")
st.markdown("**Decoder Universe** - Empowering everyday people to make better financial decisions")
st.markdown("*Part of the consumer advocacy suite for working families*")
st.markdown("**Version 11** - Complete integrated version with comprehensive databases")
