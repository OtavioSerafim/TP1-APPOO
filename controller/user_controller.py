from flask import render_template, request, redirect, url_for, flash, g, current_app

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
        if request.method == 'POST':
            capacidade_raw = request.form.get('capacidade_maxima', '').strip()
            try:
                capacidade_valor = int(capacidade_raw)
                if capacidade_valor <= 0:
                    raise ValueError
            except ValueError:
                flash('Informe um número inteiro positivo para a capacidade máxima.', 'error')
                return redirect(url_for('gestor'))

            current_app.config['ACADEMIA_CAPACIDADE_MAXIMA'] = capacidade_valor
            flash('Capacidade máxima atualizada com sucesso!', 'success')
            return redirect(url_for('gestor'))

        usuario = getattr(g, "current_user", None) # dados do usuário
        return render_template('home-gestor.html', usuario=usuario)
    
    # tela de gestão e visualização de equipamentos - exclusiva do gestor
    @staticmethod
    @autenticado
    def equipamentos():
        if request.method == 'GET':
            equipamentos = g.models.equipamento.get_all() # lista equipamentos
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template('equipamentos.html', equipamentos=equipamentos, usuario=usuario)

    # tela de cadastro de equipamentos - exclusiva do gestor
    @staticmethod
    @autenticado
    def cadastro_equipamento():
        if request.method == 'GET':
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template('cadastro-equipamento.html', usuario=usuario)

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
        usuario = getattr(g, "current_user", None) # dados do usuário
        alunos = g.models.aluno.get_all() # lista planos
        return render_template('alunos-gestor.html', usuario=usuario, alunos=alunos)
    
    # tela de cadastro de alunos - exclusiva do gestor
    @staticmethod
    @autenticado
    def cadastro_aluno():
        if request.method == 'GET':
            usuario = getattr(g, "current_user", None) # dados do usuário
            planos = g.models.plano.get_all() # lista planos
            personals = g.models.personal.get_all() # lista personal trainers
            return render_template('cadastro-aluno.html', usuario=usuario, planos=planos, personals=personals)
    
        # POST: processar cadastro de aluno
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        personal_id = request.form.get('personal_id', '')
        plano_id = request.form.get('plano_id', '')
        plano_data_inicio = request.form.get('plano_data_inicio', '')
        senha = 'Senha@luno123'
        tipo_usuario = 'aluno'

        # Criar aluno
        data = {
            'nome': nome,
            'email': email,
            'personal_id': personal_id,
            'plano_id': plano_id,
            'plano_data_inicio': plano_data_inicio,
            'senha': senha,
            'tipo_usuario': tipo_usuario
        }

        try:
            aluno_model = g.models.aluno
            aluno_id = aluno_model.create(data)
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro-aluno'))
        except ErroDadosInvalidos as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro-aluno'))
        except Exception as e:
            # Log do erro para debug (em produção, use logging)
            print(f"Erro ao cadastrar aluno: {e}")
            flash("Erro ao realizar cadastro. Tente novamente.", "error")
            return redirect(url_for('cadastro-aluno'))
    
    # tela de gerenciamento dos planos - exclusiva do gestor
    @staticmethod
    @autenticado
    def planos():
        if request.method == 'GET':
            usuario = getattr(g, "current_user", None) # dados do usuário
            planos = g.models.plano.get_all() # lista planos
            return render_template('planos.html', planos=planos, usuario=usuario)

    
    # tela de gerenciamento dos planos - exclusiva do gestor
    @staticmethod
    @autenticado
    def cadastro_plano():
        if request.method == 'GET':
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template('cadastro-plano.html', usuario=usuario)
        
        # POST: processar adição de plano
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '')
        valor_mensal = request.form.get('valor_mensal', '')
        duracao_meses = request.form.get('duracao_meses', '')

        # Criar plano
        data = {
            'nome': nome,
            'descricao': descricao,
            'valor_mensal': valor_mensal,
            'duracao_meses': duracao_meses
        }

        try:
            plano_model = g.models.plano
            plan_id = plano_model.create(data)
            flash("Plano cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro-plano'))
        except ErroDadosInvalidos as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro-plano'))
        except Exception as e:
            # Log do erro para debug (em produção, use logging)
            print(f"Erro ao cadastrar plano: {e}")
            flash("Erro ao realizar cadastro. Tente novamente.", "error")
            return redirect(url_for('cadastro-plano'))
    
    # tela de autenticação da entrada dos alunos - exclusiva do gestor
    @staticmethod
    @autenticado
    def autentica_entrada():
        usuario = getattr(g, "current_user", None) # dados do usuário
        return render_template('autentica-entrada.html', usuario=usuario)
    
    # tela de gerenciamento de fichas - exclusiva do gestor
    @staticmethod
    @autenticado
    def fichas_gestor():
        usuario = getattr(g, "current_user", None) # dados do usuário
        return render_template('fichas-gestor.html', usuario=usuario)
    
    @staticmethod
    @autenticado
    def cadastro_ficha():
        usuario = getattr(g, "current_user", None) # dados do usuário
        return render_template('cadastro-ficha.html', usuario=usuario)