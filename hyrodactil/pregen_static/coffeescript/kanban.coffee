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
      stop: (event, ui) ->
        $column = ui.item.parent()

        data =
          stage: $column.data 'stage-id'
          positions: []

        for card, i in $column.children()
          data.positions.push [$(card).data('id'), i]

        _savePositions data
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
    _savePositions = (data) ->
      $.post settings.others.updatePositionsURL,
      {data: JSON.stringify(data)},
        (result) ->
          true


    # Calls .sortable and setup the callbacks
    @each ()->
      $('.' + settings.others.containerClass).sortable settings
