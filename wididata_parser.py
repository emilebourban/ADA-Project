
print("START \n\n\n")

# Imports
import os
import json

print("\n\n\n\n\nImports \n\n\n\n")

# Paths
DATA = os.path.join("../","wikidata.json")

OUT_FILE = os.path.join("../results/", "humans_strip2.json")

n_humans = 0; n_articles = 0
first = True


# function to open and go through the wikidata JSON file line by line
def wikidata(filename):
    with open(filename, mode='rt') as f:
        f.read(2) # skip first two bytes: "[\n"
        for line in f:
            try:
                yield json.loads(line.rstrip(',\n'))
            except: 
                continue
        

with open(OUT_FILE, mode='w') as nf:
    # we iterate through the wikidata file
    for entity in wikidata(DATA):


        n_articles += 1
        # for each line, which corresponds to an entity, we check its properties
        # and record the ones that are important for us
        try :
            # Test if entity is an instance of human
            if (entity['claims']['P31'][0]['mainsnak']['datavalue']['value']['numeric-id']==5):
                # Recording unique ID
                try:
                    id_ = entity['id']
                except KeyError:
                    id_ = None
                # recording name
                try:
                    name = entity['labels']['en']['value']
                except KeyError:
                    name = None
                # recording gender
                try:
                    gender = entity['claims']['P21'][0]['mainsnak']['datavalue']['value']['id']
                except KeyError:
                    gender = None
                # recording birth date
                try:
                    birth = entity['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
                except KeyError:
                    birth = None
                # recording birth place
                try:
                    place_birth = entity['claims']['P19'][0]['mainsnak']['datavalue']['value']['id']
                except KeyError:
                    place_birth = None
                # recording death date
                try:
                    death = entity['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
                    
                except KeyError:
                    death = None
                #recording citizenships in an array since there can be more than one 
                try:
                    citizenships = []
                    for cit in entity['claims']['P27']:
                        citizenships.append(cit['mainsnak']['datavalue']['value']['id'])
                except KeyError:
                    citizenships = None
                #recording occuptions in an array since there can be more than one
                try:
                    occupations = []
                    for oc in entity['claims']['P106']:
                        occupations.append(oc['mainsnak']['datavalue']['value']['id'])
                except KeyError:
                    occupations = None
                #recording sitelinks in an array since there can be more than one
                try:
                    sitelinks = []
                    for key in entity['sitelinks']:
                        sitelinks.append(entity['sitelinks'][key]['site'])
                except:
                    sitelinks = None
                
                # creating a new dictionary with recorded properties
                new_line_dic = {"Id":id_,"name":name,"gender":gender,"birth":birth,"death":death,
                            "birth_place":place_birth,"citizenships":citizenships,"occupations":occupations,"sitelinks":sitelinks}
                # formatting 
                new_line = json.dumps(new_line_dic)
                # writing new json files  
                if first:
                    nf.write(new_line)
                    first = False
                else:
                    nf.write('\n'+new_line)
                n_humans += 1
        except KeyError :
            print('{} humans on {} articles'.format(n_humans, n_articles))

print('END OF SCRIPT')