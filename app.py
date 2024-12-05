import streamlit as st
from experta import Fact
from library_expert_system import LibraryExpertSystem


def main():
    with st.sidebar:
        st.header("Options")
        st.write("Provide your preferences below:")

        user_type = st.selectbox("Who are you?", ["", "student", "teacher", "researcher"])
        topic = st.text_input("Enter a topic of interest (e.g., AI, Data Science)").strip()
        resource_type = st.selectbox("What type of resource do you prefer?", ["", "book", "journal", "article"])
        language = st.selectbox("Preferred language", ["", "English", "French"]).strip()
        min_rating = st.slider("Minimum rating", 0.0, 5.0, 4.0, 0.1)

    # Main section for heading and recommendations
    st.title("Library Assistant Expert System")
    st.subheader("Get personalized recommendations based on your preferences:")

    # Recommendation button
    if st.button("Get Recommendation"):
        # Validate inputs
        if not user_type:
            st.error("Please select your user type.")
            return

        # Initialize the expert system
        engine = LibraryExpertSystem()
        engine.reset()

        # Add facts, allowing missing fields to be handled
        engine.declare(
            Fact(user_type=user_type),
            Fact(topic=topic if topic else None),
            Fact(resource_type=resource_type if resource_type else None),
            Fact(language=language if language else None),
            Fact(min_rating=min_rating)
        )
        engine.run()

        # Extract recommendations, explanations, and confidence scores
        recommendations = []
        explanations = []
        confidence_scores = []
        for fact in engine.facts.values():
            if "recommendation" in fact:
                recommendations.extend(fact["recommendation"])
            if "explanation" in fact:
                explanations.extend(fact["explanation"])
            if "confidence" in fact:
                confidence_scores.extend(fact["confidence"])

        # Extract alternative recommendations
        alternative_recommendations = []
        alternative_explanations = []
        alternative_confidence = []
        for fact in engine.facts.values():
            if "alternative_solution" in fact:
                alternative_recommendations.extend(fact["alternative_solution"])
            if "alternative_explanation" in fact:
                alternative_explanations.extend(fact["alternative_explanation"])
            if "alternative_confidence" in fact:
                alternative_confidence.extend(fact["alternative_confidence"])

        # Display recommendations and explanations with confidence
        if recommendations:
            st.write("### Recommendations with Explanations:")
            for i, rec in enumerate(recommendations):
                st.success(f"{i + 1}. {rec}")
                if i < len(explanations):  # Ensure the explanation exists
                    st.info(f"Explanation: {explanations[i]}")
                if i < len(confidence_scores):  # Show confidence level
                    st.info(f"Confidence: {confidence_scores[i]}%")
        else:
            st.error("No suitable recommendations found. Try different inputs.")

        # Display alternative recommendations
        if alternative_recommendations:
            st.write("### Alternative Recommendations with Explanations:")
            for i, alt_rec in enumerate(alternative_recommendations):
                st.success(f"{i + 1}. {alt_rec}")
                if i < len(alternative_explanations):
                    st.info(f"Explanation: {alternative_explanations[i]}")
                if i < len(alternative_confidence):  # Show confidence level for alternatives
                    st.info(f"Confidence: {alternative_confidence[i]}%")
        else:
            st.warning("No alternative recommendations found.")


if __name__ == "__main__":
    main()
