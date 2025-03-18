import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  static targets = ['dagen', 'uren', 'seconden', 'periode']

  secondenTargetConnected() {
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
    const daysHours = this.secondsToDaysHours(this.secondenTarget.value)
    this.dagenTarget.value = daysHours.dagen
    this.urenTarget.value = daysHours.uren
  }

  periodeTargetConnected(element) {
    if (element.textContent) {
      const dagen = this.secondsToDaysHours(element.textContent).dagen
      const uren = this.secondsToDaysHours(element.textContent).uren
      let periode = ''
      if (dagen) periode += `${dagen} dagen`
      if (dagen && uren) periode += ` en `
      if (uren) periode += `${uren} uur`
      element.textContent = periode
    }
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
