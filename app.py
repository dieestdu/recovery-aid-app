import streamlit as st
import openai
import os

# Load the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Please set it as an environment variable named 'OPENAI_API_KEY'.")
else:
    # Set OpenAI API key
    openai.api_key = openai_api_key

# Streamlit app title
st.title("Recovery Aid Finder for Fitness Injuries")

# Section 0: User Name Input
st.header("Welcome")
user_name = st.text_input("Please enter your name:")

# Section 1: Body Part Selection
st.header("Step 1: Where do you feel discomfort or pain?")
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

# Add secondary dropdown or input for complex body parts
if body_part == "Upper Back (Traps, Scapulae, Lats)":
    specific_part = st.selectbox("Specify the area:", ["Traps", "Scapulae", "Lats", "Other"])
    if specific_part == "Other":
        other_part = st.text_input("Please specify the body part:")

elif body_part == "Lower Back (Center, Left, Right, All Low Back)":
    specific_part = st.selectbox("Specify the area:", ["Center", "Left", "Right", "All Low Back"])

elif body_part == "Arm (Biceps, Triceps, Forearm)":
    specific_part = st.selectbox("Specify the area:", ["Biceps", "Triceps", "Forearm"])

elif body_part == "Thigh (Quadriceps, Hamstrings, IT Band, Adductors, Abductors)":
    specific_part = st.selectbox("Specify the area:", ["Quadriceps", "Hamstrings", "IT Band", "Adductors", "Abductors"])

elif body_part == "Lower Leg (Calf, Shin)":
    specific_part = st.selectbox("Specify the area:", ["Calf", "Shin"])

elif body_part == "Foot & Ankle (Achilles, Heel, Arch)":
    specific_part = st.selectbox("Specify the area:", ["Achilles", "Heel", "Arch"])

# Section 2: Pain Sensation
st.header("Step 2: How would you describe the pain or discomfort?")
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

# Follow-up for Clicking/Popping Sound
if "Clicking/popping sound (with or without pain)" in pain_type:
    clicking_with_pain = st.radio("Is the clicking/popping sound accompanied by pain?", ["Yes", "No"])

# Section 3: Pain Severity
st.header("Step 3: Rate the severity of your pain (1-10)")
pain_severity = st.slider(
    "Pain severity:", min_value=1, max_value=10, value=5,
    help="1 = Barely noticeable, 5 = Interferes with daily activities, 10 = Unbearable, requiring immediate attention."
)

# Section 4: Onset of Pain
st.header("Step 4: When does the pain occur?")
pain_occurrence = st.multiselect("Select all that apply:", [
    "During exercise",
    "After exercise",
    "All the time",
    "When waking up",
    "At night",
    "Other (specify)"
])
if "Other (specify)" in pain_occurrence:
    other_pain_occurrence = st.text_input("Please specify:")

pain_duration = st.selectbox("When did the pain start?", [
    "<24 hours ago",
    "1–3 days ago",
    "1 week ago",
    "More than 1 week ago"
])

# Section 5: Activity Context
st.header("Step 5: Describe the activity or movement that caused or worsens your discomfort.")
activity_context = st.selectbox("What activity caused the discomfort?", [
    "Running",
    "Cycling",
    "Lifting weights",
    "Tennis/Pádel",
    "General sports",
    "Office work",
    "Other"
])
activity_description = st.text_area(
    "Describe the specific movement (e.g., 'Squatting with 80kg')."
)

# Section 6: Relief Factors
st.header("Step 6: Have you found anything that reduces the pain or discomfort?")
relief_methods = st.multiselect("Select all that apply:", [
    "Rest",
    "Ice/Heat",
    "Stretching",
    "Massage",
    "Anti-inflammatories",
    "Nothing tried yet"
])
relief_effectiveness = st.radio("How effective are these methods?", [
    "Not effective at all",
    "Somewhat effective",
    "Very effective"
])

# Section 7: DOMS Differentiation
st.header("Step 7: Is this general soreness or localized pain?")
pain_localization = st.radio("Is the pain localized to a specific area or generalized across a muscle group?", [
    "Localized to a specific joint or spot",
    "Generalized across a muscle group"
])
# Initialize doms_improvement with a default value
if pain_localization == "Localized to a specific joint or spot":
    doms_improvement = "Not applicable"

if pain_localization == "Generalized across a muscle group":
    doms_improvement = st.radio("Has the discomfort improved with light movement or rest?", ["Yes, it feels better.", "No, it feels the same or worse."])

