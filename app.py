from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for popup chat

# Updated website structure for Pentapolis Foundation based on actual website
WEBSITE_STRUCTURE = {
    "home": {
        "url": "/",
        "keywords": ["home", "homepage", "main", "index", "landing", "start", "pentapolis foundation"],
        "description": "Main homepage",
        "sections": []
    },
    "about": {
        "url": "/about-us",
        "keywords": ["about", "about us", "who we are", "organization", "foundation", "mission", "vision", "team", "story", "history", "background", "sathish kumar", "director general"],
        "description": "About Pentapolis Foundation",
        "sections": [
            {"name": "Our Mission", "url": "/about"},
            {"name": "Our Team", "url": "/about"},
            {"name": "Director General", "url": "/about"}
        ]
    },
    "contact": {
        "url": "/contact",
        "keywords": ["contact", "contact us", "reach us", "get in touch", "phone", "email", "address", "location", "office", "headquarters"],
        "description": "Contact information and form",
        "sections": []
    },
    "naps": {
        "url": "/naps",
        "keywords": ["naps", "national apprenticeship promotion scheme", "apprenticeship program", "government scheme", "apprentice", "naps program"],
        "description": "NAPS - National Apprenticeship Promotion Scheme",
        "sections": [
            {"name": "Program Details", "url": "/naps#details"},
            {"name": "Eligibility", "url": "/naps#eligibility"},
            {"name": "Apply Now", "url": "/naps#apply"}
        ]
    },
    "nats": {
        "url": "/nats", 
        "keywords": ["nats", "national apprenticeship training scheme", "apprenticeship training", "skill development", "nats program"],
        "description": "NATS - National Apprenticeship Training Scheme",
        "sections": [
            {"name": "Program Overview", "url": "/nats#overview"},
            {"name": "Training Modules", "url": "/nats#modules"},
            {"name": "Registration", "url": "/nats#register"}
        ]
    },
    "reap": {
        "url": "/governance",
        "keywords": ["reap", "reap program", "rural employment", "agriculture", "farming", "rural development"],
        "description": "REAP - Rural Employment and Agriculture Program",
        "sections": [
            {"name": "Rural Development", "url": "/reap#rural"},
            {"name": "Agriculture Support", "url": "/reap#agriculture"},
            {"name": "Employment Opportunities", "url": "/reap#employment"}
        ]
    },
    "step": {
        "url": "/governance",
        "keywords": ["step", "step program", "skill training", "employment", "job training", "vocational training"],
        "description": "STEP - Skill Training and Employment Program",
        "sections": [
            {"name": "Skill Training", "url": "/step#training"},
            {"name": "Employment Support", "url": "/step#employment"},
            {"name": "Career Guidance", "url": "/step#career"}
        ]
    },
    "skill_development": {
        "url": "/skill-development",
        "keywords": ["skill development", "skills", "training", "capacity building", "upskilling", "reskilling", "competency", "talent development"],
        "description": "Skill development programs",
        "sections": [
            {"name": "Training Programs", "url": "/skill-development#programs"},
            {"name": "Certification", "url": "/skill-development#certification"},
            {"name": "Industry Partnership", "url": "/skill-development#partnership"}
        ]
    },
    "employment": {
        "url": "/employment",
        "keywords": ["employment", "jobs", "career", "placement", "job opportunities", "staffing", "recruitment", "hiring"],
        "description": "Employment opportunities and placement",
        "sections": [
            {"name": "Job Opportunities", "url": "/employment#jobs"},
            {"name": "Placement Support", "url": "/employment#placement"},
            {"name": "Career Counseling", "url": "/employment#counseling"}
        ]
    },
    "nation_builders": {
        "url": "/nation-builders",
        "keywords": ["nation builders", "nation building", "leadership", "future leaders", "youth leadership", "development", "next generation"],
        "description": "Nation-building initiatives for future leaders",
        "sections": [
            {"name": "Leadership Program", "url": "/nation-builders#leadership"},
            {"name": "Youth Development", "url": "/nation-builders#youth"},
            {"name": "Community Impact", "url": "/nation-builders#impact"}
        ]
    },
    "social_justice": {
        "url": "/social-justice",
        "keywords": ["social justice", "justice", "equity", "equality", "rights", "fair", "inclusive", "social change"],
        "description": "Social justice initiatives",
        "sections": [
            {"name": "Equity Programs", "url": "/social-justice#equity"},
            {"name": "Community Rights", "url": "/social-justice#rights"},
            {"name": "Inclusive Development", "url": "/social-justice#inclusive"}
        ]
    },
    "partnerships": {
        "url": "/partnerships",
        "keywords": ["partnerships", "corporate partners", "collaborations", "alliances", "tie-ups", "stakeholders", "institutions"],
        "description": "Corporate and institutional partnerships",
        "sections": [
            {"name": "Corporate Partners", "url": "/partnerships#corporate"},
            {"name": "Government Collaboration", "url": "/partnerships#government"},
            {"name": "Academic Institutions", "url": "/partnerships#academic"}
        ]
    },
    "donate": {
        "url": "/donate",
        "keywords": ["donate", "donation", "contribute", "support us", "give", "charity", "fund", "financial support", "contribute"],
        "description": "Support our cause through donations",
        "sections": [
            {"name": "One-time Donation", "url": "/donate"},
            {"name": "Monthly Giving", "url": "/donate"},
            {"name": "Corporate Sponsorship", "url": "/donate"}
        ]
    },
    "events": {
        "url": "/events",
        "keywords": ["events", "workshops", "seminars", "conferences", "training sessions", "activities", "calendar"],
        "description": "Upcoming events and workshops",
        "sections": [
            {"name": "Upcoming Events", "url": "/calendar"},
            {"name": "Workshop Calendar", "url": "/calendar"},
            {"name": "Past Events", "url": "/calendar"}
        ]
    },
    "blog": {
        "url": "/blog",
        "keywords": ["news", "updates", "announcements", "press", "media", "latest", "current"],
        "description": "Latest blog and updates",
        "sections": []
    },
    "gallery": {
        "url": "/gallery",
        "keywords": ["gallery", "photos", "images", "pictures", "albums", "visual", "media gallery"],
        "description": "Photo gallery of our work",
        "sections": []
    },
    "careers": {
        "url": "/careers",
        "keywords": ["careers", "jobs", "employment", "hiring", "work with us", "opportunities", "join us", "recruitment"],
        "description": "Career opportunities with Pentapolis Foundation",
        "sections": [
            {"name": "Current Openings", "url": "/careers#openings"},
            {"name": "Application Process", "url": "/careers#process"},
            {"name": "Benefits", "url": "/careers#benefits"}
        ]
    },
    "volunteers": {
        "url": "/contact",
        "keywords": ["volunteers", "volunteer", "volunteering", "join", "help", "contribute", "support", "get involved"],
        "description": "Volunteer opportunities",
        "sections": [
            {"name": "Volunteer Roles", "url": "/contact"},
            {"name": "Registration", "url": "/contact"},
            {"name": "Volunteer Benefits", "url": "/contact"}
        ]
    }
}

