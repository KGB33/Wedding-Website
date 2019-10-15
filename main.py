from WeddingWebsite import create_app
from WeddingWebsite.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run()
