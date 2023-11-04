# Database_Project

Team: 
    Jaya Sumanth Sasapu (12616846)
    Harshavardhan Pailla (12616368)
    Sree Harrsha Singara (14447265)
    Deerangula Harsha Vardhan (12613619)


Dataset: The sample data contains attributes like StudenetID, FirstName, Lastname, Course, Professor,
ProfessorEmail, CourseStart, CourseEnd. It contains 5 tuples. The dataset is taken as .csv file(comma
separated values).
Functional Dependencies: The functional dependencies used for the dataset are:
StudentID -> FirstName, LastName
Course, Professor -> classroom
Course -> CourseStart, CourseEnd
Professor -> ProfessorEmail
Multi-valued dependencies: The multi-valued dependencies used for the dataset are:
Course ->> Professor
Course ->> classRoom
StudentID ->> Course
StudentID ->> Professor
The functional dependencies and multi-valued dependencies are taken as .txt files(functional_dependencies.txt,multivalued_dependencies.txt).
User Input:
• Choice of the highest normal form to read(1NF,2NF,3NF,BCNF,4NF,5NF).
• Primary key used(StudentID, Course)
Core Components:
1. Input Parser: The parser function is used to read the csv file and the txt file which is used to store the functional dependencies. It breaks down the text into recognized strings of characters.
2. Normalizer: The Normalizer decomposes the input dataset into the required normal form based on the given functional dependencies. The normalization methods are used to decompose the given dataset into the user-required normal form.
3. SQL Query Generator: It refers to a tool or functionality that helps to generate the SQL queries.

Deliverables:
Source Code: Here, we have used the Python programming language to normalize the given dataset.
Code Description:
• The Python libraries are imported, to perform the required operations.
• The input dataset is given as .csv file. The read method is used to read the data from the file.
• The open method is used to open and read the functional dependencies txt file.
• The Parser method is used to convert the given input files into the string characters.
• bcnf_decomosition function is defined to decompose the relation into BCNF normal form.
• in_1nf method is defined to check whether the dataset is in 1NF or not.
• in_2nf method is defined to check whether the dataset is in 2NF or not.
• in_3nf method is defined to check whether the dataset is in 3NF or not.
• in_bcnf method is defined to check whether the dataset is in BCNF or not.
• in_4nf method is defined to check whether the dataset is in 4NF or not.
• in_5nf method is defined to check whether the dataset is in 5NF or not.
• first_normal_form function is defined to decompose the given dataset into the 1NF.
• second_normal_form function is defined to decompose the given dataset into the 2NF.
• third_normal_form function is defined to decompose the given dataset into the 3NF.
• bc_normal_form function is defined to decompose the given dataset into the BCNF.
• fourth_normal_form function is defined to decompose the given dataset into 4NF.
• decomposing_to_5nf function is defined to check for the lossless decomposition of 5NF.
• fifth_normal_form function is defined to decompose the given dataset into 5NF.
• output function is defined to generate the user required output results.
• sql_query_1NF function is defined to print the 1NF sql query as an output.
• sql_query_2_3 function is defined to print the 2NF, 3NF sql queries as output.
• sql_query_BCNF_4_5 function is defined to print the BCNF, 4NF, 5NF sql queries as output.
• Checking for the normal form of the given dataset whether it is in any type of normal form or not.
• The highest normal form of the given dataset can be found by using the functions in_1nf, in_2nf, in_3nf, in_4nf, in_bcnf and in_5nf from the variable high_normalform.



Code Execution and Flow:

• After we start running the code, we will get info in the console as below.
• Enter the highest normal formal to normalize the given table press 1 for 1NF, 2 for 2NF,3 for 3NF, B for BCNF,4 for 4NF and 5 for 5NF.
• Then press 1 to get the highest normal form of the given relation and 2 if the highest normal form is not required.
• Then enter the primary key values which is separated by commas for this relation the primary key should be given as StudentID,Course.
• If the given table is not in the normal form that is provided then it decomposes the table until it satisfies the given normal form then it provides the query of the decomposed tables.
• Else if the given table satisfies the provided normal form then it returns the query of the original table.
• For the 5NF, the candidate keys are provided for each and every table. For the student table the candidate key is StudentID, for the course table the candidate key is Course and for the professor table the candidate key is Professor.
• At the end the highest normal form satisfied by the given table is displayed. The given table satisfies only 1NF.
