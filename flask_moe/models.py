from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_moe.database import Base

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

class BoardQna(Base):
    __tablename__ = 'tbl_board_qna'
    id = Column(Integer, Sequence('qna_idx'), primary_key=True)
    section = Column(String(100), doc='게시판 구분')
    title = Column(String(255), doc='게시글 제목')
    content = Column(Text, doc='게시글 콘텐츠')
    password = Column(String(255), doc='비밀번호')
    create_date = Column(DateTime, doc="생성일")
    hit = Column(Integer, doc="조회수")
    user_name = Column(String(30), doc="유저명")
    ip = Column(String(40), doc="접속 IP")
    children = relationship("BoardQnaReply")


class BoardQnaReply(Base):
    __tablename__ = 'tbl_board_qna_reply'
    id = Column(Integer, Sequence('qna_reply_idx'), primary_key=True)
    board_id = Column(Integer, ForeignKey('tbl_board_qna.id'), doc='게시판 ID')
    parent = relationship("BoardQna", back_populates="children")    
    section = Column(String(100), doc='게시판 구분')
    content = Column(Text, doc='게시글 콘텐츠')
    password = Column(String(255), doc='비밀번호')
    create_date = Column(DateTime, doc="생성일")
    user_name = Column(String(30), doc="유저명")
    ip = Column(String(40), doc="접속 IP")
