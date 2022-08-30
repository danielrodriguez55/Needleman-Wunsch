# Author: Daniel E. Rodriguez Olivera
# Date: March 19, 2022

#Importing the imports necesary for the project
import sys
import csv

# Match, Mismatch, and Gap Penalty scores and variables
match = 1
mismatch = -1
penalty = -2

#Function solution does the Needleman-Wunsch Algorithm, this function requires 2 sequence and an option
# that option is just to choose wether we get returned the text alignment or the alignment score.
def solution(sequence1,sequence2, option):
    
    length1 = len(sequence1) #The variable length1 stores the length of the first sequence
    length2 = len(sequence2) #The variable length2 stores the length of the second sequence

    #Matrices creation
    matrix = [[0 for i in range(length2+1)] for j in range(length1 + 1)]    #The variable matrix will store the main matrix
    backtrackmatrix = [[0 for k in range(length2)] for l in range(length1)] #The variable backtrackmatrix will store the matrix that will be used to backtrack later on

    #Filling out the backtrackmatrix 
    #We go row by row comparing each position of sequence1 vs sequence2 as follows:
    #If the value in sequence1 is equal to the value in sequence 2 then that spot is a match which means its equal to 1
    #If the values are not equal then we have a mismatch so the spot is equal to -1
    for i in range(len(sequence1)):
        for j in range(len(sequence2)):
            if sequence1[i] == sequence2[j]:
                backtrackmatrix[i][j] = match   
            else:
                backtrackmatrix[i][j] = mismatch

    # Filling up the matrix using Needleman-Wunsch algorithm
    # Initializing the matrix by making the 1st row and 1st column our desired values
    # The desired values are:
    # matrix[i][0] = i * penalty
    # matrix[0][j] = j * penalty
    for i in range(length1+1):
        matrix[i][0] = i * penalty
    
    for j in range(length2 +1):
        matrix[0][j] = j * penalty

    # Filling out the matrix by using:
    #                    { matrix[i-1][j-1] + backtrackmatrix[i-1][j-1]
    #  matrix[i][j] = max{ matrix[i][j-1] + penalty
    #                    { matrix[i-1][j] + penalty
    for i in range(1, len(sequence1) + 1):
        for j in range(1, len(sequence2) + 1):
            matrix[i][j] = max(matrix[i-1][j-1] + backtrackmatrix[i-1][j-1], 
                                matrix[i][j-1] + penalty, 
                                matrix[i-1][j] + penalty)

    # Traceback
    aligned1 = ''  #The variable aligned1 stores the string of the final sequence1
    aligend2 = ''  #The variable aligned2 stores the string of the final sequence2
    score = matrix[length1][length2] #The variable score stores the alignment score

    # A while loop that wont stop until the length of either sequence is 0
    while length1 > 0 and length2 > 0:

        #This if statement checks to see if the diagonal value is the way to go
        if length1 > 0 and length2 > 0 and (matrix[length1][length2] == matrix[length1-1][length2-1] + backtrackmatrix[length1-1][length2-1]):
            aligned1 = sequence1[length1 - 1] + aligned1  #We add the letter to aligned1
            aligend2 = sequence2[length2 - 1] + aligend2  #We add the letter to aligned2
            
            #We subtract from both lengths so the loop isn't infinite
            length1 = length1 - 1
            length2 = length2 - 1
            
            
        #This else if check if up is the way to go
        elif length1 > 0 and matrix[length1][length2] == matrix[length1-1][length2] + penalty:
            aligned1 = sequence1[length1-1] + aligned1 # We add the letter to aligned1
            aligend2 = '-' + aligend2                  # Since we didn't go to the side no letter can be added so we add -

            #We subtract from length1 because we went only up and not to the side
            length1 = length1 - 1
        
        else:
            aligned1 = '-' + aligned1                    # Since we didn't go up no letter can be added so we add -
            aligend2 = sequence2[length2-1] + aligend2   # We add the letter to aligned2

            #We subtract from length 2 because we went only to the side and not up
            length2 = length2 - 1
    
    alignedtext = aligned1 + '\n' + aligend2 #The variable alignedtext stores the alignment text as specified by the professor

    #These if statements decide wether we are returned the alignment score or the alignment text
    if option == 'text':
        return alignedtext

    elif option == 'score':
        return score

openinput = open(sys.argv[1], 'r') # The variable openinput opens the input file we are given using the sys import
#openinput = open('input.csv', 'r')
result = open('results.csv', 'a', newline="") #Creation of the results cvs file that will have the results as specified by the professor

reader = csv.reader(openinput) #The variable reader stores what was read of the input file by using the import csv

header = ['sequence1', 'sequence2', 'alignment text', 'alignment score'] #The variable header stores all of the columns names as specified by the professor
lists = [] #The variable lists will hold all of the lists

listsequence1 = [] #The variable listsequence1 will hold all the values of sequence1
listsequence2 = [] #The variable listsequence2 will hold all the values of sequence2
listalignmenttext = [] #The variable listalignmenttext will hold all the values of the alignment text
listalignmentscore = [] #The variable listalignmentscore will hold all the values of the alignment scores

#This for loop reads all of the rows in reader and adds them row by row to lists
for row in reader:
    lists.append(row)

#This for loop reads all of the items in lists and add all the values in position[0] to listsequence1
for item in lists:
    if item[0] == 'sequence1':
        continue
    else:
        listsequence1.append(item[0])

#This for loop reads all of the items in lists and add all the values in position[1] to listsequence2
for item in lists:
    if item[1] == 'sequence2':
        continue
    else:
        listsequence2.append(item[1])

lengthis = 0  #The variable lengthis will store the length of sequence1

#Since there is no built in function for the length we calculate the length using a for loop that iterates through all of listsequence1 
for item in listsequence1:
    lengthis += 1

lengthwillbe = 0 #The variable lengthwillbe is used to iterate through all our created lists

#This while loop will help us iterate through all of the values of listsequence1 and listsequence2
#which we will use to obtain the alignment text and alignment score values to add them to their respective lists
while lengthwillbe != lengthis:

    text = solution(listsequence1[lengthwillbe], listsequence2[lengthwillbe], 'text') #We call the function solution to get the alignment text
    listalignmenttext.append(text) #We add the alignment text to listalignmenttext

    score = solution(listsequence1[lengthwillbe], listsequence2[lengthwillbe], 'score') #We call the function solution to get the alignment score
    listalignmentscore.append(score) #We add the alignment score to alignmentscore

    lengthwillbe += 1  #We add to lengthwillbe not only to keep iterating through listsequence1 and listsequence2 but also so the loop isn't infinite

lengthwillbe = 0 #We reset the variable

#We use our import csv to start writing to our result file
writer = csv.writer(result)
writer.writerow(header)

#This while loop will help us iterate through all the values in all our combined lists
#all these values are then stored in the answerlist and writen in their specified row
while lengthwillbe != lengthis:
    answerlist = [] 
    answerlist.append(listsequence1[lengthwillbe])
    answerlist.append(listsequence2[lengthwillbe]) 
    answerlist.append(listalignmenttext[lengthwillbe])
    answerlist.append(listalignmentscore[lengthwillbe])
    writer.writerow(answerlist)
    lengthwillbe += 1 #We add to lengthwillbe not only to keep iterating through all our lists but also so the loop isn't infinite

#Finally we close all the opened files
openinput.close()
result.close()
