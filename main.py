'''
Main file
'''

from downloader import Downloader

settings = {
    # Manga urls, should be the same website
    'manga_url': [
        'https://member.bookwalker.jp/app/03/webstore/cooperation?r=BROWSER_VIEWER/63a3e70d-f172-4e8f-ba7a-f2f961f99671/https%3A%2F%2Fbookwalker.jp%2Fde63a3e70d-f172-4e8f-ba7a-f2f961f99671%2F',
        'https://member.bookwalker.jp/app/03/webstore/cooperation?r=BROWSER_VIEWER/63a3e70d-f172-4e8f-ba7a-f2f961f99671/https%3A%2F%2Fbookwalker.jp%2Fde63a3e70d-f172-4e8f-ba7a-f2f961f99671%2F',
    ],
    # Your cookies
    'cookies': 'bweternity=2lkcyytr2ask0gs084ok00ww0g0ccskwkc8ccoooko8w0cgc; myService=1; OptanonAlertBoxClosed=2025-05-07T10:00:50.478Z; _ga=GA1.1.1128470579.1746612048; _yjsu_yjad=1746612051.29cd650d-050a-4c0d-9f22-5fddca4468e7; myStore=0; top_personalize_shelf=-2; showSlider=0; _gcl_au=1.1.180397357.1746612050.1807255146.1747347297.1747347296; cm_kp_login_account=mail; bwmember=U2FsdGVkX19oZW5seUJLV%2FwRDVona17%2B2Lr0m5ilE0c%3D; invite_code=rFAgNxR5; _ga_0GLYZDG2J2=GS2.1.s1747347294$o2$g1$t1747347370$j0$l0$h0; JSESSIONID=lmd9ZiLtaO+JonwLx7n64g__; lbwsid=07809775f33fdc28aba81cf5fa237202def68dcc5350016cfa02680eb56344c4; bwsess=017jtu1qfsoo4nrpftdkpvmgdi; cm_kp_lan=ja; _ga_EPKMR4CGNW=GS2.1.s1747376472$o3$g1$t1747377291$j60$l0$h0; _ga_QM1GNDW25K=GS2.1.s1747376472$o3$g1$t1747377291$j0$l0$h0; OptanonConsent=isGpcEnabled=0&datestamp=Fri+May+16+2025+14%3A34%3A52+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202503.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4d825361-370b-4e97-baf0-3d8b6ae34866&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=1&geolocation=HK%3B&AwaitingReconsent=false; AWSALB=cSikZ4xmJPZS1YkARLDP9TUbQ1x2iv/WuuhTB/JMhsW7thKMfmwQy5LdLOQikJTvdAan7wHGljvYZZcl87pvmp7Zo37Q1pteZ8trs9uCZk9kR9KZVuYGWm/rC4bT; AWSALBCORS=cSikZ4xmJPZS1YkARLDP9TUbQ1x2iv/WuuhTB/JMhsW7thKMfmwQy5LdLOQikJTvdAan7wHGljvYZZcl87pvmp7Zo37Q1pteZ8trs9uCZk9kR9KZVuYGWm/rC4bT',
    # Folder names to store the Manga, the same order with manga_url
    'imgdir': [
        'G:\CESHI',
        'G:\CESHI'
    ],
    # Resolution, (Width, Height), For coma this doesn't matter.
    'res': (784, 1200),
    # Sleep time for each page (Second), normally no need to change.
    'sleep_time': 1,
    # Time wait for page loading (Second), if your network is good, you can reduce this parameter.
    'loading_wait_time': 20,
    # Cut image, (left, upper, right, lower) in pixel, None means do not cut the image. This often used to cut the edge.
    # Like (0, 0, 0, 3) means cut 3 pixel from bottom of the image.
    # or set dynamic to allow the scrypt to cut_images dynamictly (This work only correct if start_page is None)
    # this removed whitespace on the corners, initialised by the Cover.
    'cut_image': None,
    # File name prefix, if you want your file name like 'klk_v1_001.jpg', write 'klk_v1' here.
    'file_name_prefix': '',
    # File name digits count, if you want your file name like '001.jpg', write 3 here.
    'number_of_digits': 3,
    # Start page, if you want to download from 3 page, set this to 3, None means from 0
    'start_page': None,
    # End page, if you want to download until 10 page, set this to 10, None means until finished
    'end_page': None,
}

if __name__ == '__main__':
    downloader = Downloader(**settings)
    downloader.download()
