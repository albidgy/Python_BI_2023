# Homework 1: OOP

In this work several classes have been created (including an abstract class). Also dunder methods have been studied and applied.

### Task 1 - ```task1.py```

The Chat, Message and User classes are implemented with the following functionality:
* Chat
  - ```chat_history``` attribute, where all messages (Message) are stored;
  - ```show_last_message``` method that displays information about the last message;
  - ```get_history_from_time_period``` method, which takes two optional arguments (dates from which and to which we look for messages and issue them). The method must also return an object of type Chat; 
  
  *By default, it takes the time when the first and last message hit the server (input type: string or datetime).
  - ```show_chat``` method that displays all messages;
  - ```recieve method``` that received a message and add it to the chat.
* Message
  -  ```text``` attribute containing the text of the message;
  - ```datetime``` attribute containing the text date and time of the chat hit message;
  - ```user``` attribute containing information about the user who left the post;
  - ```show``` method that prints or returns information about the message;
  - ```send``` method that will send a message to the chat.
* User
  - ```user``` attridute containing username;
  - ```say_hi``` method that print hello.

### Task 2 - ```task2.py```

The function call functionality is implemented as follows:
```python3
sum << Args([1, 2]) -> 3
```

### Task 3 - ```task3.py```

A float inheritance class is made, which, when receiving attributes of the <action> _ <number> format, we get the result of such an action on our number.
```python3
StrangeFloat(3.5).add_1 -> 4.5
```

### Task 4 - ```task4.py```

Replaced in the source code the maximum possible number of syntactic constructions with calls to dunder methods.

### Task 5 - ```task5.py```

Implemented work with various acidsequences (DNA, RNA, Amino).

* BiologicalSequence (abstract class)
  - working with the len function;
  - the ability to get elements by index and slice the sequence (similar to strings);
  - printing in a convenient form and the ability to convert to a string;
  - the ability to check the alphabet of the sequence for correctness.
* AcidSequence(BiologicalSequence) - intermediate class between the Biological Sequence class and the NucleicAcidSequence and AminoAcidSequence classes. Implements an interface BiologicalSequence.
* NucleicAcidSequence(AcidSequence)
  - ```complement``` - an additional method that returns a complementary sequence;
  - ```gc_content``` - additional method returning GC contents (%).
* DNASequence(NucleicAcidSequence)
* RNASequence(NucleicAcidSequence)
  - ```transcribe``` - an additional method returning the transcribed sequence.
* AminoAcidSequence(AcidSequence)
  - ```translate``` - an additional method, which returns the amino acid sequence from a one-letter notation to a three-letter notation.

Examples of the use and interaction of classes are presented in ```HW_1.ipynb```.
  
All modules required for installation are located in ```requirements.txt```.
