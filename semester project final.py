# Kayla Seidel
# semester project- Extreme Card Stacking

# "I hereby certify that this program is solely the result of my own work and \
# is in compliance with the Academic Integrity policy of the course syllabus."

# HOW TO PLAY:
# This is a card stacking game. The objective of the game is to stack the cards
# from the grid onto the stacking pile at the bottom of the screen, from lowest
# to highest value, within the given time limit. The values are ranked from ace
# to king, and club < diamond < heart < spade; for example, user would attempt
# to stack the Ace of Clubs, then Ace of Diamonds, Ace of Hearts, Ace of Spades,
# 2 of Clubs, 2 of Diamonds, etc. If the user is unable to clear the board within
# the time limit, the game is over, and the user has the option to play again.
# If the board is cleared within the time limit, the user moves on to the next
# round, in which the time is reduced by 30 seconds. The user keeps moving onto
# the next round until the time limit is 30 seconds, after which, if the board
# is cleared, the game is over, and the user has won.

import random
import Draw
import time

CARD_WIDTH = 73 # the width of each card
CARD_HEIGHT = 97 # the height of each card
SPACING = 10 # the spacing between each card

# create a deck of cards
def createDeck():
    # create an empty list for the deck, a list of suit letters, and a list of
    # card numbers
    deck = []
    suits = ["H", "D", "C", "S"]
    cardNum = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
    
    # create the deck by adding the suit letters and numbers to the deck list
    for i in range(len(cardNum)):
        for j in range(len(suits)):
            # add the indexes of card numbers and suits to add cards to deck
            # and add ".gif" to be able to invoke the downloaded gifs of the cards
            deck += [cardNum[i] + suits[j] + ".gif"]
    
    # shuffle the deck so it is randomly set up
    random.shuffle(deck)
    
    return deck # return the deck list

# ^this function creates a list of a deck of playing cards by creating a list
# of suits and a list of numbers 1 to 13, and adding the elements of each list
# to an empty list. Then, the function shuffles the deck list and returns it.


def createGrid(cardDeck):
    
    # create a 13 by 4 2D list, which will be a grid for the cards
    theGrid = [[None for col in range(13)] for row in range(4)]
    
    # add the cards from the previously created deck to the grid
    # by making each row and column combination a card number and adding
    # each card number index of the deck to the positions in the grid
    for row in range(len(theGrid)):
        for col in range(len(theGrid[0])):
            nCard = row * 13 + col
            theGrid[row][col] = cardDeck[nCard]
            
    return theGrid # return the 2D list grid of cards

# ^this function takes the deck as input, creates an empty 2D list (grid) of 4
# rows and 13 columns, and adds the cards in the deck to each position in the
# grid. It then returns the grid.


def drawBoard(gridCards, topCard, gameScore, timeRemaining):
    Draw.clear() # clear canvas
    
    # set background color to green
    Draw.setBackground(Draw.color(50, 205, 50))
    
    # draw the stacking pile, a rectangle, with the top card drawn on it
    Draw.setColor(Draw.GRAY)
    Draw.rect(508, 448, 73, 97)
    Draw.rect(509, 449, 71, 95)
    Draw.rect(510, 450, 69, 93)
    Draw.picture(topCard, 508, 448)
    
    # draw the time remaining in seconds
    Draw.setColor(Draw.WHITE)
    Draw.filledRect(10, 505, 260, 40)
    Draw.setFontSize(24)
    Draw.setFontBold(True)
    Draw.setColor(Draw.color(50, 205, 50))
    Draw.string("Time Remaining:", 20, 511)
    # when there are only 10 seconds left of the round, change the color of the
    # time to red to warn user that time is running out!
    if int(timeRemaining) <= 10:
        Draw.setColor(Draw.RED)
    else:
        Draw.setColor(Draw.color(50, 205, 50))
    Draw.string(int(timeRemaining), 220, 511)
    
    # draw the score
    Draw.setColor(Draw.WHITE)
    Draw.filledRect(10, 455, 135, 40)
    Draw.setColor(Draw.color(50, 205, 50))
    Draw.string("Score:", 20, 461)
    Draw.string(gameScore, 100, 461)
    
    # draw the start over button
    Draw.picture("start over button.gif", 930, 441)
    
    # draw a 4 x 13 grid of gray rectangles the size of the cards, to show when
    # a card is missing
    Draw.setColor(Draw.GRAY)
    for row in range(4):
        for col in range(13):
            x = col * (CARD_WIDTH + SPACING)
            y = row * (CARD_HEIGHT + SPACING)
            
            Draw.filledRect(x+SPACING, y+SPACING, CARD_WIDTH, CARD_HEIGHT)    
    
    # for each position in grid, if there should be a card, compute the x, y
    # of the card
    for row in range(len(gridCards)):
        for col in range(len(gridCards[0])):
            if gridCards[row][col] != None:
                x = col * (CARD_WIDTH + SPACING)
                y = row * (CARD_HEIGHT + SPACING)
            
                # draw the card
                Draw.picture(gridCards[row][col], x+SPACING, y+SPACING)              
                
    Draw.show() # show drawings
    
