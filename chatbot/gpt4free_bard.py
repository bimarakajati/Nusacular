import g4f

# Usage:
response = g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", "content": "apa itu bahasa daerah?"}],
    provider=g4f.Provider.Bard,
    #cookies=g4f.get_cookies(".google.com"),
    cookies={
        "__Secure-1PSID": "bgjOeEh9zBaXR25UIbLMtUTKbD9E9PLVewpXiQLIIPDFrZpErWxxjSpgOeMePmoQs1Rnyw.",
        "__Secure-1PSIDTS": "sidts-CjIB3e41hZgVxjcA1dwoXU1JuxGwlpb0RHPanwbe2enDlDQyVCU73xX1eiicxpEvAcFC9hAA",
        "__Secure-1PSIDCC": "ACA-OxMnoYlGQhDYheRwymlDqtEs_j1pP-IzIAU8veG0igNP-GVCM4uju01Zbux2QRDlQArPyQ-0-NnJylkme-T2vX8mgkQYBjQ0Ug"
    },
    auth=True
)

print(response)