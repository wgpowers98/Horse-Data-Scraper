import pandas as pd

dict = {
        'ID':[],
        'Sire':[],	
        'Grandsire':[],	
        'Dam':[],	
        'Damsire':[],	
        'Sex':[],	
        'Foaled':[],	
        'Died':[],	
        'Country':[],	
        'Colour':[],	
        'Breeder':[],
        'Owner':[],	
        'Trainer':[],	
        'Record':[],	
        'Earnings':[], 
        'Label':[],
        'Racing colours':[],
        'Jockey':[],	
        'Color':[]}

dataFrame = pd.DataFrame(dict)
dtAppend = {'ID':0,'Sire':'Brown','Owner':'WGP'}

dataFrame = dataFrame._append(dtAppend, ignore_index = True)

dataFrame.loc[dataFrame['ID'] == 0, 'Age'] = 45



print(dataFrame)