import smtplib 
import stripe
from products.models import Product
from mailjet_rest import Client
import os
from .keys import MAIL_API_KEY, MAIL_API_SECRET, my_email, password, STRIPE_KEY
from decimal import Decimal

EMAIL = my_email
PASSWORD = password

stripe.api_key = STRIPE_KEY
api_key = MAIL_API_KEY
api_secret = MAIL_API_SECRET



def send_mail(order, shipping_price, products):
    try:
        intent = stripe.PaymentIntent.retrieve(order.payment_intent_id)
        del intent.metadata['coupon_code']
        number_of_keys = len(intent.metadata.keys())
        
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "sao.perolas.pt@gmail.com",
                        "Name": "São Pérolas"
                    },
                    "To": [
                        {
                            "Email": intent.receipt_email,
                            "Name": intent.shipping["name"]
                        },
                        {
                            "Email": "sao.perolas.pt@gmail.com",
                            "Name": "São Pérolas"
                        }
                    ],
                    "TemplateID": 1238228,
                    "TemplateLanguage": True,
                    "Subject": "Obrigado pela preferência",
                    "Variables": {
                        "NUMERO_ENCOMENDA": str(order.id),
                        "data": str(order.date_ordered.date()),
                        "nome": intent.shipping["name"],
                        "morada_1": intent.shipping["address"]["line1"],
                        "morada_2": intent.shipping["address"]["state"] + ", " + intent.shipping["address"]["city"] + " "  + intent.shipping["address"]["postal_code"] + " " + intent.shipping["address"]["country"],
                        "produto_1_nome": products[0].name if number_of_keys >= 1 else "",
                        "produto_1_qt": intent.metadata.get(products[0].name) if number_of_keys >= 1 else "",
                        "produto_1_u_preço": str(products[0].price) + " €" if number_of_keys >= 1 else "",
                        "produto_1_t_preço": str(Decimal(intent.metadata.get(products[0].name)) * products[0].price) + " €" if number_of_keys >= 1 else "", 
                        "produto_2_nome": products[1].name if number_of_keys >= 2 else "",
                        "produto_2_qt": intent.metadata.get(products[1].name) if number_of_keys >= 2 else "",
                        "produto_2_u_preço": str(products[1].price) + " €" if number_of_keys >= 2 else "",
                        "produto_2_t_preço": str(Decimal(intent.metadata.get(products[1].name)) * products[1].price) + " €" if number_of_keys >= 2 else "", 
                        "produto_3_nome": products[2].name if number_of_keys >= 3 else "",
                        "produto_3_qt": intent.metadata.get(products[2].name) if number_of_keys >= 3 else "",
                        "produto_3_u_preço": str(products[2].price) + " €" if number_of_keys >= 3 else "",
                        "produto_3_t_preço": str(Decimal(intent.metadata.get(products[2].name)) * products[2].price) + " €" if number_of_keys >= 3 else "", 
                        "produto_4_nome": products[3].name if number_of_keys >= 4 else "",
                        "produto_4_qt": intent.metadata.get(products[3].name) if number_of_keys >= 4 else "",
                        "produto_4_u_preço": str(products[3].price) + " €" if number_of_keys >= 4 else "",
                        "produto_4_t_preço": str(Decimal(intent.metadata.get(products[3].name)) * products[3].price) + " €" if number_of_keys >= 4 else "", 
                        "produto_5_nome": products[4].name if number_of_keys >= 5 else "",
                        "produto_5_qt": intent.metadata.get(products[4].name) if number_of_keys >= 5 else "",
                        "produto_5_u_preço": str(products[4].price) + " €" if number_of_keys >= 5 else "",
                        "produto_5_t_preço": str(Decimal(intent.metadata.get(products[4].name)) * products[4].price) + " €" if number_of_keys >= 5 else "", 
                        "produto_6_nome": products[5].name if number_of_keys >= 6 else "",
                        "produto_6_qt": intent.metadata.get(products[5].name) if number_of_keys >= 6 else "",
                        "produto_6_u_preço": str(products[5].price) + " €" if number_of_keys >= 6 else "",
                        "produto_6_t_preço": str(Decimal(intent.metadata.get(products[5].name)) * products[5].price) + " €" if number_of_keys >= 6 else "", 
                        "produto_7_nome": products[6].name if number_of_keys >= 7 else "",
                        "produto_7_qt": intent.metadata.get(products[6].name) if number_of_keys >= 7 else "",
                        "produto_7_u_preço": str(products[6].price) + " €" if number_of_keys >= 7 else "",
                        "produto_7_t_preço": str(Decimal(intent.metadata.get(products[6].name)) * products[6].price) + " €" if number_of_keys >= 7 else "", 
                        "produto_8_nome": products[7].name if number_of_keys >= 8 else "",
                        "produto_8_qt": intent.metadata.get(products[7].name) if number_of_keys >= 8 else "",
                        "produto_8_u_preço": str(products[7].price) + " €" if number_of_keys >= 8 else "",
                        "produto_8_t_preço": str(Decimal(intent.metadata.get(products[7].name)) * products[7].price) + " €" if number_of_keys >= 8 else "", 
                        "produto_9_nome": products[8].name if number_of_keys >= 9 else "",
                        "produto_9_qt": intent.metadata.get(products[8].name) if number_of_keys >= 9 else "",
                        "produto_9_u_preço": str(products[8].price) + " €" if number_of_keys >= 9 else "",
                        "produto_9_t_preço": str(Decimal(intent.metadata.get(products[8].name)) * products[8].price) + " €" if number_of_keys >= 9 else "", 
                        "produto_10_nome": products[9].name if number_of_keys >= 10 else "",
                        "produto_10_qt": intent.metadata.get(products[9].name) if number_of_keys >= 10 else "",
                        "produto_10_u_preço": str(products[9].price) + " €" if number_of_keys >= 10 else "",
                        "produto_10_t_preço": str(Decimal(intent.metadata.get(products[9].name)) * products[9].price) + " €" if number_of_keys >= 10 else "", 
                        "produto_11_nome": products[10].name if number_of_keys >= 11 else "",
                        "produto_11_qt": intent.metadata.get(products[10].name) if number_of_keys >= 11 else "",
                        "produto_11_u_preço": str(products[10].price) + " €" if number_of_keys >= 11 else "",
                        "produto_11_t_preço": str(Decimal(intent.metadata.get(products[10].name)) * products[10].price) + " €" if number_of_keys >= 11 else "", 
                        "produto_12_nome": products[11].name if number_of_keys >= 12 else "",
                        "produto_12_qt": intent.metadata.get(products[11].name) if number_of_keys >= 12 else "",
                        "produto_12_u_preço": str(products[11].price) + " €" if number_of_keys >= 12 else "",
                        "produto_12_t_preço": str(Decimal(intent.metadata.get(products[11].name)) * products[11].price) + " €" if number_of_keys >= 12 else "", 
                        "custos_de_envio": str(shipping_price) + " €",
                        "preco_total": str((order.total_price)/100) + " €"
                    }
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            return True
        else : 
            return False
        print("Sucess: Email Sent!")
    except Exception as e:
        print("E-mail not sent!")
        return False


    
