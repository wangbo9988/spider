import requests
import re
from bs4 import BeautifulSoup
from pyecharts.charts import Bar
from pyecharts import options as opts

headers = {
    'Referer': 'https://www.qimai.cn/app/baseinfo',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

}

result = {}


def getPages(URL):
    response = requests.get(url=URL, headers=headers).text
    #   获取页面信息
    soup = BeautifulSoup(response, 'html.parser')  # 文档对象

    #   提取页面节点
    text = soup.find_all(name='div', attrs={'class': 'con0301'})
    #   输出节点的属性值
    for i in text:
        #   输出获奖情况
        description = i.find('h4').get_text().split('\xa0\xa0')
        href = description[0]  # 获奖详情页链接
        time = description[1]  # 获奖时间
        temp = re.sub("\D", " ", time)
        temp = temp.split(' ')
        year = int(temp[0])
        month = int(temp[1])
        #   打印结果
        res = '{}，时间：{}，相关链接——{}'.format(i.find_all('font')[0].get_text(), time, href)
        print(res)
        #   结果写入文件
        with open('data.txt', 'a') as f:
            f.write(res + '\n')
        if (year in result):
            if month in result[year]:
                #   该月份暂无记录
                result[year][month].append(res)
            else:
                #   该月份存在记录
                result[year][month] = [res]
        else:
            temp = {month: [res]}
            result[year] = temp
    href = soup.find_all(name='a', attrs={'class': 'pager'})
    if (href[1].get_text() == '下一页'):
        next_url = 'https://www.cust.edu.cn/cms/search/{0}'.format(href[1].get('href'))
        getPages(next_url)
    if (href[2].get_text() == '下一页'):
        next_url = 'https://www.cust.edu.cn/cms/search/{0}'.format(href[2].get('href'))
        getPages(next_url)


if __name__ == '__main__':
    url = 'https://www.cust.edu.cn/cms/search/searchResults.jsp?query=%E8%8E%B7%E5%A5%96&siteID=62&Submit=%E6%90%9C%E7%B4%A2'
    getPages(url)

    #   获取获奖年份，并对年份进行排序
    all_years = result.keys()
    all_years = list(all_years)
    all_years.sort(key=None, reverse=False)
    #   获取每年的获奖月份并进行排序
    # for year in all_years:

    #   生成图表
    bar = Bar()
    bar.add_xaxis(all_years)

    #   计算每年的获奖数量
    values = []
    for i in all_years:
        count = 0
        for temp in result[i]:
            count = count + len(result[i][temp])
        values.append(count)

    bar.add_yaxis("年份", values)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="各年获奖情况"))
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    bar.render("mycharts.html")
