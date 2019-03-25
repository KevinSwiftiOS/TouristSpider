import re
from pyquery import PyQuery
# html = '<b><span class="hs-tQlR"></span><span class="hs-VYVW"></span><span class="hs-42CK"></span><span class="hs-61V1"></span></b>';
# temp = re.sub(r'(<span){1}', "&", html);
# res = "";
# for i,word in enumerate(temp):
#     if (word == '&'):
#         res += ('&');
#
#     if (word == '1' and  i -1 >= 0 and temp[i - 1] == '>'):
#         res += ('1');
#
# doc = PyQuery(html)
# spans = list(doc('span').items());
# # 进行匹配
# str = ""
# if (len(spans) == 0):
#     print(html)
#
# else:
#     for span in spans:
#         if (span.attr('class') == 'hs-4Enz'):
#             res = re.sub(r'&', '2', res, 1);
#         if (span.attr('class') == 'hs-GOYR'):
#             res = re.sub(r'&', '3', res, 1);
#         if (span.attr('class') == 'hs-61V1'):
#             res = re.sub(r'&', '4', res, 1);
#         if (span.attr('class') == 'hs-SzzZ'):
#             res = re.sub(r'&', '5', res, 1);
#         if (span.attr('class') == 'hs-VYVW'):
#             res = re.sub(r'&', '6', res, 1);
#         if (span.attr('class') == 'hs-tQlR'):
#             res = re.sub(r'&', '7', res, 1);
#         if (span.attr('class') == 'hs-LNui'):
#             res = re.sub(r'&', '8', res, 1);
#         if (span.attr('class') == 'hs-42CK'):
#             res = re.sub(r'&', '9', res, 1);
#         if (span.attr('class') == 'hs-OEEp'):
#             res = re.sub(r'&', '0', res, 1);
#     print (res);
# res = '阳光路'
# splits = res.split(' ')
# rr = '大'
# flag = 0
# for word in splits:
#     if word == rr:
#         flag = 1;
# if( flag == 0):
#     if(res == ''):
#         res += rr
#     else:
#         res += ' ' + rr
# print(res)
# for i in range(1,10):
#     print(i)
# import demjson
# text = 'window.shop_config={userId: 0, shopId: "80199012", shopCityId: 3602, shopName: "忆家食府", address: "千岛湖镇新安东路493号新万水酒店3楼", publicTransit: "", cityId: "3602", cityCnName: "千岛湖", cityName: "千岛湖", cityEnName: "qiandaohu", isOverseasCity: 0, fullName: "忆家食府", shopGlat: "29.609048991224768", shopGlng:"119.06043026098423", cityGlat:"29.60687", cityGlng:"119.07813", power:5, shopPower:35, voteTotal:0, district:0, shopType:10, mainRegionId:71354, mainCategoryName:"私房菜", categoryURLName:"food", shopGroupId: "80199012", categoryName: "美食", loadUserDomain:"//www.dianping.com", map:{ power:5, manaScore:"0" }, mainCategoryId:1338, defaultPic:"http://qcloud.dpfile.com/pc/Xh5j1jQ8T1n3bH8u4y0eUy2GxkG1dA_6u3nMLkvNSaayKMVJSEw_x5CADA8FrX9ObX9yED0ueaDWYCwyxfLcgw.jpg", textCssVersion:"8Ft4E436q3", shopEvtId:80199012}'
# text = re.sub(r'window.shop_config=',"",text);
# print(text);
# print(demjson.decode(text)['address'])
# def get_span_text(span):
#     print(span);
#     if (span.attr('class') == 'nze2c'):
#      return '2';
#     if (span.attr('class') == 'nz35m'):
#         return '3';
#     if (span.attr('class') == 'nzi6y'):
#         return '4';
#     if (span.attr('class') == 'nz1ad'):
#         return '5';
#     if (span.attr('class') == 'nz71g'):
#         return '6';
#     if (span.attr('class') == 'nzzr3'):
#         return '7';
#     if (span.attr('class') == 'nzcxe'):
#         return '8';
#     if (span.attr('class') == 'nzowk'):
#         return '9';
#     if (span.attr('class') == 'nzbus'):
#         return '0';
#
#
# def get_comment_num(html):
#     temp = re.sub(r'(<d){1}', "&", html);
#     res = "";
#     for i, word in enumerate(temp):
#         if (word == '&'):
#             res += ('&');
#
#         if (word == '1' and i - 1 >= 0 and temp[i - 1] == '>'):
#              res += ('1');
#
#
#     doc = PyQuery(html)
#     spans = list(doc('d').items());
#     # 进行匹配
#     str = ""
#     if (len(spans) == 0):
#         return (html)
#
#     else:
#         for span in spans:
#             res = re.sub(r'&', get_span_text(span), res, 1);
#
#         return (res);
# def get_shop_taste(html):
#     doc = PyQuery(html)
#     spans = list(doc('d').items());
#     # 进行匹配
#     res = ""
#     if (len(spans) == 0):
#         return (0)
#
#     else:
#         for span in spans:
#             res += get_span_text(span);
#         if(len(res) == 2):
#           return  res[0] + '.' + res[1]
#         if(len(res) == 1):
#             return res[0] + '.1'
# print(get_shop_taste('服务: <d class="nz71g"></d>.<d class="nzcxe"></d>'))
# html = '<div class="star-each star-size"><div class="star-off star-size"></div><div class="percent-on star0-percent" style="width: 100%"><div class="star-on' + 'star-size"></div></div></div>  <div class="star-each star-size"><div class="star-off star-size"></div><div class="percent-on star1-percent"' + 'style="width: 100%"><div class="star-on star-size"></div></div></div>  <div class="star-each star-size"><div class="star-off star-size"></div><div class="percent-on star2-percent" style="width: 100%"><div class="star-on star-size"></div></div></div>  <div class="star-each star-size"><div' +'class="star-off star-size"></div><div class="percent-on star3-percent" style="width: 100%"><div class="star-on star-size"></div></div></div>  <div' + 'class="star-each star-size"><div class="star-off star-size"></div><div class="percent-on star4-percent" style="width: 0%"><div class="star-on' + 'star-size"></div></div></div>'
# pq = PyQuery(html)
# cnt = 0;
#
# for i in range(0, 5):
#     percent_on = pq('.star' + str(i) + '-percent')
#     if (percent_on.attr('style') == 'width: 100%'):
#         cnt += 1;
# print(cnt);
# str = '2018年2月3日'
# if('年' in str):
#     year = str.split('年')[0];
#     month_and_day = str.split('年')[1];
#     print(year);
#     month = month_and_day.split('月')[0];
#     day = month_and_day.split('月')[1].split('日')[0];
#     month = month.zfill(2);
#     day = day.zfill(2);
#     print(month);
#     print(day);
str = '<span class="name" target="_blank" rel="nofollow" title="" href="/member/106418977" data-click-name="用户名1" data-click-title="文字">                                小鱼儿                                </span>                                <img class="user-rank-rst " src="https://p1.meituan.net/cippiccenter/a/squarelv4.png">	                                <span class="vip"></span>'
html = PyQuery(str)
print(html('span').filter('.name').text() == "");