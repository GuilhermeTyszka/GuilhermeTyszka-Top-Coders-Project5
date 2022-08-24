from flask import Flask, render_template, request
from sqlalchemy import create_engine, text



app = Flask(__name__)
app.debug = True
db_url = "mssql+pymssql://sa:senh4forte@localhost:55949/db_lufalufa"
# A cadeia de conexao é formada por dialect[+driver]://user:password@host:port/dbname
engine = create_engine(db_url, pool_size=5, pool_recycle=3600)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/alunos')
def alunos():
    conn = engine.connect()
    sql_text = text("SELECT * FROM dbo.Alunos ORDER BY Nome")
    query = conn.execute(sql_text)
    return render_template('alunos.html', alunos=query)

@app.route('/professores')
def professores():
    conn = engine.connect()
    sql_text = text("SELECT * FROM dbo.Professores ORDER BY Nome")
    query = conn.execute(sql_text)
    return render_template('professores.html', professores=query)

@app.route('/empresas')
def empresas():
    conn = engine.connect()
    sql_text = text("SELECT * FROM dbo.EmpresasParceiras ORDER BY NomeEmpresa")
    query = conn.execute(sql_text)
    return render_template('empresas.html', empresas=query)

@app.route('/cursos')
def cursos():
    conn = engine.connect()
    sql_text = text("SELECT Cursos.NomeCurso, Disciplinas.NomeDisciplina, Disciplinas.CargaHoraria FROM Cursos INNER JOIN CursosDisciplinas ON Cursos.idCurso = CursosDisciplinas.idCurso INNER JOIN Disciplinas ON CursosDisciplinas.idDisciplina = Disciplinas.idDisciplina ORDER BY NomeCurso")
    query = conn.execute(sql_text)
    return render_template('cursosdisciplinas.html', cursos=query)

@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

@app.route('/consultas/consultaQ1')
def consultaQ1():
    conn = engine.connect()
    sql_text = text("SELECT Matriculas.idMatricula, Nome, Nota FROM Alunos INNER JOIN Matriculas on Matriculas.idAluno = Alunos.idAluno INNER JOIN NOTAS ON Notas.idMatricula = Matriculas.idMatricula WHERE Nota >= 8.5 ORDER BY Nota DESC")
    query = conn.execute(sql_text)
    return render_template('consultaQ1.html', alunos=query)

@app.route('/consultas/consultaQ2')
def consultaQ2():
    conn = engine.connect()
    sql_text = text("SELECT DISTINCT(EmpresasParceiras.NomeEmpresa) AS Empresa, count(Turmas.idEmpresa) AS Qtde_Turmas FROM EmpresasParceiras FULL OUTER JOIN Turmas ON EmpresasParceiras.idEmpresa = Turmas.idEmpresa GROUP BY EmpresasParceiras.NomeEmpresa;")
    query = conn.execute(sql_text)
    return render_template('consultaQ2.html', empresas=query)

@app.route('/consultas/consultaQ3')
def consultaQ3():
    conn = engine.connect()
    sql_text = text("SELECT Nome, NomeDisciplina, 'Professor Titular' AS Tipo FROM Disciplinas INNER JOIN Professores ON Disciplinas.idProfessor = Professores.idProfessor UNION ALL SELECT Nome, NomeDisciplina, 'Professor Auxiliar' AS Tipo FROM Disciplinas INNER JOIN Professores ON Disciplinas.idProfessorAux = Professores.idProfessor ORDER BY Nome;")
    query = conn.execute(sql_text)
    return render_template('consultaQ3.html', professores=query)


@app.route("/consultaQ4/", methods=['GET'])
def consultaQ4():
    name = request.args.get('empresa', None)
    conn = engine.connect()
    sql_text = text(f"SELECT Nome FROM dbo.EmpresasParceiras INNER JOIN dbo.Turmas ON dbo.EmpresasParceiras.idEmpresa = dbo.Turmas.idEmpresa INNER JOIN dbo.Matriculas ON dbo.Turmas.idTurma = dbo.Matriculas.idTurma INNER JOIN dbo.Alunos ON dbo.Alunos.idAluno = dbo.Matriculas.idAluno WHERE NomeEmpresa = '{name}';")
    query = conn.execute(sql_text)
    return render_template('consultaQ4.html', empresas=query, name=name)

@app.route('/consultas/consultaQ5')
def consultaQ5():
    conn = engine.connect()
    sql_text = text("SELECT DISTINCT NomeDisciplina FROM Notas INNER JOIN Disciplinas ON Notas.idDisciplina = Disciplinas.idDisciplina WHERE Notas.Nota < 7.0;")
    query = conn.execute(sql_text)
    return render_template('consultaQ5.html', disciplinas=query)

@app.route("/consultaQ6/", methods=['GET'])
def consultaQ6():
    name = request.args.get('empresa', None)
    conn = engine.connect()
    sql_text = text(f"SELECT SUM(Preco*Vagas) AS CustoFormacao FROM dbo.EmpresasParceiras INNER JOIN dbo.Turmas ON dbo.EmpresasParceiras.idEmpresa = dbo.Turmas.idEmpresa INNER JOIN dbo.Cursos ON dbo.Cursos.idCurso = dbo.Turmas.idCurso WHERE NomeEmpresa = '{name}';")
    query = conn.execute(sql_text)
    return render_template('consultaQ6.html', empresas=query, name=name)

@app.route('/consultas/consultaQ7')
def consultaQ7():
    conn = engine.connect()
    sql_text = text("SELECT EmpresasParceiras.NomeEmpresa AS Empresa, Turmas.DataInicio, NomeProcessoSeletivo FROM EmpresasParceiras FULL OUTER JOIN Turmas ON EmpresasParceiras.idEmpresa = Turmas.idEmpresa GROUP BY EmpresasParceiras.NomeEmpresa, Turmas.DataInicio, NomeProcessoSeletivo;")
    query = conn.execute(sql_text)
    return render_template('consultaQ7.html', empresas=query)

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run()
