from sqlalchemy import Column, Integer, String, Sequence, Text
from database import Base

class Source(Base):
    __tablename__ = 'tbl_sources'
    id = Column(Integer, Sequence('source_idx'), primary_key=True)
    code_num = Column(String(50), unique=True, doc='코드번호')
    description = Column(Text, doc='코드 설명')
    file_content = Column(Text, doc='코드 내용')

    def __init__(self, code_num, description, file_content):
        self.code_num = code_num
        self.description = description
        self.file_content = file_content

    def __repr__(self):
        return '<Source %r>' % (self.code_num)

    def to_dict(self):
        return dict(
            id=self.id,
            code_num=self.code_num,
            description=self.description,
            file_content=self.file_content
        )
