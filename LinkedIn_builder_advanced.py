from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import streamlit as st
import os

# Define your system and human templates
system = "You are a helpful assistant that helps create LinkedIn posts. The user will provide details about a topic and style preferences. Use that information to produce a LinkedIn post."
human_template = """ 
Below is the information provided by the user:

1. Topic: {topic}
2. Expected formality of writing style (0-10): {formality}
3. Expected enthusiasm of writing style (0-10): {enthusiasm}
4. Number of emojis in text: {emoji}
5. Template: {template}
6. Examples of prior LinkedIn posts:
{examples}

Instructions:
- Use the topic to craft a LinkedIn post.
- The style of writing should match the given formality and enthusiasm levels (0 is least formal/enthusiastic, 10 is most formal/enthusiastic).
- The post should be coherent, engaging, and suitable for LinkedIn.
- Attempt to reflect the user's general style as inferred from the provided examples, but still produce a unique, original post.
- Avoid the following words at any cost: excited, thrilled, exciting, pivotal, journey

Now, please generate the LinkedIn post.
"""

# Predefined templates
templates = {
    "No template": "",
    "How to": """
How to {DO THIS THING}:

(5 little-known steps anyone can use)

{1ST THING}: {SHORT DESCRIPTION}
{2ND THING}: {SHORT DESCRIPTION}
{3RD THING}: {SHORT DESCRIPTION}
{4TH THING}: {SHORT DESCRIPTION}
{5TH THING}: {SHORT DESCRIPTION}
""",
    "Data Driven": """
The {INDUSTRY OR CONCEPT YOU ARE TALKING ABOUT} is estimated to be {YOUR FIRST STATISTIC} yet {PEOPLE OR THINGS IN THE INDUSTRY OR CONCEPT} are {DOING SOMETHING THAT DOESN’T FIT THE STATISTIC}

There are 3 main reasons for this:

{REASON 1}: {SUPPORTING INFORMATION FOR REASON 1}
{REASON 2}: {SUPPORTING INFORMATION FOR REASON 2}
{REASON 3}: {SUPPORTING INFORMATION FOR REASON 3}

There’s a free guide below to help you find out {OR AVOID} being {UNDESIRED STATE}
""",
    "These are three things": """
here are 3 things {THAT WILL HELP ACHIEVE AN AWESOME OUTCOME}.

Wanna know what they are?

Here you go...

1 - {FIRST THING}. (REASON YOU SHOULD DO FIRST THING}).

2 - {SECOND THING}. (REASON YOU SHOULD DO SECOND THING}).

3 - {THIRD THING}. (REASON YOU SHOULD DO THIRD THING}).

If you want to know exactly how to do these 3 things, there’s a [GUIDE/VIDEO/ARTICLE] in the chit chat below. 👇

{BRIEF DESCRIPTION OF WHAT THE LINK GOES TO}

{FRIENDLY/QUIRKY/AMUSING FINAL STATEMENT}
"""
}


# Create the prompt template

def main():
    st.title("LinkedIn Post Generator")

    st.write("This app will generate a LinkedIn post based on the provided topic and style preferences. For more information, please reach out here: https://www.linkedin.com/in/dries-faems-0371569/. Check out my other free GenAI applications here: https://www.youtube.com/@GenAI_Nerd_Channel ")

    #ask user for Groq API key

    groq_api_key = st.text_input("Enter your Groq API key (check this video for instructions how to get free Groq API key: https://www.youtube.com/watch?v=_Deu9x5efvQ&t=7s):", type="password")

    # set as environment variable

    
    # Set up Groq client

    # User inputs
    topic = st.text_area("Describe the topic for the LinkedIn post:")
    formality = st.slider("How formal should the text be?", 0, 10, 5)
    enthusiasm = st.slider("How enthusiastic should the text be?", 0, 10, 5)
    emoji = st.slider("How many emojis should be included?", 0, 10, 5)
    template = st.selectbox("Choose a template:", ["No template", "How to", "Data Driven", "These are three things"])
    examples = st.text_area("Provide examples of your prior LinkedIn posts (optional):")

    if st.button("Generate Post"):
        if not topic:
            st.warning("Please provide a topic.")
        else:
            os.environ["GROQ_API_KEY"] = groq_api_key
            prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human_template)])
            chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
            chain = prompt | chat
            # Invoke the model
            response = chain.invoke({
            "topic": topic,
            "formality": formality,
            "enthusiasm": enthusiasm,
            "emoji": emoji,
            "template": templates[template],
            "examples": examples
            })
            with st.spinner("Generating your LinkedIn post..."):
                st.success("Here's your generated LinkedIn post:")
                st.write(response.content)


if __name__ == "__main__":
    main()