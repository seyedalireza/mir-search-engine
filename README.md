# MIR Course Project
This project is an information retrieval system used for finding Persian or English documents based on their respective datasets.<br>
To retrieve documents the following five stages are performed:
1. Input data is preprocessed in multiple ways, it is normalized, tokenized, and unnecessary words are removed from it.
2. *Positional* and *Bigram* indexing is done on the preprocessed inputs.
3. Indexes are compressed using *Variable Byte* and *gamma code*.
4. The query is corrected based on bigram indexing and *Jaccard* metric.
5. The query is retrieved using the following methods:<br>
  
      * Retrieval using tf-idf with lnc-ltc weighting scheme
      * Retrieval using proximity search in tf-idf space with lnc-ltc weighting scheme
<br>

To improve search results several classification methods (Naive Bayes, K-NN, SVM, and Random Forest) are implemented, that predict documents' views. In this way, the user has the option to search between the documents that have high or low view counts.
<br>

This project also contains a crawler that is used to retrieve information on papers from *Microsoft Academic* website.

# Usage
To run this program, first, install the libraries mentioned in the requirement.txt file. This can be done using pip:
<br>
```
pip install -r requirement.txt
```
Then open the entire project using an IDE, e.g. PyCharm, and run src/pre-execution.py to perform the aforementioned preprocessing tasks and then run src/main.py to access the main search engine. <br>
To execute the crawler, run src/crawler.py to retrieve information on the said papers.
