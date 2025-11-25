# # mental_health_fuzzy.py
# """
# Fuzzy Mental Health Assessment 
# """

# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
# import streamlit as st

# # ----------------- HELPERS -----------------
# def keyword_emergency_check(text):
#     if not text:
#         return False, []
#     txt = text.lower()
#     keywords = [
#         "suicide", "kill myself", "killing myself", "suicidal", "hurt myself",
#         "no point", "hopeless", "die", "death", "kill me"
#     ]
#     found = [k for k in keywords if k in txt]
#     emergency_triggers = ["suicide", "kill myself", "killing myself", "suicidal", "hurt myself", "kill me"]
#     is_emergency = any(k in txt for k in emergency_triggers)
#     return is_emergency, found

# # ----------------- IMPROVED RECOMMENDATIONS -----------------
# def generate_recommendations(score, patterns):
#     recommendations = []

#     # ------------------------------------
#     # SCORE-BASED INTERPRETATION
#     # ------------------------------------
#     if score <= 2:
#         recommendations.append(
#             "Your distress level appears low. Maintain your current healthy routines such as consistent sleep, hydration, and regular movement."
#         )

#     elif 2 < score <= 4:
#         recommendations.append(
#             "Your distress is mild. A short self-care break, a walk, or light breathing exercises can help stabilize your emotional state."
#         )

#     elif 4 < score <= 6:
#         recommendations.append(
#             "Your distress is moderate. Consider structured breaks, reducing workload temporarily, and practicing grounding techniques. Prioritize tasks and avoid overstimulation."
#         )

#     elif 6 < score <= 8:
#         recommendations.append(
#             "Your distress is high. It may help to slow down, reduce commitments where possible, and talk to a trusted person or counselor. Mindfulness and relaxation exercises can help significantly."
#         )

#     else:  # score > 8
#         recommendations.append(
#             "Your distress is very high. Please seek emotional support immediately—reach out to a mental health professional or someone you trust. Avoid isolation and practice grounding exercises."
#         )

#     # ------------------------------------
#     # PATTERN-BASED ANALYSIS
#     # ------------------------------------
#     if patterns:

#         if "Appetite Change" in patterns:
#             recommendations.append(
#                 "- Appetite changes detected. Try maintaining consistent meals and hydration. If this persists for more than a week, consider consulting a healthcare professional."
#             )

#         if "Sleep Irregularity" in patterns:
#             recommendations.append(
#                 "- Sleep irregularities noted. Aim for a stable sleep-wake schedule and reduce late-night screen use."
#             )

#         if "Low Motivation" in patterns:
#             recommendations.append(
#                 "- Low motivation observed. Break tasks into very small steps and acknowledge small achievements. Behavioral activation can help boost momentum."
#             )

#         if "Anxiety Indicators" in patterns:
#             recommendations.append(
#                 "- Anxiety patterns detected. Try slow breathing exercises (4-4-6 method) or grounding techniques like the 5-4-3-2-1 sensory tool."
#             )

#         if "Social Withdrawal" in patterns:
#             recommendations.append(
#                 "- Reduced social interaction detected. A short conversation with a familiar person can help stabilize emotional state."
#             )

#         if "Irritability Spike" in patterns:
#             recommendations.append(
#                 "- Increased irritability detected. Short pauses, hydration, and stepping outside briefly can reduce overstimulation."
#             )

#         if "Low Energy Pattern" in patterns:
#             recommendations.append(
#                 "- Low energy levels identified. Light stretching, hydration, and stepping outside for sunlight can boost alertness."
#             )

#     # ------------------------------------
#     # GENERAL FALLBACK
#     # ------------------------------------
#     if not recommendations:
#         recommendations.append(
#             "No concerning patterns detected, but maintaining balanced sleep, hydration, nutrition, and movement is always beneficial."
#         )

#     return recommendations

# # ----------------- FUZZY VARIABLES -----------------
# u = np.linspace(0, 10, 101)

