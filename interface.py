# Python interface for my Answer Set Programming Survo-puzzle Solver
#
#Survo-puzzle: The task is to fill an m*n table by intergers 1,2,...(m*n) so that each of these numbers appear only once.
#And their row and column sums are equal to integers given on the bottom and the right side of the table.
#Often some of integers are given readily in the table in order to guarantee uniquesness of the solution.
#
# This program is a GUI interface for my Survo-puzzle solver written in Answer Set Programming.
# Upon running this program a GUI interface is opened which displays a blank Survo-puzzle board of 3*3 along with one additional column for Row-sum digits and one additional row for Column-sum digits.
# The user enters Row-sum and Column-sum in the cells for a Survo puzzle. The user can optionally enter some number in the cell.  The user then clicks on the
# 'Solve' button which calls the Survo solver and fills in the rest of the puzzle in red.
# If invalid input is given (multiple digits entered in a cell or non digit characters) then,
# when 'Solve' is selected, an error message will display and the invalid entries will be
# cleared.  If the puzzle has no solutions a message box will pop up indicating so.  If the
# puzzle given has multiple solutions only one will be displayed.  Once a puzzle is solved
# the input cells are locked and the 'Solve' button is deactivated until the puzzle is
# cleared with the 'Clear' button.  The 'Clear' button may also be used to clear the board
# at any time.  The 'Quit' button closes the interface.
#

from tkinter import *
from os import system
import tkinter.messagebox

