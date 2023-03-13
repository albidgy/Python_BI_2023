# Homework 2: Decorators and Iterators

In this work, have been created:
- iterators and iterable objects;
- own function and class decorators.

### Task 1 -  ```task1_and_2.py```

The ```MyDict``` class has been written, which completely repeats the behavior of a regular dictionary, except that during iteration we get both keys and values.

### Task 2 -  ```task1_and_2.py```

The ```iter_append``` function was written, which adds a new element to the end of an iterator, returning an iterator that includes the original elements and the new element.

### Task 3 -  ```task3.py```

A class decorator ```@change_obj_type``` has been written that allows the inheritors of the str (```MyString```) and set (```MySet```) classes to return an instance of the current class for all necessary methods (__including__ methods inherited from str and set).

### Task 4 - ```task4.py```

The ```@switch_privacy``` class decorator has been written, which:
- makes all public methods of a class private;
- makes all private methods of a class public;
- dunder methods and protected methods remain unchanged.

### Task 5 - ```task5.py```

An ```OpenFasta``` context messenger has been written that reads sequences in fasta-file (both 1 sequence - ```read_record```, and all sequences in the file - ```read_records```) and returns a ```FastaRecord``` object.

Example of ```FastaRecord``` object:
```python
FastaRecord(seq='ATGGGCGATCTTGCTATGTCCGTAGCAGACATCAGG', 
            id_='>gene_01', 
            description='Test sp.')
```

### Task 6 - ```task6.py```

Prediction of different genotypes when crossing two organisms:

1. The ```print_offspting``` method allows you to get all possible (non-unique) genotypes when crossing two organisms.
2. The ```get_offspting_genotype_probability``` method calculates the probability of a certain genotype occurring (its expected proportion in the offspring).
3. The ```get_unique_genotypes_with_substring``` method returns all unique genotypes when two parents are crossed and contain a specific substring of the alleles.

Examples of using these scripts are provided in ```HW_2.ipynb```. These scripts were written and tested in __Python 3.11__.
