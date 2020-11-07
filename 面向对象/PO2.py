class Bill:
    def __init__(self,number,unit):
        self.__number=number 
        self.__unit=unit

    # 获取总价
    def GetPrice(self):
        lUnit=self.GetUnit()
        lNumber=self.GetNumber()
        lPrice=lUnit*lNumber
        if(self.TodayIsLoversDay):
            return lPrice*0.77
        return lPrice

    # 获取数量
    def GetNumber(self):
        return self.__number
    
    # 获取单价
    def GetUnit(self):
        return self.__unit

    # 当天是否七夕节
    def TodayIsLoversDay(self):
        return true

if __name__=='__main__':
    lBill=Bill(100,2)
    print(lBill.GetPrice())