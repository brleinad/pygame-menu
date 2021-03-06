
.. module:: pygameMenu.menu

==============
Creating menus
==============

Ready to go deeper into menu usage?

Configuring the menu
--------------------

The :py:class:`Menu` is the base class to draw the graphical items on
the screen. It offers many parameters to let you adapt the behavior
and the visual aspects of the menu.

The less trivial ones are explained here.

Widgets position
^^^^^^^^^^^^^^^^

By default, the widgets are centered horizontally (``widget_alignment=ALIGN_CENTER``)
and start at 0 pixels below the title bar (``widget_offset_y=O``).

The horizontal alignment can be changed with one of the following values:

==============================================  ========================
Alignment                                       Description
==============================================  ========================
:py:data:`pygameMenu.locals.ALIGN_LEFT`         Left alignment
:py:data:`pygameMenu.locals.ALIGN_CENTER`       Center alignment
:py:data:`pygameMenu.locals.ALIGN_RIGHT`        Right alignment
==============================================  ========================

The vertical alignment can be done after all widgets have been added
to the menu by calling the method :py:meth:`Menu.center_content`:

.. code-block:: python
    :emphasize-lines: 7

    menu = pygameMenu.Menu(...)

    menu.add_text_input(...)
    menu.add_selector(...)
    menu.add_button(...)
    menu.add_button(...)
    menu.center_content()

.. note:: If the menu size is insufficient to show all of the widgets, horizontal
          and/or vertical scrollbar(s) will appear automatically.

Column and row
^^^^^^^^^^^^^^

By default, the widgets are arranged in one unique column. But using the
``columns`` and ``rows`` parameters, it is possible to arrange them in
a grid.

The defined grid of ``columns`` x ``rows`` cells will be completed with
the widgets (in order of definition) **column by column** starting at the
**top-left** corner of the menu.

On-close callback
^^^^^^^^^^^^^^^^^

A callback can be defined using the ``onclose`` parameter. This parameter
can take one of these two types of values:

 - a python callable object (a function, a method, a class, ...)
   that will be called without any arguments.
 - a specific event of :py:mod:`pygameMenu`. The possible events are
   the following:

   ==========================================  ========================================
   Event                                       Description
   ==========================================  ========================================
   :py:data:`pygameMenu.events.BACK`           Go back to the previously opened menu
   :py:data:`pygameMenu.events.DISABLE_CLOSE`  The menu can not be closed
   :py:data:`pygameMenu.events.EXIT`           Exit the program (not only the menu)
   :py:data:`pygameMenu.events.RESET`          Go back to the first opened menu
   ==========================================  ========================================


Display a menu
--------------

The :ref:`First steps` chapter shows the way to execute the menu in the
application, which lets `pygame-menu` manage the event loop by calling
the :py:meth:`Menu.mainloop` :

.. code-block:: python
    :emphasize-lines: 6

    def draw_background():
        ...

    mymenu = Menu(...)

    mymenu.mainloop(surface, bgfun=draw_background)

There is a second way that gives more flexibility to the application
because the events loop remains managed outside of the menu. In this
case the application is in charge to update and draw the menu when
it is necessary.

.. code-block:: python
    :emphasize-lines: 15,16,17

    def draw_background():
        ...

    mymenu = Menu(...)

    while True:

        draw_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mymenu.is_enabled():
            mymenu.update(events)
            mymenu.draw(surface)

        pygame.display.update()


.. Document here only the members relative to the menu itself, members
.. for adding widgets are documented in another chapter.

.. autoclass:: Menu(surface, menu_height, menu_width, font, title, ...)
    :members:
    :exclude-members: add_button, add_color_input, add_image, add_label, add_text_input, add_selector, add_vertical_margin
