# Script to test your knowledge with Jeopardy! questions 
# It loads a dataset with data from Jeopardy!, chooses a question at random
# and ask the user for an answer. It checks the answer and tells the user
# the answer was correct or not

import pandas as pd
import numpy as np

# Load dataset and initial cleaning
jeopardy_data = pd.read_csv('./materials/jeopardy.csv',
        parse_dates = [' Air Date']
        )
jeopardy_data.rename(
        columns = {
            'Show Number': 'show_num',
            ' Air Date': 'air_date',
            ' Round': 'rounds',
            ' Category': 'category',
            ' Value': 'price',
            ' Question': 'question',
            ' Answer': 'answer'
            }, 
        inplace = True
        )
## Clean price colum
jeopardy_data.price.replace(
        '\$(?P<dig1>\d+),?(?P<dig2>\d+)?$','\g<dig1>\g<dig2>',
        regex = True, inplace = True
        )

jeopardy_data.price.replace('None', 0, regex = True, inplace = True)
jeopardy_data.price = pd.to_numeric(jeopardy_data.price, downcast='float')

## Clean rounds column
jeopardy_data['rounds'] = jeopardy_data['rounds'].astype("category")

## Clean show_num column
jeopardy_data['show_num'] = jeopardy_data.show_num.astype("object")

## Clean answer column
jeopardy_data.answer.replace(np.nan, 'null', inplace= True)


# Jeopardy Game
def get_random_row(dataframe):
    """Returns a row at random from the dataset"""
    num_questions = dataframe.shape[0]   
    return dataframe.iloc[np.random.randint(0, num_questions)]

# Start the game
print('This is Jeopardy!')
game_on = True

while game_on == True:
    row = get_random_row(jeopardy_data)
    print('\n{question}'.format(question = row.question))
    user_answer = input('--> ').lower()
    if user_answer == row.answer.lower():
        print('\nYou are correct!. You won {price} points'\
                .format(price = str(row.price)))
    else:
        print('\nSorry, the correct answer was: {answer}'\
                .format(answer = row.answer))

    # Keep playing?
    while True:
        keep_playing = input('Do you want to keep playing? [Y/N] ').lower()
        if keep_playing == 'y':
            break
        elif keep_playing == 'n':
            game_on = False
            break
        else:
            print("Sorry, wrong option. Please choose 'Y' or 'N'")   
