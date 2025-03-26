import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  static targets = ['link']

  initialize() {}

  connect() {}

  goToUrl(e) {
    window.location.href = e.params.url
  }

  linkTargetConnected(e) {
    if (this.isExternalURL(e.getAttribute('href'))) {
      e.classList.add('show-externallink')
    }
  }
  isExternalURL(url) {
    return new URL(url).origin !== location.origin
  }
}
