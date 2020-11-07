import random

class Bill:
    def __init__(self,number,unit):
        self.__number=number 
        self.__unit=unit

    # 获取总价
    def GetPrice(self):
        lUnit=self.GetUnit()
        lNumber=self.GetNumber()
        lPrice=lUnit*lNumber
        if(self.TodayIsLoversDay()):
            return lPrice*0.77
        if(self.TodayIsMiddleAutumn() and lPrice>399):
            return lPrice-200
        if(self.TodayIsNationalDay() and lPrice<100):
            # 生成0~9的随机数，如果为0则免单。即：十分之一概率
            lFree=random.randint(0,9)
            if(lFree==0):
                return 0.0
        return lPrice

    # 获取数量
    def GetNumber(self):
        return self.__number
    
    # 获取单价
    def GetUnit(self):
        return self.__unit

    # 当天是否七夕节
    def TodayIsLoversDay(self):
        return False
    
    # 当天是否中秋节
    def TodayIsMiddleAutumn(self):
        return False

    # 当天是否国庆节
    def TodayIsNationalDay(self):
        return True

if __name__=='__main__':
    lBill=Bill(2,40)
    lPrice=lBill.GetPrice()
    print(lPrice)