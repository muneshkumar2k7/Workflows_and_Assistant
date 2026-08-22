import streamlit as st
from dotenv import load_dotenv
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from Blog_title import Title , Gen_title_schema ,Style_schema,Score_schema,Reason_schema,Response_schema



# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.title("✍️ AI Blog Title Generator")

st.write(
    "Generate blog titles with styles, scores, and explanations using Gemini."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    audience = st.selectbox(
        "Target Audience",
        [
            "Beginner",
            "Professional",
            "Researcher"
        ]
    )

    tone = st.selectbox(
        "Tone",
        [
            "Friendly",
            "Professional"
        ]
    )

    number_of_titles = st.number_input(
        "Number of Titles",
        min_value=1,
        max_value=9,
        value=3,
        step=1
    )


# --------------------------------------------------
# Main Input
# --------------------------------------------------

topic = st.text_input(
    "Enter your topic",
    placeholder="e.g. Artificial Intelligence"
)


# --------------------------------------------------
# Generate Button
# --------------------------------------------------

generate_button = st.button(
    "🚀 Generate Titles",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Generation
# --------------------------------------------------

if generate_button:

    if not topic.strip():

        st.warning(
            "Please enter a topic first."
        )

    else:

        # Validate input using Pydantic
        try:

            user_input = Title(
                Topic=topic.strip(),
                Audience=audience,
                Tone=tone,
                Number_of_titles=number_of_titles
            )

        except Exception as e:

            st.error(
                f"Invalid input: {e}"
            )

        else:

            # Loading UI
            with st.spinner(
                "Generating your blog titles..."
            ):

                try:

                    final_response = Gen_title_schema(
                        user_input
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )

                else:

                    st.success(
                        "Titles generated successfully! 🎉"
                    )

                    # Save result
                    st.session_state["result"] = final_response


# --------------------------------------------------
# Display Results
# --------------------------------------------------

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.header("🎯 Generated Titles")


    # ----------------------------------------------
    # Display each title
    # ----------------------------------------------

    for i, title in enumerate(
        result.Generated_titles
    ):

        st.subheader(
            f"{i + 1}. {title}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**🎨 Style:** {result.Styles[i]}"
            )

        with col2:

            score = result.Scores[i]

            st.write(
                f"**⭐ Score:** {score}/10"
            )

            st.progress(
                score / 10
            )

        st.write(
            f"**💡 Reason:** {result.Reasons[i]}"
        )

        st.divider()


    # ----------------------------------------------
    # Summary
    # ----------------------------------------------

    st.header("📊 Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Titles Generated",
            len(result.Generated_titles)
        )

    with col2:

        average_score = (
            sum(result.Scores)
            / len(result.Scores)
        )

        st.metric(
            "Average Score",
            f"{average_score:.1f}/10"
        )

    with col3:

        best_score = max(result.Scores)

        st.metric(
            "Best Score",
            f"{best_score}/10"
        )