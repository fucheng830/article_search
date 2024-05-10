import requests
from urllib.parse import unquote
import time
from lxml import etree
import logging
import html2text

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def construct_time_params():
    current_millis = int(round(time.time() * 1000))
    params = {
        'sut': str(current_millis - 1000),   # 假设 sut 是当前时间戳减去 1 秒
        'sst0': str(current_millis),         # 假设 sst0 是当前的时间戳
        'lkt': f'1,{current_millis - 2000},{current_millis - 2000}'  # 假设 lkt 包含了三个用逗号分隔的时间戳，这里使用的是当前时间戳减去 2 秒
    }
    return params


class Sougou(object):
    query_url = None
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                             'Accept-Language': 'zh-CN,zh;q=0.9'})

    @staticmethod
    def run(query: str):
        url = "https://weixin.sogou.com/weixin"
        params = {
            'ie': 'utf8', # 编码
            's_from': 'input', # 来源
            '_sug_': 'y', # 是否有建议
            '_sug_type_': '', # 建议类型
            'type': '2', # 类型
            'query': unquote(query), # 查询
            'w': '01019900', # 未知
            'sut': '1458', # 未知 
            'sst0': '1707451960048', # 未知
            'lkt': '1,1707451959940,1707451959940' # 未知
        }
        time_params = construct_time_params()
        params.update(time_params)
        logging.debug(params)
        Sougou.session.headers.update = {
        'Referer': 'https://weixin.sogou.com/',
        }
        response = Sougou.session.get(url, params=params)
        Sougou.query_url = response.url 
        xpath = "//div[@class='news-box']//li"
        # 提取数据
        item_datas = []
        if response.status_code == 200:
            print(response.content)
            html_content = etree.HTML(response.content)
            items = html_content.xpath(xpath)
            for item in items:
                title = item.xpath(".//h3/a/text()")
                summary = item.xpath(".//p[@class='txt-info']/text()")
                url = item.xpath(".//h3/a/@href")
                new_url = Sougou.read_link('https://weixin.sogou.com{}'.format(url[0]))
                item_datas.append({title[0]: title, summary[0]: summary, url[0]: new_url})
            return item_datas
        else:
            logging.debug(response.status_code)
            raise Exception("Failed to fetch data")    
                

    @staticmethod
    def read_link(url: str):
        Sougou.session.headers.update = {
        'Referer': Sougou.query_url,
        }
        response = Sougou.session.get(url)
        logging.debug(response.request.headers)
        # 检查是否发生了重定向
        if response.history:
            logging.debug("Request was redirected")
            for resp in response.history:
                logging.debug("Redirected from", resp.url)

        if response.status_code == 200:
            redirect_url = Sougou.parse_and_construct_url(response.content)
            #Sougou.get_article_detail(redirect_url, url)
            return redirect_url
        else:
            logging.debug(response.status_code)

    
    def parse_and_construct_url(byte_content):
        # 将字节内容转换为字符串
        content = byte_content.decode('utf-8')

        # 初始化 URL 的各部分
        url_parts = []

        # 寻找 'url += ' 字符串并提取后面的部分
        start_phrase = "url += '"
        end_phrase = "';"
        start = 0
        while True:
            start_index = content.find(start_phrase, start)
            if start_index == -1:
                break
            start_index += len(start_phrase)
            
            end_index = content.find(end_phrase, start_index)
            if end_index == -1:
                break
            
            # 提取 URL 部分并添加到列表中
            url_parts.append(content[start_index:end_index])
            start = end_index

        # 合并 URL 部分
        constructed_url = ''.join(url_parts)
        
        # 移除可能存在的 '@' 字符
        constructed_url = constructed_url.replace("@", "")
        
        return constructed_url
    

    def get_article_detail(url: str, origin_url: str):
        Sougou.session.headers.update = {
        'Referer': origin_url,
        }
        logging.debug(url)
        response = Sougou.session.get(url)
        if response.status_code == 200:
            html = etree.HTML(response.content)
            title = html.xpath('//meta[@property="og:title"]/@content')
            head_img = html.xpath('//meta[@property="og:image"]/@content')
            description = html.xpath('//meta[@property="og:description"]/@content')
            content = html.xpath('//div[@id="js_content"]')

            text_maker = html2text.HTML2Text()
            return {
                'title': title[0] if title else None,
                'head_img': head_img[0] if head_img else None,
                'description': description[0] if description else None,
                'content': text_maker.handle(etree.tostring(content[0], pretty_print=True).decode()) if content else None
            }

    
if __name__ == "__main__":
    Sougou.run("https://weixin.sogou.com/weixin", "老年人每天需要多少小时的睡眠？")
    