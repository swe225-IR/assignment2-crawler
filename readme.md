# IR Assignment2

authors: Shilong Li, Wenjun Huang, Yang Liu

## Requirements

### Crawling Paths

- \*.ics.uci.edu/*
- \*.cs.uci.edu/*
- \*.informatics.uci.edu/*
- \*.stat.uci.edu/*
- today.uci.edu/department/information_computer_sciences/*

### Report

See [report](./Assignment-Report.md).

### Specifications

- Install the requirements
- Modify the useragent
- Implementation
  - Return URLs in domain/paths
  - Remove fragment part of the URLs (i.e., https://a.b.c/d#fragment_part)
  - Any third-party libraries
  - Optionally, in the scraper function, you can also save the URL and the web page on your local disk.
- Run with VPN
- Monitor
  - Debug
  - Restart from scratch needs deleting the frontier file (frontier.shelve), or move it to a backup location, before restarting the crawler.

### Requirements
- [ ] Honor the politeness delay for each site
- [ ] Crawl all pages with high textual information content
- [ ] Detect and avoid infinite traps
- [ ] Detect and avoid sets of similar pages with no information
- [ ] Detect and avoid dead URLs that return a 200 status but no data
- [ ] Detect and avoid crawling very large files, especially if they have low information value

### Additional Libraries
```commandline
pip install lxml
```