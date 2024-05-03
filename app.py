import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key,openai_api_key
from openai import OpenAI
from streamlit_carousel import carousel



single_image= dict(
        title="",
        text="",
        interval=None,
        img="",
    )


client = OpenAI(api_key=openai_api_key)

#setting api key
genai.configure(api_key= google_gemini_api_key)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

#Model
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

#set app to wide mode
st.set_page_config(layout="wide")

#title of the  app
st.title("🤖 Blogetron: Your AI writting assistant")

#sub header with a brief description about the app
st.subheader("Now you can craft perfect blogs with the help of AI- Blogetron is your personal writing companion.")

#Sidebar for user input

with st.sidebar:
    st.title("Input Your Blog Detail")
    st.subheader("Enter details of the blog that you want ot generate")

    #Blog title 
    blogTital = st.text_input("blog Title")

    #keyword input
    keyword = st.text_area("Keywords (comma-separated)")

    #Number of words
    num_words = st.slider("Number of words", min_value=250, max_value=2000, step=1)

    #Number of images
    num_images = st.number_input("Number of Images",min_value=0, max_value=5, step=1)

    prompt_parts = [
        f"Generate a comprehensive, engaging blog post relevant to the given title \"{blogTital}\" and keywords \"{keyword}\". Make sure to incorporate these keywords in the blog post. The blog should be approximately {num_words} words ub length, suitable for an online audiance. Ensure the content is original, informative, and maintains a consistent tone throughout."]


    #Submit Buttom
    submit_button = st.button("Gentrate Blog")

if submit_button:
    #carousel(items=test_items, width=1)

    response = model.generate_content(prompt_parts)
    images=[]
    images_gallery=[]

    for i in range(num_images):
        image_response = client.images.generate(
        model="dall-e-3",
        prompt=f"Genrate a blog post image on the title:{blogTital}",
        size="1024x1024",
        quality="standard",
        n=1,
        )
        new_image=single_image.copy()
        new_image["title"]=f"Image {i+1}"
        new_image["text"]=f"{blogTital}"
        new_image["img"]=image_response.data[0].url
        images_gallery.append(new_image)
        
        images.append(image_response.data[0].ur)
       
    for i in range(num_images):
        st.write(images[i])

    st.title("Blog images:")
    carousel(items=images_gallery, width=1)

    st.title("Your Blog post:")
    st.write(response.text)