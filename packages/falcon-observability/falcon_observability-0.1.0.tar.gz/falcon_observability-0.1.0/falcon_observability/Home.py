import streamlit as st

st.set_page_config(
    page_title="Falcon Observability",
    page_icon="./static/AIAAS_FALCON.jpg",

)
st.image('./static/AIAAS_FALCON.jpg',width=300)
st.write("# Welcome to Falcon Observatory! 👋")

st.sidebar.success("Select the page you would like to visit.")

st.markdown(
    """
Falcon, a versatile and advanced platform, stands at the forefront of technological innovation, offering comprehensive support for Large Language Models (LLMs), audio processing, and beyond. It is expertly designed to cater to a wide array of needs, including training, inference, and meticulous monitoring, ensuring a seamless and efficient experience for users.

At the heart of Falcon's offerings is its compatibility with Azure OpenAI, Llama Full model, Llama Quantized model, and the SingtelGPT model for precise and effective inference. This integration ensures that Falcon users can leverage the latest advancements in AI to achieve unparalleled results.

In the realm of audio processing, Falcon showcases its prowess by supporting the training and inference of the Whisper model. This capability allows users to explore and utilise state-of-the-art voice recognition and processing technologies. Additionally, Falcon's ability to transcribe audio seamlessly integrates with its broad spectrum of functionalities, making it a comprehensive solution for a multitude of audio-related applications.

Overall, Falcon emerges as a robust, multifaceted platform, ideally suited for those seeking to harness the power of AI in a variety of contexts, from language processing to audio analysis.


"""
)