import os
import string
import requests
from bs4 import BeautifulSoup
from lxml import html

base_url = 'https://magefan.com/blog?page={}'

page_number = 1
while page_number <= 23:

    # Send a GET request to the URL
    url = base_url.format(page_number)
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'lxml')
    blocks = soup.findAll('div' , {'class':'block-post'})
    block = soup.findAll('h3', {"class":"post-title"})
    # Find all the blocks in the page
    for block in blocks :
        # find the anchor tag within the blog post block
        headers = block.find('h3','post-title')
        folder_name =headers.text.strip() 
        valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
        folder_name = ''.join(c for c in folder_name if c in valid_chars)
        print(headers.text.strip())
        # get the background images from each div in the block 
        href_img=block.find('div','bg-img')
        img_url = href_img['data-original']
        print(img_url)
        # get the content of the image to save as png file 
        response = requests.get(img_url)
        img = response.content
        for header in headers :
        #get the link of each header    
            header_link = header.find('a')
            href = header.get("href")
            response = requests.get(href)
            content = response.text

        if href is not None:
            print(href)
        else:
            href = ''
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_name = os.path.join(folder_name, 'content.html')
        with open(file_name, 'w',encoding ='utf-8') as file:
                file.write(content)     
        img_name = os.path.join(folder_name,'image.png')  
        with open(img_name , 'wb')as f :
                f.write(img)       
    page_number = page_number + 1
    print(page_number)