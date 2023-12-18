import g4f

# Usage:
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    # model="gpt-3.5-turbo",
    # model=g4f.models.default,
    # messages=[{"role": "user", "content": "apa itu bahasa daerah?"}],
    messages=[{"role": "user", "content": "berikan puisi menggunakan bahasa jawa krama"}],
    # provider=g4f.Provider.Bing,
    provider=g4f.Provider.GeekGpt,
)

print(response)