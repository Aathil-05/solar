

# engine = create_engine('mysql+pymysql://root:aathil12@localhost:3306/solardata')
engine = create_engine('mysql+pymysql://root:EabGDkdNYaRXWrMoXyXqQEvivWFtPYWx@centerbeam.proxy.rlwy.net:46194/railway')
Base = declarative_base()



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
