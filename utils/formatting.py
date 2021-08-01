
def num_formatting(num):
    """A function that returns a human format of a number."""

    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    if magnitude == 0:
        return num
    else:
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude]) # K = 1'000, M = 1'000'000, G = 1'000'000'000, T = 1'000'000'000'000, P = 1'000'000'000'000'000