import tiktoken

ENC = tiktoken.get_encoding("cl100k_base")


def count_token(text: str) -> int:
    ids = ENC.encode(text)
    return len(ids)


def sub_tokenize(text: str, from_idx: int, end_idx: int) -> str:
    ids = ENC.encode(text)
    return try_decode(ids, from_idx, end_idx)


def try_decode(ids, s, t):
    for i in range(min(max(1, t - s - 1), 100)):
        try:
            return ENC.decode(ids[s : t - i])
        except:
            pass
