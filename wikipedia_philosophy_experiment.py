import BeautifulSoup
import urllib2
import unicodedata
import string, re
import operator
import matplotlib.pyplot as plt
import math
import requests

from requests.exceptions import HTTPError

done = False


def start():
    while True:
        print ' '
        a('!NONE', ' ', 0, [])


def a(topic, orig_input, step_count, words_used):
    global done

    if topic == '!NONE':
        topic = raw_input('Please enter a topic: ')

    if step_count == 0:
        orig_input = topic.lower()
        orig_topic = topic
        topic = re.sub(r"\s+", '_', topic)
        topic = '/wiki/' + topic

    try:
        if step_count == 0:
            print 'Searching for https://en.wikipedia.org' + topic
        r = requests.get('https://en.wikipedia.org' + topic)
        r.raise_for_status()
    except HTTPError:
        if step_count == 0:
            topic = raw_input('Article does not exist. Check spelling or enter another topic: ')
        else:
            topic = raw_input('Cannot make next jump. Please try another topic: ')
        a(topic, ' ', 0, [])
        return
    else:
        if step_count == 0:
            print 'Successfully connected to https://en.wikipedia.org' + topic
            print ' '
            print 'Origin: ' + orig_topic
        response = urllib2.urlopen('https://en.wikipedia.org' + topic)

    html = response.read()
    soup = BeautifulSoup.BeautifulSoup(html)
    div = soup.find(id="mw-content-text")

    for all_p in div.findAll('p'):
        all_link = all_p.findAll('a')
        for link in all_link:
            link_href = link.get('href').lower()
            link_text = link.getText(separator=u' ')
            if link_href.startswith('/wiki/'):
                if not link_href.startswith('/wiki/help') and not link_href.startswith('/wiki/wikipedia:'):
                    step_count += 1
                    print 'Jump ' + str(step_count) + ': ' + link_text
                    for word in words_used:
                        if word == link_text:
                            print ' '
                            topic = raw_input('Looks like we hit a loop. Please try another topic: ')
                            a(topic, ' ', 0, [])
                            return
                    words_used.append(link_text)
                    if not link_href.startswith('/wiki/philosophy'):
                        a(link_href, orig_input, step_count, words_used)
                        if done:
                            return
                        else:
                            break
                    else:
                        print ' '
                        print orig_input + ' --> philosophy in ' + str(step_count) + ' steps'
                        done = True
                        return



