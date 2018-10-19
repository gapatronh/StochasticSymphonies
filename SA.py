import numpy as np
from music21 import *
########################Functions
def durations_array(measure):
    """
    Input: Music21 Measure Object
    Output: Array of notes' duration, in order, of given Measure
    """
    durations=[]
    for nota in measure:
        durations.append(nota.quarterLength)
    if sum(durations)==4:
        return(durations)
    
def pitches_array(measure):
    """
    Input: Music21 Measure Object
    Output: Array of notes' duration, in order, of given Measure
    """
    if durations_array(measure)!=None:
        pitches=[]
        for nota in measure:
            if nota.name=="rest":
                pitches.append('R')
            else:
                pitches.append(str(nota.pitch))
        return(pitches)

def matrix_cleaner(matrix):
    """"
    Input: Transitione matrix whose entries don't all sum to 1
    Output: Corrected matrix (Maybe)
    """
    new_Matrix=np.copy(matrix)
    cleans=0
    while sum([sum(row)==1 for row in new_Matrix])!=len(new_Matrix):
        for row in new_Matrix:
            if sum(row)==1.0:
                continue
            else:
                diff=1.0-sum(row)
                row[np.random.choice(np.where((row!=0)==True)[0])]+=diff
        cleans+=1
    print("Cleans:",cleans)
    return(new_Matrix)
############Define which instruments we're going to study##############
instruments=["Soprano","Alto","Tenor","Bass"]
#####Here we'll save all the Durations and pitches arrays for every instrument#####
durationArrays={'Soprano':[],'Alto':[],'Tenor':[],'Bass':[]}
pitchArrays={'Soprano':[],'Alto':[],'Tenor':[],'Bass':[]}
#######Extraction of the measures##################3
all_bach_paths = corpus.getComposer('bach')
skipped=0 
print("Total number of Bach pieces to process from music21: %i" % len(all_bach_paths))
for it, p_bach in enumerate(all_bach_paths):
    if "riemenschneider" in str(p_bach):
        skipped += 1
        continue
    p = corpus.parse(p_bach)
#Make sure we have at least four instruments, the key is C major and have constant measure duration
    test_measure=p.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure)[1].barDuration.quarterLength
    if (len(p.parts) <4) or  (test_measure!=4) or ('C major' not in p.analyze("key").name):
        print(p_bach)
        print("Four Instruments?:",len(p.parts)<4, "4/4?", test_measure!=4, 'C Major?', 'C major' not in p.analyze("key").name)
        skipped += 1
        continue
    for part in p.parts:
        if part.partName in instruments:
            measures=part.getElementsByClass(stream.Measure)
            durationArrays[part.partName]+=[durations_array(measures[1+i].notesAndRests) for i in range(len(measures)-2)]
            pitchArrays[part.partName]+=[pitches_array(measures[1+i].notesAndRests) for i in range(len(measures)-2)]

################### Dictionary Cleansing ######################################
for key in durationArrays.keys():
    tempD=durationArrays[key]
    tempP=pitchArrays[key]
    durationArrays[key]=[tuple(tempD[i]) for i in range(len(tempD)-1) if tempD[i]!=None]
    pitchArrays[key]=[tuple(tempP[i]) for i in range(len(tempP)-1) if tempP[i]!=None]
###############################################################################


############Soprano will be base instrument
soprano_Durations=np.array(durationArrays["Soprano"])
soprano_Unique=np.unique(soprano_Durations)
soprano_Count={soprano_Unique[i]:0 for i in range(len(soprano_Unique))}
soprano_Transitions_Count={soprano_Unique[i]:[0 for j in range(len(soprano_Unique))] for i in range(len(soprano_Unique))}
soprano_Pitches=np.array(pitchArrays["Soprano"])
soprano_Pitch_Unique=np.unique(soprano_Pitches)
soprano_Pitch_Count={soprano_Pitch_Unique[i]:0 for i in range(len(soprano_Pitch_Unique))}
soprano_Pitch_Transitions_Count={soprano_Unique[i]:[0 for j in range(len(soprano_Pitch_Unique))] for i in range(len(soprano_Unique))}

