
import os
import requests
import json 
from pprint import pprint
from requests.structures import CaseInsensitiveDict
import pandas as pd
from functions.image_crawler import *
from functions import general_functions
from functions import image_crawler 
from apicaller.__apicaller_class import APICaller
import datetime
import glob
import argparse
import json
import collections
from collections import defaultdict

parser = argparse.ArgumentParser(description='Get OWL Live events.')


parser.add_argument('--size', "-size", type=int, help='how many event ids to crawl', default = 300)
parser.add_argument('--categories', "-cat", type=str, help='the categories to which the events belong', default ='["Celebrations","Entertainment","Business","Education","Sport","Political","Private"]')

parser.add_argument('--save_event_ids', "-save_ids", type=bool, help='Whether to save the event ids to a json file', default=False)
parser.add_argument('--save_events', "-save_evs", type=bool, help='Whether to save the events to a json file', default=False)
parser.add_argument('--save_images', "-save_imgs", type=bool, help='Whether to download the event images to an order', default=False)
parser.add_argument('--save_to_dataframe', "-save_df", type=bool, help='Whether to save the events in a dataframe to a csv file', default=False)

parser.add_argument('--output_path', "-path", type=str, help='output path to which to save the files', default='D:/Kulturdatenraum_Projekt/Master_Thesis/Datasets/OWL/')


args = parser.parse_args()


if not os.path.exists(args.output_path) and not os.path.isdir(args.output_path):
    os.makedirs(args.output_path)


caller = APICaller()
event_ids_list = caller.get_event_ids(args.size, args.categories)

if args.save_event_ids:
    print(f'==> Saving Event Ids' )
    caller.save_event_ids(event_ids_list, args.output_path)


if args.save_events:
    print(f'==> Saving Events to a json File' )
    caller.save_events(event_ids_list, args.output_path)


if args.save_images:
    print(f'==> Saving Event Images' )
    caller.save_images(event_ids_list, args.output_path)


if args.save_to_dataframe:
    print(f'==> Saving Events in a Dataframe to a csv File' )
    events = caller.get_events(event_ids_list)
    caller.save_events_dataframe(events, args.output_path)


