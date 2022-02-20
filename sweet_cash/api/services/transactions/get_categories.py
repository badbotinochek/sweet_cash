import logging

from api.api import formatting
from api.models.transaction_category import TransactionCategoryModel


logger = logging.getLogger(name="categories")


class GetCategories:

    def __call__(self, user_id) -> [TransactionCategoryModel]:
        categories = TransactionCategoryModel.get()
        categories = [t for t in categories]
        categories = [formatting(item) for item in categories]

        categories = (sorted(categories, key=lambda x: x['id']))
        categories = list(reversed(categories))
        list_size = len(categories)

        for num, sub_category in enumerate(categories):
            parent_id = sub_category['parent_category_id']
            for parent_category_candidate_index in range(num + 1, list_size):
                parent_category_candidate = categories[parent_category_candidate_index]
                parent_category_candidate_id = parent_category_candidate['id']
                if parent_id == parent_category_candidate_id:
                    if 'subcategories' not in parent_category_candidate:
                        parent_category_candidate['subcategories'] = []
                    a = parent_category_candidate['subcategories']
                    a.append(sub_category)
                    categories[num] = None
                    break

        y = [k for j, k in enumerate(categories) if k not in categories[j + 1:]]
        y.remove(None)

        logger.info(f'User {user_id} got categories')

        return categories
