# -*- coding:utf-8 -*-
from spider.driver.generic.consts import GenericSpiderName
from spider.driver.travel.core.traveldriver import TravelSpiderName
import sys
from spider.driver.base.driver import Driver

if __name__ == '__main__':
    if sys.argv[2] == GenericSpiderName.WEIXIN_PUBLIC:
        from spider.driver.generic.weixinspider import WeixinSpider
        spider = WeixinSpider(isheadless=False, ismobile=False, isvirtualdisplay=False,
                              spider_id=sys.argv[1],
                              name=sys.argv[2])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.XIECHENG_SPOT:
        from spider.driver.travel.xiechengspotspider import XiechengSpotSpider
        spider = XiechengSpotSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2] + sys.argv[4] == TravelSpiderName.LVMAMA_SPOT:
        from spider.driver.travel.lvmamaspotspider import LvmamaSpotSpider

        spider = LvmamaSpotSpider(isheadless=False, ismobile=False, isvirtualdisplay=False,
                                  spider_id=sys.argv[1],
                                  data_website=sys.argv[2],
                                  data_region=sys.argv[3],
                                  data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2] + sys.argv[4] == TravelSpiderName.QUNAR_SPOT:
        from spider.driver.travel.qunarspotspider import QunarSpotSpider

        spider = QunarSpotSpider(isheadless=False, ismobile=False, isvirtualdisplay=False,
                                  spider_id=sys.argv[1],
                                  data_website=sys.argv[2],
                                  data_region=sys.argv[3],
                                  data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.XIECHENG_HOTEL:
        from spider.driver.travel.xiechenghotelspider import XiechengHotelSpider
        spider = XiechengHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.QUNAR_HOTEL:
        from spider.driver.travel.qunarhotelspider import QunarHotelSpider
        spider = QunarHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.ELONG_HOTEL:
        from spider.driver.travel.elonghotelspider import ElongHotelSpider
        spider = ElongHotelSpider(isheadless=True,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.LVMAMA_HOTEL:
        from spider.driver.travel.lvmamahotelspider import LvmamaHotelSpider
        spider = LvmamaHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.MAFENGWO_HOTEL:
        from spider.driver.travel.mafengwohotelspider import MafengwoHotelSpider
        spider = MafengwoHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.FLIGGY_HOTEL:
        from spider.driver.travel.fliggyhotelspider import FliggyHotelSpider
        spider = FliggyHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.TUNIU_HOTEL:
        from spider.driver.travel.tuniuhotelspider import TuniuHotelSpider
        spider = TuniuHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()
    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_HOTEL:
        from spider.driver.travel.dianpinghotelspider import DianpingHotelSpider
        spider = DianpingHotelSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_FOOD:
        from spider.driver.travel.dianpingfoodspider import DianpingFoodSpider
        spider = DianpingFoodSpider(isheadless=False,ismobile=False,isvirtualdisplay=True,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_ENTERTAINMENT:
        from spider.driver.travel.dianpingentertainmentspider import DianpingEntertainmentSpider
        spider = DianpingEntertainmentSpider(isheadless=False,ismobile=False,isvirtualdisplay=False,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_SHOPPING:
        from spider.driver.travel.dianpingshoppingspider import DianpingShoppingSpider
        spider = DianpingShoppingSpider(isheadless=False,ismobile=False,isvirtualdisplay=True,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_HEALTH:
        from spider.driver.travel.dianpinghealthspider import DianpingHealthSpider
        spider = DianpingHealthSpider(isheadless=False,ismobile=False,isvirtualdisplay=True,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_CAR:
        from spider.driver.travel.dianpingcarspider import DianpingCarSpider
        spider = DianpingCarSpider(isheadless=False,ismobile=False,isvirtualdisplay=True,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

    elif sys.argv[2]+sys.argv[4] == TravelSpiderName.DIANPING_SPOT:
        from spider.driver.travel.dianpingspotspider import DianpingSpotSpider
        spider = DianpingSpotSpider(isheadless=False,ismobile=False,isvirtualdisplay=True,isproxy=True,initial_proxy_ip=Driver.get_curr_ip(),
                                    spider_id=sys.argv[1],
                                    data_website=sys.argv[2],
                                    data_region=sys.argv[3],
                                    data_source=sys.argv[4])
        spider.run_spider()

