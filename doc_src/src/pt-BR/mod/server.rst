Guia do servidor independente
=============================

.. contents::

Introdução
----------

Este guia explica como instalar um servidor independente e público. Um servidor público permite que qualquer jogador crie partidas.


Instalação a partir do código-fonte
-----------------------------------

- Método por arquivo:
    - Baixe o arquivo-fonte da versão mais recente em https://github.com/soundmud/soundrts/releases/latest
    - Descompacte o arquivo na pasta de sua escolha.
- Método Git:
    - para instalar a v1.3.2:
        - git clone https://github.com/soundmud/soundrts.git
        - git checkout v1.3.2
    - depois, para atualizar para a v1.3.3:
        - git fetch
        - git checkout v1.3.3
- Crie uma pasta vazia chamada "user" na pasta principal.
- Instale Python 3.7 ou posterior.
- Inicie o servidor: python server.py
- Isso gerará "user/SoundRTS.ini".
- Pressione Control+C para fechar o servidor.
- Edite o "user/SoundRTS.ini" recém-criado:
    - Defina "login" como o nome do servidor.
    - Defina "require_humans" como 1 se quiser apenas partidas com pelo menos 2 jogadores humanos.
- Inicie o servidor: python server.py
- Certifique-se de que o servidor está acessível de fora.


Como tornar o servidor acessível de fora
----------------------------------------

Na maioria dos casos você precisará configurar o roteador para encaminhar conexões TCP de entrada pela porta 2500 para o endereço IP local do servidor.

Também pode ser necessário configurar o DHCP no roteador para que o servidor tenha sempre o mesmo IP local.

Se estiver atrás de um firewall, pode ser necessário permitir conexões TCP de entrada pela porta 2500.


Como verificar se o servidor está acessível de fora
---------------------------------------------------

Para verificar se o servidor está acessível de fora da rede local, espere um jogador conectar ou, idealmente, peça a um amigo para conectar de fora.

Como último recurso, você também pode usar um site testador de port forwarding (pesquise "port forwarding tester", por exemplo). Cuidado: não posso garantir que esse tipo de site não seja malicioso! O site não deve exigir que você instale uma ferramenta, por exemplo.


A lista de servidores
---------------------

A lista de servidores é hospedada pelo metaserver.

Assim que o servidor for iniciado, ele deve ser incluído automaticamente na lista. Isso não significa que o servidor esteja acessível de fora.

Após ser parado, o servidor desaparecerá automaticamente da lista. Isso pode demorar um pouco.


O parâmetro require_humans em SoundRTS.ini
------------------------------------------

Valor padrão: 0

Se require_humans for 1, o servidor não deixará o criador da partida convidar computadores até que pelo menos dois jogadores humanos estejam registrados.

Apenas servidores públicos são afetados por este parâmetro.
