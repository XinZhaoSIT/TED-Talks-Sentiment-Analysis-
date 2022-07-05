import requests
from bs4 import BeautifulSoup  
import pandas as pd
from pathlib import Path

def write_to_csv(speakers, durations, topics, views, descriptions, tags):
    file_existed = True

    csv_file = Path(file)

    if csv_file.exists():
        file_existed = False

    list_labels = ['speakers', 'durations', 'topics', 'views', 'descriptions', 'tags']
    list_cols = [speakers, durations, topics, views, descriptions, tags]
    zipped = list(zip(list_labels, list_cols))
    ted_talk_data = dict(zipped)
    df = pd.DataFrame(ted_talk_data)
    df.to_csv(file, mode='a', index=False, header=file_existed)

def get_detail(video_link):
    print(site + video_link)
    tags_list = []

    try:
        video = requests.get(site + video_link, headers=headers, timeout=3)
        page = BeautifulSoup(video.text, 'html.parser')

        description_meta = page.find('meta', attrs={'name': 'description'})
        tag_metas = page.find_all('meta', property='og:video:tag')
        duration_meta = page.find('meta', property='og:video:duration')
        topic_meta = page.find('meta', attrs={'itemprop':'name'})
        speaker_meta = page.find('meta', attrs={'name': 'author'})
        views_meta = page.find('meta', attrs={'itemprop': 'interactionCount'})

        for tag in tag_metas:
            tags_list.append(tag['content'])

        tags_string = '|'.join(tags_list)

        return speaker_meta['content'], duration_meta['content'], topic_meta['content'], views_meta['content'], \
               description_meta['content'], tags_string

    except requests.ConnectionError:
        return None, None, None, None, None, None
    

if __name__ == "__main__":
    
    site = 'https://www.ted.com'
    file = 'ted_talks_data.csv'

    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'cookie': 'ga=GA1.2.1691398779.1595167282; _tcn=9360; _nu=1604815576; _abby=Ury3TpriLXurRFP; '
              '_gid=GA1.2.1796749197.1604815578; recommends_sticky_banner=1; '
              'muxData=mux_viewer_id=b98bfff4-c228-470f-9d37-4cc9d513a577&msn=0.32555512971574085&sid=23fdddb0-0024'
              '-4f05-a6ac-ba8cdc4f02b3&sst=1604819934674.82&sex=1604822433554.64'}

    for i in range(0, 120):
        url = site + '/talks?page=' + str(i) + '&sort=popular'
        res = requests.get(url, headers=headers, )
        print(url)
        bs = BeautifulSoup(res.text, 'html.parser')
        talks = bs.find('div', class_='row-sm-4up').find_all(class_='col')
        speakers, durations, topics, views, descriptions, tags = [], [], [], [], [], []

        df_csv = None

        try:
            df_csv = pd.read_csv(file)
        except FileNotFoundError:
            print('Not found')

        for talk in talks:
            is_existed = False
            duration_node = talk.find('a', class_='ga-link')

            topic_key = talk.find('h4', class_='h9')

            if topic_key is not None and df_csv is not None:
                topic_key = topic_key.text.strip()

                for item in df_csv.topics:
                    if topic_key == "The future we're building -- and boring":
                        print(item, topic_key, item == topic_key)
                    if item == topic_key:
                        is_existed = True
                        break

            if is_existed is False:
                speaker, duration, topic, view, description, tag = get_detail(duration_node.get('href'))

                if speaker is not None:
                    speakers.append(speaker)
                    durations.append(duration)
                    views.append(view)
                    topics.append(topic)
                    descriptions.append(description)
                    tags.append(tag)

        write_to_csv(speakers, durations, topics, views, descriptions, tags)
        print("input page number" + str(i))





