from flask import render_template, request, redirect, url_for, flash, g

from utils.decorators.Autenticado import autenticado
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos

class UserController:
    @staticmethod
    # tela de login de um usuário no programa
    def login():
        return render_template('login.html')
    
    # tela de cadastro de um usuário do programa
    @staticmethod
    def cadastro():
        if request.method == 'GET':
            return render_template('cadastro.html')
        
        # POST: processar cadastro
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        tipo_usuario = request.form.get('tipo_usuario', 'gestor')
        
        # Validação básica
        if not nome or not email or not senha:
            flash("Preencha todos os campos obrigatórios.", "error")
            return redirect(url_for('cadastro'))
        
        if len(senha) < 6:
            flash("A senha deve ter no mínimo 6 caracteres.", "error")
            return redirect(url_for('cadastro'))
        
        # Criar usuário
        data = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'tipo_usuario': tipo_usuario
        }
        
        try:
            if tipo_usuario == 'gestor':
                usuario_model = g.models.gestor
                user_id = usuario_model.create(data)
            elif tipo_usuario == 'personal':
                usuario_model = g.models.personal
                user_id = usuario_model.create(data)
            flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
            return redirect(url_for('login'))
        except ErroDadosInvalidos as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro'))
        except Exception as e:
            # Log do erro para debug (em produção, use logging)
            print(f"Erro ao cadastrar usuário: {e}")
            flash("Erro ao realizar cadastro. Tente novamente.", "error")
            return redirect(url_for('cadastro'))
    
    # tela incial - versaõ do gestor
    @staticmethod
    @autenticado
    def gestor():
        return render_template('home-gestor.html')
    
    # tela de gestão e visualização de equipamentos - exclusiva do gestor
    @staticmethod
    @autenticado
    def equipamentos():
        return render_template('equipamentos.html')

    # tela de cadastro de equipamentos - exclusiva do gestor
    @staticmethod
    @autenticado
    def cadastro_equipamento():
        if request.method == 'GET':
            return render_template('cadastro-equipamento.html')
        
        # POST: processar adição de equipamento
        nome = request.form.get('nome', '').strip()
        valor = request.form.get('valor', '')
        status = request.form.get('status', '')

        # Criar equipamento
        data = {
            'nome': nome,
            'valor': valor,
            'status': status
        }

        try:
            equipamento_model = g.models.equipamento
            machine_id = equipamento_model.create(data)
            flash("Equipamento cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro-equipamento'))
        except ErroDadosInvalidos as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro-equipamento'))
        except Exception as e:
            # Log do erro para debug (em produção, use logging)
            print(f"Erro ao cadastrar equipamento: {e}")
            flash("Erro ao realizar cadastro. Tente novamente.", "error")
            return redirect(url_for('cadastro-equipamento'))

            
    
    # tela de gerenciamento dos alunos - versão do gestor
    @staticmethod
    @autenticado
    def alunos_gestor():
        return render_template('alunos-gestor.html')
    
    #tela de cadastro de alunos - exclusiva do gestor
    @staticmethod
    @autenticado
    def cadastro_aluno():
        return render_template('cadastro-aluno.html')
    
    #tela de gerenciamento dos planos - exclusiva do gestor
    @staticmethod
    @autenticado
    def planos():
        return render_template('planos.html')
    
    #tela de autenticação da entrada dos alunos - exclusiva do gestor
    @staticmethod
    @autenticado
    def autentica_entrada():
        return render_template('autentica-entrada.html')