class PopupWebsiteChatbot:
    def __init__(self, website_structure):
        self.website_structure = website_structure
        self.greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste"]
        self.help_keywords = ["help", "what can you do", "commands", "options", "assist", "guide", "menu"]
        self.search_keywords = ["find", "where", "show", "locate", "search", "looking for", "need", "want"]
        self.thanks_keywords = ["thank", "thanks", "thank you", "thx", "appreciate"]
        self.goodbye_keywords = ["bye", "goodbye", "see you", "later", "exit", "quit"]
    
    def normalize_text(self, text):
        """Normalize text for better matching"""
        return re.sub(r'[^\w\s]', '', text.lower().strip())
    
    def calculate_page_score(self, page_info, user_input):
        """Calculate relevance score for a page based on user input"""
        score = 0
        normalized_input = self.normalize_text(user_input)
        
        for keyword in page_info["keywords"]:
            keyword_lower = keyword.lower()
            
            # Exact keyword match
            if keyword_lower == normalized_input:
                score += 20
            # Keyword appears in input
            elif keyword_lower in normalized_input:
                score += 10
            # Individual words match
            else:
                keyword_words = keyword_lower.split()
                input_words = normalized_input.split()
                matches = sum(1 for word in keyword_words if word in input_words)
                if matches > 0:
                    score += matches * 3
        
        return score
    
    def find_page(self, user_input):
        """Find the most relevant page based on user input with scoring"""
        page_scores = {}
        
        for page_name, page_info in self.website_structure.items():
            score = self.calculate_page_score(page_info, user_input)
            if score > 0:
                page_scores[page_name] = score
        
        if page_scores:
            # Get the best match
            best_page = max(page_scores, key=page_scores.get)
            # If score is very low, suggest multiple options
            if page_scores[best_page] < 5:
                return None, None
            return best_page, self.website_structure[best_page]
        
        return None, None
    
    def get_suggested_pages(self, count=6):
        """Get a list of suggested page names for help responses"""
        popular_pages = ["home", "about", "contact", "naps", "nats", "reap", "step", "skill_development", "employment", "donate"]
        available_pages = list(self.website_structure.keys())
        
        # Return popular pages that exist, then fill with others
        suggestions = [page for page in popular_pages if page in available_pages]
        remaining = [page for page in available_pages if page not in suggestions]
        
        return (suggestions + remaining)[:count]
    
    def generate_response(self, user_input):
        """Generate contextual response based on user input"""
        if not user_input.strip():
            return {
                "message": "Please ask me something! I can help you find pages on our website.",
                "type": "empty_input"
            }
        
        normalized_input = self.normalize_text(user_input)
        
        # Handle greetings
        if any(greeting in normalized_input for greeting in self.greetings):
            return {
                "message": "🙏 Namaste! I'm CHRIS, your Pentapolis Foundation website assistant. I can help you navigate to any section of our website. What are you looking for today?",
                "type": "greeting",
                "pages": self.get_suggested_pages(4)
            }
        
        # Handle thanks
        if any(thanks in normalized_input for thanks in self.thanks_keywords):
            return {
                "message": "😊 You're welcome! Is there anything else I can help you find on our website?",
                "type": "thanks"
            }
        
        # Handle goodbyes
        if any(bye in normalized_input for bye in self.goodbye_keywords):
            return {
                "message": "👋 Goodbye! Feel free to ask me anytime if you need help finding pages on our website.",
                "type": "goodbye"
            }
        
        # Handle help requests
        if any(help_word in normalized_input for help_word in self.help_keywords):
            return {
                "message": "🔍 I can help you find any page on the Pentapolis Foundation website! Here are some popular sections you can ask about:",
                "type": "help",
                "pages": self.get_suggested_pages(8)
            }
        
        # Look for specific page requests
        page_name, page_info = self.find_page(user_input)
        
        if page_info:
            # Create more natural response based on what they asked
            if any(word in normalized_input for word in ["where", "find", "locate"]):
                message = f"📍 The {page_info['description']} can be found here:"
            elif any(word in normalized_input for word in ["show", "take me", "go to"]):
                message = f"✅ Here's the {page_info['description']}:"
            else:
                message = f"✅ Found it! {page_info['description']}:"
            
            response = {
                "message": message,
                "type": "page_found",
                "page_name": page_name,
                "url": page_info["url"],
                "description": page_info["description"]
            }
            
            # Add sections if available
            if page_info.get("sections"):
                response["sections"] = page_info["sections"]
                response["has_sections"] = True
            
            return response
        
        # Handle general search queries
        if any(search_word in normalized_input for search_word in self.search_keywords):
            return {
                "message": "🔍 I couldn't find that specific page. Here are all the sections I can help you locate on the Pentapolis Foundation website:",
                "type": "search_help",
                "pages": list(self.website_structure.keys())
            }
        
        # Default response with suggestions
        return {
            "message": "🤔 I'm not sure what you're looking for. I can help you find these popular sections on the Pentapolis Foundation website:",
            "type": "not_found",
            "pages": self.get_suggested_pages(6)
        }

