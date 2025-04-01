import { Controller } from '@hotwired/stimulus'

let maxNumber = 0
let lastValidNumber = 0
export default class extends Controller {
  initialize() {
    maxNumber = Number(this.element.max)
    console.log('maxnumber', this.element.max)
  }

  maxNumberChangedHandler() {
    if (Number(this.element.value) <= maxNumber) {
      lastValidNumber = Number(this.element.value)
    } else {
      console.log(lastValidNumber)
      this.element.value = Number(lastValidNumber)
    }
  }
}
