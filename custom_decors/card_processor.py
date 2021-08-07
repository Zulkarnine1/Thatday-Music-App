def card_processor(cards,uid):
    res = []
    for card in cards:
        if (uid!=None):
            liked = uid in [user.id for user in card.users_liked]
        else:
            liked = False

        if (uid!=None):
            saved = uid in [user.id for user in card.users_saved]
        else:
            saved = False

        card = card.__dict__
        if(card["likes"]==0):
            card["likes"] = ""
        elif(card["likes"]>999):
            card["likes"] = str(card["likes"]/1000)+"k"

        card["liked"] = liked
        card["saved"] = saved
        res.append(card)

    return res