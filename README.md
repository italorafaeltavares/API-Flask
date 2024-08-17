
# API de Upload e Avaliação

Este projeto é uma API desenvolvida como parte da disciplina de **Interface de Programação de Aplicações (API) e Web Services** durante minha pós-graduação em **SRE (Site Reliability Engineering)**. A API permite o upload de arquivos CSV, a conversão desses arquivos para JSON e o armazenamento das avaliações contidas nos arquivos em um banco de dados SQLite.

## Funcionalidades

- **Geração e Validação de Tokens**: A API gera tokens de autenticação que devem ser incluídos nos cabeçalhos das requisições para acessar os endpoints protegidos.
- **Upload de Arquivos CSV**: Aceita arquivos CSV, converte-os para JSON e armazena os dados em um banco de dados.
- **Consulta de Avaliações**: Permite a consulta de todas as avaliações armazenadas no banco de dados.

## Estrutura do Projeto

- `app.py`: Arquivo principal que contém a definição da API e todas as suas funcionalidades.
- `demo.db`: Banco de dados SQLite onde as avaliações são armazenadas.
- `uploads/`: Diretório onde os arquivos CSV e JSON são armazenados após o upload.

## Endpoints

### 1. Gerar Token

**URL**: `/token`  
**Método**: `POST`  
**Descrição**: Gera um token de autenticação que deve ser usado nos demais endpoints.

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/token -H "Content-Type: application/json" -d '{"user_id": "12345"}'
```

**Resposta**:
```json
{
  "token": "eyJ1c2VyIjoiMTIzNDUifQ.ZsCIiQ.fNp3n3BtbIeM4nlB6qU0sXiX_KE"
}
```

### 2. Upload de Arquivo CSV

**URL**: `/upload`  
**Método**: `POST`  
**Descrição**: Recebe um arquivo CSV, converte para JSON e armazena as avaliações no banco de dados.

**Requisitos**:  
- Cabeçalho de autorização: `Authorization: Bearer <token>`

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/upload -H "Authorization: Bearer <seu_token>" -F "file=@caminho/do/arquivo.csv"
```

**Resposta**:
```json
[
    {
        "nome": "João Silva",
        "data": "2024-08-15",
        "quarto": "101",
        "avaliacao": "Excelente",
        "nota": 10
    },
    ...
]
```

### 3. Listar Avaliações

**URL**: `/avaliacoes`  
**Método**: `GET`  
**Descrição**: Retorna uma lista de todas as avaliações armazenadas no banco de dados.

**Requisitos**:  
- Cabeçalho de autorização: `Authorization: Bearer <token>`

**Exemplo de Requisição**:
```bash
curl -X GET http://localhost:5000/avaliacoes -H "Authorization: Bearer <seu_token>"
```

**Resposta**:
```json
[
    {
        "id": 1,
        "nome": "João Silva",
        "data": "2024-08-15",
        "quarto": "101",
        "avaliacao": "Excelente",
        "nota": 10
    },
    ...
]
```

## Configuração do Ambiente

### Pré-requisitos

- Python 3.x
- Flask
- Pandas
- Cachelib

### Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/italorafaeltavares/CSV2ReviewAPI.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd nome-do-repositorio
    ```
3. Crie um ambiente virtual e ative-o:
    ```bash
    python3  -m venv .venv
    source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`
    ```
4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
5. Execute a aplicação:
    ```bash
    python3 app.py
    ```

### Estrutura do Banco de Dados

A API utiliza um banco de dados SQLite com a seguinte estrutura:

- **Tabela `AVALIACOES`**:
  - `id`: Identificador único da avaliação.
  - `nome`: Nome do avaliador.
  - `data`: Data da avaliação.
  - `quarto`: Número do quarto avaliado.
  - `avaliacao`: Comentário sobre a avaliação.
  - `nota`: Nota dada pelo avaliador.

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests caso encontre bugs ou tenha sugestões de melhorias.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).
