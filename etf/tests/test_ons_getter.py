'''
get data from the ons
https://developer.ons.gov.uk/observations/

'''


import requests

example_url = '/datasets/cpih01/editions/time-series/versions/6/observations?time=Oct-11&geography=K02000001&aggregate=cpih1dim1A0'
example_url = 'https://api.beta.ons.gov.uk/v1/datasets/cpih01/editions/time-series/versions/4/observations?time=Apr-20&ge'
example_url = "https://api.beta.ons.gov.uk/v1/datasets"

# we can get the datasets
x = requests.get(example_url)
print(x)



if x.status_code==200:
    print('response: success')
else:
    print('response: fail')
    exit()

print()
print('the text version:')
#print(x.text)

print()
print('the dict version:')
d = x.json()
print('the keys')
print(d.keys())
# example of traversing the json
print(d['items'][0]['contacts'][0]['name'])

# print(d['id'])
# print(d['keywords'])



'''
example of the response

{'@context': 'https://cdn.ons.gov.uk/assets/json-ld/context.json', 'count': 20, 'items': [{'contacts': [{'email': '+44 (0)1329 444661', 'name': 'Population Statistics Division', 'telephone': 'pop.info@ons.gov.uk'}], 'description': 'Indicators included have been derived from the published 2019 mid-year population estimates for the UK, England, Wales, Scotland and Northern Ireland. These are the number of persons and percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of 
those aged 16 years to below State Pension age).\n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool enables users to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.', 'id': 'ageing-population-estimates', 'keywords': ['ageing', 'population'], 'links': {'editions': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions'}, 'latest_version': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions/time-series/versions/1', 'id': '1'}, 'self': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates'}, 'taxonomy': {'href': 'https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing'}}, 'next_release': '1 June 2021', 'qmi': {'href': 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/annualmidyearpopulationestimatesqmi'}, 'related_datasets': [{'href': 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland', 'title': 'Estimates of the population for the UK, England and Wales, Scotland and Northern Ireland'}], 'release_frequency': 'Annual', 'state': 'published', 'title': 'Local authority ageing statistics, based on annual mid-year population estimates'}, {'contacts': [{'email': 'pop.info@ons.gov.uk', 'name': 'Population Statistics Division', 'telephone': '+44 (0)1329 444661'}], 'description': 'Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). \n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. \n\nNote on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.', 'id': 'ageing-population-projections', 'keywords': ['ageing', 'projections', 'population'], 'links': {'editions': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions'}, 'latest_version': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions/time-series/versions/1', 
'id': '1'}, 'self': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections'}, 'taxonomy': {'href': 'https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing'}}, 'methodologies': [{'href': 'https://www.nrscotland.gov.uk/files//statistics/population-projections/sub-national-pp-18/pop-proj-principal-18-methodology.pdf', 'title': 'Scotland Methodology Guide'}, {'href': 'https://gov.wales/population-and-household-statistics-technical-information', 'title': 'Wales technical information'}, {'href': 'https://www.nisra.gov.uk/sites/nisra.gov.uk/files/publications/SNPP18-Methodology.pdf', 'title': 'Northern Ireland methodology paper'}], 'next_release': 'To be announced', 'qmi': {'href': 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/methodologies/subnationalpopulationprojectionsqmi'}, 'related_datasets': [{'href': 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/bulletins/subnationalpopulationprojectionsforengland/2018based', 'title': 'Subnational population projections for England: 2018-based'}, {'href': 'https://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/population/population-projections/sub-national-population-projections/2018-based', 'title': 'Population Projections for Scottish Areas (2018-based)'}, {'href': 'https://gov.wales/subnational-population-projections-2018-based', 'title': 'Wales subnational population projections (local authority): 2018-based'}, {'href': 'https://www.nisra.gov.uk/publications/2018-based-population-projections-areas-within-northern-ireland', 'title': '2018-based Population Projections for Areas within Northern Ireland'}, {'href': 'https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing/articles/subnationalageingtool/2020-07-20', 'title': 'Subnational ageing tool'}], 'release_frequency': 'Biennial', 'state': 'published', 'title': 'Local authority ageing statistics, population projections for older people'}, {'contacts': [{'email': 'pop.info@ons.gov.uk', 
'name': 'Population Statistics Division', 'telephone': '+44 (0)1329 444661'}], 'description': 'Indicators included are economic activity and employment rates for those aged 50-64 years, by country, region and local authority. Both economic activity and employment rates are displayed as percentages. These have been calculated from the ONS 
Annual Population Survey and have been extracted from NOMIS.\n\nhttps://www.nomisweb.co.uk/\n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which will be published in July 2020. The tool will be interactive, and users will be able to compare latest and projected measures of ageing 
for up to four different areas through selection on a map or from a drop-down menu. \n\nNote on update frequency: NOMIS provide quarterly updates on both indicators. For 
consistency with other indicators presented in the subnational ageing tool, these will be updated on an annual basis.', 'id': 'older-people-economic-activity', 'keywords': ['ageing', 'population'], 'links': {'editions': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions'}, 'latest_version': {'href': 
'https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions/time-series/versions/1', 'id': '1'}, 'self': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity'}, 'taxonomy': {'href': 'https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing'}}, 'next_release': '1 June 2021', 'qmi': {'href': 'https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/methodologies/annualpopulationsurveyapsqmi'}, 'related_datasets': [{'href': 'https://www.nomisweb.co.uk/', 'title': 'Link to NOMIS website'}], 'release_frequency': 'Quarterly but updated on CMD annually', 'state': 'published', 'title': 'Local authority ageing statistics, older people economic activity'}, {'contacts': [{'email': 'pop.info@ons.gov.uk', 'name': 'Population Statistics Division', 'telephone': '+44 (0)1329 444661'}], 'description': 'Figures presented show the movement of older people between local authorities and regions. Both indicators 
included in this dataset have been derived from the published 2019 internal migration dataset for England and Wales. The numbers presented are the net number of people aged 65 years and over and 85 years and over entering/ leaving the local authority or region in the 12-month period stated.\n\nThis dataset has been produced by the Ageing 
Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool is interactive, and users are able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a 
drop-down menu.', 'id': 'older-people-net-internal-migration', 'keywords': ['ageing', 'population'], 'links': {'editions': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions'}, 'latest_version': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions/time-series/versions/1', 'id': '1'}, 'self': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration'}, 'taxonomy': {'href': 'https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing'}}, 'next_release': '1 June 2021', 'qmi': {'href': 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/migrationwithintheuk/methodologies/in


'''
