import re
from typing import List
from lxml import etree
from urllib.parse import urlparse, ParseResult

from utils.response import Response

from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import pickle as pkl
import os
from collections import Counter
from simhash import Simhash

TAGS_ABANDON = ['CC', 'DT', 'FW', 'IN', 'LS', 'PDT', 'PRP', 'PRP$', 'RP', 'SYM', 'TO', 'PP']
TAGS_VERB = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'VP']
TAGS_ADJ = ['JJ', 'JJR', 'JJS', 'ADJP', 'ADVP']
TAGS_NOUN = ['NN', 'NNS', 'NNP', 'NNPS', 'NP']
TAGS_ADV = ['RB', 'RBR', 'RBS']
ADV_OTHERS = ['CD', 'EX', 'MD', 'UH', 'WDT', 'WP', 'WP$', 'WRB', 'SBAR', 'PRT', 'INTJ', 'PNP', '-SBJ', '-OBJ']
STOP_WORDS = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't",
              'as',
              'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't",
              'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down',
              'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't",
              'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself',
              'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's",
              'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of',
              'off',
              'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same',
              "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that',
              "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
              "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until',
              'up',
              'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's",
              'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with',
              "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself',
              'yourselves'}
WORD_ABBREVIATION = {'re', 've', 'll', 'ld', 'won', 'could', 'might', 'isn', 'aren', 'couldn', 'hasn', 'haven', 'wasn',
                     'weren'}


def scraper(url: str, resp: Response) -> List[str]:
    # words = extract_words(url, resp)
    extract_words(url, resp)
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
    links = list()
    # todo: 1. what if resp.url does not equal to the url (redirect ?)
    # todo: 2. 跑一会会trap https://swiki.ics.uci.edu/doku.php/projects:maint-spring-2021?tab_details=edit&do=media&tab_files=files&image=virtual_environments%3Ajupyterhub%3Anotebooks.jpg&ns=security
    # 续上：我们需要处理parameter调换的情况
    # todo: 3. https://urldefense.com/v3/__https:/rloganiv.github.io/__;!!CzAuKJ42GuquVTTmVmPViYEvSg!Pe8w9cwoRSztNHlTyrGJlybQ4ZD_5-oWKbzxvTlVr09ZfoUzeTWj07XuyrEktXsDyERsM1m61D8GD7Y$
    # -> solution: https://help.proofpoint.com/Threat_Insight_Dashboard/Concepts/How_do_I_decode_a_rewritten_URL%3F
    """
    processing:
    <a href="URL">
        URL can be:
            An absolute URL - points to another web site (like href="http://www.example.com/default.htm")
            A relative URL - points to a file within a web site (like href="default.htm")
            Link to an element with a specified id within the page (like href="#section2")
            Other protocols (like https://, ftp://, mailto:, file:, etc..)
            A script (like href="javascript:alert('Hello');")
        URL: https  ://    www.a.b.c  /path/to/file   ;    a=b;c=d  ?    e=f&r=z
            scheme           netloc       path             params         query
            注意：params 存在这种情况：https://www.a.b.c/path;a 没有等于号，我在下面做了处理
                query为了防止万一，我也做了处理
    """
    if resp.status == 200:
        if not resp.raw_response or not resp.raw_response.content:
            return links
        else:
            root = etree.HTML(resp.raw_response.content)
            if not root:
                return links
            a_nodes = root.xpath("//a")
            if a_nodes:
                cur_lk_p = urlparse(resp.url)
                links = [x.get('href') for x in a_nodes if x.get('href')]  # some href attribute is None
                for i in range(0, len(links)):
                    if is_url_defense(links[i]):
                        pass
                    else:
                        parsed = urlparse(links[i])
                        url_processed = handle_urls(links[i], parsed)
                        if parsed.scheme == '':
                            if parsed.netloc == '':  # href = "/xxxxx"
                                links[i] = f"{cur_lk_p.scheme}://{cur_lk_p.netloc}{url_processed}"
                            else:  # href = "//www.xxx.xxx/xxxxxx"
                                links[i] = f"{cur_lk_p.scheme}:{url_processed}"
                        else:
                            links[i] = url_processed
            else:
                return links
    else:  # to handle redirect 403, 405, etc.
        print(resp.error)
    return links


