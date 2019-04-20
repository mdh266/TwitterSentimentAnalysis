import re

def removeRegex(tokens: list) -> list:
    """
    Removes hashtags, call outs and web addresses from tokens.
    """
    expr    = '(@[A-Za-z0-a9_]+)|(#[A-Za-z0-9_]+)|'+\
              '(https?://[^\s<>"]+|www\.[^\s<>"]+)'
        
    regex   = re.compile(expr)

    cleaned = [t for t in tokens if not(regex.search(t)) if len(t) > 0]

    return list(filter(None, cleaned))



def normalize(tokens : list) -> str:
    """
    Removes non-english characters and returns lower case versions of 
    words in string form.
    """
    subbed   = [re.sub("[^a-zA-Z]+", "", s).lower() for s in tokens]
    
    filtered = filter(None, subbed)
    
    return " ".join(list(filtered))