# # Moods
# happiness = ctrl.Antecedent(u, 'happiness')
# anxiety = ctrl.Antecedent(u, 'anxiety')
# sadness = ctrl.Antecedent(u, 'sadness')
# irritability = ctrl.Antecedent(u, 'irritability')
# calmness = ctrl.Antecedent(u, 'calmness')

# # Functioning
# stress = ctrl.Antecedent(u, 'stress')
# sleep_quality = ctrl.Antecedent(u, 'sleep_quality')
# energy = ctrl.Antecedent(u, 'energy')
# motivation = ctrl.Antecedent(u, 'motivation')
# concentration = ctrl.Antecedent(u, 'concentration')

# # Behavior
# appetite = ctrl.Antecedent(u, 'appetite')
# social = ctrl.Antecedent(u, 'social')
# workload = ctrl.Antecedent(u, 'workload')

# # Consequent
# distress = ctrl.Consequent(u, 'distress')
# distress['low'] = fuzz.trimf(distress.universe, [0, 0, 4])
# distress['moderate'] = fuzz.trimf(distress.universe, [3, 5, 7])
# distress['high'] = fuzz.trimf(distress.universe, [6, 10, 10])

# # Standard membership sets
# def add_lmh(ant):
#     ant['low'] = fuzz.trimf(ant.universe, [0, 0, 4])
#     ant['medium'] = fuzz.trimf(ant.universe, [2, 5, 8])
#     ant['high'] = fuzz.trimf(ant.universe, [6, 10, 10])

# for ant in [
#     happiness, anxiety, sadness, irritability, calmness,
#     stress, sleep_quality, energy, motivation, concentration,
#     appetite, social, workload
# ]:
#     add_lmh(ant)

# # ----------------- RULE BASE -----------------
# rules = []

# # Complex multi-factor rules
# rules.append(ctrl.Rule(stress['high'] & sleep_quality['low'], distress['high']))
# rules.append(ctrl.Rule(anxiety['high'] & concentration['low'], distress['high']))
# rules.append(ctrl.Rule(sadness['high'] & motivation['low'] & social['low'], distress['high']))
# rules.append(ctrl.Rule(workload['high'] & energy['low'] & stress['high'], distress['high']))
# rules.append(ctrl.Rule(irritability['high'] & sleep_quality['low'] & stress['high'], distress['high']))

# rules.append(ctrl.Rule(happiness['high'] & calmness['high'] & stress['low'], distress['low']))
# rules.append(ctrl.Rule(energy['high'] & motivation['high'] & sleep_quality['high'], distress['low']))

# rules.append(ctrl.Rule(anxiety['high'] & sleep_quality['low'], distress['moderate']))
# rules.append(ctrl.Rule(sadness['medium'] & motivation['low'], distress['moderate']))
# rules.append(ctrl.Rule(appetite['low'] | appetite['high'], distress['moderate']))

# # Baseline rules for full coverage
# baseline = [
#     (happiness, 'high', 'low'), (happiness, 'low', 'moderate'),
#     (anxiety, 'high', 'high'), (anxiety, 'medium', 'moderate'),
#     (sadness, 'high', 'high'), (sadness, 'medium', 'moderate'),
#     (irritability, 'high', 'high'), (irritability, 'low', 'low'),
#     (calmness, 'high', 'low'), (calmness, 'low', 'moderate'),
#     (stress, 'high', 'high'), (stress, 'medium', 'moderate'),
#     (sleep_quality, 'low', 'high'), (sleep_quality, 'high', 'low'),
#     (energy, 'low', 'high'), (energy, 'high', 'low'),
#     (motivation, 'low', 'high'), (motivation, 'high', 'low'),
#     (concentration, 'low', 'high'), (concentration, 'high', 'low'),
#     (appetite, 'low', 'moderate'), (appetite, 'high', 'moderate'),
#     (social, 'low', 'moderate'), (social, 'high', 'low'),
#     (workload, 'high', 'high'), (workload, 'low', 'low'),
# ]

# for ant, lvl, out in baseline:
#     rules.append(ctrl.Rule(ant[lvl], distress[out]))

