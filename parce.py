import bs4
import requests
#Начинаем парсить страницу
i = 3336
while True:
    url = 'http://advanscene.com/html/Releases/dbrelpsp.php?id=%s' % (i)
    main_page = requests.get(url)
    main_soap = bs4.BeautifulSoup(main_page.text, "html.parser")
    game_number = main_soap('b')[0].text
    game_name = main_soap('b')[1].text
    pars_title = main_soap.select('.reltdd')
    pars_name = main_soap.select('.reltdv')
    
    #startswith
    if 'dbrelpsp.php' in main_soap('a')[1].attrs.values():
        i += 1
    else:
        break
    pass

#ссылка на оновную страницу
#http://advanscene.com/html/Releases/dbrelpsp.php?id=0001
#ссылка на обложку фронт
#http://advanscene.com/html/Releases/showpspfc.php?id=0001
#ссылка на обложку back
#http://advanscene.com/html/Releases/showpspbc.php?id=0001
#
#<a href="dbrelpsp.php?id=0002">
#	<img style="float:right; margin-bottom: 5; border-width: 0px" src="../gfx/next.png">
#	</a>
#main_soap('a')[1]
#.findAll(attrs={"class" : ["jrreg", "urreg", "frreg", "grreg"]})
#title_number = main_soap.select('.jrreg .urreg')
#title_name = main_soap.findAll(attrs={"class" : ["jrereg", "urereg", "frereg", "grereg"]})
#title_name = main_soap.select('.jrereg')
print(url)
