from bardapi import Bard

token = 'bgjOeEh9zBaXR25UIbLMtUTKbD9E9PLVewpXiQLIIPDFrZpErWxxjSpgOeMePmoQs1Rnyw.'
bard = Bard(token=token)
bard.get_answer("apa itu bahasa daerah?")['content']