import sys
from typing import Set
from urllib.parse import urlparse


def count_distinct_url(path: str) -> Set[str]:
    """
    get crawled URLs
    :param path: /path/to/Worker.log
    :return: URLs set
    """
    link = set()
    error_code = set()
    c = 0  # number of error code lines
    e = 0  # number of max entries or other exceptions
    with open(path, 'r') as f:
        while True:
            i = f.readline()
            if i:
                try:
                    if i.split(", status <")[1][0:3] == "200":
                        link.add(i.split(", status")[0].split("Downloaded ")[1])
                    else:
                        c += 1
                        error_code.add(i.split(", status <")[1][0:3])
                except Exception:
                    e += 1
                    pass
            else:
                break
    print("# of distinct links: ", len(link))
    # print(error_code)
    # print(c)
    # print(e)
    return link


def count_number_subdomain(links: Set[str], excluded=None):
    """
    Number of subdomains
    :param links: URLs crawled
    :param excluded: excluded from the results
    :return: NoneType
    """
    if excluded is None:
        excluded = {"gitlab.ics.uci.edu"}
    subdomain = {}
    for li in links:
        parsed = urlparse(li)
        if parsed.netloc in excluded:
            continue
        if not parsed.netloc.__contains__("ics.uci.edu"):
            continue
        ind = parsed.netloc.find("ics.uci.edu")
        if ind - 1 >= 0 and parsed.netloc[ind - 1] != '.':
            continue
        if subdomain.__contains__(parsed.netloc):
            subdomain[parsed.netloc] += 1
        else:
            subdomain[parsed.netloc] = 1
    # tmp = sorted(subdomain.items(), key=lambda x: x[0])
    tmp = sorted(subdomain.items(), key=lambda x: x[0].lower())
    for t in tmp:
        print("(\"" + t[0] + "\", " + str(t[1]) + "),")
    # print(subdomain)


if __name__ == '__main__':
    count_number_subdomain(count_distinct_url(sys.argv[1]))
