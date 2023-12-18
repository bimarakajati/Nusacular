from bardapi import Bard

bard = Bard(token_from_browser=True)
res = bard.get_answer("Do you like cookies?")
print(res['content'])