# Section 8: Functional Impact
st.header("Step 8: How is the pain affecting your ability to perform daily tasks or workouts?")
functional_impact = st.radio("Select one:", [
    "Minimal impact",
    "I’ve had to modify my workouts",
    "I’ve stopped exercising altogether"
])

# Section 9: Red Flag Identification
st.header("Step 9: Have you experienced any of the following symptoms?")
red_flags = st.multiselect("Select all that apply:", [
    "No",
    "Sudden, severe swelling",
    "Inability to bear weight",
    "Persistent numbness or tingling",
    "Pain not improving after a week",
    "Fever or chills associated with the pain",
    "Recent trauma or injury to the area",
    "Other unusual symptoms"
])
if "Other unusual symptoms" in red_flags:
    other_red_flags = st.text_input("Please specify:")

# Section 10: Injury History
st.header("Step 10: Have you had any similar injuries in the past?")
previous_injuries = st.radio("", ["Yes", "No"])
if previous_injuries == "Yes":
    injury_details = st.text_area("Please describe your previous injuries.")

# Section 11: Open Input
st.header("Step 11: Anything else you'd like us to know?")
additional_notes = st.text_area("Provide any additional context about your pain or discomfort.")

# Submit and Get Advice
if st.button("Get Recovery Advice"):
    st.info("Processing your input...")

    try:
        # OpenAI ChatGPT API call using GPT-4 with enhanced logic
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly trained virtual physiotherapist specializing in fitness and sports-related injuries. "
                        "Your role is to provide scientifically sound, user-centric recovery recommendations based on evidence-based practices. "
                        "Adhere to physiotherapy principles and prioritize user safety. Follow the SOAP methodology: Gather subjective inputs, analyze objectively, assess probable issues, and provide a plan. "
                        "Your advice should align with modern recovery frameworks, rather than outdated methods like RICE. "
                        "Educate users on why the injury occurred, how to recover, and how to prevent future issues. Avoid medical diagnoses but indicate red-flag symptoms that require professional attention. "
                        "Prioritize movement-based solutions (mobility and strength/stability exercises) as the primary intervention. Modify exercise intensity or volume if needed. Use rest only as a last resort and recommend it alongside professional consultation. "
                        "For all recommendations, include specific exercises, sets, reps, and video links where applicable. Dynamically adapt to the user's inputs, ensuring personalized and actionable advice for recovery and prevention. "
                        "Responses should follow this format:\n"
                        "Recovery Recommendation\n"
                        "Immediate Recovery Steps:\n"
                        "1. Provide the best mobility or stability exercise for immediate relief: name and explain it with clear instructions (e.g., 'Hip flexor stretch'). Include sets, reps, and a video link if applicable.\n"
                        "2. Provide the best mobility or stability exercise for immediate relief: name and explain it with clear instructions (e.g., 'Hip flexor stretch'). Include sets, reps, and a video link if applicable.\n"
                        "Preventive Strategies:\n"
                        "1. Suggest an additional actionable step (e.g., regression, activation, or deloading strategies) tailored to the user's input.\n"
                        "2. Suggest a strength or stability exercise addressing the root cause: name and explain it with sets, reps, and an explanation of how it prevents future injuries. Include a video link if applicable.\n"
                        "3. Provide guidance on improving movement mechanics or technique for long-term prevention, with examples or regressions as necessary.\n"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Hello {user_name},\n"
                        f"Based on your input, you are experiencing {', '.join(pain_type)} in your {body_part}.\n"
                        f"- Specific area: {specific_part if body_part in ['Upper Back (Traps, Scapulae, Lats)', 'Lower Back (Center, Left, Right, All Low Back)', 'Arm (Biceps, Triceps, Forearm)', 'Thigh (Quadriceps, Hamstrings, IT Band, Adductors, Abductors)', 'Lower Leg (Calf, Shin)', 'Foot & Ankle (Achilles, Heel, Arch)'] else ''}\n"
                        f"- Pain severity on a scale of 1 to 10: {pain_severity}\n"
                        f"- Onset of pain: {pain_duration}\n"
                        f"- Activity context: {activity_context}\n"
                        f"- Movement description: {activity_description}\n"
                        f"- Relief factors: {', '.join(relief_methods)} (Effectiveness: {relief_effectiveness})\n"
                        f"- DOMS differentiation: {pain_localization} (Improved with movement: {'Yes' if doms_improvement == 'Yes, it feels better.' else 'No'})\n"
                        f"- Red flags: {', '.join(red_flags)}\n"
                        f"- Additional context: {additional_notes}"
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

