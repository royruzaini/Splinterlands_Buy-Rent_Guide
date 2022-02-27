from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View 
import json
import pandas as pd
import requests
import ssl
import urllib.request
import certifi
from statistics import mode

# Create your views here.
def home(request):
    return render(request, "home.html")

def monster_color(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    color = [x['color'] for x in card_id if x['id'] == id]
    color = ''.join(color)
    return color

def card_name(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    name = [x['name'] for x in card_id if x['id'] == id]
    name = ''.join(name)
    return name

def card_rarity(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    rarity = [str(x['rarity']) for x in card_id if x['id'] == id]
    rarity = int(''.join(rarity))
    return rarity

def card_edition(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    edition = [str(x['editions']) for x in card_id if x['id'] == id]
    edition = int(''.join(edition))
    return edition

def splinter(color):
    if color == 'Blue':
        return 'Water'
    elif color == 'Red':
        return 'Fire'
    elif color == 'Green':
        return 'Earth'
    elif color == 'Gold':
        return 'Dragon'
    elif color == 'Black':
        return 'Death'
    elif color == 'White':
        return 'Life'
    elif color == 'Gray':
        return 'Neutral'
    else :
        return None

def monster_mana(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    cardmana = [str(x['stats']['mana'][0]) for x in card_id if x['id'] == id]
    cardmana = list(set(cardmana))
    cardmana = int(''.join(cardmana))
    return cardmana

def summoner_mana(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    cardmana = [str(x['stats']['mana']) for x in card_id if x['id'] == id]
    cardmana = list(set(cardmana))
    cardmana = int(''.join(cardmana))
    return cardmana

def monster_abilities(id):
    with open('cardsDetails.json') as f:
        card_id = json.load(f)
    tmp = [x['stats']['abilities'] for x in card_id if x['id'] == id]
    abilities = []
    for mylist in tmp:
        for s in mylist:
            if len(s) != 0:
                s = ''.join(s)
                if s not in abilities:
                    abilities.append(s)
    return abilities

with open("mycards.json") as file:
    mycards = json.load(file)
file.close

with open('C:/Users/royru/Desktop/SplinterlandsBot-History/collection.json') as f:
    BATTLEBASE = json.load(f)
f.close

class Api(TemplateView):
    # Create your views here.
    def get_cards(request):
        """ Get user's playable cards.
        """
        username = request.GET.get("username")
        edition = request.GET.get("edition")
        NoLegend = request.GET.get("NoLegend")
        NoLegendSummoners = request.GET.get("NoLegendSummoners")
        rarity = request.GET.get("rarity")

        edition = list(edition.split(","))
        rarity = list(rarity.split(","))

        if username != "" and username != "ALL":

            base_cards = [135, 136, 137, 138, 139, 140, 141, 145, 146, 147, 148, 149, 150, 151, 152, 156, 157, 158, 159, 160, 161, 162, 163, 167, 168, 169, 170, 171, 172, 173, 174, 178, 179, 180, 181, 182, 183, 184, 185, 189, 190, 191, 192, 193, 194, 195, 196, 224, 353, 354, 355, 356, 357, 358, 359, 360, 361, 367, 368, 369, 370, 371, 372, 373, 374, 375, 381, 382, 383, 384, 385, 386, 387, 388, 389, 395, 396, 397, 398, 399, 400, 401, 402, 403, 409, 410, 411, 412, 413, 414, 415, 416, 417, 423, 424, 425, 426, 427, 428, 429, 437, 438, 439, 440, 441] 
            p_cards = []

            player_cards_data = requests.get(
                'https://api2.splinterlands.com/cards/collection/' + username.lower()
            )
            player_cards = player_cards_data.json()['cards']

            for p_card in player_cards:
                # checks if base cards have been upgraded
                if p_card['card_detail_id'] in base_cards:
                    base_cards.remove(p_card['card_detail_id'])

                p_card_data = {}
                p_card_data['id'] = p_card['card_detail_id']
                p_card_data['level'] = p_card['level']
                p_card_data['edition'] = p_card['edition']
                p_card_data['rarity'] = card_rarity(int(p_card['card_detail_id']))
                p_cards.append(p_card_data)

            for base_card in base_cards:
                base_card_data = {}
                base_card_data['id'] = base_card
                base_card_data['level'] = 1
                base_card_data['edition'] = card_edition(int(base_card))
                base_card_data['rarity'] = card_rarity(int(base_card))
                p_cards.append(base_card_data)

            with open("mycards.json", "w") as outfile:
                outfile.write(json.dumps(p_cards))
            outfile.close

            edition_deck = []

            with open("mycards.json") as file:
                mycards = json.load(file)
            file.close

            for x in edition:
                if x != '':
                    x = int(x)

                    for p_card in mycards:
                    # checks if base cards have been upgraded
                        if p_card['edition'] == x:
                            edition_deck.append(p_card)
                            
            if len(edition_deck) > 0:
                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(edition_deck))
                outfile.close

            rarity_deck = []

            with open("mycards.json") as file:
                mycards = json.load(file)
            file.close

            for x in rarity:
                if x != '':
                    x = int(x)

                    for p_card in mycards:
                    # checks if base cards have been upgraded
                        if p_card['rarity'] == x:
                            rarity_deck.append(p_card)
                            
            if len(rarity_deck) > 0:
                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(rarity_deck))
                outfile.close
                
            NoLegend_deck = []

            if NoLegend == "NoLegend":
                with open("mycards.json") as file:
                    mycards = json.load(file)
                file.close

                for p_card in mycards:
                # checks if base cards have been upgraded
                    if p_card['rarity'] != 4:
                        NoLegend_deck.append(p_card)

                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(NoLegend_deck))
                outfile.close

            NoLegendSummoners_deck = []

            if NoLegendSummoners == "NoLegendSummoners":
                with open("mycards.json") as file:
                    mycards = json.load(file)
                file.close

                with open("legendarySummonersCards.json") as file:
                    NoLegendSummoners = json.load(file)
                file.close

                for p_card in mycards:
                # checks if base cards have been upgraded
                    if p_card['id'] not in NoLegendSummoners:
                        NoLegendSummoners_deck.append(p_card)

                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(NoLegendSummoners_deck))
                outfile.close

            with open("mycards.json") as file:
                mycards = json.load(file)
            file.close

            data = "mycards.json successfully created!"
            return HttpResponse(data)

        elif username == "ALL":

            with urllib.request.urlopen('https://api.splinterlands.io/cards/get_details', context=ssl.create_default_context(cafile=certifi.where())) as url:
                player_cards = json.loads(url.read().decode())

            p_cards = []

            for p_card in player_cards:
                p_card_data = {}
                p_card_data['id'] = p_card['id']
                p_card_data['level'] = 1
                try:
                    p_card_data['edition'] = int(p_card['editions'])
                except:
                    p_card_data['edition'] = 0
                p_card_data['rarity'] = p_card['rarity']
                p_cards.append(p_card_data)

            with open("mycards.json", "w") as outfile:
                outfile.write(json.dumps(p_cards))
            outfile.close

            edition_deck = []

            with open("mycards.json") as file:
                mycards = json.load(file)
            file.close

            for x in edition:
                if x != '':
                    x = int(x)

                    for p_card in mycards:
                    # checks if base cards have been upgraded
                        if p_card['edition'] == x:
                            edition_deck.append(p_card)
                            
            if len(edition_deck) > 0:
                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(edition_deck))
                outfile.close

            rarity_deck = []

            with open("mycards.json") as file:
                mycards = json.load(file)
            file.close

            for x in rarity:
                if x != '':
                    x = int(x)

                    for p_card in mycards:
                    # checks if base cards have been upgraded
                        if p_card['rarity'] == x:
                            rarity_deck.append(p_card)
                            
            if len(rarity_deck) > 0:
                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(rarity_deck))
                outfile.close

            NoLegend_deck = []

            if NoLegend == "NoLegend":
                with open("mycards.json") as file:
                    mycards = json.load(file)
                file.close

                for p_card in mycards:
                # checks if base cards have been upgraded
                    if p_card['rarity'] != 4:
                        NoLegend_deck.append(p_card)

                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(NoLegend_deck))
                outfile.close

            NoLegendSummoners_deck = []

            if NoLegendSummoners == "NoLegendSummoners":
                with open("mycards.json") as file:
                    mycards = json.load(file)
                file.close

                with open("legendarySummonersCards.json") as file:
                    NoLegendSummoners = json.load(file)
                file.close

                for p_card in mycards:
                # checks if base cards have been upgraded
                    if p_card['id'] not in NoLegendSummoners:
                        NoLegendSummoners_deck.append(p_card)

                with open("mycards.json", "w") as outfile:
                    outfile.write(json.dumps(NoLegendSummoners_deck))
                outfile.close

            with open("mycards.json") as file:
                mycards = json.load(file)
            file.close

            data = "allcards.json successfully created!"
            return HttpResponse(data)

        else :
            data = "please enter correct username! or type 'ALL' for all cards"
            return HttpResponse(data)

    def getteamwhite(request):

        mana = request.GET.get("mana")
        if mana == "ALL":
            mana = 99
        rule1 = request.GET.get("rule1")
        rule2 = request.GET.get("rule2")
        splinterteam = 'Life'

        with open("mycards.json") as file:
            mycards = json.load(file)
        file.close

        def filter_deck(battle):
            if mana == "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and  battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False

        db_decks = list(filter(filter_deck, BATTLEBASE))

        possible_decks = []

        viable = False
        team = {}
        Bestsummoner = []
        Bestmonster = []
        Besttank = []

        for battle in db_decks:
            summoner = [str(card['id']) for card in mycards if card['id'] == battle['summoner_id']]
            if not summoner:
                continue
            else:
                summoner = list(set(summoner))
                summoner = int(''.join(summoner))
                Bestsummoner.append(summoner)

        # checks if player has card with battle summoner card_detail_id
        if len(Bestsummoner) == 0:
            viable = False
        else:
            mostusesummoner = mode(Bestsummoner)
            team['summoner_id'] = mostusesummoner
            team['summoner_level'] = 1
            team['summoner_splinter'] = splinter(monster_color(int(mostusesummoner)))
            frequency = Bestsummoner.count(mostusesummoner)
            ratio = round((frequency/len(Bestsummoner)) * 100, 2)
            team['summoner_frequency'] = frequency
            team['summoner_ratio'] = str(ratio) + '%'
            cardmana = summoner_mana(int(mostusesummoner))
            BalanceMana = int(mana) - cardmana
        
            teamtoplay = {}
            teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner]

            if len(teamtoplay) > 0:

                for battle in teamtoplay:
                    tank = [str(card['id']) for card in mycards if card['id'] == battle['monster_1_id']]
                    if not tank:
                        continue
                    else:
                        tank = list(set(tank))
                        tank = int(''.join(tank))
                        Besttank.append(tank)

                if len(Besttank) > 0:
                    viable = True
                    mostusetank = mode(Besttank)
                    team['monster_1_id'] = mostusetank
                    team['monster_1_level'] = 1
                    team['monster_1_abilities'] = monster_abilities(int(mostusetank))
                    team['monster_1_splinter'] = splinter(monster_color(int(mostusetank)))
                    frequency = Besttank.count(mostusetank)
                    ratio = round((frequency/len(Besttank)) * 100, 2)
                    team['monster_1_frequency'] = frequency
                    team['monster_1_ratio'] = str(ratio) + '%'
                    cardmana = monster_mana(int(mostusetank))
                    BalanceMana = BalanceMana - cardmana

                    teamtoplay = {}
                    teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner and battle['monster_1_id'] == mostusetank]

                    for x in range(2, 7):
                        
                        if battle['monster_'+str(x)+'_id'] != "":

                            Bestmonster = []

                            for battle in teamtoplay:
                                monster = [str(card['id']) for card in mycards if card['id'] == battle['monster_'+str(x)+'_id']]
                                if not monster:
                                    continue
                                else:
                                    monster = list(set(monster))
                                    monster = int(''.join(monster))
                                    Bestmonster.append(monster)

                            if len(Bestmonster) > 0:
                                mostusemonster = mode(Bestmonster)
                                frequency = Bestmonster.count(mostusemonster)
                                ratio = round((frequency/len(Bestmonster)) * 100, 2)
                                cardmana = monster_mana(int(mostusemonster))
                                
                                if BalanceMana > 0 and BalanceMana >= cardmana :
                                    if x == 2:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 3:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 4:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 5:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 6:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id'] or mostusemonster == team['monster_'+str(x-5)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                else:
                                    team['monster_'+str(x)+'_id'] = ""
                                    team['monster_'+str(x)+'_level'] = ""
                                    team['monster_'+str(x)+'_abilities'] = []
                                    team['monster_'+str(x)+'_splinter'] = ""
                                    team['monster_'+str(x)+'_frequency'] = ""
                                    team['monster_'+str(x)+'_ratio'] = ""
                            else:
                                team['monster_'+str(x)+'_id'] = ""
                                team['monster_'+str(x)+'_level'] = ""
                                team['monster_'+str(x)+'_abilities'] = []
                                team['monster_'+str(x)+'_splinter'] = ""
                                team['monster_'+str(x)+'_frequency'] = ""
                                team['monster_'+str(x)+'_ratio'] = ""
                        else:
                            team['monster_'+str(x)+'_id'] = ""
                            team['monster_'+str(x)+'_level'] = ""
                            team['monster_'+str(x)+'_abilities'] = []
                            team['monster_'+str(x)+'_splinter'] = ""
                            team['monster_'+str(x)+'_frequency'] = ""
                            team['monster_'+str(x)+'_ratio'] = ""
                else:
                    viable = False
            else:
                viable = False
        if viable:
            possible_decks.append(team)

        if len(possible_decks) != 0:

            for battle in possible_decks:

                most_win_deck = {}

                most_win_deck['card'] = []         
                most_win_deck['card'].append('summoner')
                most_win_deck['id'] = []
                most_win_deck['id'].append(battle['summoner_id'])
                most_win_deck['name'] = []
                most_win_deck['name'].append(card_name(int(battle['summoner_id'])))
                most_win_deck['splinter'] = []
                most_win_deck['splinter'].append(splinter(monster_color(int(battle['summoner_id']))))
                most_win_deck['frequency'] = []
                most_win_deck['frequency'].append(battle['summoner_frequency'])
                most_win_deck['ratio'] = []
                most_win_deck['ratio'].append(battle['summoner_ratio'])

                for x in range(0, 6):
                    if battle['monster_'+str(x+1)+'_id'] != "" :
                        most_win_deck['card'].append('monster_'+str(x+1))
                        most_win_deck['id'].append(battle['monster_'+str(x+1)+'_id'])
                        most_win_deck['name'].append(card_name(int(battle['monster_'+str(x+1)+'_id'])))
                        most_win_deck['splinter'].append(splinter(monster_color(int(battle['monster_'+str(x+1)+'_id']))))
                        most_win_deck['frequency'].append(battle['monster_'+str(x+1)+'_frequency'])
                        most_win_deck['ratio'].append(battle['monster_'+str(x+1)+'_ratio'])

            df = pd.DataFrame(most_win_deck)
            data = df.to_html(classes='table table-bordered')
            return HttpResponse(data)
        else:
            data = "No " + splinterteam + " Team Available"
            return HttpResponse(data)

    def getteamblack(request):

        mana = request.GET.get("mana")
        if mana == "ALL":
            mana = 99
        rule1 = request.GET.get("rule1")
        rule2 = request.GET.get("rule2")
        splinterteam = 'Death'

        with open("mycards.json") as file:
            mycards = json.load(file)
        file.close

        def filter_deck(battle):
            if mana == "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and  battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False

        db_decks = list(filter(filter_deck, BATTLEBASE))

        possible_decks = []

        viable = False
        team = {}
        Bestsummoner = []
        Bestmonster = []
        Besttank = []

        for battle in db_decks:
            summoner = [str(card['id']) for card in mycards if card['id'] == battle['summoner_id']]
            if not summoner:
                continue
            else:
                summoner = list(set(summoner))
                summoner = int(''.join(summoner))
                Bestsummoner.append(summoner)

        # checks if player has card with battle summoner card_detail_id
        if len(Bestsummoner) == 0:
            viable = False
        else:
            mostusesummoner = mode(Bestsummoner)
            team['summoner_id'] = mostusesummoner
            team['summoner_level'] = 1
            team['summoner_splinter'] = splinter(monster_color(int(mostusesummoner)))
            frequency = Bestsummoner.count(mostusesummoner)
            ratio = round((frequency/len(Bestsummoner)) * 100, 2)
            team['summoner_frequency'] = frequency
            team['summoner_ratio'] = str(ratio) + '%'
            cardmana = summoner_mana(int(mostusesummoner))
            BalanceMana = int(mana) - cardmana
        
            teamtoplay = {}
            teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner]

            if len(teamtoplay) > 0:

                for battle in teamtoplay:
                    tank = [str(card['id']) for card in mycards if card['id'] == battle['monster_1_id']]
                    if not tank:
                        continue
                    else:
                        tank = list(set(tank))
                        tank = int(''.join(tank))
                        Besttank.append(tank)

                if len(Besttank) > 0:
                    viable = True
                    mostusetank = mode(Besttank)
                    team['monster_1_id'] = mostusetank
                    team['monster_1_level'] = 1
                    team['monster_1_abilities'] = monster_abilities(int(mostusetank))
                    team['monster_1_splinter'] = splinter(monster_color(int(mostusetank)))
                    frequency = Besttank.count(mostusetank)
                    ratio = round((frequency/len(Besttank)) * 100, 2)
                    team['monster_1_frequency'] = frequency
                    team['monster_1_ratio'] = str(ratio) + '%'
                    cardmana = monster_mana(int(mostusetank))
                    BalanceMana = BalanceMana - cardmana

                    teamtoplay = {}
                    teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner and battle['monster_1_id'] == mostusetank]

                    for x in range(2, 7):
                        
                        if battle['monster_'+str(x)+'_id'] != "":

                            Bestmonster = []

                            for battle in teamtoplay:
                                monster = [str(card['id']) for card in mycards if card['id'] == battle['monster_'+str(x)+'_id']]
                                if not monster:
                                    continue
                                else:
                                    monster = list(set(monster))
                                    monster = int(''.join(monster))
                                    Bestmonster.append(monster)

                            if len(Bestmonster) > 0:
                                mostusemonster = mode(Bestmonster)
                                frequency = Bestmonster.count(mostusemonster)
                                ratio = round((frequency/len(Bestmonster)) * 100, 2)
                                cardmana = monster_mana(int(mostusemonster))
                                
                                if BalanceMana > 0 and BalanceMana >= cardmana :
                                    if x == 2:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 3:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 4:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 5:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 6:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id'] or mostusemonster == team['monster_'+str(x-5)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                else:
                                    team['monster_'+str(x)+'_id'] = ""
                                    team['monster_'+str(x)+'_level'] = ""
                                    team['monster_'+str(x)+'_abilities'] = []
                                    team['monster_'+str(x)+'_splinter'] = ""
                                    team['monster_'+str(x)+'_frequency'] = ""
                                    team['monster_'+str(x)+'_ratio'] = ""
                            else:
                                team['monster_'+str(x)+'_id'] = ""
                                team['monster_'+str(x)+'_level'] = ""
                                team['monster_'+str(x)+'_abilities'] = []
                                team['monster_'+str(x)+'_splinter'] = ""
                                team['monster_'+str(x)+'_frequency'] = ""
                                team['monster_'+str(x)+'_ratio'] = ""
                        else:
                            team['monster_'+str(x)+'_id'] = ""
                            team['monster_'+str(x)+'_level'] = ""
                            team['monster_'+str(x)+'_abilities'] = []
                            team['monster_'+str(x)+'_splinter'] = ""
                            team['monster_'+str(x)+'_frequency'] = ""
                            team['monster_'+str(x)+'_ratio'] = ""
                else:
                    viable = False
            else:
                viable = False
        if viable:
            possible_decks.append(team)

        if len(possible_decks) != 0:

            for battle in possible_decks:

                most_win_deck = {}

                most_win_deck['card'] = []         
                most_win_deck['card'].append('summoner')
                most_win_deck['id'] = []
                most_win_deck['id'].append(battle['summoner_id'])
                most_win_deck['name'] = []
                most_win_deck['name'].append(card_name(int(battle['summoner_id'])))
                most_win_deck['splinter'] = []
                most_win_deck['splinter'].append(splinter(monster_color(int(battle['summoner_id']))))
                most_win_deck['frequency'] = []
                most_win_deck['frequency'].append(battle['summoner_frequency'])
                most_win_deck['ratio'] = []
                most_win_deck['ratio'].append(battle['summoner_ratio'])

                for x in range(0, 6):
                    if battle['monster_'+str(x+1)+'_id'] != "" :
                        most_win_deck['card'].append('monster_'+str(x+1))
                        most_win_deck['id'].append(battle['monster_'+str(x+1)+'_id'])
                        most_win_deck['name'].append(card_name(int(battle['monster_'+str(x+1)+'_id'])))
                        most_win_deck['splinter'].append(splinter(monster_color(int(battle['monster_'+str(x+1)+'_id']))))
                        most_win_deck['frequency'].append(battle['monster_'+str(x+1)+'_frequency'])
                        most_win_deck['ratio'].append(battle['monster_'+str(x+1)+'_ratio'])

            df = pd.DataFrame(most_win_deck)
            data = df.to_html(classes='table table-bordered')
            return HttpResponse(data)
        else:
            data = "No " + splinterteam + " Team Available"
            return HttpResponse(data)

    def getteamblue(request):

        mana = request.GET.get("mana")
        if mana == "ALL":
            mana = 99
        rule1 = request.GET.get("rule1")
        rule2 = request.GET.get("rule2")
        splinterteam = 'Water'

        with open("mycards.json") as file:
            mycards = json.load(file)
        file.close

        def filter_deck(battle):
            if mana == "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and  battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False

        db_decks = list(filter(filter_deck, BATTLEBASE))

        possible_decks = []

        viable = False
        team = {}
        Bestsummoner = []
        Bestmonster = []
        Besttank = []

        for battle in db_decks:
            summoner = [str(card['id']) for card in mycards if card['id'] == battle['summoner_id']]
            if not summoner:
                continue
            else:
                summoner = list(set(summoner))
                summoner = int(''.join(summoner))
                Bestsummoner.append(summoner)

        # checks if player has card with battle summoner card_detail_id
        if len(Bestsummoner) == 0:
            viable = False
        else:
            mostusesummoner = mode(Bestsummoner)
            team['summoner_id'] = mostusesummoner
            team['summoner_level'] = 1
            team['summoner_splinter'] = splinter(monster_color(int(mostusesummoner)))
            frequency = Bestsummoner.count(mostusesummoner)
            ratio = round((frequency/len(Bestsummoner)) * 100, 2)
            team['summoner_frequency'] = frequency
            team['summoner_ratio'] = str(ratio) + '%'
            cardmana = summoner_mana(int(mostusesummoner))
            BalanceMana = int(mana) - cardmana
        
            teamtoplay = {}
            teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner]

            if len(teamtoplay) > 0:

                for battle in teamtoplay:
                    tank = [str(card['id']) for card in mycards if card['id'] == battle['monster_1_id']]
                    if not tank:
                        continue
                    else:
                        tank = list(set(tank))
                        tank = int(''.join(tank))
                        Besttank.append(tank)

                if len(Besttank) > 0:
                    viable = True
                    mostusetank = mode(Besttank)
                    team['monster_1_id'] = mostusetank
                    team['monster_1_level'] = 1
                    team['monster_1_abilities'] = monster_abilities(int(mostusetank))
                    team['monster_1_splinter'] = splinter(monster_color(int(mostusetank)))
                    frequency = Besttank.count(mostusetank)
                    ratio = round((frequency/len(Besttank)) * 100, 2)
                    team['monster_1_frequency'] = frequency
                    team['monster_1_ratio'] = str(ratio) + '%'
                    cardmana = monster_mana(int(mostusetank))
                    BalanceMana = BalanceMana - cardmana

                    teamtoplay = {}
                    teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner and battle['monster_1_id'] == mostusetank]

                    for x in range(2, 7):
                        
                        if battle['monster_'+str(x)+'_id'] != "":

                            Bestmonster = []

                            for battle in teamtoplay:
                                monster = [str(card['id']) for card in mycards if card['id'] == battle['monster_'+str(x)+'_id']]
                                if not monster:
                                    continue
                                else:
                                    monster = list(set(monster))
                                    monster = int(''.join(monster))
                                    Bestmonster.append(monster)

                            if len(Bestmonster) > 0:
                                mostusemonster = mode(Bestmonster)
                                frequency = Bestmonster.count(mostusemonster)
                                ratio = round((frequency/len(Bestmonster)) * 100, 2)
                                cardmana = monster_mana(int(mostusemonster))
                                
                                if BalanceMana > 0 and BalanceMana >= cardmana :
                                    if x == 2:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 3:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 4:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 5:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 6:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id'] or mostusemonster == team['monster_'+str(x-5)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                else:
                                    team['monster_'+str(x)+'_id'] = ""
                                    team['monster_'+str(x)+'_level'] = ""
                                    team['monster_'+str(x)+'_abilities'] = []
                                    team['monster_'+str(x)+'_splinter'] = ""
                                    team['monster_'+str(x)+'_frequency'] = ""
                                    team['monster_'+str(x)+'_ratio'] = ""
                            else:
                                team['monster_'+str(x)+'_id'] = ""
                                team['monster_'+str(x)+'_level'] = ""
                                team['monster_'+str(x)+'_abilities'] = []
                                team['monster_'+str(x)+'_splinter'] = ""
                                team['monster_'+str(x)+'_frequency'] = ""
                                team['monster_'+str(x)+'_ratio'] = ""
                        else:
                            team['monster_'+str(x)+'_id'] = ""
                            team['monster_'+str(x)+'_level'] = ""
                            team['monster_'+str(x)+'_abilities'] = []
                            team['monster_'+str(x)+'_splinter'] = ""
                            team['monster_'+str(x)+'_frequency'] = ""
                            team['monster_'+str(x)+'_ratio'] = ""
                else:
                    viable = False
            else:
                viable = False
        if viable:
            possible_decks.append(team)

        if len(possible_decks) != 0:

            for battle in possible_decks:

                most_win_deck = {}

                most_win_deck['card'] = []         
                most_win_deck['card'].append('summoner')
                most_win_deck['id'] = []
                most_win_deck['id'].append(battle['summoner_id'])
                most_win_deck['name'] = []
                most_win_deck['name'].append(card_name(int(battle['summoner_id'])))
                most_win_deck['splinter'] = []
                most_win_deck['splinter'].append(splinter(monster_color(int(battle['summoner_id']))))
                most_win_deck['frequency'] = []
                most_win_deck['frequency'].append(battle['summoner_frequency'])
                most_win_deck['ratio'] = []
                most_win_deck['ratio'].append(battle['summoner_ratio'])

                for x in range(0, 6):
                    if battle['monster_'+str(x+1)+'_id'] != "" :
                        most_win_deck['card'].append('monster_'+str(x+1))
                        most_win_deck['id'].append(battle['monster_'+str(x+1)+'_id'])
                        most_win_deck['name'].append(card_name(int(battle['monster_'+str(x+1)+'_id'])))
                        most_win_deck['splinter'].append(splinter(monster_color(int(battle['monster_'+str(x+1)+'_id']))))
                        most_win_deck['frequency'].append(battle['monster_'+str(x+1)+'_frequency'])
                        most_win_deck['ratio'].append(battle['monster_'+str(x+1)+'_ratio'])

            df = pd.DataFrame(most_win_deck)
            data = df.to_html(classes='table table-bordered')
            return HttpResponse(data)
        else:
            data = "No " + splinterteam + " Team Available"
            return HttpResponse(data)

    def getteamred(request):

        mana = request.GET.get("mana")
        if mana == "ALL":
            mana = 99
        rule1 = request.GET.get("rule1")
        rule2 = request.GET.get("rule2")
        splinterteam = 'Fire'

        with open("mycards.json") as file:
            mycards = json.load(file)
        file.close

        def filter_deck(battle):
            if mana == "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and  battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False

        db_decks = list(filter(filter_deck, BATTLEBASE))

        possible_decks = []

        viable = False
        team = {}
        Bestsummoner = []
        Bestmonster = []
        Besttank = []

        for battle in db_decks:
            summoner = [str(card['id']) for card in mycards if card['id'] == battle['summoner_id']]
            if not summoner:
                continue
            else:
                summoner = list(set(summoner))
                summoner = int(''.join(summoner))
                Bestsummoner.append(summoner)

        # checks if player has card with battle summoner card_detail_id
        if len(Bestsummoner) == 0:
            viable = False
        else:
            mostusesummoner = mode(Bestsummoner)
            team['summoner_id'] = mostusesummoner
            team['summoner_level'] = 1
            team['summoner_splinter'] = splinter(monster_color(int(mostusesummoner)))
            frequency = Bestsummoner.count(mostusesummoner)
            ratio = round((frequency/len(Bestsummoner)) * 100, 2)
            team['summoner_frequency'] = frequency
            team['summoner_ratio'] = str(ratio) + '%'
            cardmana = summoner_mana(int(mostusesummoner))
            BalanceMana = int(mana) - cardmana
        
            teamtoplay = {}
            teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner]

            if len(teamtoplay) > 0:

                for battle in teamtoplay:
                    tank = [str(card['id']) for card in mycards if card['id'] == battle['monster_1_id']]
                    if not tank:
                        continue
                    else:
                        tank = list(set(tank))
                        tank = int(''.join(tank))
                        Besttank.append(tank)

                if len(Besttank) > 0:
                    viable = True
                    mostusetank = mode(Besttank)
                    team['monster_1_id'] = mostusetank
                    team['monster_1_level'] = 1
                    team['monster_1_abilities'] = monster_abilities(int(mostusetank))
                    team['monster_1_splinter'] = splinter(monster_color(int(mostusetank)))
                    frequency = Besttank.count(mostusetank)
                    ratio = round((frequency/len(Besttank)) * 100, 2)
                    team['monster_1_frequency'] = frequency
                    team['monster_1_ratio'] = str(ratio) + '%'
                    cardmana = monster_mana(int(mostusetank))
                    BalanceMana = BalanceMana - cardmana

                    teamtoplay = {}
                    teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner and battle['monster_1_id'] == mostusetank]

                    for x in range(2, 7):
                        
                        if battle['monster_'+str(x)+'_id'] != "":

                            Bestmonster = []

                            for battle in teamtoplay:
                                monster = [str(card['id']) for card in mycards if card['id'] == battle['monster_'+str(x)+'_id']]
                                if not monster:
                                    continue
                                else:
                                    monster = list(set(monster))
                                    monster = int(''.join(monster))
                                    Bestmonster.append(monster)

                            if len(Bestmonster) > 0:
                                mostusemonster = mode(Bestmonster)
                                frequency = Bestmonster.count(mostusemonster)
                                ratio = round((frequency/len(Bestmonster)) * 100, 2)
                                cardmana = monster_mana(int(mostusemonster))
                                
                                if BalanceMana > 0 and BalanceMana >= cardmana :
                                    if x == 2:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 3:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 4:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 5:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 6:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id'] or mostusemonster == team['monster_'+str(x-5)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                else:
                                    team['monster_'+str(x)+'_id'] = ""
                                    team['monster_'+str(x)+'_level'] = ""
                                    team['monster_'+str(x)+'_abilities'] = []
                                    team['monster_'+str(x)+'_splinter'] = ""
                                    team['monster_'+str(x)+'_frequency'] = ""
                                    team['monster_'+str(x)+'_ratio'] = ""
                            else:
                                team['monster_'+str(x)+'_id'] = ""
                                team['monster_'+str(x)+'_level'] = ""
                                team['monster_'+str(x)+'_abilities'] = []
                                team['monster_'+str(x)+'_splinter'] = ""
                                team['monster_'+str(x)+'_frequency'] = ""
                                team['monster_'+str(x)+'_ratio'] = ""
                        else:
                            team['monster_'+str(x)+'_id'] = ""
                            team['monster_'+str(x)+'_level'] = ""
                            team['monster_'+str(x)+'_abilities'] = []
                            team['monster_'+str(x)+'_splinter'] = ""
                            team['monster_'+str(x)+'_frequency'] = ""
                            team['monster_'+str(x)+'_ratio'] = ""
                else:
                    viable = False
            else:
                viable = False
        if viable:
            possible_decks.append(team)

        if len(possible_decks) != 0:

            for battle in possible_decks:

                most_win_deck = {}

                most_win_deck['card'] = []         
                most_win_deck['card'].append('summoner')
                most_win_deck['id'] = []
                most_win_deck['id'].append(battle['summoner_id'])
                most_win_deck['name'] = []
                most_win_deck['name'].append(card_name(int(battle['summoner_id'])))
                most_win_deck['splinter'] = []
                most_win_deck['splinter'].append(splinter(monster_color(int(battle['summoner_id']))))
                most_win_deck['frequency'] = []
                most_win_deck['frequency'].append(battle['summoner_frequency'])
                most_win_deck['ratio'] = []
                most_win_deck['ratio'].append(battle['summoner_ratio'])

                for x in range(0, 6):
                    if battle['monster_'+str(x+1)+'_id'] != "" :
                        most_win_deck['card'].append('monster_'+str(x+1))
                        most_win_deck['id'].append(battle['monster_'+str(x+1)+'_id'])
                        most_win_deck['name'].append(card_name(int(battle['monster_'+str(x+1)+'_id'])))
                        most_win_deck['splinter'].append(splinter(monster_color(int(battle['monster_'+str(x+1)+'_id']))))
                        most_win_deck['frequency'].append(battle['monster_'+str(x+1)+'_frequency'])
                        most_win_deck['ratio'].append(battle['monster_'+str(x+1)+'_ratio'])

            df = pd.DataFrame(most_win_deck)
            data = df.to_html(classes='table table-bordered')
            return HttpResponse(data)
        else:
            data = "No " + splinterteam + " Team Available"
            return HttpResponse(data)

    def getteamgreen(request):

        mana = request.GET.get("mana")
        if mana == "ALL":
            mana = 99
        rule1 = request.GET.get("rule1")
        rule2 = request.GET.get("rule2")
        splinterteam = 'Earth'

        with open("mycards.json") as file:
            mycards = json.load(file)
        file.close

        def filter_deck(battle):
            if mana == "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and  battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False

        db_decks = list(filter(filter_deck, BATTLEBASE))

        possible_decks = []

        viable = False
        team = {}
        Bestsummoner = []
        Bestmonster = []
        Besttank = []

        for battle in db_decks:
            summoner = [str(card['id']) for card in mycards if card['id'] == battle['summoner_id']]
            if not summoner:
                continue
            else:
                summoner = list(set(summoner))
                summoner = int(''.join(summoner))
                Bestsummoner.append(summoner)

        # checks if player has card with battle summoner card_detail_id
        if len(Bestsummoner) == 0:
            viable = False
        else:
            mostusesummoner = mode(Bestsummoner)
            team['summoner_id'] = mostusesummoner
            team['summoner_level'] = 1
            team['summoner_splinter'] = splinter(monster_color(int(mostusesummoner)))
            frequency = Bestsummoner.count(mostusesummoner)
            ratio = round((frequency/len(Bestsummoner)) * 100, 2)
            team['summoner_frequency'] = frequency
            team['summoner_ratio'] = str(ratio) + '%'
            cardmana = summoner_mana(int(mostusesummoner))
            BalanceMana = int(mana) - cardmana
        
            teamtoplay = {}
            teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner]

            if len(teamtoplay) > 0:

                for battle in teamtoplay:
                    tank = [str(card['id']) for card in mycards if card['id'] == battle['monster_1_id']]
                    if not tank:
                        continue
                    else:
                        tank = list(set(tank))
                        tank = int(''.join(tank))
                        Besttank.append(tank)

                if len(Besttank) > 0:
                    viable = True
                    mostusetank = mode(Besttank)
                    team['monster_1_id'] = mostusetank
                    team['monster_1_level'] = 1
                    team['monster_1_abilities'] = monster_abilities(int(mostusetank))
                    team['monster_1_splinter'] = splinter(monster_color(int(mostusetank)))
                    frequency = Besttank.count(mostusetank)
                    ratio = round((frequency/len(Besttank)) * 100, 2)
                    team['monster_1_frequency'] = frequency
                    team['monster_1_ratio'] = str(ratio) + '%'
                    cardmana = monster_mana(int(mostusetank))
                    BalanceMana = BalanceMana - cardmana

                    teamtoplay = {}
                    teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner and battle['monster_1_id'] == mostusetank]

                    for x in range(2, 7):
                        
                        if battle['monster_'+str(x)+'_id'] != "":

                            Bestmonster = []

                            for battle in teamtoplay:
                                monster = [str(card['id']) for card in mycards if card['id'] == battle['monster_'+str(x)+'_id']]
                                if not monster:
                                    continue
                                else:
                                    monster = list(set(monster))
                                    monster = int(''.join(monster))
                                    Bestmonster.append(monster)

                            if len(Bestmonster) > 0:
                                mostusemonster = mode(Bestmonster)
                                frequency = Bestmonster.count(mostusemonster)
                                ratio = round((frequency/len(Bestmonster)) * 100, 2)
                                cardmana = monster_mana(int(mostusemonster))
                                
                                if BalanceMana > 0 and BalanceMana >= cardmana :
                                    if x == 2:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 3:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 4:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 5:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 6:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id'] or mostusemonster == team['monster_'+str(x-5)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                else:
                                    team['monster_'+str(x)+'_id'] = ""
                                    team['monster_'+str(x)+'_level'] = ""
                                    team['monster_'+str(x)+'_abilities'] = []
                                    team['monster_'+str(x)+'_splinter'] = ""
                                    team['monster_'+str(x)+'_frequency'] = ""
                                    team['monster_'+str(x)+'_ratio'] = ""
                            else:
                                team['monster_'+str(x)+'_id'] = ""
                                team['monster_'+str(x)+'_level'] = ""
                                team['monster_'+str(x)+'_abilities'] = []
                                team['monster_'+str(x)+'_splinter'] = ""
                                team['monster_'+str(x)+'_frequency'] = ""
                                team['monster_'+str(x)+'_ratio'] = ""
                        else:
                            team['monster_'+str(x)+'_id'] = ""
                            team['monster_'+str(x)+'_level'] = ""
                            team['monster_'+str(x)+'_abilities'] = []
                            team['monster_'+str(x)+'_splinter'] = ""
                            team['monster_'+str(x)+'_frequency'] = ""
                            team['monster_'+str(x)+'_ratio'] = ""
                else:
                    viable = False
            else:
                viable = False
        if viable:
            possible_decks.append(team)

        if len(possible_decks) != 0:

            for battle in possible_decks:

                most_win_deck = {}

                most_win_deck['card'] = []         
                most_win_deck['card'].append('summoner')
                most_win_deck['id'] = []
                most_win_deck['id'].append(battle['summoner_id'])
                most_win_deck['name'] = []
                most_win_deck['name'].append(card_name(int(battle['summoner_id'])))
                most_win_deck['splinter'] = []
                most_win_deck['splinter'].append(splinter(monster_color(int(battle['summoner_id']))))
                most_win_deck['frequency'] = []
                most_win_deck['frequency'].append(battle['summoner_frequency'])
                most_win_deck['ratio'] = []
                most_win_deck['ratio'].append(battle['summoner_ratio'])

                for x in range(0, 6):
                    if battle['monster_'+str(x+1)+'_id'] != "" :
                        most_win_deck['card'].append('monster_'+str(x+1))
                        most_win_deck['id'].append(battle['monster_'+str(x+1)+'_id'])
                        most_win_deck['name'].append(card_name(int(battle['monster_'+str(x+1)+'_id'])))
                        most_win_deck['splinter'].append(splinter(monster_color(int(battle['monster_'+str(x+1)+'_id']))))
                        most_win_deck['frequency'].append(battle['monster_'+str(x+1)+'_frequency'])
                        most_win_deck['ratio'].append(battle['monster_'+str(x+1)+'_ratio'])

            df = pd.DataFrame(most_win_deck)
            data = df.to_html(classes='table table-bordered')
            return HttpResponse(data)
        else:
            data = "No " + splinterteam + " Team Available"
            return HttpResponse(data)

    def getteamgold(request):

        mana = request.GET.get("mana")
        if mana == "ALL":
            mana = 99
        rule1 = request.GET.get("rule1")
        rule2 = request.GET.get("rule2")
        splinterteam = 'Dragon'

        with open("mycards.json") as file:
            mycards = json.load(file)
        file.close

        def filter_deck(battle):
            if mana == "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 == "ALL" and rule2 == "None":
                if battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and  battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 == "None":
                if battle['ruleset'] == rule1 and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana == "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False
            elif mana != "ALL" and rule1 != "ALL" and rule2 != "None":
                rule = rule1+"|"+rule2
                if battle['ruleset'] == rule and battle['mana_cap'] == int(mana) and battle['summoner_splinter'] == splinterteam:
                    return True
                else:
                    return False

        db_decks = list(filter(filter_deck, BATTLEBASE))

        possible_decks = []

        viable = False
        team = {}
        Bestsummoner = []
        Bestmonster = []
        Besttank = []

        for battle in db_decks:
            summoner = [str(card['id']) for card in mycards if card['id'] == battle['summoner_id']]
            if not summoner:
                continue
            else:
                summoner = list(set(summoner))
                summoner = int(''.join(summoner))
                Bestsummoner.append(summoner)

        # checks if player has card with battle summoner card_detail_id
        if len(Bestsummoner) == 0:
            viable = False
        else:
            mostusesummoner = mode(Bestsummoner)
            team['summoner_id'] = mostusesummoner
            team['summoner_level'] = 1
            team['summoner_splinter'] = splinter(monster_color(int(mostusesummoner)))
            frequency = Bestsummoner.count(mostusesummoner)
            ratio = round((frequency/len(Bestsummoner)) * 100, 2)
            team['summoner_frequency'] = frequency
            team['summoner_ratio'] = str(ratio) + '%'
            cardmana = summoner_mana(int(mostusesummoner))
            BalanceMana = int(mana) - cardmana
        
            teamtoplay = {}
            teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner]

            if len(teamtoplay) > 0:

                for battle in teamtoplay:
                    tank = [str(card['id']) for card in mycards if card['id'] == battle['monster_1_id']]
                    if not tank:
                        continue
                    else:
                        tank = list(set(tank))
                        tank = int(''.join(tank))
                        Besttank.append(tank)

                if len(Besttank) > 0:
                    viable = True
                    mostusetank = mode(Besttank)
                    team['monster_1_id'] = mostusetank
                    team['monster_1_level'] = 1
                    team['monster_1_abilities'] = monster_abilities(int(mostusetank))
                    team['monster_1_splinter'] = splinter(monster_color(int(mostusetank)))
                    frequency = Besttank.count(mostusetank)
                    ratio = round((frequency/len(Besttank)) * 100, 2)
                    team['monster_1_frequency'] = frequency
                    team['monster_1_ratio'] = str(ratio) + '%'
                    cardmana = monster_mana(int(mostusetank))
                    BalanceMana = BalanceMana - cardmana

                    teamtoplay = {}
                    teamtoplay = [battle for battle in db_decks if battle['summoner_id'] == mostusesummoner and battle['monster_1_id'] == mostusetank]

                    for x in range(2, 7):
                        
                        if battle['monster_'+str(x)+'_id'] != "":

                            Bestmonster = []

                            for battle in teamtoplay:
                                monster = [str(card['id']) for card in mycards if card['id'] == battle['monster_'+str(x)+'_id']]
                                if not monster:
                                    continue
                                else:
                                    monster = list(set(monster))
                                    monster = int(''.join(monster))
                                    Bestmonster.append(monster)

                            if len(Bestmonster) > 0:
                                mostusemonster = mode(Bestmonster)
                                frequency = Bestmonster.count(mostusemonster)
                                ratio = round((frequency/len(Bestmonster)) * 100, 2)
                                cardmana = monster_mana(int(mostusemonster))
                                
                                if BalanceMana > 0 and BalanceMana >= cardmana :
                                    if x == 2:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 3:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 4:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 5:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                    if x == 6:
                                        if mostusemonster == team['monster_'+str(x-1)+'_id'] or mostusemonster == team['monster_'+str(x-2)+'_id'] or mostusemonster == team['monster_'+str(x-3)+'_id'] or mostusemonster == team['monster_'+str(x-4)+'_id'] or mostusemonster == team['monster_'+str(x-5)+'_id']:
                                            team['monster_'+str(x)+'_id'] = ""
                                            team['monster_'+str(x)+'_level'] = ""
                                            team['monster_'+str(x)+'_abilities'] = []
                                            team['monster_'+str(x)+'_splinter'] = ""
                                            team['monster_'+str(x)+'_frequency'] = ""
                                            team['monster_'+str(x)+'_ratio'] = ""
                                        else:
                                            if team['monster_'+str(x-1)+'_id'] == "":
                                                team['monster_'+str(x-1)+'_id'] = mostusemonster
                                                team['monster_'+str(x-1)+'_level'] = 1
                                                team['monster_'+str(x-1)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x-1)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x-1)+'_frequency'] = frequency
                                                team['monster_'+str(x-1)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                                team['monster_'+str(x)+'_id'] = ""
                                                team['monster_'+str(x)+'_level'] = ""
                                                team['monster_'+str(x)+'_abilities'] = []
                                                team['monster_'+str(x)+'_splinter'] = ""
                                                team['monster_'+str(x)+'_frequency'] = ""
                                                team['monster_'+str(x)+'_ratio'] = ""
                                            else:
                                                team['monster_'+str(x)+'_id'] = mostusemonster
                                                team['monster_'+str(x)+'_level'] = 1
                                                team['monster_'+str(x)+'_abilities'] =  monster_abilities(int(mostusemonster))
                                                team['monster_'+str(x)+'_splinter'] = splinter(monster_color(int(mostusemonster)))
                                                team['monster_'+str(x)+'_frequency'] = frequency
                                                team['monster_'+str(x)+'_ratio'] = str(ratio) + '%'
                                                BalanceMana = BalanceMana - cardmana
                                else:
                                    team['monster_'+str(x)+'_id'] = ""
                                    team['monster_'+str(x)+'_level'] = ""
                                    team['monster_'+str(x)+'_abilities'] = []
                                    team['monster_'+str(x)+'_splinter'] = ""
                                    team['monster_'+str(x)+'_frequency'] = ""
                                    team['monster_'+str(x)+'_ratio'] = ""
                            else:
                                team['monster_'+str(x)+'_id'] = ""
                                team['monster_'+str(x)+'_level'] = ""
                                team['monster_'+str(x)+'_abilities'] = []
                                team['monster_'+str(x)+'_splinter'] = ""
                                team['monster_'+str(x)+'_frequency'] = ""
                                team['monster_'+str(x)+'_ratio'] = ""
                        else:
                            team['monster_'+str(x)+'_id'] = ""
                            team['monster_'+str(x)+'_level'] = ""
                            team['monster_'+str(x)+'_abilities'] = []
                            team['monster_'+str(x)+'_splinter'] = ""
                            team['monster_'+str(x)+'_frequency'] = ""
                            team['monster_'+str(x)+'_ratio'] = ""
                else:
                    viable = False
            else:
                viable = False
        if viable:
            possible_decks.append(team)

        if len(possible_decks) != 0:

            for battle in possible_decks:

                most_win_deck = {}

                most_win_deck['card'] = []         
                most_win_deck['card'].append('summoner')
                most_win_deck['id'] = []
                most_win_deck['id'].append(battle['summoner_id'])
                most_win_deck['name'] = []
                most_win_deck['name'].append(card_name(int(battle['summoner_id'])))
                most_win_deck['splinter'] = []
                most_win_deck['splinter'].append(splinter(monster_color(int(battle['summoner_id']))))
                most_win_deck['frequency'] = []
                most_win_deck['frequency'].append(battle['summoner_frequency'])
                most_win_deck['ratio'] = []
                most_win_deck['ratio'].append(battle['summoner_ratio'])

                for x in range(0, 6):
                    if battle['monster_'+str(x+1)+'_id'] != "" :
                        most_win_deck['card'].append('monster_'+str(x+1))
                        most_win_deck['id'].append(battle['monster_'+str(x+1)+'_id'])
                        most_win_deck['name'].append(card_name(int(battle['monster_'+str(x+1)+'_id'])))
                        most_win_deck['splinter'].append(splinter(monster_color(int(battle['monster_'+str(x+1)+'_id']))))
                        most_win_deck['frequency'].append(battle['monster_'+str(x+1)+'_frequency'])
                        most_win_deck['ratio'].append(battle['monster_'+str(x+1)+'_ratio'])

            df = pd.DataFrame(most_win_deck)
            data = df.to_html(classes='table table-bordered')
            return HttpResponse(data)
        else:
            data = "No " + splinterteam + " Team Available"
            return HttpResponse(data)