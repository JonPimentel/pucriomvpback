from flask import Blueprint, request, jsonify
from database import db
from models import Usuario, Endereco
from flasgger import swag_from

routes = Blueprint("routes", __name__)

@routes.route("/cadastrar_usuario", methods=["POST"])
@swag_from({
    'tags': ['Usuário'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'example': {
                'nome': 'João Silva',
                'email': 'joao@email.com',
                'endereco': {
                    'rua': 'Rua das Flores',
                    'cidade': 'São Paulo'
                }
            }
        }
    }],
    'responses': {
        201: {'description': 'Usuário criado com sucesso'},
        400: {'description': 'Erro de validação'}
    }
})
def cadastrar_usuario():
    data = request.json
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400

    novo_usuario = Usuario(nome=data['nome'], email=data['email'])
    db.session.add(novo_usuario)
    db.session.commit()

    endereco = Endereco(rua=data['endereco']['rua'], cidade=data['endereco']['cidade'], usuario_id=novo_usuario.id)
    db.session.add(endereco)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso'}), 201

@routes.route("/buscar_usuario/<int:id>", methods=["GET"])
@swag_from({
    'tags': ['Usuário'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário encontrado',
            'schema': {
                'example': {
                    'id': 1,
                    'nome': 'Maria',
                    'email': 'maria@email.com',
                    'endereco': {
                        'rua': 'Rua XPTO',
                        'cidade': 'RJ'
                    }
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado'
        }
    }
})
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'endereco': {
            'rua': usuario.endereco.rua,
            'cidade': usuario.endereco.cidade
        }
    })

@routes.route("/buscar_usuarios", methods=["GET"])
@swag_from({
    'tags': ['Usuário'],
    'responses': {
        200: {
            'description': 'Lista de todos os usuários',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'email': {'type': 'string'},
                        'endereco': {
                            'type': 'object',
                            'properties': {
                                'rua': {'type': 'string'},
                                'cidade': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def buscar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
            'endereco': {
                'rua': u.endereco.rua,
                'cidade': u.endereco.cidade
            }
        } for u in usuarios
    ])

@routes.route("/deletar_usuario/<int:id>", methods=["DELETE"])
@swag_from({
    'tags': ['Usuário'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser deletado'
        }
    ],
    'responses': {
        200: {'description': 'Usuário deletado com sucesso'},
        404: {'description': 'Usuário não encontrado'}
    }
})
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    if usuario.endereco:
        db.session.delete(usuario.endereco)

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário deletado com sucesso'})
