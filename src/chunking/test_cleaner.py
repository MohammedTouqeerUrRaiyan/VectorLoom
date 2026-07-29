from src.chunking.cleaner import TextCleaner

sample = """

This      is      VectorLoom.


It      removes      spaces.


\tTabs too.



"""

print(TextCleaner.clean(sample))