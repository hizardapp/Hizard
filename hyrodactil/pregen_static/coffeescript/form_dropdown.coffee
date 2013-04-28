
window.Hizard ?= {}


class FormDropdown
  constructor: (hasErrors, objectId, @createSelector, @updateSelector) ->
    @hasErrors = if hasErrors != '' then true else false
    @objectId = if objectId != '' then parseInt(objectId, 10) else false
    @_setupEvents()

    # If we have errors, find if we attempted a create or and update and
    # auto-display this dropdown
    if @hasErrors
      if @objectId
        $td = $(@updateSelector + "[data-id=" + @objectId + "]")
        @_fillEditDropdown $td
        Foundation.libs.dropdown.toggle $td
      else
        Foundation.libs.dropdown.toggle $(@createSelector)

  # If updating a row, fill the form
  # If creating a record, autofocus the first field
  _setupEvents: () ->
    _fillEditDropdown = @_fillEditDropdown
    _fillCreateDropdown = @_fillCreateDropdown

    $(@updateSelector).click ->
      _fillEditDropdown $(this)

    $(@createSelector).click ->
      _fillCreateDropdown $(this)

  _fillCreateDropdown: ($elem) ->
    createURL = $elem.data("url")
    createDropdown = $("#" + $elem.data("dropdown"))
    createDropdown.find("form").attr "action", createURL
    console.log createDropdown
    createDropdown.find("input[type=text]").focus()

  # Replace the action and field values of the dropdown when updating and
  # put autofocus on the first field
  _fillEditDropdown: ($elem) ->
    dept = $elem.find("span").text()
    updateURL = $elem.data("url")
    editDropdown = $("#" + $elem.data("dropdown"))
    editDropdown.find("form").attr "action", updateURL
    editDropdown.find("input[type=text]").val dept
    editDropdown.find("input[type=text]").focus()


window.Hizard.FormDropdown = FormDropdown