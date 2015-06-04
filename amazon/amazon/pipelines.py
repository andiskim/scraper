from sqlalchemy.orm import sessionmaker
from models import Pages, db_connect, create_pages_table
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonPipeline(object):
	def __init__(self):
		engine = db_connect()
		create_pages_table(engine)
		self.Session = sessionmaker(bind=engine)

	def process_item(self, item, spider):
		session = self.Session()
		page = Pages(**item)

		try:
			session.add(page)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

		return item