from WeddingWebsite import create_app
from WeddingWebsite.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run()
