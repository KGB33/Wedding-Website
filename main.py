from weddingwebsite import create_app
from weddingwebsite.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run()
