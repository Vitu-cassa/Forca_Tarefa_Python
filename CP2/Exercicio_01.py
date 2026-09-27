
perfis = {
    "credenciais_do_SOC":      {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":False, "tolera_atraso_de_consistencia":False, "dado_sensivel":True},
    "telemetria_de_sensores":  {"schema_fixo":False, "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":True,  "dado_sensivel":False},
    "trilha_de_auditoria":     {"schema_fixo":False, "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":False, "dado_sensivel":True},
    "carrinho_de_licencas":    {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":False, "tolera_atraso_de_consistencia":False, "dado_sensivel":False},
    "cache_de_sessoes":        {"schema_fixo":True,  "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":True,  "dado_sensivel":True},
    }

perfil_teste = {
    "Testes_de_Funcionalidade": {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":True, "tolera_atraso_de_consistencia":True, "dado_sensivel":True}
                }
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
''' Exercício 1 — Assistente de decisão de armazenamento (Aulas 1 e 8):
        Escreva recomendar(perfil) que recebe o perfil de um conjunto de dados
        e devolve uma recomendação fundamentada: qual banco usar, qual lado do
        CAP priorizar e qual risco OWASP a escolha errada cria. Nada de if solto
        no meio do código — a função precisa explicar a decisão.

        # Entrada: dict com as chaves
        #   schema_fixo (bool), precisa_acid (bool), escala_horizontal (bool),
        #   tolera_atraso_de_consistencia (bool), dado_sensivel (bool)
        #
        # Saída: dict {"banco": "MySQL"|"MongoDB", "cap": "CP"|"AP",
        #              "justificativa": str, "risco_owasp": str}

        perfis = {
        "credenciais_do_SOC":      {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":False, "tolera_atraso_de_consistencia":False, "dado_sensivel":True},
        "telemetria_de_sensores":  {"schema_fixo":False, "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":True,  "dado_sensivel":False},
        "trilha_de_auditoria":     {"schema_fixo":False, "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":False, "dado_sensivel":True},
        "carrinho_de_licencas":    {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":False, "tolera_atraso_de_consistencia":False, "dado_sensivel":False},
        "cache_de_sessoes":        {"schema_fixo":True,  "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":True,  "dado_sensivel":True},
        }

        # Saída esperada (formato; as justificativas são suas):
        # credenciais_do_SOC     -> MySQL   | CP | "autenticar errado é pior que ficar fora do ar" | A07
        # telemetria_de_sensores -> MongoDB | AP | "perder 1s de log < parar de aceitar log"       | A09
        # trilha_de_auditoria    -> MongoDB | CP | "auditoria divergente não vale como prova"      | A08
        # ...
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _recomendar(perfis):
    for nome, itens in perfis.items():
        perfil = nome
        parametros = itens

        avaliacao = _avaliador(parametros)
        
        _formatador(perfil, avaliacao)

def _avaliador(parametros):
    try:
        avaliacao = {
            "sql": None,
            "nosql": None,
            "cap": None,
            "owasp": None,
            "justificativa": None
        }

        schema = parametros["schema_fixo"]
        acid = parametros["precisa_acid"]
        escala = parametros["escala_horizontal"]
        atraso_consistencia = parametros["tolera_atraso_de_consistencia"]
        dado_sensivel = parametros["dado_sensivel"]

        # Decide o banco
        avaliacao["sql"] = (True if acid or (dado_sensivel and schema and atraso_consistencia) else False)
        avaliacao["nosql"] = (False if avaliacao["sql"] == True else True)

        # Avalia o CAP
        avaliacao["cap"] = ("CP" if acid or dado_sensivel else "AP")


        # Avalia o OWASP considerando as escolhas erradas
        avaliacao["owasp"] = (
            "A04" if acid and not avaliacao["sql"] else
            "A03" if schema and not avaliacao["sql"] else
            "A02" if dado_sensivel and not avaliacao["sql"] else
            "A05" if not avaliacao["nosql"] and escala else
            "A01" if not avaliacao["nosql"] and atraso_consistencia else
            "Verificar caso no OWASP."
        )

        # Justificativa
        avaliacao["justificativa"] = (
            "Sistema precisa de bloqueios refinados." if avaliacao["owasp"] == "A04" else
            "Sistema exige rigidez nos dados, permitindo parametrização nas queries." if avaliacao["owasp"] == "A03" else
            "Sistema exige segurança acima de velocidade." if avaliacao["owasp"] == "A02" else
            "O sistema precisa de escalabilidade horizontal, sem abrir brechas na infra-estrutura." if avaliacao["owasp"] == "A05" else
            "A sincronia entre os sitemas deve ser garantida." if avaliacao["owasp"] == "A01" else
            "Verificar caso especifico!"
        )
        return avaliacao
    
    except Exception as e:
        print("Erro nos dados: {}".format(e))

def _formatador(perfil, avaliacao):

    banco = ("MySql" if avaliacao["sql"] else "MongoDB")

# credenciais_do_SOC     -> MySQL   | CP | "autenticar errado é pior que ficar fora do ar" | A07
    print("{:<25} -> {:<8} | {:^4} | {:<85} | {:^5} ".format(perfil, banco, avaliacao["cap"], avaliacao["justificativa"], avaliacao["owasp"]))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
try:
    _recomendar(perfis)
except Exception as e:
    print("Erro na avaliação: {}".format(e))