def linter_check_lines_max_length(max_length: int):
    with open("config.flake8", "a") as cfg:
        cfg.write(f"max-line-length = {max_length}\n")


def linter_check_mc_cabe_complexity(complexity: int):
    with open("config.flake8", "a") as cfg:
        cfg.write(f"max-complexity = {complexity}\n")


def linter_check_specify_inline_quotes(quote: str):
    with open("config.flake8", "a") as cfg:
        if quote.lower() == "одинарные":
            cfg.write("inline-quotes = '\n")
        if quote.lower() == "двойные":
            cfg.write("inline-quotes = '\n")
