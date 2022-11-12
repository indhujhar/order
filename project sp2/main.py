from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import Form,File
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from fastapi.encoders import jsonable_encoder



app = FastAPI()
templates = Jinja2Templates(directory="templates")
register = Jinja2Templates(directory="templates")
admin = Jinja2Templates(directory="templates")
delete= Jinja2Templates(directory="templates")


uri ="mongodb+srv://demo:Demo_123@cluster0.3pjyqsp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
ab = client.login
db = client.items



class User(BaseModel):
    username: str
    password: str   

class Detail(BaseModel):
    item_name:str
    price:int
    orderid:int

@app.get("/homePage", response_class=HTMLResponse) #http://127.0.0.1:8000/homePage
def show_service_page(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.get("/loginPage", response_class=HTMLResponse) #http://127.0.0.1:8000/loginPage
def show_service_page(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.get("/registerPage", response_class=HTMLResponse) #http://127.0.0.1:8000/registerPage
def show_register_page(request: Request):
    return register.TemplateResponse("home.html", context={"request": request})

@app.get("/deletePage", response_class=HTMLResponse) #http://127.0.0.1:8000/deletePage
def show_service_page(request: Request):
    return templates.TemplateResponse("delete.html", context={"request": request})  

@app.get("/updatePage", response_class=HTMLResponse) #http://127.0.0.1:8000/updatePage
def show_service_page(request: Request):
    return templates.TemplateResponse("update.html", context={"request": request})   
    
@app.get("/findPage", response_class=HTMLResponse) #http://127.0.0.1:8000/findPage
def show_service_page(request: Request):
    return templates.TemplateResponse("order.html", context={"request": request}) 

       




@app.post("/processlogin") #http://127.0.0.1:8000/processlogin
def check_user(request: Request,username:str= Form() , password:str= Form() ):

    user = ab["login"].find_one({"username": username})
    if username == user["username"] and password == user["password"]:

        return templates.TemplateResponse("orders.html", context={"request": request})
           
    else:
        return " failed"    


@app.post("/findAll", response_model=List[Detail])#http://127.0.0.1:8000/findAll
def get_user(request: Request):

    user = db["items"].find()
    l = list(user)
    return l



@app.post("/create")  #http://127.0.0.1:8000/create 
def create_user(response:Request, username: str=Form() , email: str=Form() ,DOB: str=Form(), password: str=Form() , confirmpassword: str=Form()):
    x = {"username":username,"email":email,"DOB":DOB,"password":password,"confirmpassword":confirmpassword}
    obj = db["items"].insert_one(x)
    return "Registered Successfully"
    
      

@app.post("/delete") #http://127.0.0.1:8000/delete
def delete_order(orderid: int = Form()):
    delete_order = db["items"].delete_one({"orderid": orderid})
    return f"{orderid} deleted successfully"  

@app.post("/update") #http://127.0.0.1:8000/update
def update_order(updated_user: Detail,itemname: str=Form() , price: int=Form() ,orderid: int=Form()):
    user = x[itemname,price,orderid]
    x = {"itemname":itemname,"price":price,"orderid":orderid}
    user["itemname"] = updated_user.itemname
    user["price"] = updated_user.price
    user["orderid"] = updated_user.orderid
    
    obj = db["items"].update_one(user,x)
    return f"{orderid}Registered Successfully"