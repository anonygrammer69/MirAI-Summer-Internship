from google import genai

print("genai module:", genai)
print("Version:", getattr(genai, "__version__", "No version"))
print("Client has responses:", hasattr(genai.Client(api_key="dummy"), "responses"))
print(dir(genai.Client(api_key="dummy")))