# ^this function draws the board. It takes as input the grid of cards, the top
# card (card on top of the stacking pile), the current score, and the remaining
# time. The function draws all of the elements of the board, including the time.
# score, stack pile, start over button, outlines of cards, and the card gifs
# themselves. Then, it draws all of those elements onto the canvas.


def playGame(grid, timeAllowed, score):
    startTime = time.time() # get start time from time.time()
    top = "" # set top as empty
    # when grid becomes a 4 x 13 2D list of all None's, it == empty
    empty = [[None for col in range(13)] for row in range(4)]
    
    # before starting, the remaining time is the amount of time allowed
    timeRemaining = timeAllowed
    # the highest card is the 13 of spades
    highestCard = "13S.gif"
    
    # loop while there is still time, there are still cards in the grid, and
    # the top card is not the 13 of spades (there are still moves possible)
    while timeRemaining > 0 and grid != empty and top != highestCard:
        if Draw.mousePressed(): # if user clicked
            # get the x, y coordinates of the click
            x = Draw.mouseX()
            y = Draw.mouseY()
            
            # convert x, y to row, col
            for row in grid:
                for col in grid:
                    col = x // (CARD_WIDTH + SPACING)
                    row = y // (CARD_HEIGHT + SPACING)
            
            # if row and col are both valid and the grid is not empty, assign
            # the card in the row, col position selected as the new card
            if row >= 0 and row < 4 and col >= 0 and col < 13 and \
               grid[row][col] != None:
                newCard = grid[row][col]
                
                # if the selected card's value is greater than the top card,
                # make it the top card, remove it from the grid, and draw the
                # card on the top of the stacking pile. Then add 1 to the score
                if newCard >= top:
                    top = newCard # make top newCard
                    grid[row][col] = None # remove card from list
                    Draw.picture(top, 506, 446) # draw card on pile
                    score += 1 # add 1 to score
            
            # if start over button is pressed, return None, reset board
            if x >= 930 and x <= 1175 and y >= 441 and y <= 551:
                return None, 0, 0
        
        # recompute remaining time
        timeRemaining = timeAllowed - (time.time() - startTime)
        # redraw board with the new variations
        drawBoard(grid, top, score, timeRemaining)
        
    # if the grid is empty (user has completed all stacking), returns True,
    # the amount of time remaining and the score
    if grid == empty:
        return True, timeRemaining, score
    # if time ran out or there are no more moves, returns False, the amount of
    # time remaining and the score
    else:
        return False, timeRemaining, score
    
# ^this function takes as input the grid of cards, the time allowed for the
# round, and the score. While the time is still running, the board is not
# cleared, and the top card is not the 13 of spades, when the user clicks on a
# card, if it is higher than the top card, it is moved to the top pile and 1 is
# added to the score. Then the time remaining is recomputed and the board is
# redrawn with all of the new variations to the variables. If the start over
# button is pressed, the game resets. When the code falls out of the loop, if
# it is because the grid is empty, the function returns a tuple with True,
# the amount of time remaining and the score. If the time ran out or there are
# no more moves available, the function returns a tuple with False, the 
# amount of time remaining and the score.


def endGame(end, timeAmount):
    while True:
        # if 4 rounds are won (until the total time is less than 30 seconds),
        # and the board has been cleared, user wins the game!
        if timeAmount <= 30 and end[0] == True:
            # draw the you win screen
            Draw.picture("you win.gif", 0, 0)
            
            # this is the button to press to play game again
            Draw.picture("play again.gif", 900, 370)
            
            # draw the final score of the game
            Draw.picture("final score.gif", 400, 370)
            Draw.setFontSize(40)
            Draw.setFontBold(True)
            Draw.setColor(Draw.BLACK)
            Draw.string(end[2], 525, 445) # end[2] = the final score
            
            # if user clicks on the play again button, this function returns
            # False, which will reset game
            if Draw.mousePressed():
                # get x, y coordinates
                x = Draw.mouseX()
                y = Draw.mouseY()
                if x >= 900 and x <= 1050 and y >= 370 and y <= 520:
                    return False, 0
        
        # this is for the start over button- if it was clicked, this function
        # returns False, which will reset game
        elif end[0] == None:
            return False, 0
        
        # if board was cleared, user moves on to the next round- the board resets,
        # but the points roll over and the time is reduced by 30 seconds
        elif end[0] == True:
            # if user won the round, the amount of time left is added to the score 
            finalScore = end[2] + int(end[1]) # end[2] = finalScore, end[1] = timeRemaining
            # draw the next round screen
            Draw.picture("next round.gif", 0, 0)
            
            # this is the button to press for the next round
            Draw.picture("play next round.gif", 900, 370)
            
            # draw the total score for the round
            Draw.picture("total score.gif", 400, 370)
            Draw.setFontSize(40)
            Draw.setFontBold(True)
            Draw.setColor(Draw.BLACK)            
            Draw.string(finalScore, 525, 445)
            
            # if user clicks on the next round button, returns True, which will
            # reset the board, but keeps the score and is 30 seconds less
            if Draw.mousePressed():
                # get x, y coordinates
                x = Draw.mouseX()
                y = Draw.mouseY()
                if x >= 900 and x <= 1050 and y >= 370 and y <= 520:
                    return True, finalScore
        
        # if user has not cleared the board, returns False: game is over- user
        # has the option to click play again, which will reset the board, time,
        # and score
        elif end[0] == False:
            # draw the game over screen
            Draw.picture("game over.gif", 0, 0)
            
            # this is the button to press to play again
            Draw.picture("play again.gif", 900, 370)
            
            # draw the final score of the game
            Draw.picture("final score.gif", 400, 370)
            Draw.setFontSize(40)
            Draw.setFontBold(True)
            Draw.setColor(Draw.BLACK)            
            Draw.string(end[2], 525, 445) # end[2] = the final score
            
            # if user clicks on the play again button, this function returns
            # False, which resets the game
            if Draw.mousePressed():
                # get x, y coordinates
                x = Draw.mouseX()
                y = Draw.mouseY()
                if x >= 900 and x <= 1050 and y >= 370 and y <= 520:
                    return False, 0
                
