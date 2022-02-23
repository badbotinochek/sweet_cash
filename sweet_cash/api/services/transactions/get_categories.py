import logging

from api.models.transaction_category import TransactionCategoryModel


logger = logging.getLogger(name="categories")


class GetCategories:

    def __call__(self, user_id) -> [TransactionCategoryModel]:
        categories = TransactionCategoryModel.get()

        result = []
        while categories:
            sub_category = categories.pop(0)
            for parent_candidate in categories:
                if sub_category.parent_category_id == parent_candidate.id:
                    if not hasattr(parent_candidate, 'sub_categories'):
                        setattr(parent_candidate, 'sub_categories', [])
                    parent_candidate.sub_categories.append(sub_category)
                    break

                result.append(sub_category)

            if not categories:
                result.append(sub_category)

        result = list(reversed(result))

        logger.info(f'User {user_id} got categories')

        return result
