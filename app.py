import streamlit as st
import openai
import os

# Load the API key from the environment variable
openai_api_key = st.secrets["OPENAI_API_KEY"]

if not openai_api_key:
    st.error("OpenAI API key not found. Please set it as an environment variable.")
else:
    openai.api_key = openai_api_key

# Streamlit app title
st.title("Recovery Aid Finder for Fitness Injuries")

# Section 0: User Name Input
st.header("Welcome")
user_name = st.text_input("Please enter your name:")

# Section 1: User Profile & Training History (New)
st.header("Step 1: About You & Your Training History")
exercise_type = st.selectbox("What is your primary form of exercise?", [
    "General fitness",
    "Strength training (powerlifting, bodybuilding)",
    "Endurance sports (running, cycling, swimming)",
    "Sport-specific training (tennis, football, etc.)",
    "Other"
])

training_experience = st.selectbox("How many years have you been training?", [
    "Less than 6 months",
    "6 months – 1 year",
    "1–3 years",
    "3+ years"
])

training_frequency = st.selectbox("How many times a week do you train?", [
    "1–2 times",
    "3–4 times",
    "5+ times"
])

past_injuries = st.radio("Have you had similar injuries in the past?", ["Yes", "No"])
if past_injuries == "Yes":
    past_injury_details = st.text_area("Please describe your previous injuries.")

# Section 2: Body Part Selection
st.header("Step 2: Where do you feel discomfort or pain?")
body_part = st.selectbox("Choose a body part:", [
    "Head & Neck",
    "Shoulder",
    "Upper Back (Traps, Scapulae, Lats)",
    "Lower Back (Center, Left, Right, All Low Back)",
    "Arm (Biceps, Triceps, Forearm)",
    "Hand & Wrist",
    "Elbow",
    "Hip & Groin",
    "Thigh (Quadriceps, Hamstrings, IT Band, Adductors, Abductors)",
    "Glutes",
    "Knee",
    "Lower Leg (Calf, Shin)",
    "Foot & Ankle (Achilles, Heel, Arch)"
])

# Section 3: Pain Sensation
st.header("Step 3: How would you describe the pain or discomfort?")
pain_type = st.multiselect("Select all that apply:", [
    "Sharp pain",
    "Dull ache",
    "Stiffness",
    "Swelling",
    "Tightness",
    "Tingling/numbness",
    "Burning sensation",
    "Throbbing",
    "Shooting pain",
    "Cramping",
    "Weakness",
    "Clicking/popping sound (with or without pain)"
])

# Unilateral vs Bilateral Pain
pain_side = st.radio("Is the pain on one side or both sides?", ["Unilateral (Left/Right)", "Bilateral"])

# Pain Triggers
st.header("Step 4: Pain Modifiers")
pain_worsens = st.multiselect("What makes the pain worse?", [
    "Repetitive movements",
    "Heavy loads",
    "Sudden movements",
    "Sitting for long periods",
    "Other"
])

pain_improves = st.multiselect("What makes the pain feel better?", [
    "Warm-up",
    "Stretching",
    "Load reduction",
    "Rest",
    "Other"
])

pain_trend = st.radio("Has the pain been gradually worsening or staying the same?", [
    "Gradually increasing",
    "Staying the same",
    "Improving"
])

# Section 5: Movement-Based Pain Triggers
st.header("Step 5: Movement-Based Pain Triggers")
movement_triggers = []
if body_part in ["Knee", "Hip & Groin", "Lower Leg (Calf, Shin)", "Foot & Ankle (Achilles, Heel, Arch)"]:
    movement_triggers = st.multiselect("Select the movements that trigger pain:", [
        "Squatting",
        "Lunging",
        "Jumping",
        "Running",
        "Walking uphill/downhill",
        "Bending forward"
    ])
elif body_part in ["Shoulder", "Elbow", "Arm (Biceps, Triceps, Forearm)"]:
    movement_triggers = st.multiselect("Select the movements that trigger pain:", [
        "Pressing (bench press, overhead press)",
        "Pulling (pull-ups, rows, deadlifts)",
        "Rotational movements (throwing, swinging)",
        "Repetitive typing/mouse use"
    ])

# Section 6: Recovery Progress Monitoring (New)
st.header("Step 6: Recovery Progress Monitoring")
recovery_feedback = st.radio("After following the recommended exercises, has your pain changed?", [
    "Improved",
    "No change",
    "Worse"
])

adjust_recommendations = st.radio("Would you like to adjust your recommendations based on progress?", ["Yes", "No"])

# Submit and Get Advice
if st.button("Get Recovery Advice"):
    st.info("Processing your input...")

    try:
        # OpenAI ChatGPT API call using GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert virtual physiotherapist providing recovery strategies for fitness-related injuries. "
                        "Your recommendations MUST prioritize movement-based interventions (mobility, strength, technique corrections) over passive treatments. "
                        "Avoid suggesting complete rest unless it’s a red-flag injury. Adjust your recommendations based on the user's training experience, pain timing, and symptom trends. "
                        "Responses should follow this structured format:\n"
                        "Recovery Recommendation\n"
                        "Immediate Recovery Steps:\n"
                        "1. Best movement-based exercise for immediate relief (name, how to perform it, reps, video link if applicable).\n"
                        "2. Second-best movement-based exercise for immediate relief (same structure).\n"
                        "Preventive Strategies:\n"
                        "1. Technique/movement correction strategy tailored to the user’s input.\n"
                        "2. Strength/stability exercise addressing the root cause (with reps and explanation).\n"
                        "Provide brief scientific reasoning for each recommendation."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Hello {user_name},\n"
                        f"Based on your input, you are experiencing {', '.join(pain_type)} in your {body_part}.\n"
                        f"- Pain severity: {pain_trend}\n"
                        f"- Pain is worsened by: {', '.join(pain_worsens)}\n"
                        f"- Pain improves with: {', '.join(pain_improves)}\n"
                        f"- Movement triggers: {', '.join(movement_triggers)}\n"
                        f"- Training experience: {training_experience}\n"
                        f"- Recovery progress: {recovery_feedback}\n"
                        f"Please provide the best movement-based recovery strategy following the format requested."
                    )
                }
            ],
            max_tokens=750,
            temperature=0.7
        )
        advice = response["choices"][0]["message"]["content"].strip()

        st.success("Here is your recovery advice:")
        st.write(advice)

    except Exception as e:
        st.error(f"Error communicating with OpenAI API: {e}")
