===================
atsphinx-color-text
===================

.. image:: https://img.shields.io/pypi/v/atsphinx-color-text.svg
   :target: https://pypi.org/project/atsphinx-color-text/

.. image:: https://github.com/atsphinx/color-text/actions/workflows/main.yml/badge.svg
   :target: https://github.com/atsphinx/color-text/actions

Text color changer for Sphinx.

Overview
========

This extension adds simple role to set style of text-color for HTML-based builders.

Getting started
===============

.. code:: console

   pip install atsphinx-color-text

.. code:: python

   extensions = [
       "atsphinx.color_text",
   ]

Usage
=====

Write your text with ``:color:`` role.

.. code:: rst

   Your title
   ==========

   sphinx-revealjs is presentation library for Pythonista using reStructuredText and :color:red:`Sphinx`.

When you generate HTML by ``sphinx-build -b html`` ,
"Sphinx" rendered as red color by CSS ( likely ``font-color: red;`` ).

Notes and ToDo
==============

I will not implements all color-names, but plan "RGB code" mode and custom name mode.
