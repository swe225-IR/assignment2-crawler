import re
from typing import List
from lxml import etree
from urllib.parse import urlparse

from utils.response import Response


def scraper(url: str, resp: Response) -> List[str]:
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url: str, resp: Response) -> List[str]:
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    next_links = list()
    # ## todo: what if resp.url does not equal to the url (redirect ?)
    if resp.status == 200:
        if not resp.raw_response.content:
            return next_links
        else:
            root = etree.HTML(resp.raw_response.content)
            link_nodes = root.xpath("//a")
            if link_nodes:
                this_link_parsed = urlparse(resp.url)
                next_links = [x.get('href') for x in link_nodes]
                for i in range(0, len(next_links)):
                    parsed = urlparse(next_links[i])
                    if parsed.scheme == '':
                        if parsed.netloc == '':  # href = "/xxxxx"
                            next_links[
                                i] = this_link_parsed.scheme + this_link_parsed.netloc + parsed.path + parsed.params + parsed.query
                        else:  # href = "//www.xxx.xxx/xxxxxx"
                            next_links[
                                i] = this_link_parsed.scheme + "://" + parsed.netloc + parsed.path + parsed.params + parsed.query
                    elif parsed.fragment != '':
                        next_links[
                            i] = parsed.scheme + "://" + parsed.netloc + parsed.path + parsed.params + parsed.query
            else:
                return next_links
    else:  # to handle redirect 403, 405, etc.
        print(resp.error)
    return next_links


def is_valid(url: str) -> bool:
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        elif re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False
        elif not re.match(r"(.*\.(i?cs|informatics|stat)|today)\.uci\.edu$", parsed.netloc.lower()):
            return False
        elif (re.match(r"^today\.uci\.edu$", parsed.netloc) and not re.match(
                r"^/department/information_computer_sciences/\.*", parsed.path)):
            return False
        return True
    except TypeError:
        print("TypeError for ", parsed)
        raise
