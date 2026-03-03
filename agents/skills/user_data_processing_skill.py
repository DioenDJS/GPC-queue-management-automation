import json
import re
import unicodedata

import ftfy
from langchain.tools import tool


@tool
def user_data_processing_skill(json_erro: str) -> str:
    """
    Expert em Tratamento de Dados de Usuário.
    Use esta skill para corrigir erros comuns de formatação e validação de dados de usuário.

    ESTA FERRAMENTA DEVE RETORNAR O JSON COMPLETO E INTEGRAL CORRIGIDO.

    ESTA FERRAMENTA DEVE PRESERVAR A ESTRUTURA ORIGINAL DO JSON.
    NÃO ALTERE NOMES DE CAMPOS, NÃO REMOVA OBJETOS ANINHADOS.

    INSTRUÇÕES DE ANÁLISE:
    1. Identificar: Verificar os campos 'name', 'email' e 'telefone' no payload.
    2. Corrigir:
       - Para 'name': Remover números e caracteres especiais, mantendo apenas letras e espaços.
            # Exemplos:
            # "J\u00c3\u00bfSSICA" vira "JÉSSICA"
            # "\u0122essiane" vira "Gessiane"
       - Para 'email': Validar o formato do email, garantindo a presença de '@' e um domínio válido, removendo caracteres especiais indevidos.
       - Para 'telefone': Garantir que o campo não esteja vazio ou nulo.

    REGRAS DE RESPOSTA:
    - Retorne sempre o JSON corrigido completo.
    - Informe que esta mensagem deve ser reinserida no INÍCIO do workflow.
    - Forneça uma breve explicação da correção realizada.
    - Preserve a estrutura exata (ex: 'datail_user' deve continuar aninhado).

    IMPORTANTE: O agente não deve resumir este JSON. O output deve conter o
    JSON completo para que possa ser copiado e reprocessado imediatamente.

    ============================================================================
    OUTPUT ESPERADO:
    analise_agent: "foi identificado que o campo 'name' continha caracteres inválidos (números ou caracteres especiais) e foi corrigido para conter apenas letras e espaços. O campo 'email' foi validado e corrigido para um formato válido, removendo caracteres especiais indevidos. O campo 'telefone' foi verificado para garantir que não está vazio ou nulo. Esta mensagem corrigida deve ser reinserida no início do workflow.",
    {
        "user_id": "5daeea3e-7ebb-4173-9184-f231698afcbd",
        "datail_user": {
            "name": "Maria Antonia",
            "email": "maria.antonio@gmail.com"
        },
        "telefone": "1234567890"
    }
    ==============================================================================
    """

    try:
        dados = json.loads(json_erro)

        # Suporta estrutura aninhada (datail_user) ou plana (name/email na raiz)
        nested = "datail_user" in dados
        if nested:
            detail_user = dados.get("datail_user", {})
            nome_original = detail_user.get("name", "")
            email_original = detail_user.get("email", "")
        else:
            nome_original = dados.get("name", "")
            email_original = dados.get("email", "")

        # Suporta tanto "telefone" quanto "telephone"
        telefone_original = dados.get("telefone") or dados.get("telephone") or ""

        # --- CORREÇÃO DE NOME ---
        nome_corrigido = ftfy.fix_text(nome_original)
        nome_corrigido = unicodedata.normalize("NFKC", nome_corrigido)
        nome_corrigido = re.sub(r"[^a-zA-Z\u00C0-\u00FF\s]", "", nome_corrigido)
        nome_corrigido = nome_corrigido.title()
        for prep in [" De ", " Da ", " Do ", " Dos ", " Das ", " E "]:
            nome_corrigido = nome_corrigido.replace(prep, prep.lower())

        # --- CORREÇÃO DE EMAIL ---
        email_limpo = email_original.strip().lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_limpo):
            email_limpo = "revisar_email@pendente.com"

        # --- CORREÇÃO DE TELEFONE ---
        tel_limpo = re.sub(r"\D", "", str(telefone_original))
        if not tel_limpo:
            tel_limpo = "11999999999"  # Telefone ausente — requer revisão manual

        # --- ATUALIZAÇÃO DO OBJETO ---
        if nested:
            dados["datail_user"]["name"] = nome_corrigido.strip()
            dados["datail_user"]["email"] = email_limpo
            dados["telefone"] = tel_limpo
        else:
            dados["name"] = nome_corrigido.strip()
            dados["email"] = email_limpo
            # Preserva o nome original do campo (telephone ou telefone)
            if "telephone" in dados:
                dados["telephone"] = tel_limpo
            else:
                dados["telefone"] = tel_limpo

        analise_msg = (
            "Análise concluída: Caracteres especiais e erros de encoding removidos do nome. "
            "E-mail e telefone normalizados. Este JSON deve ser reinserido no início do workflow."
        )

        return json.dumps(
            {"analise_agent": analise_msg, **dados}, ensure_ascii=False, indent=4
        )

    except json.JSONDecodeError:
        return "Erro Crítico: O input fornecido não é um JSON válido."
    except Exception as e:
        return f"Erro no processamento: {str(e)}"
