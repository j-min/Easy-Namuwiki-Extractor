# Easy NamuWiki Extractor 
Simple [Namuwiki](namu.wiki) Extractor extension of [Namu Wiki Extractor](https://github.com/hyeon0145/namu-wiki-extractor)

This module strips the namu mark from a namu wiki document and extracts its plain text only.

# Environment
- Python 2, 3
- [tqdm](https://pypi.python.org/pypi/tqdm)

# Usage

- Clone this repo : `git clone https://github.com/j-min/Easy-Namuwiki-Extractor`

- Download Namuwiki json dump inside directory of repo : `wget http://file2.unofficialnis.ga/namuwiki_161031.json`

- You can find latest dumps [here](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EB%8D%A4%ED%94%84)

- Run extractor: `python Run_extractor.py -i input_json_file -o outputfile_name`

- Tags:

```
--input (-i) : input filename
--output (-o) : output filename
--multiprocess (-m) : run multiprocessing module
--title (-t) : include titles of documents while extracting
```

# How Namuwiki Json looks like

![alt tag](https://cloud.githubusercontent.com/assets/18069263/19549777/3ba7f22e-96e1-11e6-9b2a-330cee31566d.png)

- from [web json viewer](http://jsonviewer.stack.hu/)


# Sample Output

![alt tag](https://cloud.githubusercontent.com/assets/18069263/20699834/d9974d38-b64c-11e6-9fd3-06dac16efc38.png)