# # Build control system
# distress_ctrl = ctrl.ControlSystem(rules)
# distress_sim = ctrl.ControlSystemSimulation(distress_ctrl)

# # ----------------- STREAMLIT UI -----------------
# st.set_page_config(page_title="Fuzzy Mental Health Assessment", layout="wide")
# st.title("Fuzzy Mental Health Assessment (0–10 Continuous Inputs)")

# st.markdown("""
# Move the sliders to reflect your current emotional and functional state.
# Then press **Run Fuzzy Assessment**.
# """)

# col1, col2 = st.columns(2)

# with col1:
#     st.header("Mood & Affect")
#     happiness_val = st.slider("Happiness", 0.0, 10.0, 0.0, 0.1)
#     anxiety_val = st.slider("Anxiety", 0.0, 10.0, 0.0, 0.1)
#     sadness_val = st.slider("Sadness", 0.0, 10.0, 0.0, 0.1)
#     irritability_val = st.slider("Irritability", 0.0, 10.0, 0.0, 0.1)
#     calmness_val = st.slider("Calmness", 0.0, 10.0, 0.0, 0.1)

# with col2:
#     st.header("Functioning & Behavior")
#     stress_val = st.slider("Stress", 0.0, 10.0, 0.0, 0.1)
#     sleep_val = st.slider("Sleep quality", 0.0, 10.0, 0.0, 0.1)
#     energy_val = st.slider("Energy", 0.0, 10.0, 0.0, 0.1)
#     motivation_val = st.slider("Motivation", 0.0, 10.0, 0.0, 0.1)
#     concentration_val = st.slider("Concentration", 0.0, 10.0, 0.0, 0.1)

# st.header("Other Factors")
# col3, col4, col5 = st.columns(3)
# with col3:
#     appetite_val = st.slider("Appetite normality", 0.0, 10.0, 0.0, 0.1)
# with col4:
#     social_val = st.slider("Social activity", 0.0, 10.0, 0.0, 0.1)
# with col5:
#     workload_val = st.slider("Workload pressure", 0.0, 10.0, 0.0, 0.1)

# st.header("Free text (optional)")
# free_text = st.text_area("Enter any details you'd like the system to consider:")
# self_harm = st.checkbox("Have you had thoughts of self-harm?")

# # ----------------- RUN -----------------
# if st.button("Run Fuzzy Assessment"):

#     # Emergency screening
#     is_emg, found = keyword_emergency_check(free_text)
#     if self_harm or is_emg:
#         st.error("⚠ EMERGENCY TRIGGERED — Indicators of self-harm detected. Seek immediate help.")
#         if found:
#             st.write("Keywords found:", found)

#     # Fuzzy inputs
#     inputs = {
#         'happiness': happiness_val,
#         'anxiety': anxiety_val,
#         'sadness': sadness_val,
#         'irritability': irritability_val,
#         'calmness': calmness_val,
#         'stress': stress_val,
#         'sleep_quality': sleep_val,
#         'energy': energy_val,
#         'motivation': motivation_val,
#         'concentration': concentration_val,
#         'appetite': appetite_val,
#         'social': social_val,
#         'workload': workload_val
#     }

#     for key, val in inputs.items():
#         distress_sim.input[key] = val

#     # Compute
#     try:
#         distress_sim.compute()
#         score = float(distress_sim.output['distress'])
#     except Exception as e:
#         st.error("Fuzzy computation error: " + str(e))
#         score = None

#     # ----------------- OUTPUT -----------------
#     st.subheader("Results")

#     if score is not None:
#         st.write("### Final Distress Score:", round(score, 2))

#         if score <= 3:
#             st.success("Risk Level: LOW")
#         elif score <= 7:
#             st.warning("Risk Level: MODERATE")
#         else:
#             st.error("Risk Level: HIGH")

#         # ----------------- PATTERN DETECTION -----------------
#         patterns = []

#         if appetite_val <= 3 or appetite_val >= 8:
#             patterns.append("Appetite Change")

#         if sleep_val <= 4:
#             patterns.append("Sleep Irregularity")