def is_valid(url: str) -> bool:
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)  # Parse a URL into 6 components: <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
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
                r"^/department/information_computer_sciences/\.*", parsed.path)):  # todo: 没看见这个url
            return False
        elif re.match(r"gitlab\.ics\.uci\.edu", parsed.netloc):
            return False
        return True
    except TypeError:
        print("TypeError for ", parsed)
        raise


def handle_urls(origin_url: str, parsed: ParseResult) -> str:
    """
    processing URL string
    :param origin_url: URL of this web page
    :param parsed: urlparse(origin_url)
    :return: sorted string
    """
    if parsed.query == '' and parsed.params == '':
        return parsed.geturl().split("#")[0]
    elif parsed.query == '' and parsed.params != '':
        params_str = handle_params_or_query(parsed.params, ";")
        p_id = origin_url.find(";")
        return f'{origin_url[:p_id]};{params_str}'
    elif parsed.query != '' and parsed.params == '':
        query_str = handle_params_or_query(parsed.query, "&")
        q_id = origin_url.find("?")
        return f'{origin_url[:q_id]}?{query_str}'
    else:
        query_str = handle_params_or_query(parsed.query, "&")
        params_str = handle_params_or_query(parsed.params, ";")
        p_id = origin_url.find(";")
        return f'{origin_url[:p_id]};{params_str}?{query_str}'


def handle_params_or_query(params_or_query_str: str, separator: str) -> str:
    """
    to handle the situation that two params or query strings are exactly the same except for the order
    :param params_or_query_str: params or params1=value1;params2=value2 or query1=value1&query2=value2
    :param separator: ; or &
    :return: sorted list
    """
    pair = params_or_query_str.split(separator)
    result_list = list()
    for p in pair:
        pair_list = p.split("=")
        if len(pair_list) == 2:
            result_list.append((pair_list[0], pair_list[1]))
        else:
            result_list.append((pair_list[0], ''))
    result_list.sort()
    url_partial = ''
    for r in result_list:
        url_partial += f'{r[0]}={r[1]}{separator}'
    return url_partial[:-1]  # discarding the separator at the end


def is_url_defense(url: str) -> bool:
    return True if re.compile(r'https://urldefense(?:\.proofpoint)?\.com/(v[0-9])/').search(url) else False


def extract_words(url: str, resp: Response) -> List[str]:
    '''
    Retrieve and standardize word.
    :param resp: URL response
    :return: Standardized words
    '''
    words = []
    if resp.status != 200:
        return words

    if not resp.raw_response or not resp.raw_response.content:
        return words

    html = etree.HTML(resp.raw_response.content)
    soup = BeautifulSoup(etree.tostring(html).decode('utf-8'), features="html.parser")
    raw = soup.get_text()
    standardize_words(url, raw.lower())
    # return standardize_words(url, raw.lower())


