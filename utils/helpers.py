def load_wordlist(wordlist_path):
    with open(wordlist_path, "r") as f:
        return [line.strip() for line in f if line.strip()]
