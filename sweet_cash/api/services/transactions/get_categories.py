import logging
import datetime

from api.models.transaction_category import TransactionCategoryModel
from cache_management import RedisCache


logger = logging.getLogger(name="categories")


class GetCategories(object):

    def __call__(self, user_id) -> [TransactionCategoryModel]:
        result = RedisCache.get(key='transaction:categories')

        if result is None:
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

            RedisCache.setex(key='transaction:categories',
                             time=datetime.timedelta(seconds=10),
                             obj=result)

        logger.info(f'User {user_id} got categories')

        return result
