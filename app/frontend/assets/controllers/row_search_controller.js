import { Controller } from '@hotwired/stimulus'

let searchKey = null
export default class extends Controller {
  static targets = ['row', 'searchable', 'resultCount', 'searchTaaktype']
  static values = { fieldType: String }

  connect() {
    console.log('ROW_SEARCH connected')
    searchKey = this.fieldTypeValue
    const savedQuery = sessionStorage.getItem(searchKey)

    if (savedQuery && this.hasSearchTaaktypeTarget) {
      this.searchTaaktypeTarget.value = savedQuery
    }
    this.searchableTargets.forEach((searchable) => {
      searchable.dataset.value = searchable.textContent
    })
    this.displayTypes = {
      LI: 'list-item',
      TR: 'table-row',
    }
    let formElem = this.element.querySelector('form')
    if (formElem) {
      formElem.addEventListener('submit', (e) => {
        e.preventDefault()
        return false
      })
    }
    this.search(null, savedQuery)
  }
  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  }

  search(e = null, str = '') {
    let searchString = ''
    if (e) {
      searchString = e.target.value.trim()
    } else if (str) {
      searchString = str
    }
    if (this.hasSearchTaaktypeTarget) {
      sessionStorage.setItem(searchKey, searchString)
    }

    if (searchString.length != 0) {
      this.rowTargets.forEach((searchableContainer) => {
        searchableContainer.style.display = 'none'
      })

      if (this.hasResultCountTarget) {
        this.resultCountTarget.textContent = ''
      }

      this.searchableTargets.forEach((searchable) => {
        const value = this.escapeRegExp(searchString)
        const re = new RegExp(value, 'gi')
        searchable.innerHTML = ''
        if (re.test(searchable.dataset.value)) {
          const reg = new RegExp(value, 'gi')
          let execResult
          let index = 0
          let lastIndex
          let previousText = ''
          while ((execResult = reg.exec(searchable.dataset.value)) !== null) {
            lastIndex = reg.lastIndex
            if (execResult.index != 0) {
              previousText = searchable.dataset.value.substring(index, execResult.index)
            }
            searchable.appendChild(document.createTextNode(previousText))
            const markElem = document.createElement('MARK')
            markElem.textContent = execResult[0]
            searchable.appendChild(markElem)
            index = lastIndex
          }
          const endText = searchable.dataset.value.substring(
            lastIndex,
            searchable.dataset.value.length
          )
          searchable.appendChild(document.createTextNode(endText))

          let container = searchable.closest("[data-row-search-target='row']")
          container.style.display = this.displayTypes[container.nodeName]
        } else {
          searchable.textContent = searchable.dataset.value
        }
      })
      if (this.hasResultCountTarget) {
        const foundCount = this.rowTargets.filter(
          (searchableContainer) => searchableContainer.style.display != 'none'
        ).length
        this.resultCountTarget.textContent = `${foundCount} / ${this.rowTargets.length}`
      }
    } else {
      this.rowTargets.forEach((searchableContainer) => {
        searchableContainer.style.display = this.displayTypes[searchableContainer.nodeName]
      })
      this.searchableTargets.forEach((searchable) => {
        searchable.textContent = searchable.dataset.value
      })
      if (this.hasResultCountTarget) {
        this.resultCountTarget.textContent = `${this.rowTargets.length} / ${this.rowTargets.length}`
      }
    }
  }
}
