#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from typing import Dict
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        newUser = User(email=email, hashed_password=hashed_password)
        self._session.add(newUser)
        self._session.commit()
        return newUser

    def find_user_by(self, **kwargs: Dict) -> User:
        """Find a User in the table"""
        try:
            foundUser = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return foundUser

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """Update the user with the given id in the database"""
        updateDict = {}
        searchedUser = self.find_user_by(id=user_id)
        if searchedUser is None:
            return
        for k, v in kwargs.items():
            if hasattr(User, k):
                updateDict[getattr(User, k)] = v
            else:
                raise ValueError
        self._session.query(User).filter(User.id == user_id).update(
            updateDict, synchronize_session=False)
        self._session.commit()
