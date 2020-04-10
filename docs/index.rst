:orphan:

.. include:: ../README.rst


First steps
===========

Here is a basic example of how to create a menu using ``pygame-menu``.

.. code-block:: python

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    surface = pygame.display.set_mode((400, 600))

    menu = pygameMenu.Menu(surface,
                           pygameMenu.font.FONT_BEBAS,
                           "My first menu")

    while True:

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        menu.mainloop(events)

        # Flip surface
        pygame.display.flip()


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: First steps

   _source/menu
   _source/add_widgets
   _source/gallery


Widgets API
===========

Each widget is an class that can be inserted in a menu. However
they could be used has it to design custom menu layout.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Widgets API

   _source/widget_button
   _source/widget_colorinput
   _source/widget_label
   _source/widget_menubar
   _source/widget_scrollbar
   _source/widget_selector
   _source/widget_textinput


About pygame-menu
=================

This project does not have a mailing list and so the issues tab should
be the first point of contact if wishing to discuss the project. If you
have questions that you do not feel are relavent to the issues tab or
just want to let me know what you think about the library, feel free to
email me.

Author email: pablo@ppizarror.com

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: About pygame-menu

   _source/license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`