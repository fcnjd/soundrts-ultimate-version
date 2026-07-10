Guía del servidor independiente
===============================

.. contents::

Introducción
------------

Esta guía explica cómo instalar un servidor independiente y público. Un servidor público permite que cualquier jugador cree partidas.

Instalación desde el código fuente
----------------------------------

- Método por archivo:
    - Descarga el archivo fuente de la última versión desde https://github.com/soundmud/soundrts/releases/latest
    - Descomprime el archivo en la carpeta que elijas.
- Método Git:
    - para instalar v1.3.2:
        - git clone https://github.com/soundmud/soundrts.git
        - git checkout v1.3.2
    - más tarde, para actualizar a v1.3.3:
        - git fetch
        - git checkout v1.3.3
- Crea una carpeta vacía llamada "user" en la carpeta principal.
- Instala Python 3.7 o posterior.
- Arranca el servidor: python server.py
- Esto generará "user/SoundRTS.ini".
- Pulsa Control+C para cerrar el servidor.
- Edita el "user/SoundRTS.ini" recién creado:
    - Establece "login" al nombre del servidor.
    - Establece "require_humans" a 1 si quieres solo partidas con al menos 2 jugadores humanos.
- Arranca el servidor: python server.py
- Asegúrate de que tu servidor sea accesible desde fuera.

Cómo hacer que tu servidor sea accesible desde fuera
----------------------------------------------------

En la mayoría de los casos tendrás que configurar tu router para reenviar las conexiones TCP entrantes por el puerto 2500 a la dirección IP local de tu servidor.

También puede que tengas que configurar el DHCP del router para que tu servidor tenga siempre la misma dirección IP local.

Si estás detrás de un cortafuegos, puede que tengas que permitir las conexiones TCP entrantes por el puerto 2500.

Cómo comprobar si tu servidor es accesible desde fuera
------------------------------------------------------

Para comprobar si tu servidor es accesible desde fuera de tu red local, espera a que un jugador se conecte, o idealmente pide a un amigo que se conecte desde fuera.

Como último recurso, también puedes usar un sitio web de prueba de reenvío de puertos (busca "port forwarding tester", por ejemplo). Ten cuidado: ¡no puedo garantizar que ese tipo de sitio no sea malicioso! El sitio no debería pedirte que instales una herramienta, por ejemplo.

La lista de servidores
----------------------

La lista de servidores la aloja el metaserver.

En cuanto tu servidor arranca, debería incluirse automáticamente en la lista. Eso no significa que tu servidor sea accesible desde fuera.

Tras detenerse, el servidor desaparecerá automáticamente de la lista. Puede tardar un poco.

El parámetro require_humans en SoundRTS.ini
-------------------------------------------

Valor por defecto: 0

Si require_humans está en 1, el servidor no permitirá que el creador de la partida invite a ordenadores hasta que al menos dos jugadores humanos estén registrados.

Solo los servidores públicos se ven afectados por este parámetro.
