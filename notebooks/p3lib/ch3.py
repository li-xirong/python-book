import os
import base64
import time, random, requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

"""将URL编码为安全的文件名"""
def url_to_filename(url):
    url_bytes = url.encode('utf-8')
    base64_bytes = base64.urlsafe_b64encode(url_bytes)
    filename = base64_bytes.decode('utf-8')
    filename = filename.rstrip('=') # 移除可能存在的填充字符（=） 
    return filename

"""将文件名解码回原始URL"""
def filename_to_url(filename):
    padding = 4 - (len(filename) % 4) # 填充字符（=）回填   
    if padding != 4:
        filename += '=' * padding
    base64_bytes = filename.encode('utf-8')
    url_bytes = base64.urlsafe_b64decode(base64_bytes)
    return url_bytes.decode('utf-8')

class PageDownloader:
    def __init__(self, save_dir="html_pages"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True) 
    def crawl(self, url):
        try:
            response = requests.get(url,  headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # 状态码异常处理
            return response
        except requests.exceptions.RequestException as e:
            print(f"[Error] 获取页面失败: {e}")
            return None
    def save(self, response, filename):
        try:
            if response.encoding.lower() == 'none': # 检测并设置正确的文本编码
                response.encoding = response.apparent_encoding
            with open(filename, 'w', encoding=response.encoding) as fw: # 保存内容
                fw.write(response.text)
            print(f"[Status] 已保存到 {filename}")
            return True
        except Exception as e:
            print(f"[Error] 保存页面失败: {e}")
            return False      
            
    def process(self, target_url):
        print(f"[Status] 开始抓取 {target_url}")
        response = self.crawl(target_url)
        if response and response.status_code == 200:
            filename = os.path.join(self.save_dir, url_to_filename(target_url) + '.html')
            self.save(response, filename)
        else:
            response = None
        message = "成功" if response else "失败"
        print(f"[Status] 页面抓取{message}")
        return response


class WebCrawler(PageDownloader):
    def __init__(self, trace_link=True, save_dir="html_pages"):
        super().__init__(save_dir)
        self.trace_link = trace_link
        self.task_queue = []
        self.url_cache = set() # 已访问URL集合，避免重复爬取

    def add(self, url):
        if url not in self.url_cache:
            self.task_queue.append(url)

    def addmany(self, urls):
        for url in urls:
            self.add(url)

    def fetch(self):
        print(f"[Status] 当前工作队列长度：{len(self.task_queue)}")
        if self.task_queue:
            return self.task_queue.pop(0)
        else:
            return None
        
    def parse(self, htmlstr, base_url):
        soup = BeautifulSoup(htmlstr, 'html.parser')
        new_links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].strip()
            if not href or href.startswith(('javascript:','mailto:','tel:')): # 跳过无效链接
                continue
            link = urljoin(base_url, href) # 规范化URL（转换为绝对路径并移除片段标识符）
            parsed = urlparse(link)
            if parsed.fragment:
                link = parsed._replace(fragment='').geturl()
            new_links.add(link)
        return list(new_links)

    def process(self, url):
        response = super().process(url)
        self.url_cache.add(url)
        if response and self.trace_link:
            new_seeds = self.parse(response.text, url)
            self.addmany(new_seeds)
        return response

    def run(self):
        url = self.fetch()
        while url:
            res = self.process(url)
            if len(self.url_cache) >= 10: # 抓了10个网页后就强制结束
                break
            sleep_time = random.uniform(1, 5)
            print(f"[Status] Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time) # 随机休眠，以免影响网站正常运行
            url = self.fetch()
        print(f"[Status] {self.__class__.__name__} stopped after {len(self.url_cache)} pages visited.")