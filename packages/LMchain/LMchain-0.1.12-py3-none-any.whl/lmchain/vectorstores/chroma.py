

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from lmchain.vectorstores import laiss


class Chroma:
    def __init__(self,documents,embedding_tool,chunk_size = 1280,chunk_overlap = 50,file_name = "这是一份辅助材料"):
        """
        :param document: 输入的文本内容，只要一个text文本
        :param chunk_size: 切分后每段的字数
        :param chunk_overlap: 每个相隔段落重叠的字数
        :param file_name: 文本名称/文本地址
        """
        self.text_splitter = RecursiveCharacterTextSplitter(    chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedding_tool = embedding_tool

        self.lmaiss = laiss.LMASS() #这里是用于将文本转化为vector，并且计算query相应的相似度的类

        self.documents = []
        self.vectorstore = []
        "---------------------------"
        for document in documents:
            document = [Document(page_content=document, metadata={"source": file_name})]    #对输入的document进行格式化处理
            doc= self.text_splitter.split_documents(document)    #根据
            self.documents.extend(doc)

            vector = self.lmaiss.from_documents(document, embedding_class=self.embedding_tool)
            self.vectorstore.extend(vector)

    # def __call__(self, query):
    #     query_embedding = self.embedding_tool.embed_query(query)
    #
    #     #根据query查找最近的那个序列
    #     close_id = self.lmaiss.get_similarity_vector_indexs(query_embedding, self.vectorstore, k=1)[0]
    #     #查找最近的那个段落id
    #     doc = self.documents[close_id]
    #
    #
    #     return doc

    def similarity_search(self, query):
        query_embedding = self.embedding_tool.embed_query(query)

        #根据query查找最近的那个序列
        close_id = self.lmaiss.get_similarity_vector_indexs(query_embedding, self.vectorstore, k=1)[0]
        #查找最近的那个段落id
        doc = self.documents[close_id]
        return doc

    def add_texts(self,texts,file_name = ""):
        for document in texts:
            document = [Document(page_content=document, metadata={"source": file_name})]    #对输入的document进行格式化处理
            doc= self.text_splitter.split_documents(document)    #根据
            self.documents.extend(doc)

            vector = self.lmaiss.from_documents(document, embedding_class=self.embedding_tool)
            self.vectorstore.extend(vector)

        return True





def from_texts(texts,embeddings):
    docsearch = Chroma(documents = texts,embedding_tool=embeddings)
    return docsearch



