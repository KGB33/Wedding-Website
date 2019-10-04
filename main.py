from WeddingWebsite import create_app
from WeddingWebsite.config import DevelopmentConfig

if __name__ == "__main__":
    app = create_app(DevelopmentConfig)
    app.run()
