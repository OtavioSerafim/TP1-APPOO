from flask import render_template, request, redirect, url_for, flash, g, current_app, jsonify

from utils.decorators.Autenticado import autenticado
from utils.decorators.TipoUsuario import gestor_obrigatorio
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
    
    # tela incial - versaõ do personal
    @staticmethod
    @autenticado
    def personal():
        if request.method == 'GET':
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template('home-personal.html', usuario=usuario)
    
    # tela de alunos - versaõ do personal
    @staticmethod
    @autenticado
    def alunos_personal():
        if request.method == 'GET':
            alunos = g.models.aluno.get_all() # lista alunos
            planos_raw = g.models.plano.get_all()
            planos = [dict(row) for row in planos_raw]
            personals = g.models.personal.get_all()
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template(
                'alunos-personal.html',
                usuario=usuario,
                alunos=alunos,
                planos=planos,
                personals=personals,
            )
    
    # tela de gerenciamento de fichas - versaõ do personal
    @staticmethod
    @autenticado
    def fichas_personal():
        if request.method == 'GET':
            fichas = g.models.ficha.get_all()
            exercicios = g.models.exercicio.get_all()
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template('fichas-personal.html', usuario=usuario, fichas=fichas, exercicios=exercicios)
        
    # tela de criação de fichas - versaõ do personal
    @staticmethod
    @autenticado
    def cadastro_ficha_personal():
        if request.method == 'GET':
            alunos = g.models.aluno.get_all()
            personals = g.models.personal.get_all()
            equipamentos = g.models.equipamento.listar_disponiveis()
            usuario = getattr(g, "current_user", None) # dados do usuário

            return render_template(
                'cadastro-ficha-personal.html',
                usuario=usuario,
                equipamentos=equipamentos,
                personals=personals,
                alunos=alunos
            )
        
        # POST: processar cadastro de ficha
        aluno_id = request.form.get('aluno_id', '')
        personal_id = request.form.get('personal_id', '')
        descricao = request.form.get('descricao', '').strip()

        # Processar exercícios (agora vem como array)
        exercicios_data = request.form.to_dict(flat=False)
        exercicios = []

        # Se houver exercicios[0][nome], exercicios[1][nome], etc.
        i = 0
        while f'exercicios[{i}][nome]' in exercicios_data:
            exercicio = {
                'nome': exercicios_data[f'exercicios[{i}][nome]'][0],
                'equipamento_id': exercicios_data[f'exercicios[{i}][equipamento_id]'][0],
                'series': exercicios_data[f'exercicios[{i}][series]'][0],
                'repeticoes': exercicios_data[f'exercicios[{i}][repeticoes]'][0],
                'carga': exercicios_data[f'exercicios[{i}][carga]'][0],
                'tempo_descanso': exercicios_data[f'exercicios[{i}][tempo_descanso]'][0],
                'observacoes': exercicios_data.get(f'exercicios[{i}][observacoes]', [''])[0]
            }
            exercicios.append(exercicio)
            i += 1

        # Se não houver array format, pega os valores diretos (primeiro exercício)
        if not exercicios:
            exercicio = {
                'nome': request.form.get('nome', ''),
                'equipamento_id': request.form.get('equipamento_id', ''),
                'series': request.form.get('series', ''),
                'repeticoes': request.form.get('repeticoes', ''),
                'carga': request.form.get('carga', ''),
                'tempo_descanso': request.form.get('tempo_descanso', ''),
                'observacoes': request.form.get('observacoes', '')
            }
            exercicios.append(exercicio)

        # Validação básica
        if not aluno_id or not personal_id or not exercicios:
            flash("Preencha todos os campos obrigatórios e adicione ao menos um exercício.", "error")
            return redirect(url_for('cadastro-ficha-personal'))
        
        try:
            # Criar a ficha
            ficha_data = {
                'aluno_id': aluno_id,
                'personal_id': personal_id,
                'descricao': descricao
            }
            ficha_model = g.models.ficha
            ficha_id = ficha_model.create(ficha_data)

            # Criar os exercícios vinculados à ficha
            exercicio_model = g.models.exercicio
            exercicios_criados = 0
            
            for ex in exercicios:
                # Adicionar o ficha_id a cada exercício
                ex['ficha_id'] = ficha_id
                exercicio_model.create(ex)
                exercicios_criados += 1

            flash(f"Ficha cadastrada com sucesso! {exercicios_criados} exercício(s) adicionado(s).", "success")
            return redirect(url_for('fichas-gestor'))
        
        except ErroDadosInvalidos as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro-ficha-personal'))
        except Exception as e:
            print(f"Erro ao cadastrar ficha: {e}")
            import traceback
            traceback.print_exc()
            flash("Erro ao realizar cadastro. Tente novamente.", "error")
            return redirect(url_for('cadastro-ficha-personal'))
    
    # tela incial - versaõ do gestor
    @staticmethod
    @autenticado
    @gestor_obrigatorio
    def gestor():
        if request.method == 'POST':
            capacidade_raw = request.form.get('capacidade_maxima', '').strip()
            try:
                capacidade_valor = int(capacidade_raw)
                if capacidade_valor <= 0:
                    raise ValueError
                presentes = current_app.config.get('ACADEMIA_PRESENTES', [])
                ocupacao_atual = len(presentes)
                if capacidade_valor < ocupacao_atual:
                    flash('A capacidade máxima não pode ser menor que o número de alunos presentes no momento.', 'error')
                    return redirect(url_for('gestor'))
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
    @gestor_obrigatorio
    def equipamentos():
        if request.method == 'GET':
            equipamentos = g.models.equipamento.get_all() # lista equipamentos
            usuario = getattr(g, "current_user", None) # dados do usuário
            return render_template('equipamentos.html', equipamentos=equipamentos, usuario=usuario)

    # tela de cadastro de equipamentos - exclusiva do gestor
    @staticmethod
    @autenticado
    @gestor_obrigatorio
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
    @gestor_obrigatorio
    def alunos_gestor():
        usuario = getattr(g, "current_user", None) # dados do usuário
        alunos = g.models.aluno.get_all() # lista alunos
        planos_raw = g.models.plano.get_all()
        planos = [dict(row) for row in planos_raw]
        personals = g.models.personal.get_all()
        return render_template(
            'alunos-gestor.html',
            usuario=usuario,
            alunos=alunos,
            planos=planos,
            personals=personals,
        )
    
    # tela de cadastro de alunos - exclusiva do gestor
    @staticmethod
    @autenticado
    @gestor_obrigatorio
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
    @gestor_obrigatorio
    def planos():
        if request.method == 'GET':
            usuario = getattr(g, "current_user", None) # dados do usuário
            planos = g.models.plano.get_all() # lista planos
            return render_template('planos.html', planos=planos, usuario=usuario)

    
    # tela de gerenciamento dos planos - exclusiva do gestor
    @staticmethod
    @autenticado
    @gestor_obrigatorio
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
    @gestor_obrigatorio
    def autentica_entrada():
        usuario = getattr(g, "current_user", None) # dados do usuário
        return render_template('autentica-entrada.html', usuario=usuario)
    
    # API que retorna ficha + exercicios
    @staticmethod
    @autenticado
    @gestor_obrigatorio
    def api_ficha(ficha_id: int):
        ficha = g.models.ficha.listar_por_id(ficha_id)
        if not ficha:
            return jsonify({"error": "Ficha não encontrada"}), 404
        exercicios = g.models.exercicio.listar_por_ficha(ficha_id)
        return jsonify({"ficha": ficha, "exercicios": exercicios})
    
    # tela de gerenciamento de fichas - exclusiva do gestor
    @staticmethod
    @autenticado
    @gestor_obrigatorio
    def fichas_gestor():
        fichas = g.models.ficha.get_all()
        exercicios = g.models.exercicio.get_all()
        usuario = getattr(g, "current_user", None) # dados do usuário
        return render_template('fichas-gestor.html', usuario=usuario, fichas=fichas, exercicios=exercicios)
    
    @staticmethod
    @autenticado
    @gestor_obrigatorio
    def cadastro_ficha_gestor():
        if request.method == 'GET':
            alunos = g.models.aluno.get_all()
            personals = g.models.personal.get_all()
            equipamentos = g.models.equipamento.listar_disponiveis()
            usuario = getattr(g, "current_user", None) # dados do usuário

            return render_template(
                'cadastro-ficha-gestor.html',
                usuario=usuario,
                equipamentos=equipamentos,
                personals=personals,
                alunos=alunos
            )
        
        # POST: processar cadastro de ficha
        aluno_id = request.form.get('aluno_id', '')
        personal_id = request.form.get('personal_id', '')
        descricao = request.form.get('descricao', '').strip()

        # Processar exercícios (agora vem como array)
        exercicios_data = request.form.to_dict(flat=False)
        exercicios = []

        # Se houver exercicios[0][nome], exercicios[1][nome], etc.
        i = 0
        while f'exercicios[{i}][nome]' in exercicios_data:
            exercicio = {
                'nome': exercicios_data[f'exercicios[{i}][nome]'][0],
                'equipamento_id': exercicios_data[f'exercicios[{i}][equipamento_id]'][0],
                'series': exercicios_data[f'exercicios[{i}][series]'][0],
                'repeticoes': exercicios_data[f'exercicios[{i}][repeticoes]'][0],
                'carga': exercicios_data[f'exercicios[{i}][carga]'][0],
                'tempo_descanso': exercicios_data[f'exercicios[{i}][tempo_descanso]'][0],
                'observacoes': exercicios_data.get(f'exercicios[{i}][observacoes]', [''])[0]
            }
            exercicios.append(exercicio)
            i += 1

        # Se não houver array format, pega os valores diretos (primeiro exercício)
        if not exercicios:
            exercicio = {
                'nome': request.form.get('nome', ''),
                'equipamento_id': request.form.get('equipamento_id', ''),
                'series': request.form.get('series', ''),
                'repeticoes': request.form.get('repeticoes', ''),
                'carga': request.form.get('carga', ''),
                'tempo_descanso': request.form.get('tempo_descanso', ''),
                'observacoes': request.form.get('observacoes', '')
            }
            exercicios.append(exercicio)

        # Validação básica
        if not aluno_id or not personal_id or not exercicios:
            flash("Preencha todos os campos obrigatórios e adicione ao menos um exercício.", "error")
            return redirect(url_for('cadastro-ficha-gestor'))
        
        try:
            # Criar a ficha
            ficha_data = {
                'aluno_id': aluno_id,
                'personal_id': personal_id,
                'descricao': descricao
            }
            ficha_model = g.models.ficha
            ficha_id = ficha_model.create(ficha_data)

            # Criar os exercícios vinculados à ficha
            exercicio_model = g.models.exercicio
            exercicios_criados = 0
            
            for ex in exercicios:
                # Adicionar o ficha_id a cada exercício
                ex['ficha_id'] = ficha_id
                exercicio_model.create(ex)
                exercicios_criados += 1

            flash(f"Ficha cadastrada com sucesso! {exercicios_criados} exercício(s) adicionado(s).", "success")
            return redirect(url_for('fichas-gestor'))
        
        except ErroDadosInvalidos as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro-ficha-gestor'))
        except Exception as e:
            print(f"Erro ao cadastrar ficha: {e}")
            import traceback
            traceback.print_exc()
            flash("Erro ao realizar cadastro. Tente novamente.", "error")
            return redirect(url_for('cadastro-ficha-gestor'))