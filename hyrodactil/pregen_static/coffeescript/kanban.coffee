# Kanban
# ------

# Reference jQuery.
$ = jQuery

# Provide the board div as the initial selector.
$.fn.extend
  kanban: (options) ->
    # Default settings.
    # Contains jquery ui sortable settings.
    # The 'others' object contain options not for jquery ui.
    settings =
      opacity: 0.8
      containment: 'document'
      cursor: 'move'
      distance: 5
      zIndex: 7777
      connectWith: '.kanban-list-cards'
      change: (event, ui) ->
        ui.placeholder.addClass 'kanban-card-placeholder'
      others:
        containerClass: 'kanban-list-cards'
        columnClass: 'kanban-list'
        columnHeaderClass: 'kanban-list-header'
        cardClass: 'kanban-card'
        data: null

    # Merge default settings with options recursively (the true argument)
    settings = $.extend true, settings, options

    # Creates the DOM for a column in the board and returns the jquery object
    # representing it
    _createColumn = (title) ->
      column = "<div class='#{settings.others.columnClass}'>"

      column += "<div class='#{settings.others.columnHeaderClass}'>"
      column += "<h2>#{title}</h2>"
      column += "<div class='#{settings.others.containerClass}'>"
      column += "</div>"
      column += "</div>"

      column += "</div>"

      $(column)

    # Called if some initial has been provided
    load = ($board) ->
      boardContent = ''
      for number, column of settings.others.data
        $column = _createColumn column.name

        for position, card of column.cards
          $container = $column.find('.' + settings.others.containerClass)
          $container.append $(card.content)

        console.log $column

    # Calls .sortable and setup the callbacks
    @each ()->
      others = settings.others

      if others.data?
        $(this).html others.data

      delete settings.others

      $('.' + others.containerClass).sortable settings
