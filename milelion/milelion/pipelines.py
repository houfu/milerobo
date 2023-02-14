# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from itemadapter import ItemAdapter

import weaviate

class_obj = {
    "class": "Article",
    "description": "An Article containing content on miles",
    "properties": [
        {
            "dataType": ["text"],
            "description": "Content of the article",
            "name": "content"
        },
        {
            "dataType": ["date"],
            "description": "Date when article was published",
            "name": "date_pub"
        },
        {
            "dataType": ["text"],
            "description": "Title of the article",
            "name": "title"
        },
        {
            "dataType": ["string"],
            "description": "Summary of the article",
            "name": "summary"
        },
    ],
    "vectorizer": "text2vec-openai"
}


class MilelionSavetoWeaviatePipeline:

    def __init__(self):
        resource_owner_config = weaviate.AuthClientPassword(
            username=os.getenv('WEAVIATE_USER'),
            password=os.getenv('WEAVIATE_PASSWORD'),
        )

        self.client = weaviate.Client(
            os.getenv('WEAVIATE_URL', "https://milerobosg.weaviate.network"),
            auth_client_secret=resource_owner_config,
            additional_headers={
                "X-OpenAI-Api-Key": os.getenv('OPENAI_KEY')
            }
        )

    def open_spider(self, spider):
        """
        When spider is opened,
        remove all and recreate schema.
        """
        import dotenv
        dotenv.load_dotenv('../../.env')

        self.client.batch.configure(batch_size=5, dynamic=True)

        self.client.schema.delete_all()

        self.client.schema.create_class(class_obj)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        texts = adapter.get('text')
        from langchain.text_splitter import SpacyTextSplitter
        splitter = SpacyTextSplitter.from_tiktoken_encoder(chunk_size=900, chunk_overlap=100)
        chunks = splitter.split_text(texts)
        with self.client.batch as batch:
            for chunk in chunks:
                batch.add_data_object({
                    "content": chunk,
                    "date_pub": adapter.get('date_pub'),
                    "title": adapter.get('title'),
                    "summary": adapter.get('summary'),
                }, "Article")
        return item
