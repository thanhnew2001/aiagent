from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json", scopes=SCOPES
)
creds = flow.run_local_server(port=8080)  # 👈 This will prompt you to log in

# Save credentials to a pickle file
with open("token.pickle", "wb") as token:
    pickle.dump(creds, token)
print("✅ Token saved as token.pickle")
