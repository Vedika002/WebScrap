import requests, re
import pandas as pd
from bs4 import BeautifulSoup


def run(url, selected_entry):
    # url="https://ofac.treasury.gov"

    response= requests.get(url+"/recent-actions")
    html_content=response.text

    soup=BeautifulSoup(html_content, 'html.parser')

    rows=[]
    data_list = []
    arr=[]
    rows=soup.find("div",{"class":"view-content"}).find_all("div", {"class":"views-row"})
    
    for row in rows:
        a_tag=row.find("a")
        heading = a_tag.text
        if "updates" in heading.lower() or "update" in heading.lower():
            url1 = a_tag['href']
            arr.append({"heading":heading,"link":url+url1})

    all_paragraphs = []
    ur = []
    for u in arr:
        url=u["link"]
        ur.append(url)
    for i in ur:
        
        response = requests.get(i)
        html_content = response.text
        soup=BeautifulSoup(html_content, 'html.parser')
        div_elements = soup.find("div",{"class":"clearfix text-formatted usa-prose field field--name-field-body field--type-text-long field--label-visually_hidden"}).find_all("div",{"class": "field__item"})
        
        for div in div_elements:
            paragraphs = div.find_all('p')
            
            for paragraph in paragraphs:
            
                newpara=str(paragraph).replace("\n"," ")
                
                paragraph_parts=newpara.split('<br/><br/>')
                
                
                for part in paragraph_parts:
                    part=BeautifulSoup(part, 'html.parser')
                    text = part.get_text().replace("\n"," ")
                    if '-to-' in text:
                        parts = text.split('-to-')
                        text = parts[1].strip() 
                    all_paragraphs.append(text.strip())
                    
    name_pattern = r'^[^()]*'
    alias_pattern = r'\(a\.k\.a\..+?\)'
    pob_pattern = r'POB ([^;]+)'
    dob_pattern = r'DOB ([^;]+)'
    gender_pattern = r'Gender\s+(Male|Female)'

    for inside_para in all_paragraphs:
        name_match = re.search(name_pattern, inside_para)
    
        if name_match:
            name = name_match.group(0).strip()
            
        else:
            continue  

        alias_matches = re.findall(alias_pattern, inside_para)
        aliases = []
        for alias_match in alias_matches:
            alias = alias_match.strip().replace("a.k.a.", "").replace("(","").replace(")","").replace('"', '').replace("f.k.a.","").strip()
            aliases.extend(alias.split(';')) 
        
        pob_match = re.search(pob_pattern, inside_para)
        pob = pob_match.group(1).strip() if pob_match else ""
        
        dob_match = re.search(dob_pattern, inside_para)
        dob = dob_match.group(1).strip() if dob_match else ""

        gender_match = re.search(gender_pattern, inside_para)
        gender= gender_match.group(1).strip() if gender_match else ""
        
        person_data = {
                        "Name": name,
                        "POB": pob,
                        "DOB": dob,
                        "Gender": gender
                    }
                
        for i, alias in enumerate(aliases):
            person_data[f"Alias{i+1}"] = alias

        data_list.append(person_data)

    df = pd.DataFrame(data_list)

    df.to_excel('output.xlsx', index=False)
        # print(f"Name: {name}")
        # for idx, alias in enumerate(aliases, start=1):
        #             print(f"Alias {idx}: {alias.strip()}")
        # if pob:
        #     print(f"POB: {pob}")
        # if dob:
        #     print(f"DOB: {dob}")
        # if gender:
        #     print(f"Gender: {gender}")    
        # print("\n")


        



        
    





