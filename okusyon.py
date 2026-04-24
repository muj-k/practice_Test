User = {} #ユーザーID,ユーザー名
item = {} #商品ID,商品状態

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


#ユーザー情報をUserに登録{id:name}
def Add_user(cmd):
    if cmd[1] in User:
        return print("ERR_USER_EXISTS")
    
    User[cmd[1]] = cmd[2]
        
    return print("SUCCESS")
    
#商品情報をitemに登録{id:Itemクラス}
def Add_Item(cmd):
    if cmd[1] in item:
        return print("ERR_ITEM_EXISTS")

    if cmd[4] not in User:
        return print("ERR_USER_NOT_FOUND")
    
    
    Items = Item(cmd[2],int(cmd[3]),cmd[4])
    item[cmd[1]] = Items
    
    return print("SUCCESS")


#入札情報を踏まえてitem情報を変更
def bid_Item(cmd):
    
    #エラー処理
    if cmd[1] not in item:
        return print("ERR_ITEM_NOT_FOUND")
    else:
        items = item[cmd[1]]
    
    if cmd[2] not in User:
        return print("ERR_USER_NOT_FOUND")
    
    if items.item_status == "ENDED":
        return print("ERR_AUCTION_ENDED")
    
    if items.Seller == cmd[2]:
        return print("ERR_OWN_ITEM")
    
    if int(cmd[3]) <= items.bid_price or int(cmd[3]) <= items.initial_price:
        return print("ERR_LOW_PRICE")
    else:
        items.bid_price = int(cmd[3])
        items.bidder = cmd[2]
        
        return print("SUCCESS")

#商品のオークションを終了 (ItemのstatusをENDEDに変更)  
def End_Item(cmd):
    
    if cmd[1] not in item:
        return print("ERR_ITEM_NOT_FOUND")
    else:
        items =item[cmd[1]]
    
    if items.item_status == "ENDED":
        return print("ERR_AUCTION_ENDED")
    else:
        items.set_endstatus()
        
        return print("SUCCESS")
    
def result(cmd):
    
    if cmd[1] not in item:
        return print("ERR_ITEM_NOT_FOUND")
    else:
        items = item[cmd[1]]
        
    if items.bid_price ==0:
        value_result = items.initial_price
    else:
        value_result = items.bid_price
        
    if items.bidder is None:
        bidder_result = "NONE"
    else :
        bidder_result = items.bidder
        
    return print(f"RESULT {cmd[1]} {items.name} {items.item_status} {bidder_result} {value_result}")

N=int(input())

for i in range(N):
    cmd = list(map(str,input().split()))
    
    if cmd[0] == "ADD_USER":
        Add_user(cmd)
    elif cmd[0] == "ADD_ITEM":
        Add_Item(cmd)
    elif cmd[0] == "BID":
        bid_Item(cmd)
    elif cmd[0] == "END_ITEM":
        End_Item(cmd)
    elif cmd[0] == "PRINT_RESULT":
        result(cmd)