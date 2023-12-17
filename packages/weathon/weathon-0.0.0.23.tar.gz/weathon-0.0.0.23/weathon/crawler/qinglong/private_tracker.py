# -- coding: utf-8 --
# @Time    : 2022/10/7 23:28
import requests
from lxml import etree

requests.packages.urllib3.disable_warnings()


class PtSign:

    def __init__(self):
       
        self.session = requests.Session()
        self.sites:list[dict[str,str]] = [
                                            {
                                                'website': 'hdfans',
                                                'signin_url': 'https://hdfans.org/attendance.php',
                                                'cookie': "c_secure_uid=NDY4NjQ%3D; c_secure_pass=5c912ce277ba25e9c850ba1831aa3022; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=eWVhaA%3D%3D; c_secure_login=bm9wZQ%3D%3D"
                                            },]


    def signin(self,cookie, signin_url) -> str:
        headers:dict[str, str] = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        
        response = self.session.get(signin_url, headers=headers)
        html = etree.HTML(response.text)
        signin_msg = html.xpath('//td[@class="embedded"]/h2/text()|//td[@class="embedded"]//p//text()|//*[@class="embedded"]//*[@class="text"]//text()')
        signin_msg = signin_msg[0] + ',' + ''.join(signin_msg[1:]) + '\n'
        try:
            msg1 = ''.join(html.xpath('//*[@id="outer"]//a/font/text()|//*[@id="outer"]//a/font/span/text()'))
            if '未' in msg1:
                signin_msg += msg1
        except Exception as e:
            print(e)
            pass
        
        return signin_msg

    def signin_all(self):
        for site in self.sites:
            print(site["website"] + '->' + self.signin(cookie=site["cookie"], signin_url=site["signin_url"]))


if __name__ == '__main__':
    pt_sign = PtSign()
    pt_sign.signin_all()
