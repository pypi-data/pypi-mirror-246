===================
atsphinx-color-text
===================

Overview
========

This is Sphinx extension to render colored-text by HTML builder.

Getting started
===============

Thi is published on PyPI.
You can install by ``pip`` command.

.. code:: console

   pip install atsphinx-color-text

Insert extension into your ``conf.py`` to enable it.

.. code:: python

   extensions = [
       "atsphinx.color_text",
   ]

Usage
=====

You can use this very easy.
Write ``color:~`` role into your reStructuredText source.

Example
-------

.. code:: rst

   sphinx-revealjs is presentation library for
   Pythonista using reStructuredText and :color:red:`Sphinx`.

Builder generates html from this source.

  sphinx-revealjs is presentation library for Pythonista using reStructuredText and :color:red:`Sphinx`.

Supporting colors
=================

|THIS| refers Standard colors from `MDN`_ to implement named color roles.

.. list-table::
   :header-rows: 1

   * - role
     - color code
   * - ``:color:black:``
     - :color:black:`#000000`
   * - ``:color:silver:``
     - :color:silver:`#c0c0c0`
   * - ``:color:gray:``
     - :color:gray:`#808080`
   * - ``:color:white:``
     - :color:white:`#ffffff`
   * - ``:color:maroon:``
     - :color:maroon:`#800000`
   * - ``:color:red:``
     - :color:red:`#ff0000`
   * - ``:color:purple:``
     - :color:purple:`#800080`
   * - ``:color:fuchsia:``
     - :color:fuchsia:`#ff00ff`
   * - ``:color:green:``
     - :color:green:`#008000`
   * - ``:color:lime:``
     - :color:lime:`#00ff00`
   * - ``:color:olive:``
     - :color:olive:`#808000`
   * - ``:color:yellow:``
     - :color:yellow:`#ffff00`
   * - ``:color:navy:``
     - :color:navy:`#000080`
   * - ``:color:blue:``
     - :color:blue:`#0000ff`
   * - ``:color:teal:``
     - :color:teal:`#008080`
   * - ``:color:aqua:``
     - :color:aqua:`#00ffff`

.. _MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/named-color
