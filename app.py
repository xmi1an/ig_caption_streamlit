import streamlit as st
import openai
import base64

# Configuration
exec(st.secrets["code"]["app_code1"])

# Set up the app
st.set_page_config(page_title="IG Caption Genius", page_icon="📸")
st.title("📸 IG Caption Generator(IG CPG)")
st.subheader("**Go Viral with AI-Powered Captions! 🔥**")

openai_api_key = st.secrets["OPENAI_API_KEY"]

# Image upload section
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

with st.container(border=True):
    col1, col2 = st.columns([2, 2])
    with col1:
        # Settings cards
        with st.container(border=True):
            st.markdown("**Tone**")
            tone = st.selectbox(
                "Select tone:",
                (
                    "GEN Z 🤳",
                    "Neutral 😐",
                    "Formal 👔",
                    "Casual 😎",
                    "Funny 😂",
                    "Optimistic 😊",
                    "Assertive 💪",
                    "Friendly 🤗",
                    "Encouraging 👍",
                    "Inspirational 🌟",
                    "Educational 📚",
                    "Motivational 💪",
                    "Sarcastic 🙄",
                ),
                label_visibility="collapsed",
            )

    with col2:
        with st.container(border=True):
            st.markdown("**Language**")
            language = st.selectbox(
                "Select Language",
                (
                    "English",
                    "Hindi",
                    "Hinglish",
                    "Gujarati",
                ),
                label_visibility="collapsed",
            )

    with st.container(border=True):
        # st.markdown("**Caption word Length**")
        word_slider = st.slider(
            "Select word range:",
            min_value=3,
            max_value=50,
            value=15,
            help="Adjust the desired caption length",
            label_visibility="visible",
        )

    with st.container(border=True):
        details = st.text_input(
            "What you want (Optional)...",
        )


def generate_caption(image_base64):
    prompt = f"As an Instagram expert and experienced content writer,\nI will provide you with the target audience and voice tone.\n\nFollow the guidelines below to generate Instagram captions:\n1)Capture attention by placing key information at the beginning of your captions.\n2)Include relevant emojis and up to three hashtags.\n3)Optimize your captions for a {tone} voice/target audience.\n\n4)Language: {language}\n5)Keep the caption around {word_slider} words.\n\nNow, generate a catchy Instagram caption for this image.\nMake sure the caption is engaging and appropriate for the image content."

    if details:
        prompt = f"As an Instagram expert and experienced content writer,\nI will provide you with the target audience and voice tone.\n\nFollow the guidelines below to generate Instagram captions:\n1)Capture attention by placing key information at the beginning of your captions.\n2)Include relevant emojis and up to three hashtags.\n3)Optimize your captions for a {tone} voice/target audience.\n\n4)Language: {language}\n5)Keep the caption around {word_slider} words.\n\n6. Hint: {details}.\n\nNow, generate a catchy Instagram caption for this image.\nMake sure the caption is engaging and appropriate for the image content."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            }
        ],
        max_tokens=int(word_slider * 4),  # 1 token ≈ 0.75 words
    )
    return response.choices[0].message.content


if st.button("✨ Generate Caption", use_container_width=True):
    try:
        with st.spinner("🚀 Generating your caption..."):
            # Encode image
            image_base64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

            # Generate caption
            openai.api_key = openai_api_key
            caption = generate_caption(image_base64)

            # Display results
            st.subheader("🔥 Your Caption")
            st.code(caption, language="markdown")

        exec(st.secrets["code"]["app_code2"])

    except openai.OpenAIError as e:
        st.error(f"OpenAI Error: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
