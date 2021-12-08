import pandas as pd
import csv
from transformers import BartForConditionalGeneration, BartTokenizer
from typing import List
from tqdm import tqdm
import time

from EpiTator.epitator.annotator import AnnoDoc
from EpiTator.epitator.count_annotator import CountAnnotator
from EpiTator.epitator.date_annotator import DateAnnotator
from EpiTator.epitator.geoname_annotator import GeonameAnnotator

tqdm.pandas()

# function that extracts location names/admin codes/lat/lng, case and death counts, and date ranges from the input string
# uses epitator since it already trained rules for extracting medical/infectious disease data
def epitator_extract(txt, max_ents=1):
    # input string and add annotators
    t0 = time.time()

    doc = AnnoDoc(txt)
    print('doc', time.time()-t0)
    doc.add_tiers(GeonameAnnotator())
    print('geoname', time.time()-t0)
    doc.add_tiers(CountAnnotator())
    print('count', time.time()-t0)
    doc.add_tiers(DateAnnotator())
    print('date', time.time()-t0)

    # extract geographic data
    geos = doc.tiers["geonames"].spans
    geo_admin1s = [x.geoname.admin1_code for x in geos]
    geo_admin2s = [x.geoname.admin2_code for x in geos]
    geo_admin3s = [x.geoname.admin3_code for x in geos]
    geo_admin4s = [x.geoname.admin4_code for x in geos]
    geo_names = [x.geoname.name for x in geos]
    geo_lats = [x.geoname.latitude for x in geos]
    geo_lons = [x.geoname.longitude for x in geos]

    input(txt)

    # extract case counts and death counts
    counts = doc.tiers["counts"].spans
    cases_counts = [x.metadata['count'] for x in counts if 'case' in x.metadata['attributes'] and 'death' not in x.metadata['attributes']]
    cases_tags = [x.metadata['attributes'] for x in counts if 'case' in x.metadata['attributes'] and 'death' not in x.metadata['attributes']]
    death_counts = [x.metadata['count'] for x in counts if 'death' in x.metadata['attributes']]
    death_tags = [x.metadata['attributes'] for x in counts if 'death' in x.metadata['attributes']]

    # extract the date range
    dates = doc.tiers["dates"].spans
    dates_start = [pd.to_datetime(x.metadata["datetime_range"][0], errors='coerce') for x in dates]
    dates_end = [pd.to_datetime(x.metadata["datetime_range"][1], errors='coerce') for x in dates]

    # return only max_ents entities from the extracted lists
    # currently set to the first result for each list, since that is usually the most important one
    # and other ones can be filler/garbage data
    return pd.Series([
        geo_admin1s[:max_ents],
        geo_admin2s[:max_ents],
        geo_admin3s[:max_ents],
        geo_admin4s[:max_ents],
        geo_names[:max_ents],
        geo_lats[:max_ents],
        geo_lons[:max_ents],
        cases_counts[:max_ents],
        cases_tags[:max_ents],
        death_counts[:max_ents],
        death_tags[:max_ents],
        dates_start[:max_ents],
        dates_end[:max_ents],
    ])

def extract_publish_date(text: str) -> str:
    return re.search(r'[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])', text)[0]

# helper function to summarize an input text with the BART model
def summarizer(text: str) -> str:
    input_ids = tokenizer(text, return_tensors='pt', max_length=1024, padding=True, truncation=True)['input_ids']
    summary_ids = model.generate(input_ids.cuda())
    summary = ''.join([tokenizer.decode(s) for s in summary_ids])
    summary = summary.replace('<s>', '').replace('</s>', '')
    return summary

if __name__ == "__main__":

    # Extract metadata
    df = dict()
    with open('promed_dengue.csv',newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        keys = False
        values = False
        for row in reader:
            if not keys:
                keys = row[1:]
            elif not values:
                values = row[1:]
            else:
                break

        for i in range(len(keys)):
            if keys[i] == 'title':
                values[i] = values[i][2:-2]
            df[keys[i]] = [values[i]]

    # Create dataframe
    df = pd.DataFrame.from_dict(df)

    # Set up our BART transformer summarization model
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').cuda()

    df['summary'] = df['content'].progress_apply(summarizer)
    input(df['summary'])


    df[['admin1_code',
    'admin2_code',
    'admin3_code',
    'admin4_code',
    'location_name',
    'location_lat',
    'location_lon',
    'cases',
    'cases_tags',
    'deaths',
    'deaths_tags',
    'dates_start',
    'dates_end',]] = df['summary'].progress_apply(epitator_extract)
    df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
    df = df.applymap(lambda y: pd.NA if isinstance(y, (list, str)) and len(y) == 0 else y)

    print(df['dates_start'])