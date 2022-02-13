import logging


from api.models.transaction_category import TransactionCategoryModel


logger = logging.getLogger(name="categories")


class GetCategories:

    def __call__(self, user_id) -> [TransactionCategoryModel]:
        categories = TransactionCategoryModel.get_transaction_categories()

        categories = [t for t in categories]
        print(categories[0])
        print(type(categories[0]))
        logger.info(f'User {user_id} got categories')

        return categories
