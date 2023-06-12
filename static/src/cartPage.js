const cartPage = {
    template:/*html*/`
    <div id="cart">
        <h1>Cart</h1>
        <div class="framed">
            <table id="cart-table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Count</th>
                        <th>Item price</th>
                        <th>Price</th>
                        <th>Remove</th>
                    </tr>
                </thead>
                <tbody v-if="cart.length">
                    <tr v-for="item in cart">
                        <td><router-link v-bind:to="'/product/'+item.product.id">{{item.product.name}}</router-link></td>
                        <td><input v-bind:value="item.quantity" type="number" max="99" min="1" v-on:change="updateCart(item.product.id,$event.target.value)"/></td>
                        <td>{{item.product.price}}-&nbsp;kr</td>
                        <td>{{item.product.price*item.quantity}}-&nbsp;kr</td>
                        <td><button class="button material-symbols-outlined"  v-on:click="removeFromCart(item.product.id)">delete</button></td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <td>Total</td>
                        <td></td>
                        <td></td>
                        <td>{{priceSum}}-&nbsp;kr</td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        <h1>Checkout</h1>
        <div class="framed">
            <form id="checkout-form" v-on:submit.prevent="order">
                <p class="error" v-if="errMessage">{{errMessage}}</p>
                <p class="success" v-if="message">{{message}}</p>
                <fieldset>
                    <legend>Billing details</legend>
                    <div>
                        <label for="firstname">First name:</label>
                        <input id="firstname" v-model="firstname" type="text" autocomplete="given-name">
                    </div>
                    <div>
                        <label for="lastname">Last name:</label>
                        <input id="lastname" v-model="lastname" type="text" autocomplete="family-name">
                    </div>
                    <div>
                        <label for="email">Email:</label>
                        <input id="email" v-model="email" type="text" autocomplete="email">
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Delivery adress</legend>
                    <div>
                        <label for="street">Street:</label>
                        <input id="street" v-model="street" type="text" autocomplete="adress-line2">
                    </div>
                    <div>
                        <label for="city">City:</label>
                        <input type="text" v-model="city" id="city" autocomplete="adress-line1">
                    </div>
                    <div>
                        <label for="postalcode">Postal&nbsp;code:</label>
                        <input id="postalcode" v-model="postcode" type="number" min="0" max="9999" autocomplete="postal-code">
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Submit order</legend>
                    <div>
                        <input class="submit-input" id="agreetos" v-model="tosCheck" type="checkbox">
                        <label id="agreetos" for="agreetos">I agree to the</label><a id="tos-link" v-on:click="openTos">general terms of service</a>
                    </div>
                    <input class="button" type="submit" value="&nbsp;Submit&nbsp;">
                </fieldset>
            </form>
        </div>
        <dialog ref="tos" id="tos">
            <h2>Terms of service</h2>
            <button class="material-symbols-outlined button" v-on:click="closeTos">close</button>
            <ol>
                <li>
                    <p>All birds purchased from Gulls and Us are considered property of the store and must be returned upon demand. Failure to do so will result in legal action against the customer.</p>
                </li>
                <li>
                    <p>Customers are not allowed to name their purchased birds as it interferes with the store's branding and marketing efforts.</p>
                </li>
                <li>
                    <p>Gulls and Us reserves the right to sell any bird purchased by a customer without notice or consent.</p>
                </li>
                <li>
                    <p>Any damage caused by a purchased bird is the sole responsibility of the customer, and Gulls and Us will not be held liable for any injuries or damages caused by the bird.</p>
                </li>
                <li>
                    <p>Customers are not allowed to take pictures or videos of their purchased birds without express written consent from Gulls and Us. Any violation of this rule will result in legal action against the customer.</p>
                </li>
                <li>
                    <p>Gulls and Us reserves the right to randomly inspect customers' homes to ensure that their purchased birds are being properly cared for. Failure to comply with these inspections will result in the confiscation of the bird.</p>
                </li>
                <li>
                    <p>Customers are required to purchase a lifetime supply of bird food from Gulls and Us at a marked-up price. Failure to do so will result in the revocation of the customer's bird ownership.</p>
                </li>
                <li>
                    <p>Gulls and Us reserves the right to modify these terms of service at any time without notice. It is the customer's responsibility to regularly check for updates and comply with the new terms.</p>
                </li>
            </ol>
        </dialog>
    </div>
    `,
    props: ["cart", "user"],
    emits: ["updateCart"],
    data: function () {
        return {
            firstname: "",
            lastname: "",
            email: "",
            street: "",
            city: "",
            postcode: "",
            message:"",
            errMessage:"",
            tosCheck:false
        }
    },
    methods: {
        openTos: function () {
            this.$refs.tos.showModal()
        },
        closeTos: function () {
            this.$refs.tos.close()
        },
        removeFromCart: async function (productid) {
            let response = await fetch("/cart/" + productid, {
                method: "DELETE"
            })
            if (response.status == 200) {
                this.$emit("updateCart")
            }
        },
        updateCart: async function (productid, newQuantity) {
            const quantity = parseInt(Math.max(1, Math.min(newQuantity, 99)))
            let response = await fetch("/cart/" + productid, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "quantity": quantity })
            })
            if (response.status == 200) {
                this.$emit("updateCart")
            }
        },
        checkOrder:function(){
            if (!this.firstname||
                !this.lastname||
                !this.email||
                !this.street||
                !this.city||
                !this.postcode){
                    this.errMessage="You must fill all the fields"
                    setTimeout(()=>this.errMessage="",5000)
                    return false
                }
                let emailRegex=/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
                if (!emailRegex.test(this.email)){
                    this.errMessage="Invalid email format. Use the format: email@example.org"
                    setTimeout(()=>this.errMessage="",5000)
                    return false 
                }
                let postRegex=/^\d{4}$/
                if (!postRegex.test(this.postcode)){
                    this.errMessage="Postal code must be four digits"
                    setTimeout(()=>this.errMessage="",5000)
                    return false
                }
                return true
        },
        order: async function () {
            if(!this.cart.length){
                this.errMessage="No products in cart"
                setTimeout(()=>this.errMessage="",5000)
                return
            }
            if (!this.checkOrder()){
                return
            }
            if (!this.tosCheck){
                this.errMessage="You must agree to the terms of service"
                setTimeout(()=>this.errMessage="",5000)
                return
            }
            let products=[]
            for (let product of this.cart){
                products.push({"productid":product.product.id,"quantity":product.quantity})
            }
            let response = await fetch("/order", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "firstname": this.firstname, "lastname": this.lastname, "email": this.email, "street": this.street, "city": this.city, "postcode": this.postcode,"products":products })
            })
            if (response.status ==200){
                result=await response.json()
                this.message=result.message
                setTimeout(()=>this.message="",5000)
                this.firstname= ""
                this.lastname= ""
                this.email= ""
                this.street= ""
                this.city= ""
                this.postcode= ""
                this.$emit("updateCart")
            }else if (response.status==400){
                result=await response.json()
                this.errMessage=result.message
                setTimeout(()=>this.errMessage="",5000)
            }
        }
    },
    computed: {
        priceSum: function () {
            if (this.cart) {
                return this.cart.reduce((sum, item) => sum + item.product.price * item.quantity, 0)
            }
            return 0
        }
    },
    watch: {
        $route: {
            handler: function () {
                document.title = "Cart - Gulls and Us"
            },
            immediate: true
        }
    },
}