def standardize_words(url: str, text: str):
    """
    Standardize words and filter stopword
    At first, we get the classification of words according to nltk library.
    Second, we do an initial filter for special cases like special character.
    Third, we do a second filter and lemmatization based on the classification.
    Forth, we do a final filter based on stopword.
    :param url: url of this web content
    :param text: Web content
    """
    # todo: 1. logger()函数获取所有pages累积的words字典
    # todo: 2. current_page_word = 0
    counter_all_word_num_path, counter_page_word_num_path, hash_values_path = 'counter_all_word_num.pkl', 'counter_page_word_num.pkl', 'hash_values.pkl'
    # counter_all_word_num, counter_page_word_num = logger(counter_all_word_num_path), logger(counter_page_word_num_path)
    word_list, current_page_word_num = [], 0
    lemmatizer = WordNetLemmatizer()
    unstandardized_words = word_tokenize(text.lower())
    word_pos_tags = nltk.pos_tag(unstandardized_words)
    for word_pos_tag in word_pos_tags:
        # Special case filter
        if special_case_filter(word_pos_tag[0]) == '':
            continue
        # Get the classification of words and do the initial filter
        wordnet_tag = pos_tags_filter(word_pos_tag[1])
        if wordnet_tag == '':
            continue
        elif wordnet_tag == 'add':
            # todo: replace the code blow
            # todo: 2. 这里不用words存，直接改第1步读的字典值就行，然后current_page_word += 1
            word_list.append(word_pos_tag[0])
            # counter_all_word_num.update([word_pos_tag[0]])
            current_page_word_num += 1
        else:
            # Lemmatization
            standardize_word = lemmatizer.lemmatize(word_pos_tag[0], wordnet_tag)

            # Remove stopwords
            if stopwords_filter(standardize_word) == '':
                continue
            else:
                word_list.append(standardize_word)
                # counter_all_word_num.update([standardize_word])
                current_page_word_num += 1
    # todo: 4. logger()函数获取存有最大page的words数量和相应url的pkl文件，用current_page_word进行比较更新
    # todo: 5. logger()保存2个pkl
    if similarity_comparison(url=url, word_list=word_list, f_path=hash_values_path) is False:
        counter_all_word_num, counter_page_word_num = logger(counter_all_word_num_path), logger(
            counter_page_word_num_path)
        counter_all_word_num.update(word_list)
        counter_page_word_num.update({url: current_page_word_num})
        logger(counter_all_word_num_path, counter_all_word_num), logger(counter_page_word_num_path,
                                                                        counter_page_word_num)
    # return words


def special_case_filter(word: str) -> str:
    if len(word) == 1:
        return ''
    elif (len(word) >= 2) and (word in WORD_ABBREVIATION):
        return ''
    return word


def pos_tags_filter(tag: str) -> str:
    """
    Filter the words that belong to the tags we do not need and get wordnet compatible tags
    :param tag: Pos tags
    :return: Wordnet compatible tags
    """
    if tag in TAGS_ADJ:
        return nltk.corpus.wordnet.ADJ
    elif tag in TAGS_VERB:
        return nltk.corpus.wordnet.VERB
    elif tag in TAGS_NOUN:
        return nltk.corpus.wordnet.NOUN
    elif tag in TAGS_ADV:
        return nltk.corpus.wordnet.ADV
    elif tag in ADV_OTHERS:
        return 'add'
    else:
        return ''


def stopwords_filter(word: str) -> str:
    if word in STOP_WORDS:
        return ''
    return word


def logger(f_path: str, dict=None) -> dict:
    """
    :param f_path: File path
    :param dict: None: read, else: the dictionary for save
    :return: Dict from pkl file
    """
    if dict is None:
        if os.path.isfile(f_path) is False:
            return Counter()
        f = open(f_path, 'rb')
        counter = pkl.load(f)
        f.close()
        return counter
    else:
        f = open(f_path, 'wb')
        pkl.dump(dict, f)
        f.close()


def hamming_distance(int_a, int_b):
    x = (int_a ^ int_b) & ((1 << 64) - 1)
    ans = 0
    while x:
        ans += 1
        x &= x - 1
    return ans


def similarity_comparison(url: str, word_list: list, f_path: str, hash_threshold=10) -> bool:
    page_hash_value = Simhash(word_list).value
    if os.path.isfile(f_path) is False:
        f = open(f_path, 'wb')
        pkl.dump([page_hash_value], f)
        f.close()
        return False
    else:
        f = open(f_path, 'rb')
        hash_values = pkl.load(f)
        f.close()
        for hash_value in hash_values:
            if hamming_distance(hash_value, page_hash_value) <= hash_threshold:
                print("[simhash filter] -> " + url)
                return True
        f = open(f_path, 'wb')
        hash_values.append(page_hash_value)
        pkl.dump(hash_values, f)
        f.close()
        return False