#         if motivation_val <= 3:
#             patterns.append("Low Motivation")

#         if anxiety_val >= 6:
#             patterns.append("Anxiety Indicators")

#         if social_val <= 2:
#             patterns.append("Social Withdrawal")

#         if irritability_val >= 6:
#             patterns.append("Irritability Spike")

#         if energy_val <= 3:
#             patterns.append("Low Energy Pattern")

#         st.write("### Detected Patterns:")
#         if patterns:
#             st.write(patterns)
#         else:
#             st.write("No significant patterns detected.")

#         # ----------------- RECOMMENDATIONS -----------------
#         st.write("### Recommendations")
#         recs = generate_recommendations(score, patterns)
#         for r in recs:
#             st.write("- " + r)

#     else:
#         st.write("Final distress score could not be computed.")






# mental_health_fuzzy.py
"""
Fuzzy Mental Health Assessment
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st

# ----------------- HELPERS -----------------
def keyword_emergency_check(text):
    if not text:
        return False, []
    txt = text.lower()
    keywords = [
        "suicide", "kill myself", "killing myself", "suicidal", "hurt myself",
        "no point", "hopeless", "die", "death", "kill me"
    ]
    found = [k for k in keywords if k in txt]
    # stronger triggers that indicate immediate concern
    emergency_triggers = ["suicide", "kill myself", "killing myself", "suicidal", "hurt myself", "kill me"]
    is_emergency = any(k in txt for k in emergency_triggers)
    return is_emergency, found

# ----------------- IMPROVED RECOMMENDATIONS -----------------
def generate_recommendations(score, patterns, crisis_trigger=False):
    recommendations = []

    # ------------------------------------
    # SCORE-BASED INTERPRETATION
    # ------------------------------------
    if score is None:
        recommendations.append("Unable to compute distress score.")
        return recommendations

    if score <= 2:
        recommendations.append(
            "Your distress level appears low. Maintain healthy routines such as consistent sleep, hydration, and regular movement."
        )

    elif 2 < score <= 4:
        recommendations.append(
            "Your distress is mild. A short self-care break, a walk, or light breathing exercises can help stabilize your emotional state."
        )

    elif 4 < score <= 6:
        recommendations.append(
            "Your distress is moderate. Consider structured breaks, reducing workload temporarily, and practicing grounding techniques. Prioritize tasks and avoid overstimulation."
        )

    elif 6 < score <= 8:
        recommendations.append(
            "Your distress is high. It may help to slow down, reduce commitments where possible, and talk to a trusted person or counselor. Mindfulness and relaxation exercises can help significantly."
        )

    else:  # score > 8
        recommendations.append(
            "Your distress is very high. Please seek emotional support immediately—reach out to a mental health professional or someone you trust. Avoid isolation and practice grounding exercises."
        )

    # ------------------------------------
    # PATTERN-BASED ANALYSIS
    # ------------------------------------
    if patterns:

        if "Appetite Change" in patterns:
            recommendations.append(
                "- Appetite changes detected. Try maintaining consistent meals and hydration. If this persists for more than a week, consider consulting a healthcare professional."
            )

        if "Sleep Irregularity" in patterns:
            recommendations.append(
                "- Sleep irregularities noted. Aim for a stable sleep-wake schedule and reduce late-night screen use."
            )

        if "Low Motivation" in patterns:
            recommendations.append(
                "- Low motivation observed. Break tasks into very small steps and acknowledge small achievements. Behavioral activation can help boost momentum."
            )

        if "Anxiety Indicators" in patterns:
            recommendations.append(
                "- Anxiety patterns detected. Try slow breathing exercises (4-4-6 method) or grounding techniques like the 5-4-3-2-1 sensory tool."
            )

        if "Social Withdrawal" in patterns:
            recommendations.append(
                "- Reduced social interaction detected. A short conversation with a familiar person can help stabilize emotional state."
            )

        if "Irritability Spike" in patterns:
            recommendations.append(
                "- Increased irritability detected. Short pauses, hydration, and stepping outside briefly can reduce overstimulation."
            )

        if "Low Energy Pattern" in patterns:
            recommendations.append(
                "- Low energy levels identified. Light stretching, hydration, and stepping outside for sunlight can boost alertness."
            )

        if "Suicidal Ideation" in patterns:
            recommendations.append(
                "- Suicidal thoughts detected. You deserve immediate support. Consider reaching out to someone you trust, a crisis line, or local emergency services. If you are in immediate danger, call your local emergency number."
            )

        if "Self-harm Thoughts" in patterns:
            recommendations.append(
                "- Self-harm thoughts detected. Please prioritize immediate safety: avoid being alone if possible, remove access to means, and contact a trusted person or professional."
            )

    # ------------------------------------
    # CRISIS-SPECIFIC
    # ------------------------------------
    if crisis_trigger:
        # Additional urgent, non-directive guidance
        recommendations.append(
            "- You are showing signs of significant distress. If thoughts of harming yourself are present or intensifying, contact local emergency services or a crisis helpline right away. If possible, stay with someone you trust while you seek help."
        )

    # ------------------------------------
    # GENERAL FALLBACK
    # ------------------------------------
    if not recommendations:
        recommendations.append(
            "No concerning patterns detected, but maintaining balanced sleep, hydration, nutrition, and movement is always beneficial."
        )

    return recommendations

# ----------------- FUZZY VARIABLES -----------------
u = np.linspace(0, 10, 101)

# Moods
happiness = ctrl.Antecedent(u, 'happiness')
anxiety = ctrl.Antecedent(u, 'anxiety')
sadness = ctrl.Antecedent(u, 'sadness')
irritability = ctrl.Antecedent(u, 'irritability')
calmness = ctrl.Antecedent(u, 'calmness')

# Functioning
stress = ctrl.Antecedent(u, 'stress')
sleep_quality = ctrl.Antecedent(u, 'sleep_quality')
energy = ctrl.Antecedent(u, 'energy')
motivation = ctrl.Antecedent(u, 'motivation')
concentration = ctrl.Antecedent(u, 'concentration')

# Behavior
appetite = ctrl.Antecedent(u, 'appetite')
social = ctrl.Antecedent(u, 'social')
workload = ctrl.Antecedent(u, 'workload')

# Consequent
distress = ctrl.Consequent(u, 'distress')
distress['low'] = fuzz.trimf(distress.universe, [0, 0, 4])
distress['moderate'] = fuzz.trimf(distress.universe, [3, 5, 7])
distress['high'] = fuzz.trimf(distress.universe, [6, 10, 10])

# Standard membership sets helper
def add_lmh(ant):
    ant['low'] = fuzz.trimf(ant.universe, [0, 0, 4])
    ant['medium'] = fuzz.trimf(ant.universe, [2, 5, 8])
    ant['high'] = fuzz.trimf(ant.universe, [6, 10, 10])

for ant in [
    happiness, anxiety, sadness, irritability, calmness,
    stress, sleep_quality, energy, motivation, concentration,
    appetite, social, workload
]:
    add_lmh(ant)

# ----------------- RULE BASE -----------------
rules = []

# Complex multi-factor rules
rules.append(ctrl.Rule(stress['high'] & sleep_quality['low'], distress['high']))
rules.append(ctrl.Rule(anxiety['high'] & concentration['low'], distress['high']))
rules.append(ctrl.Rule(sadness['high'] & motivation['low'] & social['low'], distress['high']))
rules.append(ctrl.Rule(workload['high'] & energy['low'] & stress['high'], distress['high']))
rules.append(ctrl.Rule(irritability['high'] & sleep_quality['low'] & stress['high'], distress['high']))

rules.append(ctrl.Rule(happiness['high'] & calmness['high'] & stress['low'], distress['low']))
rules.append(ctrl.Rule(energy['high'] & motivation['high'] & sleep_quality['high'], distress['low']))

rules.append(ctrl.Rule(anxiety['high'] & sleep_quality['low'], distress['moderate']))
rules.append(ctrl.Rule(sadness['medium'] & motivation['low'], distress['moderate']))
rules.append(ctrl.Rule(appetite['low'] | appetite['high'], distress['moderate']))

# Baseline rules for full coverage
baseline = [
    (happiness, 'high', 'low'), (happiness, 'low', 'moderate'),
    (anxiety, 'high', 'high'), (anxiety, 'medium', 'moderate'),
    (sadness, 'high', 'high'), (sadness, 'medium', 'moderate'),
    (irritability, 'high', 'high'), (irritability, 'low', 'low'),
    (calmness, 'high', 'low'), (calmness, 'low', 'moderate'),
    (stress, 'high', 'high'), (stress, 'medium', 'moderate'),
    (sleep_quality, 'low', 'high'), (sleep_quality, 'high', 'low'),
    (energy, 'low', 'high'), (energy, 'high', 'low'),
    (motivation, 'low', 'high'), (motivation, 'high', 'low'),
    (concentration, 'low', 'high'), (concentration, 'high', 'low'),
    (appetite, 'low', 'moderate'), (appetite, 'high', 'moderate'),
    (social, 'low', 'moderate'), (social, 'high', 'low'),
    (workload, 'high', 'high'), (workload, 'low', 'low'),
]

for ant, lvl, out in baseline:
    rules.append(ctrl.Rule(ant[lvl], distress[out]))

# Build control system
distress_ctrl = ctrl.ControlSystem(rules)
distress_sim = ctrl.ControlSystemSimulation(distress_ctrl)

# ----------------- STREAMLIT UI -----------------
st.set_page_config(page_title="Fuzzy Mental Health Assessment", layout="wide")
st.title("Fuzzy Mental Health Assessment")

st.markdown("""
Move the sliders to reflect your current emotional and functional state.
Then press **Run Fuzzy Assessment**.
""")

col1, col2 = st.columns(2)

with col1:
    st.header("Mood & Affect")
    happiness_val = st.slider("Happiness", 0.0, 10.0, 0.0, 0.1)
    anxiety_val = st.slider("Anxiety", 0.0, 10.0, 0.0, 0.1)
    sadness_val = st.slider("Sadness", 0.0, 10.0, 0.0, 0.1)
    irritability_val = st.slider("Irritability", 0.0, 10.0, 0.0, 0.1)
    calmness_val = st.slider("Calmness", 0.0, 10.0, 0.0, 0.1)

with col2:
    st.header("Functioning & Behavior")
    stress_val = st.slider("Stress", 0.0, 10.0, 0.0, 0.1)
    sleep_val = st.slider("Sleep quality", 0.0, 10.0, 0.0, 0.1)
    energy_val = st.slider("Energy", 0.0, 10.0, 0.0, 0.1)
    motivation_val = st.slider("Motivation", 0.0, 10.0, 0.0, 0.1)
    concentration_val = st.slider("Concentration", 0.0, 10.0, 0.0, 0.1)

st.header("Other Factors")
col3, col4, col5 = st.columns(3)
with col3:
    appetite_val = st.slider("Appetite normality", 0.0, 10.0, 0.0, 0.1)
with col4:
    social_val = st.slider("Social activity", 0.0, 10.0, 0.0, 0.1)
with col5:
    workload_val = st.slider("Workload pressure", 0.0, 10.0, 0.0, 0.1)

st.header("Safety-related Factors")
col_s1, col_s2 = st.columns(2)
with col_s1:
    suicidal_val = st.slider("Suicidal thoughts (0 = none, 10 = frequent/intense)", 0.0, 10.0, 0.0, 0.1)
with col_s2:
    selfharm_val = st.slider("Self-harm thoughts (0 = none, 10 = frequent/intense)", 0.0, 10.0, 0.0, 0.1)

st.header("Free text (optional)")
free_text = st.text_area("Enter any details you'd like the system to consider:")

# ----------------- RUN -----------------
if st.button("Run Fuzzy Assessment"):

    # Emergency screening (free text)
    is_emg, found = keyword_emergency_check(free_text)

    # If any suicide/self-harm slider is non-zero OR emergency keyword found, show immediate alert
    pre_emergency = False
    if suicidal_val > 0 or selfharm_val > 0 or is_emg:
        pre_emergency = True
        st.error("⚠ EMERGENCY TRIGGERED — Indicators of suicidal ideation or self-harm detected. Seek immediate help.")
        if found:
            st.write("Keywords found in text:", found)

    # Fuzzy inputs (crisp)
    inputs = {
        'happiness': happiness_val,
        'anxiety': anxiety_val,
        'sadness': sadness_val,
        'irritability': irritability_val,
        'calmness': calmness_val,
        'stress': stress_val,
        'sleep_quality': sleep_val,
        'energy': energy_val,
        'motivation': motivation_val,
        'concentration': concentration_val,
        'appetite': appetite_val,
        'social': social_val,
        'workload': workload_val
    }

    for key, val in inputs.items():
        distress_sim.input[key] = val

    # Compute fuzzy distress
    try:
        distress_sim.compute()
        score = float(distress_sim.output['distress'])
    except Exception as e:
        st.error("Fuzzy computation error: " + str(e))
        score = None

    # ----------------- CRISIS OVERRIDE LOGIC -----------------
    crisis_trigger = False
    # Force higher scores when suicide/self-harm signals present or keywords found.
    # Highest severity: 7+
    if suicidal_val >= 7 or selfharm_val >= 7 or is_emg:
        # push to critical (near 10)
        score = max(score or 0, 9.5)
        crisis_trigger = True
    # Moderate severity: 4-6
    elif suicidal_val >= 4 or selfharm_val >= 4:
        score = max(score or 0, 8.0)
        crisis_trigger = True
    # Any non-zero signal: at least moderate
    elif suicidal_val > 0 or selfharm_val > 0:
        score = max(score or 0, 6.0)
        crisis_trigger = True

    # ----------------- OUTPUT -----------------
    st.subheader("Results")

    if score is not None:
        st.write("### Final Distress Score:", round(score, 2))

        if score <= 3:
            st.success("Risk Level: LOW")
        elif score <= 7:
            st.warning("Risk Level: MODERATE")
        else:
            st.error("Risk Level: HIGH")

        # ----------------- PATTERN DETECTION -----------------
        patterns = []

        if appetite_val <= 3 or appetite_val >= 8:
            patterns.append("Appetite Change")

        if sleep_val <= 4:
            patterns.append("Sleep Irregularity")

        if motivation_val <= 3:
            patterns.append("Low Motivation")

        if anxiety_val >= 6:
            patterns.append("Anxiety Indicators")

        if social_val <= 2:
            patterns.append("Social Withdrawal")

        if irritability_val >= 6:
            patterns.append("Irritability Spike")

        if energy_val <= 3:
            patterns.append("Low Energy Pattern")

        # Suicide-related patterns
        if suicidal_val > 0:
            patterns.append("Suicidal Ideation")
        if selfharm_val > 0:
            patterns.append("Self-harm Thoughts")

        st.write("### Detected Patterns:")
        if patterns:
            st.write(patterns)
        else:
            st.write("No significant patterns detected.")

        # ----------------- RECOMMENDATIONS -----------------
        st.write("### Recommendations")
        recs = generate_recommendations(score, patterns, crisis_trigger=crisis_trigger)
        for r in recs:
            st.write("- " + r)

        # Crisis-mode extra guidance (non-directive, safety focused)
        if crisis_trigger:
            st.markdown("---")
            st.error("Important safety guidance (please read):")
            st.write(
                "- If you have immediate plans or intent to harm yourself, call your local emergency number right now.\n"
                "- If you can, reach out to a trusted friend, family member, or colleague and let them know you need support.\n"
                "- Use grounding techniques (e.g., hold a cold object, name 5 things you can see/hear/touch) and practice slow breathing.\n"
                "- Consider contacting a crisis helpline or mental health professional in your area."
            )

    else:
        st.write("Final distress score could not be computed.")