# Initialize chatbot
chatbot = PopupWebsiteChatbot(WEBSITE_STRUCTURE)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint with section support"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip() if data else ''
        
        if not user_message:
            return jsonify({
                "error": "Please enter a message",
                "message": "Please ask me something! I can help you find pages on our website.",
                "type": "empty_input"
            }), 400
        
        # Generate response using chatbot
        response = chatbot.generate_response(user_message)
        
        # Add timestamp
        response['timestamp'] = datetime.now().strftime("%H:%M")
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Chat error: {str(e)}")
        
        return jsonify({
            "error": "Something went wrong",
            "message": "😅 Sorry, I had a little hiccup. Please try asking again!",
            "type": "error",
            "timestamp": datetime.now().strftime("%H:%M")
        }), 500

@app.route('/pages')
def get_pages():
    """API endpoint to get all available pages"""
    return jsonify({
        "pages": WEBSITE_STRUCTURE,
        "total_pages": len(WEBSITE_STRUCTURE),
        "page_names": list(WEBSITE_STRUCTURE.keys())
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chatbot": "ready",
        "pages_available": len(WEBSITE_STRUCTURE)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "This endpoint doesn't exist. Try /chat for chatbot or /pages for page list.",
        "type": "not_found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "message": "This endpoint requires a different HTTP method.",
        "type": "method_error"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "😅 Something went wrong on our end. Please try again!",
        "type": "server_error"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
