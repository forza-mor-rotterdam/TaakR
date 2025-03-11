import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  static targets = ['dagen', 'uren', 'seconden']

  connect() {
    console.log('dagen uren connected')
    this.urenSeconden = 60 * 60
    this.dagenSeconden = 24 * this.urenSeconden
    const huidigeSeconden = this.secondenTarget.value
    const huidigeDagenSeconden = huidigeSeconden - (huidigeSeconden % this.dagenSeconden)
    const huidigeUrenSeconden = huidigeSeconden - huidigeDagenSeconden
    this.dagen = huidigeDagenSeconden / this.dagenSeconden
    this.uren =
      (huidigeUrenSeconden - (huidigeUrenSeconden % this.urenSeconden)) / this.urenSeconden
    this.dagenTarget.value = this.dagen
    this.urenTarget.value = this.uren
  }
  dagenChangedHandler(e) {
    this.dagen = Math.floor(e.target.value)
    this.dagenTarget.value = this.dagen
    this.setSecondenField()
  }
  urenChangedHandler(e) {
    this.uren = Math.floor(e.target.value)
    this.uren = this.uren > 13 ? 13 : this.uren
    this.urenTarget.value = this.uren
    this.setSecondenField()
  }
  setSecondenField() {
    this.secondenTarget.value = this.dagen * this.dagenSeconden + this.uren * this.urenSeconden
  }
}
