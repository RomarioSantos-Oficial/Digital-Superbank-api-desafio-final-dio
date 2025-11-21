"""
Router principal da API v1
"""
from fastapi import APIRouter
from src.api.v1.endpoints import (
    auth, accounts, transactions, credit_cards, investments, chatbot, 
    bill_payments, pix_keys
)

api_router = APIRouter()

# Inclui as rotas
api_router.include_router(auth.router)
api_router.include_router(accounts.router)
api_router.include_router(transactions.router)
api_router.include_router(credit_cards.router)
api_router.include_router(investments.router)
api_router.include_router(chatbot.router)
api_router.include_router(bill_payments.router)
api_router.include_router(pix_keys.router)
