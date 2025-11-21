# 🚀 GUIA DE INÍCIO RÁPIDO

## Executar o Projeto Completo

### Opção 1: Script Automático (Uma Janela)

Executa Backend e Frontend na mesma janela com logs integrados:

```powershell
.\start.ps1
```

**Características:**
- ✅ Verifica dependências automaticamente
- ✅ Instala o que estiver faltando
- ✅ Exibe logs de ambos os serviços
- ✅ Pressione `Ctrl+C` para parar tudo

---

### Opção 2: Janelas Separadas

Abre Backend e Frontend em janelas separadas do PowerShell:

```powershell
.\start-separate.ps1
```

**Características:**
- ✅ Backend em uma janela
- ✅ Frontend em outra janela
- ✅ Logs separados para cada serviço
- ✅ Feche as janelas para parar

---

## Primeira Execução

### 1. Verificar Pré-requisitos

```powershell
# Verificar Python
python --version
# Deve ser 3.8+

# Verificar Node.js
node --version
# Deve ser 16+
```

### 2. Executar

```powershell
# Na raiz do projeto
.\start.ps1
```

O script irá configurar tudo automaticamente!

---

## URLs dos Serviços

Após iniciar, acesse:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost:3000 | Interface do usuário |
| **Backend API** | http://localhost:8000 | API REST |
| **Documentação** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |

---

## Primeiro Acesso

1. ✅ Abra http://localhost:3000
2. ✅ Clique em "Cadastre-se"
3. ✅ Preencha seus dados
4. ✅ Faça login
5. ✅ Crie uma conta bancária
6. ✅ Faça um depósito
7. ✅ Explore as funcionalidades!

---

## Parar os Serviços

### Se usou `start.ps1`:
- Pressione `Ctrl+C` na janela do PowerShell

### Se usou `start-separate.ps1`:
- Feche as janelas do Backend e Frontend

---

## Problemas Comuns

### "Python não encontrado"
```powershell
# Instale Python de: https://python.org
# Marque a opção "Add to PATH" durante instalação
```

### "Node.js não encontrado"
```powershell
# Instale Node.js de: https://nodejs.org
# Escolha a versão LTS (recomendada)
```

### "Porta 8000 ou 3000 já em uso"
```powershell
# Parar processo na porta 8000
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force

# Parar processo na porta 3000
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force
```

### Backend não encontra módulos
```powershell
cd Backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend não encontra módulos
```powershell
cd Frontend
Remove-Item -Recurse -Force node_modules
npm install
```

---

## Estrutura de Pastas

```
Digital Superbank/
│
├── start.ps1              ← Execute este (opção 1)
├── start-separate.ps1     ← Ou este (opção 2)
├── README.md              ← Documentação completa
│
├── Backend/               ← API FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── src/
│
└── Frontend/              ← App React
    ├── package.json
    ├── vite.config.js
    └── src/
```

---

## Desenvolvimento

### Backend (FastAPI)

```powershell
cd Backend
.\.venv\Scripts\Activate.ps1
python main.py
```

### Frontend (React)

```powershell
cd Frontend
npm run dev
```

---

## Build para Produção

### Backend
```powershell
cd Backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```powershell
cd Frontend
npm run build
# Arquivos em: dist/
```

---

## Comandos Úteis

### Backend

```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar com reload
uvicorn main:app --reload

# Executar testes
pytest
```

### Frontend

```powershell
# Instalar dependências
npm install

# Desenvolvimento
npm run dev

# Build
npm run build

# Preview build
npm run preview

# Lint
npm run lint
```

---

## 🎯 Próximos Passos

1. ✅ Execute `.\start.ps1`
2. ✅ Acesse http://localhost:3000
3. ✅ Cadastre um usuário
4. ✅ Explore o sistema!

---

**Dúvidas?** Consulte o [README.md](./README.md) completo.

**Pronto para começar?** Execute: `.\start.ps1` 🚀
