#Assignment 2
#For this assignment you'll be looking at 2017 data on immunizations from the CDC. Your datafile for this assignment is in assets/NISPUF17.csv. A data users guide for this, which you'll need to map the variables in the data to the questions being asked, is available at assets/NIS-PUF17-DUG.pdf. Note: you may have to go to your Jupyter tree (click on the Coursera image) and navigate to the assignment 2 assets folder to see this PDF file).

#Question 1
#Write a function called proportion_of_education which returns the proportion of children in the dataset who had a mother with the education levels equal to less than high school (<12), high school (12), more than high school but not a college graduate (>12) and college degree.

#This function should return a dictionary in the form of (use the correct numbers, do not round numbers):

#    {"less than high school":0.2,
#    "high school":0.4,
#    "more than high school but not college":0.2,
#    "college":0.2}

import pandas as pd

df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
df.head()

#We are going to use column EDUC1 for mother's education

def proportion_of_education():
    # your code goes here
    edu_dict = {"less than high school": 0,
                "high school": 0,
                "more than high school but not college": 0,
                "college": 0}
  
    #Vars to extract the length (count) for each mother's education group
    less_than = df[df['EDUC1'] == 1]
    equal_to = df[df['EDUC1'] == 2]
    more_than = df[df['EDUC1'] == 3]
    college = df[df['EDUC1'] == 4]
  
    #Assign the mother's education level rations in comparison to the length of the entire DF
    edu_dict["less than high school"] = len(less_than)/len(df)
    edu_dict["high school"] = len(equal_to)/len(df)
    edu_dict["more than high school but not college"] = len(more_than)/len(df)
    edu_dict["college"] = len(college)/len(df)
  
    return edu_dict

print("Question 1\n")
print(proportion_of_education())
print("\n")

#---------------------------------------------------

#Question 2
#Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza vaccine from a healthcare provider. Return a tuple of the average number of influenza vaccines for those children we know received breastmilk as a child and those who know did not.

#This function should return a tuple in the form (use the correct numbers:

#(2.5, 0.1)

import pandas as pd

df = pd.read_csv('assets/NISPUF17.csv', index_col=0)

def average_influenza_doses():
    # YOUR CODE HERE
    #Create two vars, one for all breastfed children, and the other with all non-breastfed children
    bmilk_vax = df[(df['CBF_01'] == 1)]
    no_bmilk_vax = df[(df['CBF_01'] == 2)]

    #Retrieves the mean of the vaccine doses per child group
    doses_bf_child = bmilk_vax['P_NUMFLU'].mean()
    doses_nbf_child = no_bmilk_vax['P_NUMFLU'].mean()
    
    return (doses_bf_child, doses_nbf_child)
  
  
print("Question 2\n")
print(average_influenza_doses())
print("\n")

#---------------------------------------------------

#Question 3
#It would be interesting to see if there is any evidence of a link between vaccine effectiveness and sex of the child. Calculate the ratio of the number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose) versus those who were vaccinated but did not contract chicken pox. Return results by sex.

#This function should return a dictionary in the form of (use the correct numbers):

#    {"male":0.2,
#    "female":0.4}
#Note: To aid in verification, the chickenpox_by_sex()['female'] value the autograder is looking for starts with the digits 0.0077.

import pandas as pd

df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
#Replace all '77' and '99' values by 0
df['HAD_CPOX'] = df['HAD_CPOX'].replace([77, 99], 0)

def chickenpox_by_sex():
    # YOUR CODE HERE
    #Create a new DF on the condition that the # of varicella doses is >= 1 AND that the child had contracted chickenpox
    new_df = df[(df['P_NUMVRC'] >= 1) & (df['HAD_CPOX'] >= 1)]

    #Group by male/female & had/didn't have chickenpox
    male_had_cpox = new_df[(new_df['SEX'] == 1) & (new_df['HAD_CPOX'] == 1)]
    male_no_cpox = new_df[(new_df['SEX'] == 1) & (new_df['HAD_CPOX'] == 2)]
    female_had_cpox = new_df[(new_df['SEX'] == 2) & (new_df['HAD_CPOX'] == 1)]
    female_no_cpox = new_df[(new_df['SEX'] == 2) & (new_df['HAD_CPOX'] == 2)]

    #Male and female ratios
    male_ratio = len(male_had_cpox['HAD_CPOX']) / len(male_no_cpox['HAD_CPOX'])
    female_ratio = len(female_had_cpox['HAD_CPOX']) / len(female_no_cpox['HAD_CPOX'])

    return {"male": male_ratio,
            "female": female_ratio}


print("Question 3\n")
print(chickenpox_by_sex())
print("\n")

#print(chickenpox_by_sex()['female'])

#------------------------------------------------

#Question 4
#A correlation is a statistical relationship between two variables. If we wanted to know if vaccines work, we might look at the correlation between the use of the vaccine and whether it results in prevention of the infection or disease [1]. In this question, you are to see if there is a correlation between having had the chicken pox and the number of chickenpox vaccine doses given (varicella).

#Some notes on interpreting the answer. The had_chickenpox_column is either 1 (for yes) or 2 (for no), and the num_chickenpox_vaccine_column is the number of doses a child has been given of the varicella vaccine. A positive correlation (e.g., corr > 0) means that an increase in had_chickenpox_column (which means more no’s) would also increase the values of num_chickenpox_vaccine_column (which means more doses of vaccine). If there is a negative correlation (e.g., corr < 0), it indicates that having had chickenpox is related to an increase in the number of vaccine doses.

#Also, pval is the probability that we observe a correlation between had_chickenpox_column and num_chickenpox_vaccine_column which is greater than or equal to a particular value occurred by chance. A small pval means that the observed correlation is highly unlikely to occur by chance. In this case, pval should be very small (will end in e-18 indicating a very small number).

#[1] This isn’t really the full picture, since we are not looking at when the dose was given. It’s possible that children had chickenpox and then their parents went to get them the vaccine. Does this dataset have the data we would need to investigate the timing of the dose?

def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd

    df = pd.read_csv('assets/NISPUF17.csv', index_col=0)
    #Replace all '77' and '99' values by 0
    df['HAD_CPOX'] = df['HAD_CPOX'].replace([77, 99], 0)

    #Create new df based on conditions that child had/didn't have chickenpox AND the child had >=0 doses of varicella vaccine
    new_df = df[(df['HAD_CPOX'] >=1) & (df['P_NUMVRC'] >=0)]

    #Create new df with index and two columns, based on new_df results
    cpdf = pd.DataFrame({"had_chickenpox_column": new_df['HAD_CPOX'],
                     "num_chickenpox_vaccine_column": new_df['P_NUMVRC']})

    #Correlation and pval
    corr, pval=stats.pearsonr(cpdf["had_chickenpox_column"],cpdf["num_chickenpox_vaccine_column"])
  
    return corr


print("Question 4\n")
print(corr_chickenpox())
