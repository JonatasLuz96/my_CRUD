import os
from sqlalchemy import Column, String, Integer 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configurando a enginer do Banco de Dados
engine = create_engine('sqlite:///database.db')

# Criando a sessão
Session = sessionmaker(bind=engine)

# Criando a tabela
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

def insert_user(user_name, type_user):
    # Iniciando a sessão no BD
    session = Session()

    # Tratamento de erro
    try:
        if all([user_name, type_user]):
            user = Usuario(name=user_name, type=type_user)
            session.add(user)
            session.commit()
            print(f'Usuário {user_name}, foi cadastrado com sucesso!')
        else:
            print('É obrigatório preencher o nome e o tipo do usuário!')

    except Exception as e:
        session.rollback()
        print(f'Ops! Ocorreu um erro ao cadastrar o usuário {user_name}: {e}')
        
    finally:
        session.close()

def select_user(user_name=''):
    session = Session()
    try:
        if user_name:
            data = session.query(Usuario).filter(Usuario.name == user_name) # Fazendo uma consulta na classe usuário e filtrando o campo nome.
        else:
            data = session.query(Usuario).all()

        for i in data:
            print(f'Usuário: {i.name} - Tipo: {i.type}')

    except Exception as e:
        print(f'Ocorreu algum erro ao consultar o(s) usuário(s): {e}')
    finally:
        session.close()

def update_user_name(id_user, user_name, user_type):
    session = Session()
    try:
        if all([id_user, user_name]):
            user = session.query(Usuario).filter(Usuario.id == id_user).first()
            user.name = user_name
            user.type = user_type
            session.commit()
            print('Usuário atualizado com sucesso!')
        else:
            print('É obrigatório infomar o id do usuário para atualização.')   
        
    except Exception as e:
        session.rollback() # Serve para retornar o código
        print(f'Ocorreu um erro ao atualizar o usuário: {e}')
    finally:
        session.close()

def delete_user(id_user):
    session = Session()
    try:
        if id_user:
            user = session.query(Usuario).filter(Usuario.id == id_user).first()
            session.delete(user)
            session.commit()
            print(f'Usuário do {id_user}, deletado com sucesso!')
        else:
            print('Não foi possível encontrar o id do usuário!')

    except Exception as e:
        session.rollback()
        print(f'Erro ao deletar o usuário.')

    finally:
        session.close()



if __name__ == '__main__':
    os.system('cls')
    Base.metadata.create_all(engine)
    # insert_user('Adele', 'Cantora')
    # select_user('João')
    # update_user_name(3, 'Gabriel', 'Advogado')
    # delete_user(4)

