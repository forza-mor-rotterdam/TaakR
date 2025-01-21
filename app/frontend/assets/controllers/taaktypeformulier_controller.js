import { Controller } from '@hotwired/stimulus'
import $ from 'jquery' // Import jQuery
// eslint-disable-next-line no-unused-vars
import Select2 from 'select2'

let form = null
let inputList = null
// eslint-disable-next-line no-unused-vars
let formData = null
export default class extends Controller {
  static targets = ['formTaaktype', 'voorbeeldWel', 'voorbeeldNiet', 'link']

  initializeSelect2() {
    const afdelingen = this.formTaaktypeTarget.querySelector('#afdelingen_1')
    const middelen = this.formTaaktypeTarget.querySelector('#taaktypemiddelen_1')
    const volgend_select = this.formTaaktypeTarget.querySelector('#volgende_taaktypes_1')
    const gerelateerde_onderwerpen_select = this.formTaaktypeTarget.querySelector(
      '#gerelateerde_onderwerpen_1'
    )
    const gerelateerde_taaktypes_select = this.formTaaktypeTarget.querySelector(
      '#gerelateerde_taaktypes_1'
    )

    this.doSelect2(afdelingen, 'Zoek op afdeling')
    this.doSelect2(middelen, 'Zoek op materieel')
    this.doSelect2(volgend_select, 'Zoek op taaktype')
    this.doSelect2(gerelateerde_onderwerpen_select, 'Zoek op onderwerp')
    this.doSelect2(gerelateerde_taaktypes_select, 'Zoek op taaktype')
  }

  connect() {
    form = this.formTaaktypeTarget
    inputList = document.querySelectorAll('[type="text"]')
    this.defaultErrorMessage = 'Vul a.u.b. dit veld in.'

    formData = new FormData(form)
    this.initializeSelect2()

    for (const input of inputList) {
      const error = input.closest('.form-row').getElementsByClassName('invalid-text')[0]

      input.addEventListener('input', () => {
        if (input.validity.valid) {
          input.closest('.form-row').classList.remove('is-invalid')
          error.textContent = ''
        } else {
          error.textContent = this.defaultErrorMessage
          input.closest('.form-row').classList.add('is-invalid')
        }
      })
    }

    if (this.voorbeeldWelTarget.querySelectorAll('.task--hideable.hide').length === 0) {
      this.voorbeeldWelTarget.querySelector('button.btn-textlink').classList.add('hide')
    }
    if (this.voorbeeldNietTarget.querySelectorAll('.task--hideable.hide').length === 0) {
      this.voorbeeldNietTarget.querySelector('button.btn-textlink').classList.add('hide')
    }
  }
  doSelect2(element, placeholder = 'Zoek op') {
    $(element).select2({ placeholder: placeholder })
    this.setNotRequiredSelect2(element)
  }

  setNotRequiredSelect2(s2Element) {
    const small = document.createElement('small')
    small.textContent = '(Niet verplicht)'
    const required = s2Element.closest('.form-row').querySelector('select').hasAttribute('required')
    if (!required) {
      s2Element.closest('.form-row').querySelector('label').appendChild(small)
    }
  }

  addExample(e) {
    const hiddenExamples = e.target.parentNode.querySelectorAll('.hide')
    if (hiddenExamples.length > 0) {
      hiddenExamples[0].classList.remove('hide')
    }
    if (e.target.parentNode.querySelectorAll('.hide').length === 0) {
      e.target.classList.add('hide')
    }
  }
  linkFormulierToevoegen(e) {
    const hiddenLinks = this.linkTargets.filter((link) => link.classList.contains('hide'))
    if (hiddenLinks.length > 0) {
      hiddenLinks[0].classList.remove('hide')
      hiddenLinks[0].querySelector('input[type=text]').focus()
      if (hiddenLinks.length === 1) {
        e.target.classList.add('hide')
      }
    }
  }
}
