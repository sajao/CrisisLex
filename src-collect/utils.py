def get_terms(input_filename):
    terms = []
    for line in input_filename:
        terms.append(line.strip())
    return terms