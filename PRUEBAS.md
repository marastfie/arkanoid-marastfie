# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- nivel válido y nivel inexistente;
- nivel con filas de distinta longitud;
- paleta en ambos límites de la pantalla;
- rebote contra pared, paleta y cada tipo de bloque;
- pérdida de una vida y reinicio de la bola;
- victoria al eliminar el último bloque y derrota al agotar vidas;
- salida limpia con Escape y al cerrar la ventana.

Una mejora opcional no debe romper ninguno de estos casos.

## Ejercicios

- **1: cargar_nivel**: Comprueba que el fichero existe, lee las líneas no vacías
  y verifica que todas tienen el mismo ancho. Lanza `FileNotFoundError` o
  `ValueError` si algo falla.
- **2: preparar_entidades**: Ajusta el tamaño de la paleta y la coloca centrada en
  la parte inferior con `midbottom`, reinicia puntuación (0), vidas (3) y mensaje
  final, y coloca la bola justo encima de la paleta con `reiniciar_bola()`.
- **3: crear_bloques**: recorre el nivel carácter a carácter y crea un bloque por
  cada simbolo, guardando su posición, su color y su tipo.
- **4: procesar_input**: mueve la paleta a izquierda o derecha con las flechas
  o con A/D, y evita que se salga de la pantalla por los bordes.
- **5: actualizar_bola**: mueve la bola y la hace rebotar en las paredes, el techo,
  la paleta y los bloques. Al romper un bloque lo elimina y suma sus puntos.
  Si la bola cae se pierde una vida; sin vidas se pierde la partida, y sin
  bloques se gana.
- **6: dibujar_escena**: pinta el fondo, los bloques con su color, la paleta,
  la bola y los marcadores de puntos y vidas, y el mensaje final si lo hay.
- **7: run**: La funcion prepara el juego y repite el bucle principal: lee los eventos
  (salir con Escape o cerrando la ventana), mueve la paleta y la bola y pinta
  la escena. Al ganar o perder muestra el mensaje 2 segundos con el self.esperar(2000) y cierra.

## Pruebas realizadas

Esto son pruebas que he ido realizando a medida que hacia los ejercicios, las primeras con los `print()` de la funcion en el main y despues sobre el juego:

- Nivel válido (`demo.txt`): se cargan 6 filas y se ven 60 bloques.
- Nivel inexistente: sale `FileNotFoundError`.
- Filas de distinta longitud: sale `ValueError`.
- Paleta en los bordes: se para sin salirse por ninguno de los dos lados.
- Rebotes: la bola rebota en paredes, techo, paleta y bloques
- Pérdida de vida: las vidas bajan en 1 y la bola vuelve a la paleta.
- Derrota y victoria: sale el mensaje correspondiente y el juego se cierra.
- Salida: Escape y la ✕ de la ventana cierran el juego sin errores.

## Uso de la IA

Sobre todo ha sido utilizada para hacer el md de una manera mas 'bonita' para que se vea visualmente mejor.
Tambien he sido utilizada en algun momento para el entendimiento de alguna funcion en el arkanoid_core.py.
Y por ultimo me ha ayudado a la creacion de la funcion `actualizar_bola()` debido a que era la mas compleja

He subido todo los cambios a mi repositorio para una mas facil y mejor visualización.