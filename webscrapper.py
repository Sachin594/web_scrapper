from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper1.log",level=logging.INFO)
app=Flask(__name__)
@app.route('/',methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/review',methods=['POST','GET'])
def index():
    if request.method=='POST':
        try :
            searchstring=request.form['content'].replace(' ','')
            url="https://www.flipkart.com/search?q="+ searchstring
            urlclient=uReq(url)
            flipkart_page=urlclient.read()
            urlclient.close()
            flipkart_html=bs(flipkart_page,'html.parser')
            bigbox=flipkart_html.find_all('div',{'class':'_1AtVbE col-12-12'})
            del bigbox[0:2]
            box =bigbox[0].div.find('a',{'class':'_1fQZEK'})['href']
            product_page=requests.get('https://www.flipkart.com'+box)
            product_html=bs(product_page.text,'html.parser')
            comment_boxes=product_html.find_all('div',{'class':'_16PBlm'})
            filename=searchstring+'.csv'
            s=open(filename,'w')
            headers='Product,Customer,Rating,Heading,Comment'
            s.write(headers)
            reviews=[]
        
            for i in comment_boxes:
                try:
                    #name.encode(encoding='utf-8')
                    name=i.div.find('p',{'class':'_2sc7ZR _2V5EHH'}).text
                
                except:
                    logging.info('name')
                
                try:
                    #rating.encode(encoding='utf-8')
                    rating=i.div.div.div.div.text
                
                except:
                    rating='No Rating'
                    logging.info('rating')
                
                try:
                    #commenthead.encodw(encoding='utf8)
                    commenthead=i.div.find('p',{'class':'_2-N8zT'}).text
                
                except:
                    commenthead='NO COMMENT HEAD'
                    logging.info('commenthead')
            
                try:
                    comment=i.find('div',{'class':''}).text
                
                except Exception as e :
                    logging.info(e)
                
                mydict={'Product':searchstring,"Name":name,"Rating":rating,"CommentHead":commenthead,"Comment":comment}
                reviews.append(mydict)
            logging.info('my final results are {}'.format(reviews))
            return render_template('result.html',reviews=reviews[0:len(reviews)-1])
        
        except Exception as e1:
            logging.info(e1)
            return 'Something Is Wrong'
        
    # return render_template('results.html')    
    else:
        return render_template('index.html')
  
if __name__=='__main__' :
    app.run(host='0.0.0.0')

        
    
    
        