for it,measure in enumerate(soprano_Durations):   
    if it<len(soprano_Durations)-1:
        soprano_Transitions_Count[measure][list(soprano_Unique).index(soprano_Durations[it+1])]+=1
        soprano_Count[measure]+=1
    soprano_Pitch_Transitions_Count[measure][list(soprano_Pitch_Unique).index(soprano_Pitches[it])]+=1        
    soprano_Pitch_Count[soprano_Pitches[it]]+=1
soprano_matrix=np.array([np.array(soprano_Transitions_Count[measure])/soprano_Count[measure] for measure in soprano_Unique])
soprano_pitch_matrix=np.array([np.array(soprano_Pitch_Transitions_Count[measure])/soprano_Count[measure] for measure in soprano_Unique])
spm=matrix_cleaner(soprano_pitch_matrix)
#################################################DTU's
alto_Durations=np.array(durationArrays["Alto"])
alto_Unique=np.unique(alto_Durations)
soprano_Alto_Transitions={soprano_Unique[i]:[0 for j in range(len(alto_Unique))] for i in range(len(soprano_Unique))}
alto_Pitches=np.array(pitchArrays["Alto"])
alto_Pitch_Unique=np.unique(alto_Pitches)
alto_Pitches_Transitions={alto_Unique[i]:[0 for j in range(len(alto_Pitch_Unique))] for i in range(len(alto_Unique))}
alto_Durations_Count={alto_Unique[i]:0 for i in range(len(alto_Unique))}

tenor_Durations=np.array(durationArrays["Tenor"])
tenor_Unique=np.unique(tenor_Durations)
soprano_Tenor_Transitions={soprano_Unique[i]:[0 for j in range(len(tenor_Unique))] for i in range(len(soprano_Unique))}
tenor_Pitches=np.array(pitchArrays["Tenor"])
tenor_Pitch_Unique=np.unique(tenor_Pitches)
tenor_Pitches_Transitions={tenor_Unique[i]:[0 for j in range(len(tenor_Pitch_Unique))] for i in range(len(tenor_Unique))}
tenor_Durations_Count={tenor_Unique[i]:0 for i in range(len(tenor_Unique))}

bass_Durations=np.array(durationArrays["Bass"])
bass_Unique=np.unique(bass_Durations)
soprano_Bass_Transitions={soprano_Unique[i]:[0 for j in range(len(bass_Unique))] for i in range(len(soprano_Unique))}
bass_Pitches=np.array(pitchArrays["Bass"])
bass_Pitch_Unique=np.unique(bass_Pitches)
bass_Pitches_Transitions={bass_Unique[i]:[0 for j in range(len(bass_Pitch_Unique))] for i in range(len(bass_Unique))}
bass_Durations_Count={bass_Unique[i]:0 for i in range(len(bass_Unique))}

for it,measure in enumerate(soprano_Durations):   
    if it<len(soprano_Durations)-1:
        soprano_Alto_Transitions[measure][list(alto_Unique).index(alto_Durations[it+1])]+=1
        soprano_Tenor_Transitions[measure][list(tenor_Unique).index(tenor_Durations[it+1])]+=1 
        soprano_Bass_Transitions[measure][list(bass_Unique).index(bass_Durations[it+1])]+=1
for it,measure in enumerate(alto_Durations):
    alto_Pitches_Transitions[measure][list(alto_Pitch_Unique).index(alto_Pitches[it])]+=1
    alto_Durations_Count[measure]+=1
for it,measure in enumerate(tenor_Durations):    
    tenor_Pitches_Transitions[measure][list(tenor_Pitch_Unique).index(tenor_Pitches[it])]+=1
    tenor_Durations_Count[measure]+=1
for it,measure in enumerate(bass_Durations):
    bass_Pitches_Transitions[measure][list(bass_Pitch_Unique).index(bass_Pitches[it])]+=1
    bass_Durations_Count[measure]+=1
        
