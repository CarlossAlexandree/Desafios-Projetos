from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Certifique-se de que está '/' para acessar direto pelo link http://127.0.0.1:5000
@main.route('/')
def index():
    cars = [
        {"brand": "Toyota", "model": "Corolla", "year": 2020, "price": 100000},
        {"brand": "Ford", "model": "Focus", "year": 2019, "price": 80000},
        {"brand": "Chevrolet", "model": "Cruze", "year": 2021, "price": 95000}
    ]
    # O Flask vai procurar este arquivo estrito dentro da pasta 'templates'
    return render_template('car_sales.html', cars=cars)