import sys
import numpy as np

def get_score(data_array):

    def encoding_array(i):
        switcher={
                    1:np.array([1,0,0,0,0,0,0]),
                    2:np.array([0,1,0,0,0,0,0]),
                    3:np.array([0,0,1,0,0,0,0]),
                    4:np.array([0,0,0,1,0,0,0]),
                    5:np.array([0,0,0,0,1,0,0]),
                    6:np.array([0,0,0,0,0,1,0]),
                    7:np.array([0,0,0,0,0,0,1])
                 }
        return switcher.get(i,np.array([0,0,0,0,0,0,0]))

    #Fever
    fever = encoding_array(data_array['fever'])
    #Cough
    cough = encoding_array(data_array['coughcheck'])
    #Shortness of breadth
    sb = encoding_array(data_array['shortnesscheck'])
    #Improvement
    sym_impr = encoding_array(data_array['symp'])

    inputs = np.concatenate(
    (
    [
    data_array['gender'],
    data_array['age'],
    data_array['height'],
    data_array['weight'],
    data_array['hr'],
    data_array['bp'],
    data_array['kidney'],
    data_array['heart'],
    data_array['lung'],
    data_array['stroke'],
    data_array['diabetes'],
    data_array['hypertension'],
    data_array['immunocompromised'],
    data_array['transplant']
    ],
    fever,
    cough,
    sb,
    [
    data_array['taste'],
    data_array['fatigue'],
    data_array['sore_throat'],
    data_array['headache'],
    data_array['muscle'],
    data_array['chill'],
    data_array['nausea'],
    data_array['nasal'],
    data_array['diarrhea']
    ],
    sym_impr,
    [data_array['international']
    ]
    )
    )


    weights = np.array([
    0, #gender
    0, #age
    0, #height
    0, #weight
    0, #heart rate
    0, #bp
    0, #kidney
    0, #Heart
    0, #Lungs
    0, #Stroke
    0, #Diabetes
    0, #Hypertension
    0, #HIV/Immunocompromised
    0, #Transplant
    7, #fever 98.6-100.4
    8, #fever 100.4-104
    6, #fever comes and goes
    5, #fever not measured
    0, #no fever
    0, #fever-padding
    0, #fever-padding
    8, #cough
    0, #cough padding
    0, #cough padding
    0, #cough padding
    0, #cough padding
    0, #cough padding
    0, #cough padding
    8, #shortness w/ chest pain
    0, #shortness w/ sweating
    0, #no shortness
    0, #shortness padding
    0, #shortness padding
    0, #shortness padding
    0, #shortness padding
    23, #Loss of taste/smell
    6,  #Fatigue
    4,    #Sore throat
    4,    #headache
    4,    #muscle pain
    4,    #chills
    2,    #nausea/vomiting
    2,    #nasal congestion
    2,    #diarrhea
    -2, #improved
    2,  #no change
    4,  #worsened
    6, #worsened considerably
    0, #improvement padding
    0,#improvement padding
    0, #improvement padding
    23]) #international travel

    health = np.dot(weights,inputs)
    return health
'''
    layer_1_data = np.append(layer_1_data, data_array['gender,data_array['age,axis=1) #GENDER
    layer_1_data = np.append(layer_1_data, ,axis=1) # AGE
    layer_1_data = np.append(layer_1_data, data_array['height,axis=1) # HEIGHT
    layer_1_data = np.append(layer_1_data, data_array['weight,axis=1) # WEIGHT
    layer_1_data = np.append(layer_1_data, data_array['hr,axis=1)  #Heart Rate
    layer_1_data = np.append(layer_1_data, data_array['bp,axis=1)  #BP
    layer_1_data = np.append(layer_1_data, data_array['kidney,axis=1) #Kidney
    layer_1_data = np.append(layer_1_data, data_array['heart,axis=1) #Heart
    layer_1_data = np.append(layer_1_data, data_array['lung,axis=1) #Lung
    layer_1_data = np.append(layer_1_data, data_array['stroke,axis=1) #Stroke
    layer_1_data = np.append(layer_1_data, data_array['diabetes,axis=1) #Diabetes
    layer_1_data = np.append(layer_1_data, data_array['hypertension,axis=1) #Hypertension
    layer_1_data = np.append(layer_1_data, data_array['immunocompromised,axis=1) #HIV/Immunocompromised
    layer_1_data = np.append(layer_1_data, data_array['transplant,axis=1) #Transplant
    layer_1_data = np.append(layer_1_data, fever) #Fever
    layer_1_data = np.append(layer_1_data, cough) #Cough
    layer_1_data = np.append(layer_1_data, sb) #Shortness of breadth
    layer_1_data = np.append(layer_1_data, data_array['taste) #Loss of taste/smell
    layer_1_data = np.append(layer_1_data, data_array['fatigue) #Fatigue
    layer_1_data = np.append(layer_1_data,other_symp) #Other Symptoms
    layer_1_data = np.append(layer_1_data,sym_impr) #Improvemenet ?
    layer_1_data = np.append(layer_1_data,data_array['international) #International Travel

    #Assemble Weights

    # GENDER, AGE, HEIGHT, WEIGHT weights
    weight_gahw = np.array([0,0,0,0])  #4
    #Heart Rate/BP weights
    weight_hb = np.array([0,0])  #2
    #Prev Conditions
    #kidney
    #Heart
    #Lungs
    #Stroke
    #Diabetes
    #Hypertension
    weight_pc = np.array([0,0,0,0,0,0])  #6
    #Immunocompromised
    #HIV
    #Transplant
    weight_im = np.array([0,0])  #2
    #Symptoms
    #Fever
    weight_f = np.array([7,8,6,5,0,0,0])  #7
    #Cough
    weight_c = np.array([8,6,0,0,0,0,0])  #7
    #Shortness of breadth
    weight_sb = np.array([8,0,0,0,0,0,0])  #7
    #Loss of taste/smell
    weight_ts = np.array([23])  #1
    #Fatigue
    weight_ftg = np.array([6])   #1
    #Other Symptoms
    #Sore throat
    #headache
    #muscle pain
    #chills
    #nausea/vomiting
    #nasal congestion
    #diarrhea
    weight_os = np.array([4,4,4,4,2,2,2])   #7
    #Improvement
    weight_impr = np.array([-2,2,4,6,0,0,0])
    #International Travel
    weight_international = np.array([23])
    weight = np.empty((num,0))
    weight = np.append(weight,weight_gahw)
    weight = np.append(weight,weight_hb)
    weight = np.append(weight,weight_pc)
    weight = np.append(weight,weight_im)
    weight = np.append(weight,weight_f)
    weight = np.append(weight,weight_c)
    weight = np.append(weight,weight_sb)
    weight = np.append(weight,weight_ts)
    weight = np.append(weight,weight_ftg)
    weight = np.append(weight,weight_os)
    weight = np.append(weight,weight_impr)
    weight = np.append(weight,weight_international)

    health = np.dot(weight,layer_1_data)
'''
