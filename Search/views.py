from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models

word = ""
def settings(request):
    """This function reads the TSV file, parse it and upload it to the MONGO DB"""
    file = open("word_search.tsv")
    array = []
    for f in file:
        temp = f.strip()
        array.append(temp.split('\t')) #Since TSV stands for Tab Seperated VALUES, we are seperating each data with respect to \t
    for data in array:
        obj = models.WordsData()
        obj.word = data[0]
        obj.word_rank = data[1]
        obj.save()
    return HttpResponse("<h3>TSV Data Successfully uploaded in the database</h3>")

def sorter(x):
    return len(x.word) #Key method to sort the array accordig to string length

def search(request):
    """This function processes the GET request search/?word= and returns a JSON array of 25 most relevent words """
    keyword = request.GET["word"]
    word = keyword
    data = models.WordsData.objects.filter(word__icontains=keyword).order_by("-word_rank")
    #The above ORM query selects data that matches  the keyword and orders it by word usage in descending order
    #The above ORM query confirms the first constrait, i.e., matches can occur anywhere in the string
    result = list(data)
    if len(result) > 25:
        max_length = 25
    else:
        max_length = len(result)
    """Since the data are in descending order in terms of usage and we require maximum of only 25 most common words, 
    we eliminate all words except the first 25 words"""
    temp_result = []
    checked = []
    i = 0
    while i < max_length:
        if keyword == result[i].word[0:len(keyword)]:
            """according to constraint given, matches at the start of the word should rank higher"""
            temp_result.append(result[i])
            checked.append(i)
        i += 1
    i = 0
    while i < max_length:
        if i in checked:
            i += 1
            continue
        else:
            temp_result.append(result[i])
            i += 1
    """The above code inserts all the words that matches  at the start in the list first"""
    final = sorted(temp_result, key=sorter)
    """The above code sorts the list according to the length of the word, 3rd constraint"""
    last = []
    for f in final:
        last.append(f.word)
    return JsonResponse({'context':last})