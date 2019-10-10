#!/usr/bin/env python
# coding: utf-8

# In[68]:

#####################################################################################################################################
# the following code was used to generate the master sheet for the first 180 participants

# code for randomizing AI statements

import random
import pandas
import itertools

random.seed(1234)

#### create a dataframe to start with

# create conditions: 1. create 6 conditions and repeate for 30 times (N subject=30); 
# 2. randomly shuffle the conditions across participants (random assignment to conditions)
# 3. for each condition/subject repeat 16 times (16 trials/subject)
condition= list(range(1,7))*30
random.shuffle(condition)
condition= list(itertools.chain(*[[i]*16 for i in condition]))


# create subject number: 1. create 180 subject numbers
# 2. repeate each subject number 16 times (16 trials/subject); 
subject=list(range(1,181))
subject=list(itertools.chain(*[[i]*16 for i in subject]))

# create trial number: 1. create trial number 1-16; 2. repeat for each subject
trial_num= list(range(1,17))*180


# put the above variables into a dictionary and turn the dict into a dataframe
data= {'Subject': subject,
       'Condition': condition,
       'Trial Number': trial_num
      }
data= pandas.DataFrame.from_dict(data)


# A note of the conditions: Odd conditions(1, 3,5): human partner; Even conditions(2, 4, 6): AI partner
# condition 1,2: Low Similarity; Condition 3, 4: Medium Similarity; Condition 5, 6: High Similarity


# create the trial question text variable:

questions={
    1: 'favorite season',
    2: 'social media',
    3: 'movie genres',
    4: 'cuisines',
    5: 'oversea countries',
    6: 'music genres',
    7: 'historical figures',
    8: 'deserted on an island',
    9: 'a million dollars',
    10: 'fear most',
    11: 'qualities in friend',
    12: 'gossip',
    13: 'stressful things',
    14: 'how to unwind',
    15: 'personal qualities',
    16: 'change about yourself'
}

data['Trial Question']= [questions[i] for i in data['Trial Number']]

# add the partern variable to dataframe

data['Partner']= ['Human' if i in [1, 3, 5] else 'AI' for i in data['Condition']]

# add the similarity manipulation variable to dataframe (L=low; M=medium; H=high)

data['Similarity']=['L' if i in [1, 2] else 'M' if i in [3, 4] else 'H' for i in data['Condition']]

###### create the trial type variable to indicate which trials within each subject are the Same versus Different trial

#create a random generator for a list of same trials within each subject depending on the condition
def gen_same_trials(Condition):
    
    ''' generate a list of same trial numbers randomly selected from the 16 trials within a subject, 
    given the condition (Condition) that the subject is in'
    '''
    Num_same_trials= 4 if Condition in [1, 2] else 8 if Condition in [3, 4] else 12
    
    same_trials= random.sample(range(1,17), Num_same_trials)
        
    return same_trials


Trial_Type=[]

def subject_trial_type(SubjectID):
    
    sliced= data[data['Subject']== SubjectID]
    
    Cond= list(sliced['Condition'])[0]
    
    same_trials= gen_same_trials(Cond)
    
    trials=[]
    
    for i in sliced['Trial Number']:
        if i in same_trials:
            trial='SAME'
        else:
            trial='DIFF'
        trials.append(trial)
    
    Trial_Type.append(trials)
    

for i in data['Subject'].unique():
    
    subject_trial_type(i)
    

Trial_Type= list(itertools.chain(*Trial_Type))

data['Trial Type']= Trial_Type # Trial_Type==1: Same answer; Trial_Type==0: Different answer


######### create a randomized answer index for each trial where Trial_Type==0

def draw_answer_index(TrialType):
    if TrialType== 'DIFF':
        return random.sample([1,2,3], 1)
    else:
        return 'Same'

data['Answer Index']= data['Trial Type'].apply(draw_answer_index)


######### export the dataframe to a csv file

path='C:...\\randomized trials.csv' # define a path

data.to_csv(path)
    


# In[ ]:


