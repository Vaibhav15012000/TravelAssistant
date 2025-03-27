import streamlit as st
import requests
import cohere

# Set Cohere API key
co = cohere.Client("7F4u3gSqaut45bDIDrxwldXq6MdXHIXLVnWpA5NH")

# Pexels API Key (Replace with your actual API key)
PEXELS_API_KEY = "2rw8Awi0FizklY7vOS6TDIaRV8oGQL0L96XlklmZ5SRUQDJCfProTnCE"

# Set Page Config
st.set_page_config(page_title="Personal Travel Assistant", page_icon="🌍", layout="wide")

# Custom CSS for scrollable background image and fixed aspect ratio
st.markdown(
    """
    <style>
        /* Ensuring background image scrolls */
        .stApp {
            background: url('https://img.freepik.com/premium-photo/travel-concept-around-world-with-landmarks-white-background_41969-15557.jpg?w=2000') no-repeat right;
            background-size: cover; /* Ensures image does not stretch */
            overflow-y: scroll; /* Enables scrolling */
        }

        /* Content styling */
        .main {
            background: rgba(255, 255, 255, 0.85);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        }

        /* Title styling */
        .title {
            color: #2E86C1; 
            text-align: center; 
            font-size: 40px; 
            font-weight: bold;
        }

        /* Section header styling */
        .section-header {
            color: #154360; 
            font-size: 24px; 
            font-weight: bold;
        }

        /* Info card styling */
        .info-card {
            background: white; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1); 
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>🌍 Personal Travel Assistant</h1>", unsafe_allow_html=True)

# Sidebar for User Input
with st.sidebar:
    st.header("👤 Personal Details")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)
    num_travelers = st.number_input("Number of travelers:", min_value=1, step=1)
    departure_location = st.text_input("Departure City:")
    trip_type = st.text_input("Which type of trip you are planning?:")

    st.header("🏨 Accommodation & Special Needs")
    num_rooms = st.number_input("Number of hotel rooms:", min_value=1, step=1)

    has_seniors = st.checkbox("Senior citizens traveling?")
    num_seniors = st.number_input("Number of seniors:", min_value=0, step=1) if has_seniors else 0
    senior_ages = st.text_input("Ages of senior citizens (comma-separated):") if has_seniors else "None"

    has_children = st.checkbox("Children traveling?")
    num_children = st.number_input("Number of children:", min_value=0, step=1) if has_children else 0
    child_ages = st.text_input("Ages of children (comma-separated):") if has_children else "None"

    st.header("✈️ Travel Preferences")
    destination = st.text_input("Travel destination:")
    trip_days = st.number_input("Trip duration (days):", min_value=1, step=1)
    budget = st.selectbox("Select your budget:", ["Low ($500-$1000)", "Medium ($1000-$3000)", "Luxury ($3000+)"])
    interests = st.text_area("Your travel interests:")
    special_requirements = st.text_area("Special requirements:")

# Function to Fetch Images
def get_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=3"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["large"]
    return "https://via.placeholder.com/400"

# Generate Itinerary
if st.button("🚀 Generate Travel Plan"):
    with st.spinner("Planning your trip..."):
        prompt = f"""
        You are a professional travel assistant. Plan a detailed {trip_days}-day trip for {name}, aged {age}, traveling with {num_travelers} people.
        Departure from: {departure_location}
        Trip Type: {trip_type}
        Destination: {destination}
        Budget: {budget}
        Interests: {interests}
        Special Requirements: {special_requirements}
        Accommodation: {num_rooms} rooms needed.
        Senior Citizens: {num_seniors}, Ages: {senior_ages}
        Children: {num_children}, Ages: {child_ages}

        Create a structured, detailed itinerary covering:
        - Flight details (arrival & departure times)
        - Breakfast, lunch, and dinner options with restaurant suggestions
        - Morning, afternoon, and evening activities each day
        - Must-visit attractions based on interests
        - Accessibility needs for seniors & children
        - Relaxation time or free exploration slots

        Format the itinerary clearly, listing Day 1, Day 2, etc.
        """
        response = co.generate(model="command", prompt=prompt, max_tokens=1200)
        
        st.success("✅ Here's your personalized travel itinerary:")

        itinerary_text = response.generations[0].text.split("\n\n")

        # Layout: Display Itinerary and Images in Columns
        col1, col2 = st.columns(2)

        for day in itinerary_text:
            if day.strip():
                with col1:
                    st.markdown(f"<div class='info-card'><h3>{day.split(':')[0]}</h3><p>{day}</p></div>", unsafe_allow_html=True)

                # Extract keyword for image search
                keyword = destination if "-" not in day else day.split("-")[1].strip()
                image_url = get_image(keyword)

                with col2:
                    st.image(image_url, caption=f"{keyword}", use_container_width=True)