class Survo_puzzleGUI:
    def __init__(self):
        # Constuctor for the GUI interface.  Creates the window and draws the interface.
        self.main_window = Tk()                               # create main window
        self.main_window.title('Survo-puzzle Solver')
        self.main_window.resizable(width=FALSE,height=FALSE)  # make window non-resizable
        self.MainFrame = Frame(width=12, height=12)             # set-up frame for grid
        self.MainFrame.grid(row=0,column=0)                   # activate the frame
        self.subFrame = [([0]*4) for i in range(4)]           # create array for the subframes

        
        
        for i in range(4):
            for j in range(4):
                # create and activate the subframe
                self.subFrame[i][j] = Frame(self.MainFrame,bd=3,relief='ridge')  
                self.subFrame[i][j].grid(row=i*4,column=j*4,rowspan=4,columnspan=4)
        self.cell = [([0]*9) for i in range(9)]               # create array for individual cells
        for i in range(4):
            for j in range(4):
                # create and activate the 16 cells (4 rows of 4 cells).
                # The cells are Entry widgets which allow text input.
                if (i==3 or j ==3):
                    self.cell[i][j] = Entry(self.subFrame[i//3][j//3], width = 2, fg='black') #allocate width=2 for Row-sum and Column-sum cells
                else:
                    self.cell[i][j] = Entry(self.subFrame[i//3][j//3], width = 1, fg='black') # allocate width=1 for 3*3
                self.cell[i][j].grid(row=i,column=j,)
        self.cell[3][3].config(state='readonly')      # make the cell[3][3] as non-writable 
        self.button_row = Frame()                             # create a frame for the buttons
        self.button_row.grid(row=4,column=0)                 # activate the button frame

        # create and activate the 'Solve', 'Clear', and 'Quit' buttons.
        # when the 'Solve' button is clicked the solve_puzzle method is called
        # when the 'Clear' button is clicked the clear_board method is called
        # when the 'Quit' button is clicked the window is destroyed and the program ends
        self.solve_button = Button(self.button_row,text='Solve',command=self.solve_puzzle)
        self.clear_button = Button(self.button_row,text='Clear',command=self.clear_board)
        self.quit_button = Button(self.button_row,text='Quit',command=self.main_window.destroy)
        self.solve_button.grid(row=0,column=0)
        self.clear_button.grid(row=0,column=1)
        self.quit_button.grid(row=0,column=2)

        mainloop()                                            # wait for input

        
    def create_input_file(self):
        # This function creates the file, tempsurvo.sm, from the values input into the cells by the
        # user.  The function also checks if the input is valid.  It returns a boolean value
        # indicating if the input was valid or not.  If the input is not valid, this routine 
        # clears the invalid inputs and pops up a message window indicating that the input was 
        # invalid.  The file tempsurvo.sm is created whether the input was valid or not. 
        valid = True                                          
        fhandle = open('tempsurvo.sm','w')                      # open the file for writing
        for i in range(4):                                    # loop through the cells
            for j in range(4):
                value = self.cell[i][j].get()
                if len(value) > 0 :                            # if a cell is not empty
                    if (j==3) and value.isdigit():
                        fhandle.write('rowsums('+str(i+1)+','+value+').\n')
                    elif (i==3) and value.isdigit():
                        fhandle.write('colsums('+str(j+1)+','+value+').\n')
                    elif len(value)==1 and value.isdigit():     # and it contains a valid digit(1 to 9 for 3*3)
                        # then write a predicate of the form "pos(value,i,j)." to the file
                        fhandle.write('matrix('+str(i+1)+','+str(j+1)+','+value+').\n')
                    else:                                     # if the cell contains invalid input
                        self.cell[i][j].delete(0,END)         # delete the value in the cell
                        valid = False                         # flag the data as invalid
        fhandle.close() 
        if not valid:                                         # if invalid, pop-up a message window
            tkinter.messagebox.showinfo('Error','One or more invalid values were entered.  They have been cleared.')
        return valid                                          # return the valid flag

    def display_output(self):
        # This function reads file survoout.sm and displays the data in the GUI.  This file is created by the
        # Answer Set Survo-puzzle solver and should therefore always have correct formatting. A valid file will
        # contain either a single line with the string "*** no models found." or containing 9 lines of the
        # form 'matrix(i,j,n), and/or rowsums(i,rs) and/or colsums(j,cs)' where n, i, j, rs, cs are integers in the range from 1 to 9, row, column, row-sum and column-sum.
        # A final line consisting the string '::endmodel'.
        fhand2 = open('survoout.sm','r')                        # open the output file created by the solver.
        aspmodel = fhand2.readlines()                         # read all the lines of the file into and array
        # if the first character of the file was an '*' it means the file does not contain an answer.
        # A message will be popped up to indicate this.
        if aspmodel[0][0] == '*':                       
            tkinter.messagebox.showinfo('No Solution','The Survo-puzzle you have given has no solution.')
        else:                                                 # otherwise, if there was a solution
            for item in aspmodel:                             # loop through the strings from the file
                if item[0] == 'm':                            # lines containing data will start with 'p'
                    # on the next two lines 1 is subtracted because in the file rows and columns start with 1 not 0  
                    i = int(item[7])-1                        # the 6th character will indicate row
                    j = int(item[9])-1                        # the 8th character will indicate column
                    if len(self.cell[i][j].get()) == 0:       # if the data is for a cell that is currently blank
                        self.cell[i][j].config(fg='red')      # change the cell's text color to red
                        self.cell[i][j].insert(0,item[11])     # write the value to the GUI
                    self.cell[i][j].config(state='readonly')  # make all cells read-only
            self.solve_button.config(state=DISABLED)          # disable to 'Solve' button


    def solve_puzzle(self):
        # This is the function called when the 'Solve' button is clicked.  It calls the routine to create the
        # input file from the data in the GUI.  Provided the data was valid, if does a systems call to the Survo-puzzle
        # solver and then calls the routine that outputs the results back to the GUI.
        if self.create_input_file():
            system("clingo tempsurvo.sm survo_puzzle.lp | mkatoms > survoout.sm")
            self.display_output()
                    

    def clear_board(self):
        # This is the routine that is called when the 'Clear' button is clicked.  It first activates the 'Solve' 
        # button.  It then loops through all of the input cells in the GUI, changing their state to Normal,
        # their color to black, and deletes the data in the cell.
        self.solve_button.config(state=NORMAL)
        for i in range(4):
            for j in range(4):
                self.cell[i][j].config(state=NORMAL,fg='black')
                self.cell[i][j].delete(0,END)
                
        
# Create the GUI      
Survo_puzzleGUI()
        

