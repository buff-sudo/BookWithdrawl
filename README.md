# BookWithdrawl
This is a sample of the code used to automate the book withdrawl procedure at my public library. All propietary information has been cleaned and the code is not intended to run as currently presented.

The process is to take a list of barcodes from books that have been physically withdrawn, but have not been input into the ILS. Then, the code uses windows automation to search for the item record in the ILS, check if there are other copies that are able to circulate, and if not, adds the item to a csv file so that selectors can be notified that a book in their collection may need to be repurchased according to their preferences.
