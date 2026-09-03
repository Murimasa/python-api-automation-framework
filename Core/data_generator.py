from faker import Faker

fake = Faker()


class DataGenerator:

    @staticmethod
    def generate_post_data():
        """Генерирует уникальный payload для создания поста."""
        return {
            "title": fake.sentence(nb_words=4),
            "body": fake.paragraph(nb_sentences=2),
            "userId": fake.random_int(min=1, max=10),
        }

    @staticmethod
    def generate_user_data():
        """Генерирует реалистичные данные пользователя."""
        return {
            "name": fake.name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "address": {
                "street": fake.street_name(),
                "city": fake.city(),
                "zipcode": fake.zipcode(),
            },
        }