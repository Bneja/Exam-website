const prodPage = {
    template:/*html*/`
<div id="prod-page">
    <div v-if="!loading" id="prodpage-listing-container">
        <div class="framed product-listing">
            <img v-bind:src="product.imgpath" v-bind:alt="product.name">
                <div class="productpage-information">
                    <div class="product-description">
                        <h2 class="product-name"><span>{{product.name}}</span>&nbsp;<span class="product-price">{{product.price}},-&nbsp;kr</span></h2>
                        <p class="product-shortdesc">{{product.shortdesc}}</p>
                    </div>
                    <form action="">
                        <div>
                            <label for="count">Count:</label>
                            <input id="count" type="number" min="1" max="99" v-model="quantity">
                        </div>
                        <div>
                            <label for="price">Price:</label>
                            <input type="text" id="price" v-bind:value="product.price.toString()+',-&nbsp;kr'" readonly>
                        </div>
                        <input type="button" class="button" v-on:click="addToCart" value="&nbsp; Add to Cart &nbsp;">
                    </form>
                </div>  
        </div>
        <h1>Details</h1>
        <div class="framed">
            <p>{{product.desc}}</p>
        </div>
    </div>
    <img v-else src="static/src/images/loading.gif" />
    <cart-aside v-if="!loading" v-bind:cart="cart"></cart-aside>
</div>
    `,
    props: ["user", "cart"],
    emits: ["updateCart"],
    data: function () {
        return {
            product: { imgpath: "", price: 0 },
            loading: false,
            quantity: 1,
        }
    },
    watch: {
        $route: {
            handler: async function () {
                this.loading = true
                let response = await fetch("/products/" + this.$route.params.id)
                if (response.status == 200) {
                    this.loading = false
                    this.product = await response.json()
                    document.title = this.product.name + " - Gulls and Us"
                }
            },
            immediate: true
        },
        quantity: function () {
            this.quantity = parseInt(Math.max(1, Math.min(this.quantity, 99)))
        }
    },
    methods: {
        addToCart: async function () {
            const limitedQuantity = Math.max(1, Math.min(this.quantity, 99))
            let response = await fetch("/cart/" + this.$route.params.id, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "quantity": limitedQuantity })
            })
            if (response.status == 200) {
                this.$emit("updateCart")
            }
        }
    }
}