sam=np.array([np.array(soprano_Alto_Transitions[measure])/soprano_Count[measure] for measure in soprano_Unique]) 
stm=np.array([np.array(soprano_Tenor_Transitions[measure])/soprano_Count[measure] for measure in soprano_Unique])
sbm=np.array([np.array(soprano_Bass_Transitions[measure])/soprano_Count[measure] for measure in soprano_Unique])
sam=matrix_cleaner(sam)
stm=matrix_cleaner(stm)
sbm=matrix_cleaner(sbm)

psam=np.array([np.array(alto_Pitches_Transitions[measure])/alto_Durations_Count[measure] for measure in alto_Unique]) 
pstm=np.array([np.array(tenor_Pitches_Transitions[measure])/tenor_Durations_Count[measure] for measure in tenor_Unique])
psbm=np.array([np.array(bass_Pitches_Transitions[measure])/bass_Durations_Count[measure] for measure in bass_Unique])
psam=matrix_cleaner(psam)
pstm=matrix_cleaner(pstm)
psbm=matrix_cleaner(psbm)

#####################################

furDiana=stream.Score()
soprano_part=stream.Part()
alto_part=stream.Part()
tenor_part=stream.Part()
bass_part=stream.Part()
soprano=[np.random.choice(soprano_Unique)]
alto=[]
tenor=[]
bass=[]
psoprano=[]
palto=[]
ptenor=[]
pbass=[]
for i in range(5):
    last_measure=soprano[-1]
    soprano.append(soprano_Unique[np.random.choice(range(len(soprano_Unique)),p=soprano_matrix[list(soprano_Unique).index(last_measure)])])
    alto.append(alto_Unique[np.random.choice(range(len(alto_Unique)),p=sam[list(soprano_Unique).index(last_measure)])])
    tenor.append(tenor_Unique[np.random.choice(range(len(tenor_Unique)),p=stm[list(soprano_Unique).index(last_measure)])])
    bass.append(bass_Unique[np.random.choice(range(len(bass_Unique)),p=sbm[list(soprano_Unique).index(last_measure)])])
    
    psoprano.append(soprano_Pitch_Unique[np.random.choice(range(len(soprano_Pitch_Unique)),p=spm[list(soprano_Unique).index(last_measure)])])
    palto.append(alto_Pitch_Unique[np.random.choice(range(len(alto_Pitch_Unique)), p=psam[list(alto_Unique).index(alto[-1])])])
    ptenor.append(tenor_Pitch_Unique[np.random.choice(range(len(tenor_Pitch_Unique)),p=pstm[list(tenor_Unique).index(tenor[-1])])])
    pbass.append(bass_Pitch_Unique[np.random.choice(range(len(bass_Pitch_Unique)),p=psbm[list(bass_Unique).index(bass[-1])])])

def flatten(list_of_arrays):
    return([item for array in list_of_arrays for item in array])

soprano=flatten(soprano);psoprano=flatten(psoprano)
alto=flatten(alto);palto=flatten(palto)
tenor=flatten(tenor);ptenor=flatten(ptenor)
bass=flatten(bass); pbass=flatten(pbass)
for i in range(len(alto)):
    if palto[i]=="R":
        r=note.Rest()
    else:
        r=note.Note(palto[i])
    r.quarterLength=alto[i]
    alto_part.append(r)
for i in range(len(tenor)):
    if ptenor[i]=="R":
        r=note.Rest()
    else:
        r=note.Note(ptenor[i])
    r.quarterLength=tenor[i]
    tenor_part.append(r)
for i in range(len(bass)):
    if pbass[i]=="R":
        r=note.Rest()
    else:
        r=note.Note(pbass[i])
    r.quarterLength=bass[i]
    bass_part.append(r)
furDiana.append(alto_part)
furDiana.append(tenor_part)
furDiana.append(bass_part)
furDiana.show("musicxml")