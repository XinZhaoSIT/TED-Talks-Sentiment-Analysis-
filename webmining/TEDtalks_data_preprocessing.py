import pandas as pd

def covert_durations(dur):
    
    def convert(seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        dt ="%d:%02d:%02d" % (hour, minutes, seconds)
    
        return dt

    dur1 = []
    for i in dur:
        dur1.append(convert(i))
    
    return dur1

def get_chunk_csv(path, chunk_size=1000):
    
    data = pd.read_csv(path, chunksize=chunk_size, index_col=0, engine='python')   
    chunk_data = pd.DataFrame(data.get_chunk(chunk_size))   
    df = chunk_data.to_csv('ted_talks_data_1000.csv')

    return df  

if __name__ == "__main__":
    
    file = 'ted_talks_data.csv'
    
    data = pd.read_csv(file, engine='python')
        
    data['lengths'] = covert_durations(data['durations'])

    data=data.replace(to_replace='?�?',value='')
    data=data.replace(to_replace='�',value='')
    data['speakers']=data.speakers.str.replace('+','and',regex=True)
    data['speakers']=data.speakers.str.replace('(TED)','',regex=True)
    data['speakers']=data.speakers.str.replace('[^a-zA-Z0-9 ]', '')
    data['descriptions']=data.descriptions.str.replace('[^a-zA-Z0-9 ]', '')
    data['topics']=data.topics.str.replace('[^a-zA-Z0-9 ]', '')
    data['tags']=data.tags.str.replace('TED-Ed', '',regex=True)
    data['tags']=data.tags.str.replace('TED Fellows', '',regex=True)
    data['tags']=data.tags.str.replace('TEDMED', '',regex=True)
    data['tags']=data.tags.str.replace('TEDx', '',regex=True)
    print(data.isnull().any())
    data.to_csv('ted_talks_data_clean.csv',index=False)
    get_chunk_csv('ted_talks_data_clean.csv')

  
    

    
    

    

