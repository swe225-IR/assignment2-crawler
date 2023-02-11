# IR Assignment2

Authors: Shilong Li, Wenjun Huang, Yang Liu

## How to run this project on Windows

1. on Windows: `ssh <your-uci-netid>@openlab.ics.uci.edu`
2. On Linux: `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
3. On Linux: `chmod +x Miniconda3-latest-Linux-x86_64.sh`
4. on Linux: `bash ./Miniconda3-latest-Linux-x86_64.sh` (all type yes)
5. On Windows: `git clone https://github.com/swe225-IR/assignment2-crawler.git`
6. On Windows: `scp -r ./assignment2-crawler <your-uci-netid>@open.ics.uci.edu: ~/projects/`
7. On Linux: `cd ~/projects/assignment2-cralwer`
8. On Linux: `conda create -n a2 python=3.10 && conda activate a2`
9. On Linux: `chmod +x ./setup.sh && ./setup.sh`
10. Modify `config.ini`
11. On linux: `python launch.py`
12. If you want to delete the crawler log before, just `chmod +x ./clean.sh && ./clean.sh`

## Requirements

### Crawling Paths

- \*.ics.uci.edu/*
- \*.cs.uci.edu/*
- \*.informatics.uci.edu/*
- \*.stat.uci.edu/*
- today.uci.edu/department/information_computer_sciences/*

### Report

See [report](./CS221_assignment2.pdf).

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
- [x] Honor the politeness delay for each site
- [x] Crawl all pages with high textual information content
- [x] Detect and avoid infinite traps
- [x] Detect and avoid sets of similar pages with no information
- [x] Detect and avoid dead URLs that return a 200 status but no data
- [x] Detect and avoid crawling very large files, especially if they have low information value

### Additional Libraries
See [requirements.txt](./requirements.txt)
