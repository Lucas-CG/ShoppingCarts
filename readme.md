# Shopping Carts

O código lê 1 ou mais arquivos .json com registros de acessos a páginas de produtos e carrinhos de compras, *localizados na pasta input*, registrando na sua saída carrinhos de compras que expiraram (**o usuário adicionou pelo menos um item ao seu carrinho - realizou o fluxo entre as páginas "product" e "basket" para um produto - e não realizou mais nenhuma interação por 10 ou mais minutos**).

A saída é registrada na pasta *output*. Exemplos de arquivos de entrada e saída foram adicionados às duas pastas.

Os arquivos de entrada esperados contêm multiplas linhas no formato do exemplo abaixo:

`{"timestamp": "2019-01-01 13:02:00", "customer": "customer-x", "product": "product-x"}`

Permite-se que o usuário adicione mais de um item ao seu carrinho.

## Requisitos

O projeto foi desenvolvido em *Python 3* com a biblioteca *Apache Beam*.

Portanto, é necessário que ambos estejam instalados no seu sistema, além do gerenciador de pacotes *pip3*. Caso não estejam, utilize os seguintes comandos:

### Python3:

Instale-o com o seu gerenciador de pacotes. Seguem alguns exemplos para diferentes plataformas.

#### Ubuntu/Debian

`apt install python3 python3-pip`

#### Fedora/Red Hat

`dnf install python3 python3-pip`

#### Mac

`brew install python3`

(Certifique-se de que o *brew* esteja instalado)

### Apache Beam

Use o pip3 para instalá-lo:

`pip3 install apache-beam`

### Execução

Para utilizar o executável, faça um *clone* do repositório. Execute o código carts.py. Não é necessário especificar argumentos na linha de comando:

`python3 carts.py`

### Verificação dos resultados:

Como mencionado, basta ler o arquivo JSON gerado na pasta *output*.

Há dois arquivos de entrada, nomeados *page-views.json* e *page-views2.json*, localizados na pasta input. O segundo arquivo foi adicionado para testar o segundo critério de expiração do carrinho: caso um novo acesso ao site tenha sido feito depois de 10 ou mais minutos, o carrinho expira mesmo assim.

A lida deles mostra que as linhas de saída esperadas são:

`{"timestamp": "2019-01-01 13:02:00", "customer": "customer-2", "product": "product-2"}`
`{"timestamp": "2019-01-01 16:30:00", "customer": "customer-4", "product": "product-2, product-3"}`

Isto poderá ser analisado com uma nova execução do código.
