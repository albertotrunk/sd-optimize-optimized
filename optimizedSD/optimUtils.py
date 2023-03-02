import os
import pandas as pd


def split_weighted_subprompts(text):
    """
    grabs all text up to the first occurrence of ':' 
    uses the grabbed text as a sub-prompt, and takes the value following ':' as weight
    if ':' has no value defined, defaults to 1.0
    repeats until no text remaining
    """
    remaining = len(text)
    prompts = []
    weights = []
    while remaining > 0:
        if ":" in text:
            idx = text.index(":") # first occurrence from start
            # grab up to index as sub-prompt
            prompt = text[:idx]
            remaining -= idx
            # remove from main text
            text = text[idx+1:]
            # find value for weight
            idx = text.index(" ") if " " in text else len(text)
            if idx != 0:
                try:
                    weight = float(text[:idx])
                except: # couldn't treat as float
                    print(f"Warning: '{text[:idx]}' is not a value, are you missing a space?")
                    weight = 1.0
            else: # no value found
                weight = 1.0
            # remove from main text
            remaining -= idx
            text = text[idx+1:]
            # append the sub-prompt and its weight
            prompts.append(prompt)
            weights.append(weight)
        else: # no : found
            if len(text) > 0: # there is still text though
                # take remainder as weight 1
                prompts.append(text)
                weights.append(1.0)
            remaining = 0
    return prompts, weights

def logger(params, log_csv):
    os.makedirs('logs', exist_ok=True)
    cols = [arg for arg, _ in params.items()]
    if not os.path.exists(log_csv):
        df = pd.DataFrame(columns=cols) 
        df.to_csv(log_csv, index=False)

    df = pd.read_csv(log_csv)
    for arg in cols:
        if arg not in df.columns:
            df[arg] = ""
    df.to_csv(log_csv, index = False)

    cols = list(df.columns)
    data = dict(params.items())
    li = {col: data.get(col, '') for col in cols}
    df = pd.DataFrame(li,index = [0])
    df.to_csv(log_csv,index=False, mode='a', header=False)