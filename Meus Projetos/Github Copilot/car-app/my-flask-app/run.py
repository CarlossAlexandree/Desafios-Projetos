from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ativa o modo debug para recarregamento automático ao alterar arquivos
    app.run(debug=True)