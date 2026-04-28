
class AuctionSystem:
    def __init__(self):
        self.users = {}
        self.items = {}
    
    #ユーザー情報をUserに登録{id:name}
    def add_user(self,cmd):
        if cmd[1] in self.users:
            return "ERR_USER_EXISTS"
        
        self.users[cmd[1]] = cmd[2]
            
        return "SUCCESS"
    
    #商品情報をitemに登録{id:Itemクラス}
    def add_Item(self,cmd):
        if cmd[1] in self.items:
            return "ERR_ITEM_EXISTS"

        if cmd[4] not in self.users:
            return "ERR_USER_NOT_FOUND"

        try:
            price = int(cmd[3])
        except:
            return "ValueError"
        
        
        item = Item(cmd[2],price,cmd[4])
        self.items[cmd[1]] = item
        
        return "SUCCESS"
        
    #入札情報を踏まえてitem情報を変更
    def bid_Item(self,cmd):
        
        #エラー処理
        if cmd[1] not in self.items:
            return "ERR_ITEM_NOT_FOUND"
        else:
            items = self.items[cmd[1]]
        
        if cmd[2] not in self.users:
            return "ERR_USER_NOT_FOUND"
        
        if items.item_status == "ENDED":
            return "ERR_AUCTION_ENDED"
        
        if items.Seller == cmd[2]:
            return "ERR_OWN_ITEM"
        
        try:
            price = int(cmd[3])
        except:
            return "ValueError"
        
        if price <= items.bid_price or price <= items.initial_price:
            return "ERR_LOW_PRICE"
        else:
            items.bid_price = price
            items.bidder = cmd[2]
            
            return "SUCCESS"
        
    #商品のオークションを終了 (ItemのstatusをENDEDに変更)  
    def end_Item(self,cmd):
        
        if cmd[1] not in self.items:
            return "ERR_ITEM_NOT_FOUND"
        else:
            items =self.items[cmd[1]]
        
        if items.item_status == "ENDED":
            return "ERR_AUCTION_ENDED"
        else:
            items.set_endstatus()
            
            return "SUCCESS"     
            
    def result(self,cmd):
        
        if cmd[1] not in self.items:
            return "ERR_ITEM_NOT_FOUND"
        else:
            items = self.items[cmd[1]]
            
        if items.bid_price ==0:
            value_result = items.initial_price
        else:
            value_result = items.bid_price
            
        if items.bidder is None:
            bidder_result = "NONE"
        else :
            bidder_result = items.bidder
            
        return f"RESULT {cmd[1]} {items.name} {items.item_status} {bidder_result} {value_result}"




class Item:
    def __init__(self,name,value,SellerID):
        self.name = name
        self.initial_price = value
        self.Seller = SellerID
        self.bidder =None
        self.bid_price=0
        self.item_status = "ACTIVE"
    
    def get_bid_price(self):
        return self.bid_price
    
    def get_SellerID(self):
        return self.Seller
    
    def get_name(self):
        return self.name
    
    def set_endstatus(self):
        self.item_status = "ENDED"


N=int(input())

system = AuctionSystem()

for i in range(N):
    cmd = list(map(str,input().split()))
    
    try:
        if cmd[0] == "ADD_USER":
            result = system.add_user(cmd)
        elif cmd[0] == "ADD_ITEM":
            result = system.add_Item(cmd)
        elif cmd[0] == "BID":
            result = system.bid_Item(cmd)
        elif cmd[0] == "END_ITEM":
            result = system.end_Item(cmd)
        elif cmd[0] == "PRINT_RESULT":
            result = system.result(cmd)
        else:
            result = "CMD_ERROR"
            
    except IndexError:
        # 配列の要素外アクセス（単語数不足）が起きたらここでキャッチ！
        result = "ERR_MISSING_ARGUMENT"
    except Exception as e:
        # その他、想定外のシステムエラーが起きた場合の最終防衛線
        result = "ERR_SYSTEM_ERROR"
        
    print(result)