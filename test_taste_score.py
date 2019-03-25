from pyquery import PyQuery as pq
str = '<span class="sml-rank-stars sml-str50 star"></span>'+ '<span class="score">' +  '<span class="item">口味：很好</span>' + '<span class="item">环境：非常好</span>' +  '<span class="item">服务：非常好</span>' + '<span class="item">人均：25元</span>' + '</span>'

html = pq(str)
##获取元素
if(html('span.score')):
    items = (html('span.item'));
    #获得字符串
    score =  items.eq(3).text();
    #返回分数
    print(score[3:len(score)]);
score = "25元"
if("元" in score):
    print(1);
