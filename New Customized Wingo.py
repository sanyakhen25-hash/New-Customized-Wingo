import streamlit as st
from PIL import Image
import pytesseract
import random
import re

st.set_page_config(page_title="Wingo Predictor", layout="centered")

st.title("🔮 Wingo Color Predictor (Image-Based)")
st.markdown("Upload a screenshot of the Wingo game result and get predictions.")

# Upload image
uploaded_file = st.file_uploader("📷 Upload Wingo Screenshot", type=["png", "jpg", "jpeg"])

# Select timeframe
timeframe = st.radio("⏳ Select Time Frame", ["30 Seconds", "1 Minute", "3 Minutes", "5 Minutes"], horizontal=True)

def extract_numbers_from_text(text):
    # Search for sequences of 2-digit numbers
    numbers = re.findall(r'\b\d{2}\b', text)
    return [int(n) for n in numbers[-10:]]  # Last 10 results

def predict_next_color(number):
    if number in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]:
        return "Violet"
    elif number % 2 == 0:
        return "Blue"
    else:
        return "Red"

def big_or_small(number):
    return "Big" if number >= 25 else "Small"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_column_width=True)

    with st.spinner("🔍 Extracting data..."):
        ocr_result = pytesseract.image_to_string(image)
        numbers = extract_numbers_from_text(ocr_result)

    if numbers:
        st.success("✅ Detected Recent Numbers:")
        st.write(numbers)

        last_number = numbers[-1]
        predicted_color = predict_next_color(last_number + 1)
        bs_prediction = big_or_small(last_number + 1)

        st.markdown("### 🔮 Prediction for Next Game")
        st.write(f"**Time Frame:** {timeframe}")
        st.write(f"**Predicted Number (est.):** {last_number + 1}")
        st.write(f"**Color Prediction:** 🎨 `{predicted_color}`")
        st.write(f"**Big or Small:** 🔢 `{bs_prediction}`")

    else:
        st.warning("❌ No numbers detected. Try a clearer screenshot.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")