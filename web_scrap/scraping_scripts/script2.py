import requests, re
import pandas as pd
from bs4 import BeautifulSoup
url="https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.html"
response= requests.get(url)
html_content=response.text

soup=BeautifulSoup(html_content, 'html.parser')

ol_elements = soup.find_all('ol')

for ol_element in ol_elements:
    
    for li in ol_element.find_all('li'):
       
    
        text = li.get_text()
        
        name_pattern = r'(?:Name 6:\s*([A-Za-z\s-]+))|(?:Organisation Name:\s*([^:]+))' 
        alias_pattern = r"(\d+): (?=\s*(.*?)\s*\d:)"
        pob_pattern = r"POB: (?<=POB)(.*)(?=Nationality)"
        group_id_pattern = r"Group ID: (\d+)"

        name_match = re.search(name_pattern, text)

        name_script_tags=li.find('b', text='Name (non-Latin script):')
        title_tags=li.find('b',text='Title:')

        alias_match = re.findall(alias_pattern, text)
        dob_match = re.search(r'(\d+/\d+/\d+)', text)

        nationality_tags=li.find('b', text='Nationality:')
        pob_tags=li.find('b', text='POB:')
        good_quality_tags=li.find('b',text='Good quality a.k.a:')
        low_quality_tags=li.find('b',text='Low quality a.k.a:')
        aka_tags=li.find('b',text='a.k.a:')
        position_tags=li.find('b',text='Position:')
        other_info_tags=li.find('b',text='Other Information:')
        listed_on_tags=li.find('b', text='Listed on:')
        UK_Sanctions_tags=li.find('b',text='UK Sanctions List Date Designated:')
        last_updated_tags=li.find('b', text='Last Updated:')

        group_id_match = re.search(group_id_pattern, text)

        name = name_match.group(0).strip() if name_match else ""
        aliases = [alias[1].strip() for alias in alias_match]
        dob = dob_match.group(1).strip() if dob_match else ""  
        group_id = group_id_match.group(1).strip() if group_id_match else ""

        print(f"{name}")
        c=1
        for i, alias in enumerate(aliases, start=1):
            if alias!=name:
                print(f"Alias {c}: {alias}")
                c+=1
        if name_script_tags:
            name_script=name_script_tags.next_sibling.strip() 
            print(f"Name (non-Latin script): {name_script}")      
           
        if title_tags:
            title = title_tags.next_sibling.strip()
            print(f"Title: {title}")        
        print(f"DOB: {dob}")
        if pob_tags:
            pob = pob_tags.next_sibling.strip()
            print(f"POB: {pob}")
        if good_quality_tags:
            good_quality=good_quality_tags.next_sibling.strip()
            print(f"Good quality a.k.a: {good_quality}")   
        if low_quality_tags:
            low_quality=low_quality_tags.next_sibling.strip()
            print(f"Low quality a.k.a: {low_quality}")        
        if aka_tags:
            aka=aka_tags.next_sibling.strip()
            print(f"a.k.a: {aka}")    
        if nationality_tags:
            nationality = nationality_tags.next_sibling.strip()
            print(f"Nationality: {nationality}")
        if position_tags:
            position = position_tags.next_sibling.strip()
            print(f"Position: {position}") 
        if other_info_tags:
            other_info=other_info_tags.next_sibling.strip()
            print(f"Other Information: {other_info}")    
        if listed_on_tags:
            listed_on = listed_on_tags.next_sibling.strip()
            print(f"Listed on: {listed_on}")    
        if UK_Sanctions_tags:
            UK_sanctions=UK_Sanctions_tags.next_sibling.strip()
            print(f"UK Sanctions List Date Designated: {UK_sanctions}")  
        if last_updated_tags:
            last_updated=last_updated_tags.next_sibling.strip()   
            print(f"Last Updated: {last_updated}") 

        print(f"Group ID: {group_id}")
         










