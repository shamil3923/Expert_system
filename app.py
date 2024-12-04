import streamlit as st
from experta import Fact
from library_expert_system import LibraryExpertSystem


def main():
    st.title("Library Recommendation System")
    st.write("Get personalized recommendations based on your profile, language preference, and rating.")

    # User inputs
    user_type = st.selectbox("Who are you?", ["", "student", "teacher", "researcher"])
    topic = st.text_input("Enter a topic of interest (e.g., AI, Data Science)").strip()
    resource_type = st.selectbox("What type of resource do you prefer?", ["", "book", "journal", "article"])
    language = st.selectbox("Preferred language", ["", "English", "French"]).strip()
    min_rating = st.slider("Minimum rating", 0.0, 5.0, 4.0, 0.1)

    # Recommendation button
    if st.button("Get Recommendation"):
        # Validate inputs
        if not user_type or not topic or not resource_type:
            st.error("Please complete all fields to get a recommendation.")
            return

        # Initialize the expert system
        engine = LibraryExpertSystem()
        engine.reset()
        engine.declare(
            Fact(user_type=user_type),
            Fact(topic=topic),
            Fact(resource_type=resource_type),
            Fact(language=language if language else "any"),  # Handle missing language
            Fact(min_rating=min_rating)
        )
        engine.run()

        # Extract recommendations and explanations
        recommendations = []
        explanations = []
        for fact in engine.facts.values():
            if "recommendation" in fact:
                recommendations.extend(fact["recommendation"])
            if "explanation" in fact:
                explanations.extend(fact["explanation"])

        # Extract alternative recommendations
        alternative_recommendations = []
        alternative_explanations = []
        for fact in engine.facts.values():
            if "alternative_solution" in fact:
                alternative_recommendations.extend(fact["alternative_solution"])
            if "alternative_explanation" in fact:
                alternative_explanations.extend(fact["alternative_explanation"])

        # Display recommendations and explanations
        if recommendations:
            st.write("### Recommendations with Explanations:")
            for i, rec in enumerate(recommendations):
                st.success(f"{i + 1}. {rec}")
                if i < len(explanations):  # Ensure the explanation exists
                    st.info(f"Explanation: {explanations[i]}")
        else:
            st.error("No suitable recommendations found. Try different inputs.")

        # Display alternative recommendations
        if alternative_recommendations:
            st.write("### Alternative Recommendations with Explanations:")
            for i, alt_rec in enumerate(alternative_recommendations):
                st.success(f"{i + 1}. {alt_rec}")
                if i < len(alternative_explanations):
                    st.info(f"Explanation: {alternative_explanations[i]}")
        else:
            st.warning("No alternative recommendations found.")


if __name__ == "__main__":
    main()
