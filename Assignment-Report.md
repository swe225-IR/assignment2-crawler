# Report

Authors: Shilong Li, Wenjun Huang, Yang Liu

## Q1: Number of unique pages

How many unique pages did you find? Uniqueness is established by the URL, but discarding the fragment part. So, for
example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL.

As far as we know, we have crawled **110432** unique pages, which followed the rules:

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

What are the 50 most common words in the entire set of pages? (Ignore English stop words, which can be found, for
example, here Links to an external site.) Submit the list of common words ordered by frequency.
The 50 most common words are:

```json
{
  "just for example": 10,
  "example 2": 11
}

```

## Q4: Number of subdomains

How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically and the
number of unique pages detected in each subdomain. The content of this list should be lines containing URL, number, for
example:
http://vision.ics.uci.edu, 10 (not the actual number here)

The subdomain and its number are listed below:

```json
{
  "wiki.ics.uci.edu": 46099,
  "swiki.ics.uci.edu": 34938,
  "ngs.ics.uci.edu": 2013,
  "www.ics.uci.edu": 1884,
  "wics.ics.uci.edu": 780,
  "grape.ics.uci.edu": 515,
  "sli.ics.uci.edu": 340,
  "sdcl.ics.uci.edu": 202,
  "vision.ics.uci.edu": 200,
  "cml.ics.uci.edu": 181,
  "isg.ics.uci.edu": 136,
  "futurehealth.ics.uci.edu": 122,
  "duttgroup.ics.uci.edu": 87,
  "plrg.ics.uci.edu": 84,
  "mcs.ics.uci.edu": 83,
  "acoi.ics.uci.edu": 74,
  "transformativeplay.ics.uci.edu": 53,
  "tutors.ics.uci.edu": 44,
  "emj.ics.uci.edu": 36,
  "computableplant.ics.uci.edu": 33,
  "dgillen.ics.uci.edu": 25,
  "cbcl.ics.uci.edu": 23,
  "studentcouncil.ics.uci.edu": 21,
  "iasl.ics.uci.edu": 20,
  "industryshowcase.ics.uci.edu": 20,
  "mds.ics.uci.edu": 19,
  "student-council.ics.uci.edu": 19,
  "mhcid.ics.uci.edu": 17,
  "cyberclub.ics.uci.edu": 15,
  "mswe.ics.uci.edu": 14,
  "code.ics.uci.edu": 13,
  "cwicsocal18.ics.uci.edu": 12,
  "flamingo.ics.uci.edu": 12,
  "www-db.ics.uci.edu": 12,
  "support.ics.uci.edu": 11,
  "cradl.ics.uci.edu": 10,
  "unite.ics.uci.edu": 10,
  "chenli.ics.uci.edu": 9,
  "asterix.ics.uci.edu": 7,
  "create.ics.uci.edu": 7,
  "nalini.ics.uci.edu": 7,
  "sherlock.ics.uci.edu": 7,
  "archive.ics.uci.edu": 6,
  "xtune.ics.uci.edu": 6,
  "checkin.ics.uci.edu": 5,
  "helpdesk.ics.uci.edu": 5,
  "statconsulting.ics.uci.edu": 5,
  "elms.ics.uci.edu": 4,
  "evoke.ics.uci.edu": 4,
  "luci.ics.uci.edu": 4,
  "redmiles.ics.uci.edu": 4,
  "stairs.ics.uci.edu": 4,
  "tippersweb.ics.uci.edu": 4,
  "cert.ics.uci.edu": 3,
  "fr.ics.uci.edu": 3,
  "graphics.ics.uci.edu": 3,
  "hpi.ics.uci.edu": 3,
  "hub.ics.uci.edu": 3,
  "keys.ics.uci.edu": 3,
  "mondego.ics.uci.edu": 3,
  "mse.ics.uci.edu": 3,
  "onboarding.ics.uci.edu": 3,
  "tad.ics.uci.edu": 3,
  "esl.ics.uci.edu": 2,
  "hack.ics.uci.edu": 2,
  "hai.ics.uci.edu": 2,
  "informatics.ics.uci.edu": 2,
  "informatics.mt-live.ics.uci.edu": 2,
  "intranet.ics.uci.edu": 2,
  "ipf.ics.uci.edu": 2,
  "motifmap-rna.ics.uci.edu": 2,
  "motifmap.ics.uci.edu": 2,
  "mt-live.ics.uci.edu": 2,
  "netreg.ics.uci.edu": 2,
  "pgadmin.ics.uci.edu": 2,
  "rstudio-hub.ics.uci.edu": 2,
  "seal.ics.uci.edu": 2,
  "wearablegames.ics.uci.edu": 2,
  "www.cert.ics.uci.edu": 2,
  "Transformativeplay.ics.uci.edu": 1,
  "accessibility.ics.uci.edu": 1,
  "aiclub.ics.uci.edu": 1,
  "containers.ics.uci.edu": 1,
  "dejavu.ics.uci.edu": 1,
  "dynamo.ics.uci.edu": 1,
  "frost.ics.uci.edu": 1,
  "graphmod.ics.uci.edu": 1,
  "hobbes.ics.uci.edu": 1,
  "i-sensorium.ics.uci.edu": 1,
  "instdav.ics.uci.edu": 1,
  "ipubmed.ics.uci.edu": 1,
  "jgarcia.ics.uci.edu": 1,
  "mailboss.ics.uci.edu": 1,
  "malek.ics.uci.edu": 1,
  "mdogucu.ics.uci.edu": 1,
  "pastebin.ics.uci.edu": 1,
  "perennialpolycultures.ics.uci.edu": 1,
  "phpmyadmin.ics.uci.edu": 1,
  "psearch.ics.uci.edu": 1,
  "radicle.ics.uci.edu": 1,
  "riscit.ics.uci.edu": 1,
  "sourcerer.ics.uci.edu": 1,
  "speedtest.ics.uci.edu": 1,
  "svn.ics.uci.edu": 1,
  "tastier.ics.uci.edu": 1,
  "ugradforms.ics.uci.edu": 1,
  "webmail.ics.uci.edu": 1,
  "www.graphics.ics.uci.edu": 1,
  "www.informatics.ics.uci.edu": 1
}
```