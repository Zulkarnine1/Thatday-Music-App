def card_processor(cards,uid):
    res = []
    for card in cards:
        if (uid!=None):
            liked = uid in [user.id for user in card.users_liked]
        else:
            liked = False

        card = card.__dict__
        if(card["likes"]==0):
            card["likes"] = ""
        elif(card["likes"]>999):
            card["likes"] = str(card["likes"]/1000)+"k"

        card["liked"] = liked
        res.append(card)

    return res