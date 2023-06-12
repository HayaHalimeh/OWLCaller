
import requests
from requests.structures import CaseInsensitiveDict
import json
from pprint import pprint
from typing import List, Mapping, Union
import numpy as np
from tqdm import tqdm
import pandas as pd
from functions.image_crawler import *
from functions import general_functions
from functions import image_crawler 
import glob
from collections import defaultdict
import collections


class APICaller:


    def __init__(self) -> None:
        
        self.headers = CaseInsensitiveDict()
        self.headers["accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.url = "https://api.owl-live.de:443/Event"
        
        pass


    def get_event_ids(self, size: int = 300, 
                      Categories:str = '["Celebrations","Entertainment","Business","Education","Sport","Political","Private"]') -> List[int]:
        '''
        Gets event ids specific to given Categories

        size: number of events 
        Categories: Categories to which the events belong
        '''
        
        url = self.url + "/Filter"
        event_ids_list = list()

        nr_iterations = int(np.ceil(size / 100))
        set_size = 0


        for run in tqdm(range(nr_iterations)):
            if run == nr_iterations - 1  and size % 100 != 0:
                offset = set_size
                set_size = size % 100 #offset + 
                #print(run, offset, set_size)
            
            else:
                offset = run * 100 
                set_size =  100 - offset % 100 #offset +
                #print(run, offset, set_size)


            data = '{"Offset":"' + str(offset) + '", "Size":"' + str(set_size) + '","Categories":' + Categories + '}'
            #print(data)

            try:
                resp = requests.post(url, headers=self.headers, data=data)
                temp = [resp.json()['hits'][idx]['id'] for idx in range(0, len(resp.json()['hits']))]
                event_ids_list.extend( list(set(temp)))

            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", e)


        
        print("In Total Got", len(event_ids_list), 'unique ids')
        return event_ids_list
        



    def save_event_ids(self, event_ids_list: List[int] = None,
                ids_output_path: str = None):
        '''
        Saves the a list of event_ids to a json output file with the respective day's date
        '''
        
        import datetime
        today = datetime.date.today()
        events= {'event_ids': event_ids_list}

        file_out = f"{ids_output_path}/owl_ids_{str(today).replace('-', '_')}.json"
        general_functions.save_json_file(events, file_out)
        
        print(f'Dict with {len(events["event_ids"])} event ids saved to {file_out}' )
                


    def get_events(self, event_ids: Union[List[int], int]) ->  collections.defaultdict:

        """
        send a request to the owl api to get information about events and returns them in a default dict format
        event_ids:  list of event ids

        """
        responses = defaultdict(list)

        url = self.url + "/GetEventItemByID/"
        for event_id in tqdm(event_ids):
            try:
                resp = requests.get(url+str(event_id), headers=self.headers)
                
                for key, value in resp.json().items():
                    responses[key].append(value)

            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", e)

        return responses
            

    def save_events(self, event_ids: Union[List[int], int],
                    events_output_path: str = None) :

        """
        send a request to the owl api to get information about events and saves them in events_output_path in a default dict format
        event_ids:  list of event ids
        events_output_path: output path
        """

        import datetime
        today = datetime.date.today()

        responses = defaultdict(list)
        url = self.url + "/GetEventItemByID/"
     
        for event_id in event_ids:
            try:
                resp = requests.get(url+str(event_id), headers=self.headers)
                
                for key, value in resp.json().items():
                    responses[key].append(value)

            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", e)

        file_out = f"{events_output_path}/owl_data_{str(today).replace('-', '_')}.json"
        general_functions.save_json_file(responses, file_out)

        print(f'Dict with {len(responses["id"])} events saved to {file_out}' )
            


    def get_images(self, event_ids: List[int] = None) -> collections.defaultdict:
        
        url = self.url + "/GetEventItemByID/"
        responses = defaultdict(list)

        for event_id in event_ids:
            try:
                resp = requests.get(url+str(event_id), headers=self.headers)
                
                content = resp.json()
                if 'mainImage' in content.keys() and 'contentUrl' in content['mainImage'].keys() :
                    if content['mainImage']['contentUrl'] != None:
                        responses[content['id']].append(content['mainImage']['contentUrl'])

            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", e)

        return responses



    def save_images(self, event_ids: List[int] = None,
                                    images_output_path: str = None):
        
        url = self.url + "/GetEventItemByID/"

        count=0
        for event_id in event_ids:
            try:
                resp = requests.get(url+str(event_id), headers=self.headers)
                content = resp.json()
                if 'mainImage' in content.keys() and 'contentUrl' in content['mainImage'].keys() :
                    if content['mainImage']['contentUrl'] != None:
                        image_crawler.request_save_image(content['mainImage']['contentUrl'], f'{images_output_path}\{content["id"]}.jpg')
                        count += 1


                        
            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", e)

        
        print(f"In Total {count/len(event_ids):.2f} % of Images downloaded and saved to {images_output_path}")




    def save_events_dataframe(self, events: collections.defaultdict=None,
                              output_path:str =None):

        '''
        
        '''
        import datetime
        today = datetime.date.today()

        dataframe = pd.DataFrame.from_dict(events, orient='index').transpose()
        file_out = f"{output_path}/owl_data_{str(today).replace('-', '_')}.csv"

        dataframe.to_csv(file_out, index=False)
        print(f'Dataframe with {len(dataframe)} events saved to {file_out}' )


        





'''

 def get_events_and_images(self, event_ids: List[int] = None,
                        output_path : str = None):
        
        """
        send requests to the owl api to get information about events with ids stored in 'event_ids'
        substracts the main image url, requests it and saves it in dataframe with the defined 'columns' along other 
        events information
        """

        dataframe = pd.DataFrame()

        for id in event_ids:
            
            event = {}
            resp = self.get_event(id)
            print(id, event_ids.index(id)/len(event_ids), resp.status_code)
            
            if resp.status_code != 200:
                #print(resp.status_code)
                break

            else:
                try:
                    content =  resp.json()
                    #for col in columns:
                    for col in content.keys():

                            if col=="mainImage" and content['mainImage']['contentUrl'] != None:
                                event['image_id'] = content['id_str']

                                img_out_path = output_path + 'images/image_' + str(content['id_str']) + '.jpg'
                                
                                img_url = content['mainImage']['contentUrl']
                                
                                image_crawler.request_save_image(img_url,img_out_path)
                                print("image downloaded")

                                event[col] = ""
                            else:
                                event[col] = str(content[col])
                    #else:
                    #    event[col] = ""

                except requests.exceptions.ConnectTimeout:
                    print("expection")

                    df_data = pd.DataFrame(event, index=[0])
                    dataframe = pd.concat([dataframe, df_data] , ignore_index=True)

                    

                    #file_out = f"{output_path}{output_file}"
                    #dataframe.to_csv(file_out, index=False,)
                    #print(f'saved to {file_out}, {len(dataframe)} events' )


            #df_data = pd.DataFrame(event, index=[0])
            #dataframe = pd.concat([dataframe, df_data] , ignore_index=True)

        return dataframe
         

        #file_out = f"{output_path}{output_file}"
        #dataframe.to_csv(file_out, index=False,)
        #print(f'saved to {file_out}', {len(dataframe)} events' )

        #pass

'''