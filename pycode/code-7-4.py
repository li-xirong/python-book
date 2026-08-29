import requests
from pathlib import Path

class StaticPageCrawler:
    """静态网页爬虫类"""
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    def crawl_and_save(self, url, output_path):
        """爬取网页并保存为HTML文件"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding  # 自动检测编码
            Path(output_path).write_text(response.text, encoding='utf-8')
            print(f"✓ 成功保存: {url} → {output_path}")
            return True
        except Exception as e:
            print(f"✗ 爬取失败: {url} - {str(e)}")
            return False
# 使用示例
if __name__ == "__main__":
    urls = [
        "https://gaokao.eol.cn/bei_jing/dongtai/202407/t20240720_2625168.shtml",
        "https://gaokao.eol.cn/bei_jing/dongtai/202406/t20240625_2619192.shtml"
    ]
    crawler = StaticPageCrawler()
    for i, url in enumerate(urls, 1):
        crawler.crawl_and_save(url, f"gaokao_page_{i}.html")
