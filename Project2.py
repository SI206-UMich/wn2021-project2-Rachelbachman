from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    f=open(filename, "r")
    soup=BeautifulSoup(f, 'html.parser')
    authors=soup.find_all("a", class_="authorName")
    titles=soup.find_all("a", class_="bookTitle")

    newAuthors=[]
    newTitles=[]

    for title in titles:
        striptitle=title.text.strip()
        newTitles.append(striptitle)

    for author in authors:
        stripauthor=author.text.strip()
        newAuthors.append(stripauthor)

    l=list(zip(newTitles, newAuthors))

    f.close()
    return l
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """



def get_search_links():
    url="https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    resp=requests.get(url)
    soup=BeautifulSoup(resp.content, 'html.parser')

    url_list=[]
    table=soup.find('table', class_='tableList')
    x=table.find_all('tr')
    for row in x[:10]:
        info = row.find_all('td')
        url=info[0].find('a')
        link="https://www.goodreads.com" + str(url['href'])
        url_list.append(link)
    return url_list
    
    

    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """


def get_book_summary(book_url):
    resp= requests.get(book_url)
    soup= BeautifulSoup(resp.text, 'html.parser')
    title=soup.find('h1', class_='gr-h1--serif')
    title_text=title.text.strip()
    pages=soup.find('span', itemprop='numberOfPages')
    pages_text=pages.text.split()
    pages_num=int(pages_text[0])
    author=soup.find('span', itemprop= 'name')
    author_text=author.text.strip()
    
    bookInfo= (title_text, author_text, pages_num)
    return bookInfo 
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    


def summarize_best_books(filepath):
    f=open(filepath,'r')
    soup=BeautifulSoup(f, 'html.parser')

    category=soup.find_all('h4', class_='category__copy')
    categories=[]
    for i in category:
        categories.append(i.text.strip())

    name=soup.find_all('img', class_='category__winnerImage')
    titles=[]
    for i in name:
        titles.append(i['alt'])
    links=soup.find_all('div', class_='category clearFix')
    urls=[]
    for i in links:
        new=i.find('a').get('href')
        urls.append(new)
    lst=list(zip(categories, titles, urls))

    f.close()
    return lst



    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    


def write_csv(data, filename):
    with open(filename, 'w') as f:
        write=csv.writer(f)
        write.writerow(['Book Title', 'Author Name'])
        for i in data:
            write.writerow(i)
        
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):
    search_urls=get_search_links()

    # call get_search_links() and save it to a static variable: search_urls


    def test_get_titles_from_search_results(self):
        localvar=get_titles_from_search_results('search_results.htm')
        self.assertEqual(len(localvar), 20)
        self.assertIsInstance(localvar, list)
        for i in localvar:
            variable=i
            self.assertIsInstance(variable, tuple)

        
        testTuple=localvar[0]
        self.assertEqual(testTuple, ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # call get_titles_from_search_results() on search_results.htm and save to a local variable

        # check that the number of titles extracted is correct (20 titles)

        # check that the variable you saved after calling the function is a list

        # check that each item in the list is a tuple

        # check that the first book and author tuple is correct (open search_results.htm and find it)

        # check that the last title is correct (open search_results.htm and find it)

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)
        self.assertEqual(len(TestCases.search_urls), 10)
        for i in TestCases.search_urls:
            self.assertIsInstance(i, str)
        for i in TestCases.search_urls:
            self.assertEqual(i[0:35], 'https://www.goodreads.com/book/show')

        # check that the length of TestCases.search_urls is correct (10 URLs)


        # check that each URL in the TestCases.search_urls is a string
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)

        # check that the number of book summaries is correct (10)

            # check that each item in the list is a tuple

            # check that each tuple has 3 elements

            # check that the first two elements in the tuple are string

            # check that the third element in the tuple, i.e. pages is an int

            # check that the first book in the search has 337 pages
        summaries=[]
        for i in TestCases.search_urls:
            summaries.append(get_book_summary(i))
        self.assertEqual(len(summaries),10)
        for i in summaries:
            self.assertIsInstance(i,tuple)

            self.assertEqual(len(i), 3)
            self.assertIsInstance(i[0], str)
            self.assertIsInstance(i[1], str)
            self.assertIsInstance(i[2], int)
        self.assertEqual(summaries[0][2], 337)
            

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        variable= summarize_best_books('best_books_2020.htm')
        self.assertEqual(len(variable), 20)

        for i in variable: 
            var=i
            self.assertIsInstance(var, tuple)
            self.assertEqual(len(i), 3)

        testTuple2=variable[0]
        self.assertEqual(testTuple2, ('Fiction', 'The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))

        testTuple3= variable[-1]
        self.assertEqual(testTuple3, ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))
        # check that we have the right number of best books (20)

            # assert each item in the list of best books is a tuple

            # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        


    def test_write_csv(self):
        writer_var=get_titles_from_search_results('search_results.htm')
        write_csv(writer_var, 'test.csv')
        with open('test.csv', 'r') as f:
            read_csv=csv.reader(f)
            csv_lines=[]
            for i in read_csv:
                csv_lines.append(i)
        self.assertEqual(len(csv_lines),21)
        self.assertEqual(csv_lines[0], ['Book Title', 'Author Name'])
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison'])
        # call get_titles_from_search_results on search_results.htm and save the result to a variable

        # call write csv on the variable you saved and 'test.csv'

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)


        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'

        

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



