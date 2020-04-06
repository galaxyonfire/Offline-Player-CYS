import mechanicalsoup
import requests
import re
import hashlib
import os
import sys

STORY_LINK = ''

#######################################################
#
#   Above is the only link you need to replace.
#   Make sure the single quotes surround the link!
#
#   Below is the code -- feel free to take a look!
#
#######################################################

assert(STORY_LINK != '')

STORY = mechanicalsoup.StatefulBrowser()
STORY.open(STORY_LINK)

STORY_NAME = STORY.get_current_page().find(id='ctl09').string.strip()
STORY_VIEWER_LINK = 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=' + re.findall(re.compile('\?[0-9]+'), STORY.get_current_page().find(type='submit')['onclick'])[0][1:]

assert(STORY_NAME != '')
assert(STORY_VIEWER_LINK != '')

STORY.close()

ONLY_NUM = re.compile('\d+')
POSTBACK = re.compile('^P')
ILLEGAL_CHARS = re.compile(':|\?')
CSS_OBJECTS = ['/App_Themes/CYS/Styles.css', '/App_Themes/CYS/images/storyviewer_masthead_background.gif', '/App_Themes/CYS/images/storyviewer_masthead_logo.gif']

def bhash(browser):
    """
        browser: a StatefulBrowser
    
    Returns the hash of the browser
    based on story contents
    """
    return hashlib.sha1(browser.get_current_page().body.find(style="padding:0px 30px 50px 30px").div
                        .encode('utf-8')).hexdigest()[:10]

def pageTitle(browser):
    """
        browser: a StatefulBrowser

    Returns a unique title of a page
    """
    page = browser.get_current_page()
    title = page.find(id='_storyTitle').string
    title = title.replace(" ", "_")
    ftitle = re.sub(ILLEGAL_CHARS, '', title)
    return ftitle + bhash(browser)

def write(browser):
    """
        browser: a StatefulBrowser

    Writes the HTML data of the page to
    the corresponding .html file
    """
    name = pageTitle(browser) + ".html"
    with open("Story_Data/" + STORY_NAME + '/' + name, "w") as f:
        f.write(browser.get_current_page().prettify(formatter="html"))

def getChildren(browser):
    """
        browser: a StatefulBrowser
    
    Generates a list of child browsers, where each child follows one of the
    links/story options on the page of the parent browser.
    """
    children = []
    for link in browser.links(onclick=POSTBACK):
        if 'End Game and Leave Comments' == link.string:
            return []
        cp = mechanicalsoup.StatefulBrowser(session=browser.session)
        cp.open(STORY_VIEWER_LINK)
        cp.select_form('#pbForm')
        cp['pbAction'] = 'FollowLink'
        cp['pbValue'] = ONLY_NUM.findall(link['onclick'])[0]
        cp.submit_selected()
        children.append(cp)
    return children

def cleanup(browser, childTitles):
    """
        browser: a StatefulBrowser
        childTitles: a list of unique pageTitles for each Postback link in the browser
    
    Removes server-dependence of a page and switches links to local files
    Note that after cleanup you cannot call getChildren() successfully
    """
    links = browser.links()
    links[1]['href'] = START_NAME + '.html'
    links[2]['href'] = "javascript: if (confirm('Your current page is " + pageTitle(browser) + ".html')) window.close();"

    for index in range(4, len(links)):
        # this is wonky but will have to do -- no other way to get child names w/hahes
        if 'End Game and Leave Comments' == links[index].string:
            links[index]['href'] = 'http://chooseyourstory.com'
        else:
            fstring = childTitles[index-4]
            links[index]['href'] = fstring + ".html"
        del links[index]['onclick']

    browser.get_current_page().form.decompose()
    browser.get_current_page().script.decompose()
    browser.get_current_page().link['href'] = "../css/Styles.css"
    temp = str(browser.get_current_page().style.string)
    temp = temp.replace('/App_Themes/CYS/images/storyviewer_masthead_background.gif', '../css/storyviewer_masthead_background.gif')
    browser.get_current_page().style.string.replace_with(temp)
    browser.get_current_page().img['src'] = '../css/storyviewer_masthead_logo.gif'

def chartstory(start_browser):
    """
        start_browser: the StatefulBrowser of the 'first page' of the story
    
    Chart the story in a BFS inspired manner and
    clean/write each page to a HTML file
    """

    fringe = []
    fringe.append(start_browser)
    visited = set()
    visited.add(pageTitle(start_browser))
    
    while(True):
        if len(fringe) == 0:
            break
        
        node = fringe.pop(0)
        visited.add(pageTitle(node))
        
        childTitles = []
        for child in getChildren(node):
            childTitles.append(pageTitle(child))
            if pageTitle(child) not in visited:
                fringe.append(child)
            else:
                child.close()
        cleanup(node, childTitles)
        write(node)
        node.close()

if __name__ == '__main__':
    start_browser = mechanicalsoup.StatefulBrowser()
    start_browser.open(STORY_VIEWER_LINK)

    if 'Story_Data' not in os.listdir():
        os.mkdir('Story_Data')

    if 'css' not in os.listdir('Story_Data/'):
        os.mkdir('Story_Data/css')
        for obj in CSS_OBJECTS:
            url = 'http://chooseyourstory.com' + obj
            name = obj.split('/')[-1]
            r = requests.get(url)
            with open('Story_Data/css/' + name, 'wb') as f:
                f.write(r.content)

    if STORY_NAME not in os.listdir('Story_Data/'):
        os.mkdir('Story_Data/' + STORY_NAME)
    else:
        print("ALERT: " + STORY_NAME + " seems to already be downloaded, rerunning this script will overwrite current files")
        print("Proceed? ", end='')
        if input('[yes/no] ') != 'yes':
            sys.exit()

    START_NAME = pageTitle(start_browser)
    start_html = '<html><meta http-equiv="refresh" content="0; Story_Data/' + STORY_NAME + '/' + START_NAME + '.html' + '"><meta name="keywords" content="automatic redirection"></html>'

    with open('Play_' + STORY_NAME + '.html', 'w') as f:
        f.write(start_html)

    chartstory(start_browser)
