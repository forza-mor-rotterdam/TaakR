import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  static targets = ['row', 'searchable', 'resultCount']

  connect() {
    this.searchableTargets.forEach((searchable) => {
      searchable.dataset.value = searchable.textContent
    })
    this.displayTypes = {
      LI: 'list-item',
      TR: 'table-row',
    }
  }
  search(e) {
    this.rowTargets.forEach((searchableContainer) => {
      searchableContainer.style.display = 'none'
    })
    this.resultCountTarget.textContent = ''
    this.searchableTargets.forEach((searchable) => {
      const re = new RegExp(e.target.value, 'gi')
      let newContent = searchable.dataset.value
      if (re.test(searchable.dataset.value)) {
        let container = searchable.closest("[data-row-search-target='row']")
        container.style.display = this.displayTypes[container.nodeName]
        newContent = newContent.replace(re, function (match) {
          return '<mark>' + match + '</mark>'
        })
      }
      searchable.innerHTML = newContent
    })
    const foundCount = this.rowTargets.filter(
      (searchableContainer) => searchableContainer.style.display != 'none'
    ).length
    this.resultCountTarget.textContent = `${foundCount} / ${this.rowTargets.length}`
  }
}
