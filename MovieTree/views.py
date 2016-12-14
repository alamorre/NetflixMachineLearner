from django.shortcuts import render
from .models import Survey
from .models import Question

def index(request):
    Survey.objects.all().delete()
    return render(request, 'MovieTree/index.html')

def add_survey(request):
    if request.method == 'POST':
        question_pk = int(request.POST['current_question'])
        question_asked = int(request.POST['current_question'])
        answer_given = int(request.POST['answer_given'])
        Survey.objects.create(question_asked = question_asked, answer_given = answer_given)

        last_question = Question.objects.latest('pk')
        if (question_pk < last_question.pk):
            question_pk = int(request.POST['current_question']) + 1
            context = {'question': Question.objects.get(pk=question_pk)}
            return render(request, 'MovieTree/view_question.html', context)
        else:
            answer_vector = []
            keyword_vector = []
            for survey in Survey.objects.all():
                answer_vector.append(int(survey.answer_given))
                keyword_vector.append(Question.objects.get(pk=int(survey.question_asked)).question_keyword)

            # This method will find the 1 or 2 things in the array worth searching
            def findSearch(keyword_vector, answer_vector):
                import heapq
                res = heapq.nlargest(2, answer_vector)
                spotOne = answer_vector.index(res[0])
                spotTwo = answer_vector.index(res[1])
                if spotOne == spotTwo:
                    string = keyword_vector[spotOne]
                else:
                    string = keyword_vector[spotOne] + ' & ' + keyword_vector[spotTwo]
                return string

            # search google for the top 3 movies
            def getGoogleMovies(argv):
                import requests
                from lxml import etree
                import os
                keyword = argv
                keyword = keyword.replace(' ', '%20')
                # path
                COOKIE_FOLDER_PATH = './cookie'
                COOKIE_PATH = COOKIE_FOLDER_PATH + '/netflix.cookie'

                session = requests.Session()
                if not os.path.exists(COOKIE_FOLDER_PATH):
                    os.makedirs(COOKIE_FOLDER_PATH)

                searchurl = "https://play.google.com/store/search?q=" + keyword + "&c=movies&hl=en"

                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, sdch, br',
                    'Accept-Language': 'en-US',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Cookie': 'NID=91=W6mt-ED6UMyvUhIpbRuxfMILlKtmKW_asxBIZirwBuq3FaK8jrot-oJou8cK-VjXESLT3qmeOC8-pNBUCi56fST3jESU0-SWUb_5rwVjJrl2pVDeKdu0Di7UUWQ6qXgc; PLAY_PREFS=CssECAASxgQKAkNBEIHon-6HKxqHBBESExQV1AHVAacCxATjBeUF6AXXBtgG3gbfBpCVgQaRlYEGkpWBBpeVgQa3lYEGuJWBBryVgQa9lYEGwJWBBsGVgQbElYEG1JWBBtmVgQbylYEG-JWBBpuWgQadloEGnpaBBp-WgQagloEG7peBBoWYgQa-mIEGiZuBBq2bgQbLm4EGvJ2BBt2dgQbnnYEGkJ6BBqSggQbaoIEG4qKBBvOigQb8ooEGi6OBBpqkgQavpYEG6qWBBsamgQbUpoEG1aaBBtamgQb-poEGgKeBBoKngQaEp4EGhqeBBoingQaKp4EGo6iBBs6ogQbyqIEG9KiBBqOpgQa8rIEG1q-BBsGwgQaHsoEGibKBBquygQbWsoEGsbSBBta5gQbruoEGosCBBsDAgQbtwIEG8sCBBtbCgQbtw4EGjMWBBo_FgQbKxoEGy8aBBrHHgQb4x4EGrcmBBrDJgQaeyoEGqsqBBtjMgQbczIEG3c2BBobOgQahz4EGxc-BBsTSgQaq14EGy9mBBszZgQbU24EG8tuBBufegQbd5IEGl-WBBrDsgQb97YEG1_WBBrr7gQa7_4EGyf-BBtWDggawhIIGyISCBvuEgga5hoIGpoeCBqeHggazh4IG7IeCBu2HggbrjYIG-42CBpmOggbMkYIGlZiCBvyZggaZmoIGwZqCBveaggaMpIIGmvDiOyiL6J_uhys6JGQ2ZTVkMGNlLWIyZjQtNGFiZi04OWE2LWZkNWEzM2RhYjU5OEABSAA:S:ANO1ljK4shpA9Wc2fg; _gat=1; S=billing-ui-v3=AYixsbfqXlsSq2iVkwK790s_tzgfmAjN:billing-ui-v3-efe=AYixsbfqXlsSq2iVkwK790s_tzgfmAjN; _ga=GA1.3.1349128454.1479579007',
                    'origin': 'https://play.google.com',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
                }

                response = session.get(searchurl, headers=headers)
                # print(response.content)
                et = etree.HTML(response.content)
                movies = {}
                rows = et.xpath('//*[@id="body-content"]/div/div/div[1]/div/div')

                count = 0
                result = [];

                for row in rows:
                    category = row.xpath('./div/div/h2/a/text()')[0]
                    moviesOfCategory = row.xpath('./div/div/div')

                    for movie in moviesOfCategory:
                        imageurl = movie.xpath('./div/div[@class="cover"]/div/div/div/img/@src')[0]  # movie image
                        title = movie.xpath('./div/div[@class="details"]/a[@class="title"]/@title')[0]  # movie title
                        type = movie.xpath(
                            './div/div[@class="details"]/div[@class="subtitle-container"]/a/@title')  # movie type
                        if len(type) > 0:
                            type = type[0]
                        else:
                            type = ""
                        movies[title] = [imageurl, type, category]
                        if count >= 3:
                            return result
                        result.append([title, imageurl, type, category])
                        count += 1

            query_string = findSearch(keyword_vector, answer_vector)
            top_movies = getGoogleMovies(query_string)

            movie_first = top_movies[0]
            movie_second = top_movies[1]
            movie_third = top_movies[2]

            context = { 'movie_first_title' : movie_first[0],
                        'movie_first_image': movie_first[1],
                        'movie_second_title' : movie_second[0],
                        'movie_second_image' : movie_second[1],
                        'movie_third_title' : movie_third[0],
                        'movie_third_image': movie_third[1],
                        }

            return render(request, 'MovieTree/give_recommendation.html', context)

def view_question(request):
    if request.method == 'GET':
        question_pk = 1
        context = { 'question' : Question.objects.get(pk=question_pk) }
        return render(request, 'MovieTree/view_question.html', context)

def view_database(request):
    survey_list = Survey.objects.all()
    question_list = Question.objects.all()
    context = { 'survey_list': survey_list,
                'question_list': question_list
               }
    return render(request, 'MovieTree/view_database.html', context)

def recorder(request):
    return render(request, 'MovieTree/recorder.html')

def recorderWorker(request):
    return render(request, 'MovieTree/recorderWorker.js')