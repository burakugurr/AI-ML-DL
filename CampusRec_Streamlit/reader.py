import pandas as pd


def create_df(gender,ssc_p,ssc_b,hsc_p,hsc_b,hsc_s,degree,degree_t,workex,etest,special,mba,salary):

    if degree_t=='Others':
        degree_t_CommMgmt =0
        degree_t_SciTech=0
    elif degree_t =='Sci&Tech':
        degree_t_CommMgmt =0
        degree_t_SciTech=1
    else:
        degree_t_CommMgmt =1
        degree_t_SciTech=0

    if gender=='Male':
        gender=0
    else:
        gender=1
    
    if special=='Mkt&HR':
        special=0
    else:
        special=1

    if workex=='No':
        workex=0
    else:
        workex=1
    if hsc_b=='Others':
        hsc_b =0
    else:
        hsc_b =1
    if ssc_b=='Others':
        ssc_b =0
    else:
        ssc_b =1
    if hsc_s=='Arts':
        hsc_s_Commerce=0
        hsc_s_Science=0
    elif hsc_s=='Science':
        hsc_s_Commerce=0
        hsc_s_Science=1
    else:
        hsc_s_Commerce=1
        hsc_s_Science=0


    data={'gender':gender,
    'ssc_p':ssc_p,
    'hsc_p':hsc_p,
    'degree_p':degree,
    'etest_p':etest,
    'mba_p':mba,
    'salary':salary,
    'ssc_b_Central':ssc_b,
    'gender_F':gender,
    'hsc_b_Central':hsc_b,
    'hsc_s_Commerce':hsc_s_Commerce,
    'hsc_s_Science':hsc_s_Science,
    'degree_t_Comm&Mgmt':degree_t_CommMgmt,
    'degree_t_Sci&Tech':degree_t_SciTech,
    'workex_Yes':workex,
    'specialisation_Mkt&Fin':special,


    }
    df = pd.DataFrame(data,columns=['ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p', 'salary',
       'ssc_b_Central', 'gender_F', 'hsc_b_Central', 'hsc_s_Commerce',
       'hsc_s_Science', 'degree_t_Comm&Mgmt', 'degree_t_Sci&Tech',
       'workex_Yes', 'specialisation_Mkt&Fin'],index=[0])
    print(df)
    return df