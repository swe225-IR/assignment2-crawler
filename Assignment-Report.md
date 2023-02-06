# Report

Authors: Shilong Li, Wenjun Huang, Yang Liu

## Q1: Number of unique pages

How many unique pages did you find? Uniqueness is established by the URL, but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL.

As far as we know, we have crawled xxx unique pages, which followed the rules:
- Skip `https://gitlab.ics.uci.edu/*`
- 

However, we did not actually crawl all the web pages in the requirements, because of:
- Network issues
  - Max entries
  - Cache server being shut down
  - VPN connection
- Text processing
  - Slow

## Q2: Longest page

What is the longest page in terms of number of words? (HTML markup doesn’t count as words)

In terms of number of words, the longest page is `https://xxx`. It has xxx words in total.

## Q3: 50 most common words

What are the 50 most common words in the entire set of pages? (Ignore English stop words, which can be found, for example, here Links to an external site.) Submit the list of common words ordered by frequency.
The 50 most common words are:
```json
{
  "just for example" : 10,
  "example 2": 11
}

```

## Q4: Number of subdomains

How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically and the number of unique pages detected in each subdomain. The content of this list should be lines containing URL, number, for example:
http://vision.ics.uci.edu, 10 (not the actual number here)

The subdomain and its number are listed below:
```json
{
  "subdomain.ics.uci.edu": 10,
  "subdomain2.ics.uci.edu": 9
}
```