window.Hizard ?= {}

CompanySettings = (postURL, deleteURL, upURL, downURL) ->
  # Things that never change
  $saveButton = $('.save')
  $alert = undefined

  # Getting all the divs/info necessary for a given page
  currentUrl = document.URL

  pages = ['questions', 'stages']
  data =
    questions:
      valueNames: ['id', 'name', 'type_field']
    stages:
      valueNames: ['id', 'name']
  currentPage = undefined

  for page in pages
    currentPage = page if currentUrl.indexOf(page) != -1

  unless currentPage
    return

  currentData = data[currentPage]

  # Grabbing form input for this page
  $inputs = ($('.form-' + field) for field in currentData.valueNames)

  # And init the list
  table = new List('sort-table', {valueNames: currentData.valueNames})

  # Events on inputs
  # ----------------------------------------------------------------

  for $input in $inputs
    $input.focus ->
      $input.removeClass 'error'
      $input.next('small').remove()

    $input.keypress (event) ->
      keycode = ((if event.keyCode then event.keyCode else event.which))
      if keycode is 13
        $saveButton.click()
        event.preventDefault()
        event.stopPropagation()


  # Adding/Editing items
  # ----------------------------------------------------------------

  # When you click the edit button, populate form and autofocus
  $('body').on 'click', '.edit', (e) ->
    itemId = $(this).closest('tr').find('.id').text()
    itemValues = table.get('id', itemId).values()
    for $input, i in $inputs
      value = itemValues[currentData.valueNames[i]]
      # Select? need to get the option value
      if $input.is('select')
        value = $input.find('option:contains("' + value + '")').val();

      $input.val(value)

    $inputs[$inputs.length - 1].focus()

  # Call the ajax view on click
  $saveButton.click ->
    isUpdate = true
    object = {}

    for $input, i in $inputs
      object[currentData.valueNames[i]] = $input.val()

    unless object.id
      isUpdate = false
      delete object.id

    # hardcoded relying on name as being required
    return unless object.name

    $.post postURL, object, (data) ->
      if data.result is 'error'
        $input.addClass 'error' for $input in $inputs

        $error = $('<small>').addClass('error')
        for error of data.errors
          $error.text data.errors[error]
        $inputs[$inputs.length - 1].after $error

        if isUpdate
          item = table.get('id', object.id).values()
          for $input, i in $inputs
            $input.val(item[currentData.valueNames[i]])
      else

        # Hardcoded for now
        if currentPage is 'questions'
          object.type_field = $('.form-type_field  option:selected').text()

        for $input in $inputs
          $input.val('')

        object.id = data.id
        if isUpdate
          item = table.get('id', data.id)
          item.values object
        else
          # listjs kinda suck sometimes
          # fail to add if list is empty
          location.reload() if table.items.length is 0
          table.add object

          if currentPage is 'stages'
            changeArrows(object)

      $alert.remove() if $alert
      displayMessage data.result, data.message

  # Fakes a django message
  displayMessage = (type, message) ->
    # We only want one alert showing
    $('div[class^="alert-"]').remove()

    $alert = $('<div>')
    $alert.addClass 'alert-' + type
    $alert.data 'alert', 'js'
    $alert.html message + '<a href=\'#\' class=\'close\'>&times;</a>'
    $alert.prependTo '.container'


  # Delete stuff
  # ---------------------------------------------------
  $('body').on 'click', 'a.delete-link', ->
    link = $(this)
    $tr = link.closest('tr')
    refUrl = deleteURL
    name = $tr.find('.name').text()
    id = $tr.find('.id').text()
    url = refUrl.replace('8888', id)
    $('#delete-confirm-modal').foundation 'reveal', 'open'
    $('#delete-confirm-modal #object-name').text name
    $('#delete-confirm-modal #confirm-delete-link').attr 'href', url

  $('body').on 'click', 'a#cancel-link', ->
    $('#delete-confirm-modal').foundation 'reveal', 'close'

  $('body').on 'click', '.close', ->
    $(this).parent().remove()


  # Reorder stuff for stages
  changeArrows = () ->
    # Adding down arrow to the previous last one
    $table = $('#sort-table')
    $last = $table.find('tr:nth-last-child(2)')
    itemId = $last.find('.id').text()
    url = downURL.replace(0, itemId)
    $last.find('td:first').html '<a href=\'' + url + '\'}\'><i class=\'icon-arrow-down icon-2x\'></i></a>'

    # Swapping arrows for the newly created one
    $new = $table.find('tr:last')
    itemId = $new.find('.id').text()
    url = upURL.replace(0, itemId)
    $new.find('td:nth-child(2)').html '<a href=\'' + url + '\'}\'><i class=\'icon-arrow-up icon-2x\'></i></a>'
    $new.find('td:first').html ''


window.Hizard.CompanySettings = CompanySettings
