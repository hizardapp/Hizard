# Kanban
# ------

# Reference jQuery.
$ = jQuery

# Provide the board div as the initial selector.
$.fn.extend
  kanban: (options) ->
    # Used to know if we need to update the stages as well
    differentSortable = false

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
      receive: (event, ui) ->
        differentSortable = true
      stop: (event, ui) ->
        _savePositions ui.item.parent()
      others:
        containerClass: 'kanban-list-cards'
        columnClass: 'kanban-list'
        columnHeaderClass: 'kanban-list-header'
        cardClass: 'kanban-card'
        data: null
        updatePositionsURL: ''

    # Merge default settings with options recursively (the true argument)
    settings = $.extend true, settings, options

    # Do an ajax call to save the positioning on the server
    _savePositions = ($column) ->
      # Only put the stage if it changed column
      data =
        stage: if differentSortable then $column.data 'stage-id' else null
        positions: []

      for card, i in $column.children()
        data.positions.push [$(card).data('id'), i]

      # Some troubles with nested arrays so jsonize it first
      dataToSend =
        data: JSON.stringify(data)

      differentSortable = false

      $.post settings.others.updatePositionsURL,
        dataToSend,
        (result) ->
          # TODO: display errors
          true


    # Calls .sortable and setup the callbacks
    @each ()->
      $('.' + settings.others.containerClass).sortable settings
