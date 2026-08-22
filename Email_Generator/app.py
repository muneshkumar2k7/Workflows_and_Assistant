import streamlit as st
from Gen_Email import Email, prompt , llms
from pydantic import ValidationError


#Memory 
if "recent_emails" not in st.session_state:
    st.session_state.recent_emails = []

#side bar
st.sidebar.title("Email Generator")
if st.sidebar.button("New Email",key="new_email"):
    st.session_state.recipient = ""
    st.session_state.topic = ""
    st.session_state.purpose = ""
    st.session_state.details = ""
    st.session_state.generated_email = ""

    st.rerun()


st.sidebar.subheader("Recents")


for index,email in enumerate(st.session_state.recent_emails):
    if st.sidebar.button(
        email["topic"], key=f"recent_{index}"):

      st.session_state.topic = email["topic"]
      st.session_state.recipient = email["recipient"]
      st.session_state.purpose = email["purpose"]
      st.session_state.details = email["details"]
      st.session_state.tone = email["tone"]
      st.session_state.length = email["length"]
      if st.session_state.generated_email:
        st.subheader("Generated Email")
        st.write(st.session_state.generated_email)

      st.rerun()
      




st.header(" AI Email Generator  ")
st.write("Generate professional emails")

topic = st.text_input("Topic", key="topic")
purpose = st.text_input("Purpose", key="purpose")
recipient = st.text_input("Recipient Email", key="recipient")
details = st.text_area("Details", key="details")


length = st.selectbox(
    "Length",
    ["short", "medium", "long"]
)


tone = st.selectbox(
    "Tone",
   ["Casual", "Professional", "Friendly"]
)


generate = st.button("Generate Email")


if generate:
   try:  
        email = Email(
        topic=topic,
        Recipient=recipient,
        tone=tone, 
        length=length, 
        details=details,
        purpose=purpose
      )

    
        email_prompt = prompt.invoke(email.model_dump())
        result = llms.invoke(email_prompt)

        email_record = {
    "topic": topic,
    "recipient": recipient,
    "purpose": purpose,
    "details": details,
    "tone": tone,
    "length": length,
    "generated_email": result.content
}   
        st.write(topic)
        st.write(purpose)
        st.write("Details:", details)
        st.write("EMAIL RECORD:", email_record)
        
        st.session_state.recent_emails.insert(0, email_record)
        st.subheader("Generated Email")
        st.write(result.content)
    

   
   except ValidationError as e:
        st.error("Please correct the following input errors:")
        for error in e.errors():
            field = error["loc"][0]
            message = error["msg"]

            st.error(f"{field}: {message}")