#####################################################################################################################################
# too many suspicious participants in the first 180 subjects; we decided to recruit more
# the following code was used to generate the master sheet for participants 181 to 200 (but we only collected up to ss195)


# code for randomizing AI statements

import random
import pandas
import itertools

random.seed(1234)

#### create a dataframe to start with

# create conditions: 1. create the corresponding number of specific conditions; 
# 2. randomly shuffle the conditions across participants (random assignment to conditions)
# 3. for each condition/subject repeat 16 times (16 trials/subject)
condition= list(itertools.chain([1]*8, [3]*6, [5]*6))
random.shuffle(condition)
condition= list(itertools.chain(*[[i]*16 for i in condition]))


# create subject number: 1. create 20 subject numbers (SS181-200)
# 2. repeate each subject number 16 times (16 trials/subject); 
subject=list(range(181,201))
subject=list(itertools.chain(*[[i]*16 for i in subject]))

# create trial number: 1. create trial number 1-16; 2. repeat for each subject
trial_num= list(range(1,17))*20


# put the above variables into a dictionary and turn the dict into a dataframe
data= {'Subject': subject,
       'Condition': condition,
       'Trial Number': trial_num
      }
data= pandas.DataFrame.from_dict(data)


# A note of the conditions: Odd conditions(1, 3,5): human partner; Even conditions(2, 4, 6): AI partner
# condition 1,2: Low Similarity; Condition 3, 4: Medium Similarity; Condition 5, 6: High Similarity


# create the trial question text variable:

questions={
    1: 'favorite season',
    2: 'social media',
    3: 'movie genres',
    4: 'cuisines',
    5: 'oversea countries',
    6: 'music genres',
    7: 'historical figures',
    8: 'deserted on an island',
    9: 'a million dollars',
    10: 'fear most',
    11: 'qualities in friend',
    12: 'gossip',
    13: 'stressful things',
    14: 'political positions',
    15: 'personal qualities',
    16: 'change about yourself'
}

data['Trial Question']= [questions[i] for i in data['Trial Number']]

# add the partern variable to dataframe

data['Partner']= ['Human' if i in [1, 3, 5] else 'AI' for i in data['Condition']]

# add the similarity manipulation variable to dataframe (L=low; M=medium; H=high)

data['Similarity']=['L' if i in [1, 2] else 'M' if i in [3, 4] else 'H' for i in data['Condition']]

###### create the trial type variable to indicate which trials within each subject are the Same versus Different trial

#create a random generator for a list of same trials within each subject depending on the condition
def gen_same_trials(Condition):
    
    ''' generate a list of same trial numbers randomly selected from the 16 trials within a subject, 
    given the condition (Condition) that the subject is in'
    '''
    Num_same_trials= 4 if Condition in [1, 2] else 8 if Condition in [3, 4] else 12
    
    same_trials= random.sample(range(1,17), Num_same_trials)
        
    return same_trials

## generate trial type for each trial, given a specific SS and their condition

Trial_Type=[]

def subject_trial_type(SubjectID):
    
    sliced= data[data['Subject']== SubjectID]
    
    Cond= list(sliced['Condition'])[0]
    
    same_trials= gen_same_trials(Cond)
    
    trials=[]
    
    for i in sliced['Trial Number']:
        if i in same_trials:
            trial='SAME'
        else:
            trial='DIFF'
        trials.append(trial)
    
    Trial_Type.append(trials)
    


for i in data['Subject'].unique():
    
    subject_trial_type(i)
    

Trial_Type= list(itertools.chain(*Trial_Type))

data['Trial Type']= Trial_Type # Trial_Type==1: Same answer; Trial_Type==0: Different answer


######### create a randomized answer index for each trial where Trial_Type==0

def draw_answer_index(TrialType):
    if TrialType== 'DIFF':
        return random.sample([1,2,3], 1)
    else:
        return 'Same'

data['Answer Index']= data['Trial Type'].apply(draw_answer_index)


######### export the dataframe to a csv file

path='C:..\\randomized trials_SS181toSS200.csv' # define a path

data.to_csv(path)
    





