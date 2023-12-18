"""
At the command line, only need to run once to install the package via pip:

$ pip install bardapi
$ pip install git+https://github.com/dsdanielpark/Bard-API.git
$ pip install bardapi==0.1.23a
"""

from bardapi import BardCookies

cookie_dict = {
    "__Secure-1PSID": "bgjOeEh9zBaXR25UIbLMtUTKbD9E9PLVewpXiQLIIPDFrZpErWxxjSpgOeMePmoQs1Rnyw.",
    "__Secure-1PSIDTS": "sidts-CjIB3e41heXPlXBldjpuIWpqlhnjZ8Xxr5TysG80d10jVMc2YJxCahQ5hR1QV2lC_vecKxAA",
    "__Secure-1PSIDCC": "ACA-OxMRXw4N1sQQe2uy_NY807SS4aF5lAA_l64_cjyOUU-0-NnJylkme-T2vX8mgkQYBjQ0Ug"
    # Any cookie values you want to pass session object.
}

bard = BardCookies(cookie_dict=cookie_dict)
print(bard.get_answer("apa itu bahasa daerah?")['content'])