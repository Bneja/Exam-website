const homePage = {
  template:/*html*/`
      <div id="listing-title">
          <h1>{{products.length}} products</h1>
          <div>
              Sort by:
              <select v-model="sortMethod" v-on:change="sort" name="sort">
                  <option selected="selected" value="relevance">Relevance</option>
                  <option value="price">Price low - high</option>
                  <option value="priceHigh">Price high - low</option>
                  <option value="name">Name</option>
              </select>
          </div>
      </div>
      <div id="home-page">
        <div id="prod-listing" v-if="products.length">
            <article v-for="product in products" v-on:click="goToProdPage(product.id)">
                <img class="prod-img" v-bind:src="product.imgpath" v-bind:alt="product.name"/>
                <div class="details-container">
                    <strong>{{product.name}}</strong>
                    <strong class="prod-price">{{product.price}}-&nbsp;kr</strong>
                    <span>{{product.shortdesc}}</span>
                </div>
            </article>
        </div>
        <img v-else-if="loading" src="static/src/images/loading.gif"/>
        <strong v-else-if="noResult">No results</strong>
        <cart-aside v-if="!loading && !noResult" v-bind:cart="cart"></cart-aside>
      </div>
        `,
  props: ["cart"],
  data: function () {
    return {
      products: [],
      noResult: false,
      loading: false,
      sortMethod: "relevance"
    }
  },
  watch: {
    $route: {
      handler: async function () {
        let cookie = decodeURIComponent(document.cookie).split(";")
        for (item of cookie) {
          while (item.charAt(0) == ' ') {
            item = item.substring(1)
          }
          if (item.indexOf('sortPreference=') == 0) {
            this.sortMethod = item.substring('sortPreference='.length, item.length)
            break
          }
        }
        this.loading = true
        this.products = []
        let response = await fetch("/products")
        if (response.status == 200) {
          this.loading = false
          let result = await response.json()
          if (this.$route.params.kword) {
            let filteredProd = this.search(result)
            document.title = this.$route.params.kword + " - Gulls and Us"
            if (filteredProd.length) {
              this.noResult = false
              this.products = filteredProd
            } else {
              this.noResult = true
            }
          } else {
            document.title = "Gulls and Us"
            this.noResult = false
            this.products = result
          }
          this.sort()
        }
      },
      immediate: true
    }
  },
  methods: {
    goToProdPage: function (id) {
      this.$router.push({ name: "prodPage", params: { id: id } })
    },
    search: function (array) {
      const keyword = this.$route.params.kword.toLowerCase()
      return array.filter(item => {
        for (key in item) {
          if ((key === "name" || key === "price" || key == "shortdesc") &&
            item[key].toString().toLowerCase().includes(keyword)) {
            return true
          }
        }
      })
    },
    sortRelevance: function () {
      let keyword = this.$route.params.kword
      if (keyword && this.products) {
        keyword = keyword.toLowerCase()
        for (item of this.products) {
          let score = 0
          for (key in item) {
            key = key.toString()
            if (item[key].toString().toLowerCase().includes(keyword)) {
              const value=item[key].toString().toLowerCase()
              const index=value.indexOf(keyword)
              switch (key) {
                //Subtracting index so products where keyword is at the beggining comes first 
                case "name": score += (10-index)
                  break
                case "price": score += 4
                  break
                case "shortdesc": score += 3
                  break
                case "desc": score += 1
              }
            }
          }
          item.score = score
        }
        this.products.sort((a, b) => b.score - a.score)
      } else {
        this.products.sort((a, b) => a.id - b.id)
      }
    },
    sortPrice: function () {
      this.products.sort((a, b) => a.price - b.price)
    },
    sortPriceHigh: function () {
      this.products.sort((a, b) => b.price - a.price)
    },
    sortName: function () {
      this.products.sort((a, b) => {
        const nameA = a.name.toLowerCase()
        const nameB = b.name.toLowerCase()

        if (nameA < nameB) { return -1 }
        if (nameA > nameB) { return 1 }
        return 0
      })
    }
    ,
    sort: function () {
      const d = new Date()
      d.setTime(d.getTime() + 30 * 24 * 60 * 60 * 1000)
      document.cookie = `sortPreference=${this.sortMethod}; expires=${d.toUTCString()}; SameSite=Strict;`
      switch (this.sortMethod) {
        case "relevance":
          this.sortRelevance()
          break
        case "price":
          this.sortPrice()
          break
        case "priceHigh":
          this.sortPriceHigh()
          break
        case "name":
          this.sortName()
      }
    }
  }
}
