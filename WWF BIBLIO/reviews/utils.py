def average_rating(rating_list): # Boky page 142 dev web Dango
    if not rating_list:
        return 0
    return round(sum(rating_list) / len(rating_list)) # fonction d'arrondissement round(5.67 , 1) = 5.8