# Homework 3: Internet

This work is devoted to the study of working with requests.

### Task 1 -  ```task1.py```

Dealing with the ```IMDb Top 250 Movies List```:

1.1 output the top 4 films by the number of user ratings and the number of these ratings;

1.2 Output the top 4 best years (based on the average rating of films this year) and the average rating;

1.3 Plot a sorted barplot showing the number of films in the list for each director (only for directors with more than 2 films in the list);

1.4 Output the top 4 most popular directors (by the total number of people who have rated their films);

1.5 Save data for all 250 films as a table with columns (name, rank, year, rating, n_reviews, director) in any format.

### Task 2 -  ```task2.py```

The ```telegram_logger``` decorator has been written, which logs the launches of the decorated functions and sends .log files and the status of the function execution. See HW_3.ipynb for details on how the decorator works.

### Task 3 - ```my_tblastn.py```

The ```TBlastn``` class was written in the ```my_tblastn``` module, which allows you to align protein sequences with sequences from the __wgs NCBI database__. When creating an __object__ of the TBlastn class, you need to specify: 
- __prot_seq__ (protein sequence); 
- __taxon__ (must be specified along with NCBI taxon_id).

As a result, a list of objects of type ```Alignment``` is returned with the following attributes:
- ```subj_name``` - name of reference sequence;
- ```subj_id``` - id of reference sequence;
- ```subj_len``` - length of reference sequence;
- ```subj_range``` - start, end of attachment of the protein sequence of the reference;
- ```score``` - score of alignment;
- ```e_value``` - E-value of alignment;
- ```identity``` - percent match of two sequences;
- ```query_seq``` - aligned parse sequence;
- ```subj_seq``` - sequence on which query_seq aligned.

All modules required for installation are located in ```requirements.txt```.

Examples of using these scripts are provided in ```HW_3.ipynb```. These scripts were written and tested in __Python 3.11__.
