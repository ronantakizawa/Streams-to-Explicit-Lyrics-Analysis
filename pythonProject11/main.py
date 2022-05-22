import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as p
from scipy import stats

rng = np.random.default_rng()

# Word bank of different genres of words.
# Words were chosen by hiphop media companies (XXL, Billboard).
# 20 words per genre to have no disadvantages for certain genres.
material_words = ['chain', 'ice', 'money', 'cash', 'ring', "ap", "rolly", "thousand",
                  "lambo", "rari", "hundred", "milli""flex", "car", "mansion", "broke", "bands", "100", "blue", "green"]
sports_words = ['hoop', 'nba', 'ball', 'ring', "3", "23", "nike", "addidas", "bat", "court",
                "swim", "golf", "swing", "shoot", "dribble", "drive", "jordan", "lebron", "rain"
                ]
sex_words = ['thot', 'tits', 'love', 'fake', "whore", "dick", "cock", "pussy", "stripper",
             "heart", "baby", "wife", "bang", "punani", "suck", "tities", "nut", "heartbreak",
             "girl", "boy"]
drug_words = ['molly', 'perc', 'lean', 'xan', 'weed', 'kush', 'coke', 'rocks',
              'codeine', "henny", "drank", "sip", "smoke" "stash", "crush", "syrup", "fenny",
              " od ", " cup ", "mix"]
adlib_words = ['yeah', 'skrt', 'uh', 'wha', 'woo', "ay", "ayy", "slat", "what", "aye", "lit",
               "ah", "yo", "yuh", "mane", "man", "bro", "cap", "bow", " ha "]
crime_words = ['glock', 'trap', "44", "gun", "knife", "slit", "pop", "kill", "murder",
               "chopper", "snitch", "real", "beef", "streets", "pop", "hood", "projects", "gang",
               "mob", "dead"]
swear_words = ['fuck', 'shit', 'bitch', 'nigga', 'cunt', "nigger", "stupid", "idiot",
               "crap", 'ass', "motherfucker", "bitch", "chink", "beaner", "bastard", "twat", "fat", "skinny", "damn",
               "ugly"]





# Function that reads text files.
# Using the counter variable and the list above, it tracks the number of matching words
# in the lyrics.

def calculate(file_path, sex_words, drug_words, adlib_words, crime_words, swear_words,
              material_words, sports_words):
    # Counter variables
    drug_counter = 0
    sex_counter = 0
    adlib_counter = 0
    crime_counter = 0
    swear_counter = 0
    material_counter = 0
    sports_counter = 0
    with open(file_path, 'r') as f:
        # The first line is artist name, second is the stream number today.
        artist = f.readline().strip()
        views = float(f.readline().strip())
        for line in f:
            # Make line lowercase to avoid case sensitivity
            line = line.lower()
            # Add to counter if words are in line
            for word in sex_words:
                if word in line:
                    sex_counter += 1
            for word in drug_words:
                if word in line:
                    drug_counter += 1
            for word in adlib_words:
                if word in line:
                    adlib_counter += 1
            for word in crime_words:
                if word in line:
                    crime_counter += 1
            for word in swear_words:
                if word in line:
                    swear_counter += 1
            for word in material_words:
                if word in line:
                    material_counter += 1
            for word in sports_words:
                if word in line:
                    sports_counter += 1
    # Returns all created variables
    return artist, views, sex_counter, drug_counter, adlib_counter, crime_counter, \
           swear_counter, material_counter, sports_counter


# Reads in data.txt which has labels already created
table = pd.read_csv(r"data")
pd.set_option("display.max_columns", None)

# Creates data frame by reading in data from the txt files through calculate function
for i in range(1, 21):
    # Since all text files are numbered, the iteration can read through all txt files
    k = str(i)
    # The file path will be k + txt. It gets the desired variable by choosing the
    # index of the returned variables.
    # Numbers are converted to floats to work in scipy and matplotlib
    name = calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                     swear_words, material_words, sports_words)[0]
    streams = calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                        swear_words, material_words, sports_words)[1]
    sex_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                swear_words, material_words, sports_words)[2])
    drug_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                 swear_words, material_words, sports_words)[3])
    adlib_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                  swear_words, material_words, sports_words)[4])
    crime_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                  swear_words, material_words, sports_words)[5])
    swear_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                  swear_words, material_words, sports_words)[6])
    material_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                     swear_words, material_words, sports_words)[7])
    sports_count = float(calculate(k + '.txt', sex_words, drug_words, adlib_words, crime_words,
                                   swear_words, material_words, sports_words)[8])
    # Create a new row in table using the newly created variables above
    table.loc[len(table.index)] = [name, streams, sex_count, drug_count, adlib_count, crime_count,
                                   swear_count, material_count, sports_count]




influence = []
association_strength = []
names = []

# Creates graphs for all columns in data table
for g in range(2, len(table.columns)):
    string = table.columns[g]
    names.append(string)
    x = table.loc[:, string]
    # Streams will always be the dependent variable
    y = table.loc[:, "streams"]
    # Create a scatterplot
    plt.plot(x, y, 'o', label='original data')
    plt.legend()
    # Add labels to the graph
    plt.title("" + string + " and streams")
    plt.xlabel(string)
    plt.ylabel("Streams")
    # Create a line of regression according to the scatterplot
    res = p.stats.linregress(x, y)
    plt.plot(x, res.intercept + res.slope * x, 'r', label='fitted line')
    plt.show()

    # Calculate correlation coefficient using built-in Scipy functions
    r = p.stats.pearsonr(x, y)[0]
    print("Correlation Coefficient for " + string + " and Streams:")
    print(r)
    print()
    print("Correlation of Determination:")
    print(r * r)
    print('--------------------------------------------')
    influence.append(r * r)
    association_strength.append(-r)

# Create piechart for Correlation of Determination
fig = plt.figure(figsize=(10, 7))
plt.pie(influence, labels=names)
plt.title("Most Influential Variables for Streams")
plt.show()

# Create piechart for Correlation Coefficient
fig2 = plt.figure(figsize=(10, 7))
plt.pie(association_strength, labels=names)
plt.title("Variables with Strongest Correlation")
plt.show()


