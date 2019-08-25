====
psed
====


CLI utility for text search / replace.


Usage example
=============

Input file:

.. code-block::

    [ERROR] Some error
    [INFO] Some info
    [WARNING] Some warning
    [ERROR] Other error
    [ERROR] There's a lot of errors
    [DEBUG] And one debug

Run psed:

.. code-block:: bash:

    psed --input ./sample \
         --find '\[(ERROR)\]' \
         --find '\[(INFO)\]' \
         --find '\[(WARNING)\]' \
         --replace '[LIGHT_\1]'

Output file:

.. code-block::

    [LIGHT_ERROR] Some error
    [LIGHT_INFO] Some info
    [LIGHT_WARNING] Some warning
    [LIGHT_ERROR] Other error
    [LIGHT_ERROR] There's a lot of errors
    [DEBUG] And one debug
