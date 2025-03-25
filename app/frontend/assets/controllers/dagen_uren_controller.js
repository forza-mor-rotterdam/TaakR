import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  static targets = ['dagen', 'uren', 'seconden']

  secondenTargetConnected() {
    this.dagenMax = 365
    this.urenMax = 23
    this.urenSeconden = 60 * 60
    this.dagenSeconden = 24 * this.urenSeconden
    const huidigeSeconden = this.secondenTarget.value ? this.secondenTarget.value : 0
    const huidigeDagenSeconden = huidigeSeconden - (huidigeSeconden % this.dagenSeconden)
    const huidigeUrenSeconden = huidigeSeconden - huidigeDagenSeconden
    this.dagen = huidigeDagenSeconden / this.dagenSeconden
    this.uren =
      (huidigeUrenSeconden - (huidigeUrenSeconden % this.urenSeconden)) / this.urenSeconden
    this.dagenTarget.value = this.dagen
    this.urenTarget.value = this.uren
    const daysHours = this.secondsToDaysHours(this.secondenTarget.value)
    this.dagenTarget.value = daysHours.dagen
    this.urenTarget.value = daysHours.uren
  }

  dagenChangedHandler(e) {
    this.dagen = Math.floor(e.target.value)
    this.dagen = this.dagen > this.dagenMax ? this.dagenMax : this.dagen
    this.dagenTarget.value = this.dagen
    this.setSecondenField()
  }

  urenChangedHandler(e) {
    this.uren = Math.floor(e.target.value)
    if (this.uren > this.urenMax) {
      this.dagen = this.dagen >= this.dagenMax ? this.dagenMax : this.dagen + 1
      this.dagenTarget.value = this.dagen
      this.uren = 0
    }
    if (this.uren < 0) {
      this.dagen = this.dagen <= 0 ? 0 : this.dagen - 1
      this.dagenTarget.value = this.dagen
      this.uren = this.urenMax
    }

    this.uren = this.uren > this.urenMax ? this.urenMax : this.uren
    this.urenTarget.value = this.uren
    this.setSecondenField()
  }

  setSecondenField() {
    this.secondenTarget.value = this.dagen * this.dagenSeconden + this.uren * this.urenSeconden
  }

  secondsToDaysHours(seconden) {
    const urenSeconden = 60 * 60
    const dagenSeconden = 24 * urenSeconden
    const huidigeSeconden = Number(seconden)
    const huidigeDagenSeconden = huidigeSeconden - (huidigeSeconden % dagenSeconden)
    const huidigeUrenSeconden = huidigeSeconden - huidigeDagenSeconden
    const dagen = huidigeDagenSeconden / dagenSeconden
    const uren = (huidigeUrenSeconden - (huidigeUrenSeconden % urenSeconden)) / urenSeconden
    return { dagen: dagen, uren: uren }
  }
}
