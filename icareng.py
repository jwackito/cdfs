# ##############################################################################
# ICARENG Database objects for easy access
# Copyright (C) 2015-07 Joaquin Bogado <jbogado@linti.unlp.edu.ar>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#################################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


dbname = 'database.db'
Base = declarative_base()

class Database():
    def __init__(self, dbname=':memory:'):
        self.engine = create_engine('sqlite:///' + dbname, echo=True)
        #uncomment this line to access to a mysql database
        #self.engine = create_engine('mysql://user:pass@localhost/cdfs')
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

class Epoch(Base):
    '''
    This table reprensent the position of the SAC-D at epoch
    '''
    __tablename__ = 'epoch'

    id = Column(Integer, primary_key=True)
    epoch = Column(DateTime)
    alpha = Column(Float)
    alpha_eq = Column(Float)
    b_calc = Column(Float)
    b_eq = Column(Float)
    i = Column(Float)
    l = Column(Float)
    l_star = Column(Float)
    pos_x = Column(Float)
    pos_y = Column(Float)
    pos_z = Column(Float)
    pos_lat = Column(Float)
    pos_lon = Column(Float)
    pos_alt = Column(Float)
    mtl = Column(Float)
    pos_quality = Column(Float)

    fedos = relationship("FEDO", order_by="FEDO.id", backref="epoch")
    feios = relationship("FEIO", order_by="FEIO.id", backref="epoch")
    fpdos = relationship("FPDO", order_by="FPDO.id", backref="epoch")
    fpios = relationship("FPIO", order_by="FPIO.id", backref="epoch")

class FEDODesc(Base):
    '''
    FEDO description
    '''
    __tablename__ = 'fedo_desc'

    id = Column(Integer, primary_key=True)
    energy = Column(Float)
    crosscalib = Column(Float)
    label = Column(String(50))
    fedos = relationship("FEDO", order_by="FEDO.id", backref="desc")

class FEDO(Base):
    '''
    FEDO measurement
    '''
    __tablename__ = 'fedo'

    id = Column(Integer, primary_key=True)
    fedo = Column(Float)
    quality = Column(Float)
    epoch_id = Column(Integer, ForeignKey('epoch.id'))
    fedo_desc_id = Column(Integer, ForeignKey('fedo_desc.id'))

class FEIODesc(Base):
    '''
    FEIO description
    '''
    __tablename__ = 'feio_desc'

    id = Column(Integer, primary_key=True)
    energy = Column(Float)
    crosscalib = Column(Float)
    label = Column(String(50))
    feios = relationship("FEIO", order_by="FEIO.id", backref="desc")

class FEIO(Base):
    '''
    FEIO measurement
    '''
    __tablename__ = 'feio'

    id = Column(Integer, primary_key=True)
    feio = Column(Float)
    quality = Column(Float)
    epoch_id = Column(Integer, ForeignKey('epoch.id'))
    feio_desc_id = Column(Integer, ForeignKey('feio_desc.id'))

class FPDODesc(Base):
    '''
    FPDO description
    '''
    __tablename__ = 'fpdo_desc'

    id = Column(Integer, primary_key=True)
    energy = Column(Float)
    crosscalib = Column(Float)
    label = Column(String(50))
    fpdos = relationship("FPDO", order_by="FPDO.id", backref="desc")

class FPDO(Base):
    '''
    FPDO measurement
    '''
    __tablename__ = 'fpdo'

    id = Column(Integer, primary_key=True)
    fpdo = Column(Float)
    quality = Column(Float)
    epoch_id = Column(Integer, ForeignKey('epoch.id'))
    fpdo_desc_id = Column(Integer, ForeignKey('fpdo_desc.id'))

class FPIODesc(Base):
    '''
    FPIO description
    '''
    __tablename__ = 'fpio_desc'

    id = Column(Integer, primary_key=True)
    energy = Column(Float)
    crosscalib = Column(Float)
    label = Column(String(50))
    fpios = relationship("FPIO", order_by="FPIO.id", backref="desc")

class FPIO(Base):
    '''
    FPIO measurement
    '''
    __tablename__ = 'fpio'

    id = Column(Integer, primary_key=True)
    fpio = Column(Float)
    quality = Column(Float)
    epoch_id = Column(Integer, ForeignKey('epoch.id'))
    fpio_desc_id = Column(Integer, ForeignKey('fpio_desc.id'))

