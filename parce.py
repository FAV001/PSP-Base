import bs4
import requests
import shutil
import urllib3
import json
#Начинаем парсить страницу
i = 1
chunk_size = 10240
games = []
save_images = False
while True:
    url = 'http://advanscene.com/html/Releases/dbrelpsp.php?id=%s' % (str(i).zfill(4))
    session = requests.Session()
    main_page = session.get(url)
    main_soap = bs4.BeautifulSoup(main_page.text, "html.parser")
    game_number = main_soap('b')[0].text
    game_name = main_soap('b')[1].text
    pars_title = main_soap.select('.reltdd')
    pars_name = main_soap.select('.reltdv')
    y = 0
    game_region = ''
    game_language = ''
    game_genre = ''
    game_date = ''
    game_Filename = ''
    game_dirname = ''
    game_umdserial = ''
    game_isosize = ''
    game_isocrc32 = ''
    game_umdversion = ''
    game_pspversion = ''
    game_regionduplicates = ''
    for title in pars_title:
        if title.text == 'Region': game_region = pars_name[y].text
        if title.text == 'Language(s)': game_language = pars_name[y].text
        if title.text == 'Genre': game_genre = pars_name[y].text
        if title.text == 'Publishing Company': game_company = pars_name[y].text
        if title.text == 'Date': game_date = pars_name[y].text
        if title.text == 'Filename': game_Filename = pars_name[y].text
        if title.text == 'Dir Name': game_dirname = pars_name[y].text
        if title.text == 'UMD Serial': game_umdserial = pars_name[y].text
        if title.text == 'ISO Size': game_isosize = pars_name[y].text
        if title.text == 'ISO Crc32': game_isocrc32 = pars_name[y].text
        if title.text == 'UMD Version': game_umdversion = pars_name[y].text
        if title.text == 'PSP Version': game_pspversion = pars_name[y].text
        if title.text == 'Region Duplicate(s)': game_regionduplicates = pars_name[y].text
        if save_images:
            if title.text == 'Boxart Front Cover':
                if 'showpspfc.php' in str(pars_name[y]):
                    cover_front_url = 'http://advanscene.com/html/Releases/showpspfc.php?id=%s' % (str(i).zfill(4))
                    cover_front_page = requests.get(cover_front_url)
                    cover_front_soap = bs4.BeautifulSoup(cover_front_page.text, "html.parser")
                    im = cover_front_soap.select("div img")[1]
                    image_url = 'http://advanscene.com/html/Releases/' + im['src']
                    http = urllib3.PoolManager()
                    r = http.request('GET', image_url, preload_content=False)
                    path = r'Cover\Front\%s.%s' % (str(i).zfill(4), image_url[-3:])
                    with open(path, 'wb') as out:
                        while True:
                            data = r.read(chunk_size)
                            if not data:
                                break
                            out.write(data)
                        r.release_conn()
                pass
            if title.text == 'Boxart Back Cover':
                if 'showpspbc.php' in str(pars_name[y]):
                    cover_back_url = 'http://advanscene.com/html/Releases/showpspbc.php?id=%s' % (str(i).zfill(4))
                    cover_back_page = requests.get(cover_back_url)
                    cover_back_soap = bs4.BeautifulSoup(cover_back_page.text, "html.parser")
                    im = cover_back_soap.select("div img")[1]
                    image_url = 'http://advanscene.com/html/Releases/' + im['src']
                    http = urllib3.PoolManager()
                    r = http.request('GET', image_url, preload_content=False)
                    path = r'Cover\Back\%s.%s' % (str(i).zfill(4), image_url[-3:])
                    with open(path, 'wb') as out:
                        while True:
                            data = r.read(chunk_size)
                            if not data:
                                break
                            out.write(data)
                        r.release_conn()
                pass
            if title.text == 'Game Icon':
                icon_url = 'http://advanscene.com/html/Releases/impic.php?id=%s' % (str(i).zfill(4))
                http = urllib3.PoolManager()
                #icon = session.get(icon_url)
                r = http.request('GET', icon_url, preload_content=False, headers={'referer': url})
                path = r'Icon\%s.jpg' % (str(i).zfill(4))
                with open(path, 'wb') as out:
                    while True:
                        data = r.read(chunk_size)
                        if not data:
                            break
                        out.write(data)
                    r.release_conn()
                pass
        y += 1

    t = str(main_soap('a')[1].attrs.values())
    games.append({
        'name': game_name,
        'number': game_number,
        'region': game_region,
        'language': game_language,
        'genre': game_genre,
        'date': game_date,
        'Filename': game_Filename,
        'dirname': game_dirname,
        'umdserial': game_umdserial,
        'isosize': game_isosize,
        'isocrc32': game_isocrc32,
        'umdversion': game_umdversion,
        'pspversion': game_pspversion,
        'regionduplicates': game_regionduplicates
    })
    #startswith
    if (('dbrelpsp.php' in str(main_soap('a')[1].attrs.values())) and (i != 1)) or (('dbrelpsp.php' in str(main_soap('a')[0].attrs.values())) and (i == 1)):
        i += 1
    else:
        break
    pass
    print('Games - > %s' % i)
with open('games.json', 'w') as fp:
    json.dump(games, fp)
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
