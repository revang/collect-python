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
        return self.Discount(lPrice)
    
    # 处理打折优惠
    def Discount(self,pPrice):
        return pPrice

    # 获取数量
    def GetNumber(self):
        return self.__number
    
    # 获取单价
    def GetUnit(self):
        return self.__unit

class LoversDayBill(Bill):
    def Discount(self,pPrice):
        return pPrice*0.77

class MiddleAutumnBill(Bill):
    def Discount(self,pPrice):
        if(pPrice>399):
            return pPrice-200
        return super().Discount(pPrice)

class NationalDayBill(Bill):
    def Discount(self,pPrice):
        if(pPrice<100):
            # 生成0~9的随机数，如果为0则免单。即：十分之一概率
            lFree=random.randint(0,9)
            if(lFree==0):
                return 0.0
        return super().Discount(pPrice)

if __name__=='__main__':
    lBill=LoversDayBill(100,2)
    print(lBill.GetPrice())

    lBill=MiddleAutumnBill(2,300)
    print(lBill.GetPrice())

    lBill=NationalDayBill(2,40)
    print(lBill.GetPrice())