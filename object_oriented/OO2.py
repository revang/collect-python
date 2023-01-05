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
    #构造函数，调用父类的构造函数初始化属性值
    def __init__(self,number,unit):
        super().__init__(number,unit)

    def Discount(self,pPrice):
        return pPrice*0.77

if __name__=='__main__':
    lBill=LoversDayBill(100,2)
    print(lBill.GetPrice())