# ^this function deals with the code after playGame() has returned. It takes as
# input whatever playGame returns, and the total time allowed for the game. If
# the total time allowed for the game is less than or equal to 30 and the user
# clears the board, user wins and the final score is displayed, and the function
# returns False. If playGame returned None, this function returns False. If
# playGame returned True, it displays next round and total score so far (score +
# remaining time), and function returns True and the score. If playGame returned
# False, it displays game over and final score, and this function returns False.
# This function is returned once the user clicks the button that says either
# "play" or "play again."
              
                    
def titlePage():
    # draw the title page screen and start button
    Draw.picture("title page.gif", 0, 0)
    Draw.picture("start-game-button.gif", 449, 420)
    Draw.show() # show drawings
    
    # if start button is clicked, return function- takes the code back to the
    # main function
    while True:
        if Draw.mousePressed():
            # get x, y coordinates
            x = Draw.mouseX()
            y = Draw.mouseY()
            
            if x >= 449 and x <= 649 and y >= 420 and y <= 520:
                Draw.clear()
                return
            
# ^this function is the game's title page. It draws the title page and start
# game button and when user clicks the start game button, it returns to the
# main function
          
                
def instructionsPage():
    # draw instructions page
    Draw.picture("instructions.gif", 0, 0)
    Draw.show() # show drawing
    
    # if play game button is clicked, return function- takes the code back to the
    # main function
    while True:
        if Draw.mousePressed():
            # get x, y coordinates
            x = Draw.mouseX()
            y = Draw.mouseY()
            
            if x >= 125 and x <= 522 and y >= 392 and y <= 542:
                Draw.clear()
                return
            
# ^this function draws the game's instructions. When user clicks the start
# button, the function returns to the main function
    
    
def main():
    Draw.setCanvasSize(1090, 555) # draw a 1090 x 555 canvas
    titlePage() # invoke the title page
    instructionsPage() # invoke the instructions page
    totalTimeAllowed = 120 # set total time to 120
    totalScore = 0 # set total score to 0
    
    # loop for the entirety of the game
    while True:
        # create the deck and then create the grid of cards, using the deck as
        # input
        theDeck = createDeck()
        cardGrid = createGrid(theDeck)
        # set the game variable to the playGame function
        game = playGame(cardGrid, totalTimeAllowed, totalScore)
        # set the theEnd variable to the endGame function
        theEnd = endGame(game, totalTimeAllowed)
        
        # if the user won the round (but not the whole game yet):
        # if the first element of game (playGame)'s returned tuple returned True,
        # reset the grid of cards, decrease the total time by 30, and recompute
        # the total score
        if game[0] == True:
            cardGrid = createGrid(theDeck)
            totalTimeAllowed = totalTimeAllowed - 30
            totalScore = theEnd[1] # theEnd[1] = the total score
        
        # if the user either won or lost the game:
        # if the first element game's returned tuple is False or None, or the
        # first element of theEnd's returned tuple is False, reset the grid of
        # cards, set the total time back to 120, and reset the total score to 0
        elif game[0] == False or game[0] == None or theEnd[0] == False:
            cardGrid = createGrid(theDeck)
            totalTimeAllowed = 120
            totalScore = 0

main()

# ^this is the main function of the program. It draws the canvas, title page,
# then the instructions, and sets the default total time allowed and score.
# For the entirety of the game, the function takes the deck, inputs it into
# the grid, then runs the playGame function, and then the endGame function.
# If the first element of the tuple returned from playGame() is True, this
# function resets the grid, decreases the total time by 30, and recomputes the
# total score (the game is not over). If the first element of the tuple returned
# from playGame() is False or none, or the first element of theEnd function
# returns False, this function resets the grid, time, and score back to their
# defaults (this means the game is over).