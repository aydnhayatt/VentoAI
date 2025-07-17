import google.generativeai as genai
genai.configure(api_key="AIzaSyA5uWz-ICtFEfpFM872MevAC2pDbqu4Y-U")

models = genai.list_models()

for model in models:
    print(model.name)
